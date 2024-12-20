from django import template

register = template.Library()

@register.filter
def get_item(dictionary, key):
    keys = {
        'Referencia': ['referencia_fk__referencia_pk', 'referencia_pk'],
        'Marca':  ['referencia_fk__marca', 'marca'],
        'Codigo ALCOM': 'cod_equipo_pk',
        'Serial': 'serial',
        'Estado': 'estado',
        'Categoria': 'categoria',
        'Nombres': 'first_name',
        'Apellidos': 'last_name',
        'Usuario': 'username',
        'Correo': 'email',
        'Cargo': 'position',
    }

    # Obtener la clave real que corresponde al valor del diccionario
    real_key = keys.get(key, key)  # Si no se encuentra la clave, usar el valor original

    # Si real_key es una lista, buscar el primer valor disponible en el diccionario
    if isinstance(real_key, list):
        for k in real_key:
            if k in dictionary:
                return dictionary[k]
        return ''  # Si no se encuentra ninguna clave, devolver cadena vacía
    else:
        # Si real_key es una clave única, devolver su valor
        return dictionary.get(real_key, '')