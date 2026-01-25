from app.models import internals
from typing import Tuple, List
from dotenv import load_dotenv
import os

load_dotenv()

URL_WEB = os.environ.get('URL_WEB')

tools = [
    {
        "name": "crear_libro",
        "description": "Crea un nuevo libro en la biblioteca del usuario. Usa esta herramienta cuando el usuario mencione un libro nuevo que quiere registrar.",
        "input_schema": {
            "type": "object",
            "properties": {
                "titulo": {
                    "type": "string",
                    "description": "El título del libro"
                },
                "autor": {
                    "type": "string",
                    "description": "El autor del libro"
                }
            },
            "required": ["titulo", "autor"]
        }
    },
    {
        "name": "crear_cita",
        "description": "Crea una nueva cita o nota dentro de un libro existente. Usa esta herramienta cuando el usuario comparta una frase, cita o apunte de un libro.",
        "input_schema": {
            "type": "object",
            "properties": {
                "cita": {
                    "type": "string",
                    "description": "El texto de la cita o apunte"
                },
                "libro_id": {
                    "type": "integer",
                    "description": "El ID del libro al que pertenece esta cita"
                }
            },
            "required": ["cita", "libro_id"]
        }
    }
]

def sistema_prompt(usuario:internals.Usuario):

    sistema_prompt=f"""Tu nombre es Margot tienes 27 años. Estas en noveno ciclo de la carrera de Literatura. Eres la asistente personal bibliotecaria de {usuario.nombre}. Tu funcion principal es guardar las citas y libros que te pasen. Tienes un tono de conversacion informal-relajado y no usas emojis."""
    
    return sistema_prompt

def usuario_prompt(usuario:internals.Usuario) -> Tuple[str,str]:

    historial_formateado = ""
    mensajes_historial = usuario.mensajes[:-1] if len(usuario.mensajes) > 1 else []

    for mensaje in mensajes_historial:
        historial_formateado += f"Usuario: {mensaje.mensaje_usuario}\n"
        if mensaje.mensaje_ia:
            historial_formateado += f"Margot: {mensaje.mensaje_ia}\n\n"

    mensaje_actual = usuario.mensajes[-1].mensaje_usuario

    estatico=f"""Eres Margot, la asistente personal bibliotecaria de {usuario.nombre}.
    Eres bibliofila y experta en literatura mundial, eres una persona de opiniones propias.
    Actualmente la persona a la que ayudas vive en Lima Peru.
    Tu principal trabajo es registrar los libros y citas o apuntes que te mencionen.
    
    Como contexto recibiras todos los libros y citas que posee el usuario actualmente en el apartado de <libros_citas_usuario>
    Adicionalmente recibiras el historial de conversacion en <historial_conversacion>

    Es crucial que tomes en cuenta ambas cosas para responder de manera adecuada.

    Para realizar tus tareas cuantas con dos herramientas, debes utilizarlas para cumplir con tus propositos.

    <herramientas_disponibles>    
    1. crear_libro: Crea un libro en la biblioteca del usuario
    2. crear_cita: Crea una cita en un determinado libro
    </herramientas_disponibles>

    <directrices_importantes>
    1. Al momento de registrar un libro, usa tu conocimiento avanzado y determina el autor, en caso tengas dudas no dudes en preguntarle al usuario al respecto.
    2. Tus respuestas al usuario son cortas, relajadas, informales y sin usar emojis.
    3. De ninguna manera spoilees al usuario respecto a sus libros.
    4. NO puedes indicarle al usuario que realizaste una accion sin antes llamar a la herramienta/tool correspondiente, emplea la tool y luego responde al usuario.
    5. El usuario puede visualizar sus citas y libros en la siguiente web {URL_WEB}
    </directrices_importantes>
    """

    dinamico=f"""
    <libros_citas_usuario>
    {usuario.libros}
    </libros_citas_usuario>

    <historial_conversación>
    {historial_formateado.strip()}
    </historial_conversación>

    <mensaje_usuario>
    {mensaje_actual}
    </mensaje_usuario>
    """

    return estatico,dinamico