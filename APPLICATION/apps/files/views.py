from io import BytesIO
from PIL import Image
from django.http import HttpResponse
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.apps import apps
from django.core.files.base import ContentFile
from django.conf import settings
import os
import io
from django.db import transaction

def compress_and_convert_to_webp(image_file):

    img = Image.open(image_file)

    if img.mode in ("RGBA", "P"):
        img = img.convert("RGB")

    img_io = BytesIO() # Comprimir la imagen y reducir su tamaño
    img.save(img_io, format='WEBP', quality=40) 

    img_content = ContentFile(img_io.getvalue(), name=f"{image_file.name.split('.')[0]}.webp")
    return img_content

@require_POST
@transaction.atomic
def update_file(request):
    app_name = request.POST.get('app_name')
    table = request.POST.get('table')
    field = request.POST.get('field')
    record_id = request.POST.get('record_id')
    file = request.FILES.get('file')  # Cambiado de 'image' a 'file' para soportar ambos tipos
    file_type = request.POST.get('type')

    print(app_name, table, field, record_id, file, file_type)

    # Verificar campos requeridos
    if not (app_name and table and field and record_id and file and file_type):
        messages.error(request, 'Faltan campos requeridos')
        return HttpResponse(status=400)

    # Validar tipo de archivo
    if file_type == 'image':
        try:
            img = Image.open(file)
            img.verify()  # Verificar que sea una imagen válida
        except (IOError, SyntaxError):
            messages.error(request, 'El archivo subido no es una imagen válida.')
            return HttpResponse(status=400)

    try:
        Model = apps.get_model(app_name, table)
        instance = Model.objects.get(pk=record_id)

        # Verificar que el campo existe en el modelo
        if not hasattr(instance, field):
            messages.error(request, f'El campo "{field}" no existe en el modelo "{table}".')
            return HttpResponse(status=400)

        # Eliminar el archivo anterior si no es la imagen por defecto o un archivo nulo
        current_file_path = getattr(instance, field)
        if current_file_path and current_file_path.url != settings.MEDIA_URL + 'default/default_user.jpg':
            current_file_full_path = os.path.join(settings.MEDIA_ROOT, current_file_path.name)
            if os.path.isfile(current_file_full_path):
                os.remove(current_file_full_path)

        # Guardar nuevo archivo
        if file_type == 'image':
            new_file_name = f'image_{record_id}.webp'
            compressed_image = compress_and_convert_to_webp(file)
            new_file = ContentFile(compressed_image.read(), name=new_file_name)
        elif file_type == 'file':
            new_file = ContentFile(file.read(), name=file.name)
        else:
            messages.success(request, 'El arcivo no es valido')
            return HttpResponse(status=400)

        setattr(instance, field, new_file)  # Guardar el archivo en el campo
        instance.save()

        # Mensaje de éxito
        messages.success(request, 'Archivo actualizado correctamente')
        return HttpResponse(status=200)

    except ValueError:
        messages.error(request, 'ID de registro no válido')
        return HttpResponse(status=400)
    except Model.DoesNotExist:
        messages.error(request, 'El registro no existe')
        return HttpResponse(status=404)
    except LookupError:
        messages.error(request, 'Ha ocurrido un error inesperado.')
        return HttpResponse(status=400)
    except Exception as e:
        messages.error(request, f'Ha ocurrido un error: {str(e)}')
        return HttpResponse(status=500)


def delete_file(request):
    app_name = request.POST.get('app_name')
    table = request.POST.get('table')
    field = request.POST.get('field')
    record_id = request.POST.get('record_id')

    if not (app_name and table and field and record_id):
        messages.error(request, 'Faltan campos requeridos')
        return HttpResponse(status=400)

    try:
        Model = apps.get_model(app_name, table)
        instance = Model.objects.get(pk=record_id)

        if not hasattr(instance, field):
            messages.error(request, f'El campo "{field}" no existe en el modelo "{table}".')
            return HttpResponse(status=400)

        current_file_path = getattr(instance, field)
        if not current_file_path:
            messages.error(request, 'No hay archivo que eliminar.')
            return HttpResponse(status=400)

        current_file_full_path = os.path.join(settings.MEDIA_ROOT, current_file_path.name)
        if os.path.isfile(current_file_full_path):
            os.remove(current_file_full_path)
            setattr(instance, field, None)

            instance.save()

            messages.success(request, 'Archivo eliminado correctamente')
            return HttpResponse(status=200)
        
        else:
            instance.delete()  # Eliminar el registro si el archivo no existe
            messages.error(request, 'El archivo no existe en el servidor. Eliminando el registro.')
            return HttpResponse(status=200)

    except ValueError:
        messages.error(request, 'ID de registro no válido')
        return HttpResponse(status=400)
    except Model.DoesNotExist:
        messages.error(request, 'El registro no existe')
        return HttpResponse(status=404)
    except LookupError:
        messages.error(request, 'Ha ocurrido un error inesperado.')
        return HttpResponse(status=400)
    except Exception as e:
        messages.error(request, f'Ha ocurrido un error: {str(e)}')
        return HttpResponse(status=500)


@require_POST
def download_file(request):
    app_name = request.POST.get('app_name')
    table = request.POST.get('table')
    field = request.POST.get('field')
    record_id = request.POST.get('record_id')

    if not (app_name and table and field and record_id):
        messages.error(request, 'Faltan campos requeridos')
        return HttpResponse(status=400)

    try:
        Model = apps.get_model(app_name, table)
        instance = Model.objects.get(pk=record_id)

        if not hasattr(instance, field):
            messages.error(request, f'El campo "{field}" no existe en el modelo "{table}".')
            return HttpResponse(status=400)

        current_file_path = getattr(instance, field)

        if not current_file_path:
            messages.error(request, 'No hay archivo para descargar.')
            return HttpResponse(status=404)

        current_file_full_path = os.path.join(settings.MEDIA_ROOT, current_file_path.name)

        if not os.path.isfile(current_file_full_path):
            messages.error(request, 'El archivo no existe en el servidor.')
            return HttpResponse(status=404)
        
        image = Image.open(current_file_full_path)
        img_io = io.BytesIO()
        image.convert('RGB').save(img_io, 'PNG')  # Convertir a PNG
        img_io.seek(0)
        
        with open(current_file_full_path, 'rb') as file:
            response = HttpResponse(file.read(), content_type='application/octet-stream')
            response['Content-Disposition'] = f'attachment; filename="{os.path.basename(current_file_full_path)}"'
            messages.success(request, 'El archivo se descargo de forma correcta.')
            return response

    except ValueError:
        messages.error(request, 'ID de registro no válido')
        return HttpResponse(status=400)
    except Model.DoesNotExist:
        messages.error(request, 'El registro no existe')
        return HttpResponse(status=404)
    except LookupError:
        messages.error(request, 'Ha ocurrido un error inesperado.')
        return HttpResponse(status=400)
    except Exception as e:
        messages.error(request, f'Ha ocurrido un error: {str(e)}')
        return HttpResponse(status=500)
   


@require_POST
@transaction.atomic
def dowload_image(request):
    app_name = request.POST.get('app_name')
    table = request.POST.get('table')
    