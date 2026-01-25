from pydantic import BaseModel

class COTRespuesta(BaseModel):
    respuesta_al_usuario: str|None