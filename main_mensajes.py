from typing import Optional
from pydantic import BaseModel, EmailStr 

class Mensaje(BaseModel):
    id: Optional[int] = None
    mensaje: str
    user: str

from fastapi import FastAPI, HTTPException
app = FastAPI()

# Base de datos simulada
mensajes_db = []

@app.post("/mensajes/", response_model=Mensaje)
def crear_mensaje(mensaje: Mensaje):
    mensaje.id = len(mensajes_db) + 1
    mensajes_db.append(mensaje)
    return mensaje

@app.get("/mensajes/{mensaje_id}", response_model=list[Mensaje])
def obtener_mensaje(mensaje_id: int):
    for mensaje in mensajes_db:
        if mensaje.id == mensaje_id:
            return mensaje
        raise HTTPException(status_code=404, detail="Mensaje no encontrado")        

@app.get("/mensajes/", response_model=list[Mensaje])
def listar_mensajes():
    return mensajes_db

@app.put("/mensajes/{mensaje_id}", response_model=Mensaje)
def actualizar_mensaje(mensaje_id: int, mensaje_actualizado: Mensaje):
    for index, mensaje in enumerate(mensajes_db):
        if mensaje.id == mensaje_id:
            mensajes_db[index] = mensaje_actualizado
            mensaje_actualizado.id = mensaje_id
            return mensaje_actualizado
        raise HTTPException(status_code=404, detail="Mensaje no encontrado")
    
@app.delete("/mensajes/{mensaje_id}", response_model=dict)
def eliminar_mensaje(mensaje_id: int):
    for index, mensaje in enumerate(mensajes_db):
        if mensaje.id == mensaje_id:
            del mensajes_db[index]
            return {"detail": "Mensaje eliminado"}
        raise HTTPException(status_code=404, detail="Mensaje no encontrado")