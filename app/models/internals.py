from typing import Optional, List
from pydantic import BaseModel, Field

class Cita(BaseModel):
    
    cita: str = Field(..., description="Texto de la cita")

class Mensaje(BaseModel):
    
    mensaje_usuario: str = Field(..., description="Mensaje enviado por el usuario")
    mensaje_ia: Optional[str] = Field(None, description="Respuesta de la IA")
    audio: Optional[str] = Field(None, max_length=500, description="URL o path del audio")

class Libro(BaseModel):

    id: int = Field(None, description="ID del libro (autoincremental)")
    titulo: str = Field(..., max_length=200, description="Título del libro")
    autor: str = Field(..., max_length=200, description="Autor del libro")
    citas: List[Cita] = []

class Usuario(BaseModel):
    
    numero: str = Field(..., description="Número de WhatsApp (primary key)")
    nombre: str|None = Field(default = None, max_length=100, description="Nombre del usuario")
    mensajes: List[Mensaje] = []
    libros: dict[str,Libro] = {}
