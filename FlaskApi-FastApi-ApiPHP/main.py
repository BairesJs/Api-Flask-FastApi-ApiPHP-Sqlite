from pydantic import BaseModel
import sqlite3
from fastapi import FastAPI, HTTPException

class DatosCreate(BaseModel):
    nombre: str
    direccion: str
    telefono: str
    email: str

class Datos(DatosCreate):
    id: int

# Conexión a la base de datos SQLite
conn = sqlite3.connect('db.sqlite')

app = FastAPI()

@app.get("/datos/")
async def get_datos():
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM datos")
    datos = cursor.fetchall()
    return {"datos": datos}

@app.delete("/datos/{dato_id}")
async def delete_dato(dato_id: int):
    cursor = conn.cursor()
    cursor.execute("DELETE FROM datos WHERE id = ?", (dato_id,))
    conn.commit()
    if cursor.rowcount == 0:
        raise HTTPException(status_code=404, detail="Dato not found")
    return {"message": f"Dato with ID {dato_id} deleted successfully"}

@app.post("/datos/", response_model=Datos)
async def create_dato(dato: DatosCreate):
    cursor = conn.cursor()
    cursor.execute("INSERT INTO datos (nombre, direccion, telefono, email) VALUES (?, ?, ?, ?)",
                   (dato.nombre, dato.direccion, dato.telefono, dato.email))
    conn.commit()
    last_id = cursor.lastrowid
    return {"id": last_id, **dato.dict()}
