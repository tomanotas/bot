from app import desacople
from fastapi import Depends, FastAPI, BackgroundTasks, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from app.config.settings import logfire, logger
import os

from app.models import external_models

load_dotenv()

SETUP = os.getenv("SETUP")

app = FastAPI(title="Hook API")
logfire.instrument_fastapi(app)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

procesados={}

@app.get("/")
def hola():
    return "Hola a todos"

@app.post("/hook")
async def whatsapp_webhook(request: Request, payload: external_models.KapsoWebhookPayload, background_tasks: BackgroundTasks):

    idempotency_key = request.headers.get("x-idempotency-key")

    if(idempotency_key in procesados): return
    procesados[idempotency_key]=1

    #print(payload)

    mensaje = ""
    user_phone = None

    for i in payload.data:

        if user_phone is None: user_phone = i.message.from_

        if i.message.type == "text":

            mensaje += i.message.text.body + "\n"

        elif i.message.type == "audio":

            mensaje += i.message.kapso.transcript.text + "\n"

    user_phone="+"+user_phone

    print(f"Usuario: {user_phone}")
    print(f"Mensaje: {mensaje}")

    if SETUP == "LOCAL":
        return await desacople.principal(user_phone, mensaje)
    else:
        background_tasks.add_task(desacople.principal, user_phone, mensaje)

