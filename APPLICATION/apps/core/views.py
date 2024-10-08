from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from datetime import datetime
import random

@login_required
def home(request):
    # Obtener la hora actual
    now = datetime.now()
    current_hour = now.hour

    # Definir los saludos
    if current_hour < 12:
        greeting = f'¡Buenos días! {request.user.first_name}'
    elif 12 <= current_hour < 18:
        greeting = f'¡Buenas tardes! {request.user.first_name}'
    else:
        greeting = "¡Hola!"

    # Lista de frases
    phrases = [
        "La vida es un 10% lo que me sucede y un 90% cómo reacciono a ello. Recuerda que tienes el poder de cambiar tu perspectiva y tus respuestas ante las adversidades.",
        "La mejor manera de predecir el futuro es crearlo. Cada pequeño paso que tomes hoy puede ser el fundamento de tus grandes sueños de mañana.",
        "Haz de cada día tu obra maestra. Cada día es una nueva oportunidad para hacer algo grandioso, así que aprovecha cada momento y da lo mejor de ti.",
        "El único modo de hacer un gran trabajo es amar lo que haces. Si no has encontrado eso que amas, sigue buscando; no te conformes, el amor por tu trabajo es la clave del éxito.",
        "El éxito no es la clave de la felicidad. La felicidad es la clave del éxito. Si amas lo que haces, serás exitoso en lo que emprendas.",
        "No cuentes los días, haz que los días cuenten. Cada día es una nueva oportunidad para crecer, aprender y acercarte a tus metas.",
        "Las dificultades a menudo preparan a las personas comunes para un destino extraordinario. No temas enfrentar los retos, son oportunidades disfrazadas.",
        "La única forma de hacer un gran trabajo es amar lo que haces. Si aún no lo has encontrado, sigue buscando hasta que lo logres.",
        "La vida es como andar en bicicleta. Para mantener el equilibrio, debes seguir adelante. No te detengas ante los obstáculos, sigue avanzando.",
        "No importa cuántas veces caigas, lo que importa es cuántas veces te levantes. Cada caída es una lección y una oportunidad para volver más fuerte.",
        "El viaje de mil millas comienza con un solo paso. No subestimes el poder de empezar; cada paso cuenta en tu camino hacia el éxito.",
        "Los sueños no se hacen realidad a través de la magia. Se necesita sudor, determinación y trabajo duro. No te rindas ante la primera dificultad.",
        "Si quieres alcanzar la grandeza, deja de pedir permiso. La verdadera grandeza se logra cuando te atreves a ser diferente y sigues tu propio camino.",
        "La vida es lo que sucede mientras estás ocupado haciendo otros planes. No olvides disfrutar el momento presente mientras trabajas en tus objetivos.",
        "La única limitación es la que tú te pones. No dejes que el miedo o la duda te detengan; eres capaz de lograr cosas increíbles si lo intentas.",
        "La perseverancia es la clave del éxito. A menudo, es la última llave en el llavero la que abre la puerta.",
        "No importa cuántas veces fracases, siempre que aprendas de ello. Cada fracaso es una lección que te acerca más a tu objetivo.",
        "El éxito no se mide por lo que has logrado, sino por los obstáculos que has superado. Tu historia es única y valiosa, así que sigue escribiéndola.",
        "Tu actitud, no tu aptitud, determinará tu altitud. Mantén una mentalidad positiva y abierta, y verás cómo se abren nuevas oportunidades.",
        "La vida no se trata de encontrarte a ti mismo, sino de crearte a ti mismo. Eres el arquitecto de tu destino, así que construye la vida que deseas.",
        "Cree en ti mismo y todo será posible. La confianza es la base de todos los logros; si no crees en ti, ¿quién lo hará?",
        "La felicidad no es algo hecho. Proviene de tus propias acciones. Si quieres ser feliz, actúa con amor y gratitud todos los días.",
        "La mejor venganza es un éxito masivo. No dejes que las opiniones de los demás te frenen; enfócate en tus objetivos y trabaja para alcanzarlos.",
        "Las grandes cosas nunca provienen de zonas de confort. Atrévete a salir de tu zona de confort y explorar nuevas oportunidades.",
        "El éxito es la suma de pequeños esfuerzos repetidos día tras día. No subestimes el poder de la constancia y el trabajo diario.",
        "A veces, las cosas más pequeñas ocupan más espacio en tu corazón. No olvides apreciar las pequeñas cosas de la vida, son las que realmente cuentan.",
        "Las oportunidades no ocurren, las creas. No esperes a que algo suceda, sal y hazlo. Toma la iniciativa y crea tu propio camino.",
        "No hay mayor agitación que la que se siente al no ser fiel a uno mismo. Sé auténtico y fiel a tus valores; eso te llevará lejos.",
        "Nunca es demasiado tarde para ser lo que podrías haber sido. Cada día es una nueva oportunidad para reinventarte y perseguir tus sueños.",
        "La creatividad es la inteligencia divirtiéndose. Permítete ser creativo y explorar nuevas ideas; eso es lo que hace que la vida sea emocionante.",
        "La vida es un espejo y te devuelve lo que das. Si ofreces amor y positividad, recibirás lo mismo a cambio.",
        "La forma en que te tratas a ti mismo establece el estándar para los demás. Aprende a amarte y respetarte; eso es fundamental para construir relaciones sanas.",
        "Es mejor ser un fracasado que un no intentarlo. Si no arriesgas, nunca sabrás de lo que eres capaz.",
        "El verdadero fracaso es no haberlo intentado. Aprovéchate de cada oportunidad para aprender y crecer; cada intento cuenta.",
        "La disciplina es el puente entre tus metas y logros. La constancia y la dedicación son claves para alcanzar lo que deseas.",
        "No tienes que ser grande para comenzar, pero tienes que comenzar para ser grande. Da ese primer paso y verás cómo se desarrollan las cosas.",
        "Si no luchas por lo que quieres, no llores por lo que has perdido. La lucha es parte del proceso; no te desanimes.",
        "La vida es un desafío, enfréntalo. La manera en que enfrentas tus desafíos define quién eres realmente.",
        "Los límites solo existen en tu mente. Atrévete a pensar en grande y rompe las barreras que te detienen.",
        "El cambio es la ley de la vida. Y aquellos que solo miran al pasado o al presente, seguramente perderán el futuro.",
        "La verdadera medida de un hombre no se ve en los momentos de comodidad y conveniencia, sino en aquellos de desafío y controversia.",
        "Si quieres vivir una vida feliz, átala a una meta, no a personas ni a cosas. La claridad de tus objetivos es lo que te dará dirección.",
        "El tiempo que disfrutas perder no es tiempo perdido. No te sientas culpable por disfrutar de las cosas que amas.",
        "Haz lo que puedas, con lo que tengas, donde estés. No esperes por las condiciones perfectas; comienza con lo que tienes.",
        "El crecimiento comienza en la incomodidad. Salir de tu zona de confort es lo que te lleva a nuevas experiencias y aprendizajes.",
        "La forma en que piensas determina cómo vives. Una mentalidad positiva puede cambiar tu vida de maneras sorprendentes."
    ]

    # Seleccionar una frase aleatoria
    random_phrase = random.choice(phrases)

    # Pasar los datos a la plantilla
    context = {
        'greeting': greeting,
        'random_phrase': random_phrase,
    }

    return render(request, 'home.html', context)


@login_required
def site_construction(request):
    return render(request, 'construction.html')

