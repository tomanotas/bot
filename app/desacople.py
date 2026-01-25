from app.api_functions import db_functions, whatsapp
from app import agents_nativo
from app.models import internals
from dotenv import load_dotenv
from httpx import Response
import asyncio, os

load_dotenv()

URL_WEB = os.environ.get('URL_WEB')

async def principal(user_phone:str,mensaje:str):

    tasks=[]

    usuario = internals.Usuario(numero=user_phone)
    usuario_call = await db_functions.leer_usuario(user_phone)

    if(usuario_call.status_code==200):

        usuario.nombre=usuario_call.json()["nombre"]

        tasks.append(asyncio.create_task(db_functions.leer_libros_usuario(user_phone)))
        tasks.append(asyncio.create_task(db_functions.leer_citas_usuario(user_phone)))    
        tasks.append(asyncio.create_task(db_functions.leer_mensajes_usuario(user_phone,5)))

        libros_call:Response = await tasks[0]

        if(libros_call.status_code==200):
            libros_total=libros_call.json()
            for i in libros_total: usuario.libros[i["id"]]=internals.Libro(id=i["id"],titulo=i["titulo"],autor=i["autor"])

        citas_call:Response = await tasks[1]

        if(citas_call.status_code==200):
            citas_total=citas_call.json()
            for i in citas_total: usuario.libros[i["libro"]].citas.append(internals.Cita(cita=i["cita"]))

        mensajes_call:Response = await tasks[2]

        if(mensajes_call.status_code==200):
            mensajes_total=mensajes_call.json()
            for i in mensajes_total: usuario.mensajes.append(internals.Mensaje(mensaje_usuario=i["mensaje_usuario"],mensaje_ia=i["mensaje_ia"]))
        
    else:

        await whatsapp.send_text_message(f"Hola! Porfavor registrate por {URL_WEB}",user_phone)
        return "Terminado"
 
    usuario.mensajes.append(internals.Mensaje(mensaje_usuario=mensaje))

    print(usuario)

    respuesta = await agents_nativo.margot(usuario)

    await whatsapp.send_text_message(respuesta,usuario.numero)
    await db_functions.crear_mensaje(usuario.numero,mensaje,respuesta)

    return respuesta