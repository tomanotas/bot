from httpx import AsyncClient, Response, Timeout
from dotenv import load_dotenv
from app.utils import retry_on_failure
import json, os

timeout = Timeout(20.0)

load_dotenv()

API_KEY = os.environ.get('KAPSO_API_KEY')
PHONE_NUMBER_ID = os.environ.get('KAPSO_PHONE_NUMBER_ID')

KAPSO_API_BASE = "https://api.kapso.ai/meta/whatsapp/v24.0"

@retry_on_failure()
async def send_text_message(mensaje:str,numero:str):

    headers = {
        "X-API-Key": API_KEY,
        "Content-Type": "application/json"
    }

    url = f"{KAPSO_API_BASE}/{PHONE_NUMBER_ID}/messages"

    payload = {
        "messaging_product": "whatsapp",
        "to": numero,
        "type": "text",
        "text": {"body": mensaje}
    }

    async with AsyncClient(timeout=timeout) as client:
        response = await client.post(
            url,
            json=payload,
            headers=headers
        )
        return response
