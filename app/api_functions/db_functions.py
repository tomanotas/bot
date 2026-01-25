import os
from httpx import AsyncClient, Response, Timeout
from dotenv import load_dotenv
from app.utils import retry_on_failure

load_dotenv()

API_URL = os.getenv("API_URL")
timeout = Timeout(20.0)


# =========================================================
# USUARIOS
# =========================================================
@retry_on_failure()
async def crear_usuario(numero: str, nombre: str) -> Response:
    """Crear un nuevo usuario"""
    async with AsyncClient(timeout=timeout) as client:
        response = await client.post(
            f"{API_URL}/api/usuarios/",
            json={"numero": numero, "nombre": nombre}
        )
        return response

@retry_on_failure()
async def leer_usuario(numero: str) -> Response:
    """Obtener un usuario por su número de WhatsApp"""
    async with AsyncClient(timeout=timeout) as client:
        response = await client.get(f"{API_URL}/api/usuarios/{numero}/")
        return response

@retry_on_failure()
async def actualizar_usuario(numero: str, nombre: str) -> Response:
    """Actualizar un usuario"""
    async with AsyncClient(timeout=timeout) as client:
        response = await client.put(
            f"{API_URL}/api/usuarios/{numero}/",
            json={"numero": numero, "nombre": nombre}
        )
        return response


# =========================================================
# LIBROS
# =========================================================
@retry_on_failure()
async def crear_libro(titulo: str, autor: str, usuario: str) -> Response:
    """Crear un nuevo libro"""
    async with AsyncClient(timeout=timeout) as client:
        response = await client.post(
            f"{API_URL}/api/libros/",
            json={"titulo": titulo, "autor": autor, "usuario": usuario}
        )
        return response

@retry_on_failure()
async def leer_libro(libro_id: int) -> Response:
    """Obtener un libro por su ID"""
    async with AsyncClient(timeout=timeout) as client:
        response = await client.get(f"{API_URL}/api/libros/{libro_id}/")
        return response

@retry_on_failure()
async def leer_todos_libros() -> Response:
    """Obtener todos los libros"""
    async with AsyncClient(timeout=timeout) as client:
        response = await client.get(f"{API_URL}/api/libros/")
        return response

@retry_on_failure()
async def actualizar_libro(libro_id: int, titulo: str, autor: str, usuario: str) -> Response:
    """Actualizar un libro"""
    async with AsyncClient(timeout=timeout) as client:
        response = await client.put(
            f"{API_URL}/api/libros/{libro_id}/",
            json={"titulo": titulo, "autor": autor, "usuario": usuario}
        )
        return response

@retry_on_failure()
async def leer_libros_usuario(numero_usuario: str) -> Response:
    """Obtener todos los libros de un usuario"""
    async with AsyncClient(timeout=timeout) as client:
        response = await client.get(f"{API_URL}/api/usuarios/{numero_usuario}/libros/")
        return response

@retry_on_failure()
async def leer_citas_usuario(numero_usuario: str) -> Response:
    """Obtener todas las citas de los libros de un usuario"""
    async with AsyncClient(timeout=timeout) as client:
        response = await client.get(f"{API_URL}/api/usuarios/{numero_usuario}/citas/")
        return response

@retry_on_failure()
async def buscar_libro_por_titulo(titulo: str) -> Response:
    """Buscar un libro por título (búsqueda exacta)"""
    response = await leer_todos_libros()

    if response.status_code in [200, 201]:
        libros = response.json()
        for libro in libros:
            if libro.get("titulo", "").lower() == titulo.lower():
                # Retornar response con el libro encontrado
                return response

    return response


# =========================================================
# CITAS
# =========================================================
@retry_on_failure()
async def crear_cita(cita: str, libro_id: int) -> Response:
    """Crear una nueva cita"""
    async with AsyncClient(timeout=timeout) as client:
        response = await client.post(
            f"{API_URL}/api/citas/",
            json={
                "cita": cita,
                "libro": libro_id
            }
        )
        return response

@retry_on_failure()
async def leer_cita(cita_id: int) -> Response:
    """Obtener una cita por su ID"""
    async with AsyncClient(timeout=timeout) as client:
        response = await client.get(f"{API_URL}/api/citas/{cita_id}/")
        return response

@retry_on_failure()
async def leer_todas_citas() -> Response:
    """Obtener todas las citas"""
    async with AsyncClient(timeout=timeout) as client:
        response = await client.get(f"{API_URL}/api/citas/")
        return response

@retry_on_failure()
async def leer_citas_libro(libro_id: int) -> Response:
    """Obtener todas las citas de un libro"""
    async with AsyncClient(timeout=timeout) as client:
        response = await client.get(f"{API_URL}/api/libros/{libro_id}/citas/")
        return response

@retry_on_failure()
async def actualizar_cita(cita_id: int, cita: str, libro_id: int) -> Response:
    """Actualizar una cita"""
    async with AsyncClient(timeout=timeout) as client:
        response = await client.put(
            f"{API_URL}/api/citas/{cita_id}/",
            json={
                "cita": cita,
                "libro": libro_id
            }
        )
        return response


# =========================================================
# MENSAJES
# =========================================================
@retry_on_failure()
async def crear_mensaje(usuario: str, mensaje_usuario: str, mensaje_ia: str = None, audio: str = None) -> Response:
    """Crear un nuevo mensaje"""
    async with AsyncClient(timeout=timeout) as client:
        response = await client.post(
            f"{API_URL}/api/mensajes/",
            json={
                "usuario": usuario,
                "mensaje_usuario": mensaje_usuario,
                "mensaje_ia": mensaje_ia,
                "audio": audio
            }
        )
        return response

@retry_on_failure()
async def leer_mensaje(mensaje_id: int) -> Response:
    """Obtener un mensaje por su ID"""
    async with AsyncClient(timeout=timeout) as client:
        response = await client.get(f"{API_URL}/api/mensajes/{mensaje_id}/")
        return response

@retry_on_failure()
async def leer_todos_mensajes() -> Response:
    """Obtener todos los mensajes"""
    async with AsyncClient(timeout=timeout) as client:
        response = await client.get(f"{API_URL}/api/mensajes/")
        return response

@retry_on_failure()
async def leer_mensajes_usuario(numero_usuario: str, limit: int = 6) -> Response:
    """Obtener mensajes de un usuario, ordenados por tiempo (más recientes primero)

    Args:
        numero_usuario: Número de WhatsApp del usuario
        limit: Cantidad de mensajes a retornar (últimos k mensajes). Si es None, retorna todos.
    """
    async with AsyncClient(timeout=timeout) as client:
        url = f"{API_URL}/api/usuarios/{numero_usuario}/mensajes/"
        if limit is not None:
            url += f"?limit={limit}"
        response = await client.get(url)
        return response

@retry_on_failure()
async def actualizar_mensaje(mensaje_id: int, usuario: str, mensaje_usuario: str, mensaje_ia: str = None, audio: str = None) -> Response:
    """Actualizar un mensaje"""
    async with AsyncClient(timeout=timeout) as client:
        response = await client.put(
            f"{API_URL}/api/mensajes/{mensaje_id}/",
            json={
                "usuario": usuario,
                "mensaje_usuario": mensaje_usuario,
                "mensaje_ia": mensaje_ia,
                "audio": audio
            }
        )
        return response
