from app.models import internals
from app.api_functions import db_functions


async def acciones(tool_name: str, function_args: dict, api_state: internals.Usuario):
    """
    Ejecuta las acciones de las tools llamadas por Margot

    Args:
        tool_name: Nombre de la tool a ejecutar
        function_args: Argumentos de la tool
        api_state: Usuario actual

    Returns:
        str: Respuesta de la ejecución de la tool
    """

    if tool_name == "crear_libro":
        titulo = function_args.get("titulo")
        autor = function_args.get("autor")
        usuario = api_state.numero

        response = await db_functions.crear_libro(titulo=titulo, autor=autor, usuario=usuario)

        if response.status_code in [200, 201]:
            libro = response.json()
            return f"Libro '{titulo}' de {autor} creado exitosamente con ID {libro['id']}"
        else:
            return f"Error al crear el libro: {response.status_code}"

    elif tool_name == "crear_cita":
        cita = function_args.get("cita")
        libro_id = function_args.get("libro_id")

        response = await db_functions.crear_cita(cita=cita, libro_id=libro_id)

        if response.status_code in [200, 201]:
            cita_creada = response.json()
            return f"Cita guardada exitosamente en el libro con ID {cita_creada['id']}"
        else:
            return f"Error al crear la cita: {response.status_code}"

    else:
        return f"Tool '{tool_name}' no reconocida"
