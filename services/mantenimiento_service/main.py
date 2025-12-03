from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, List
import asyncpg
import os
from datetime import date

app = FastAPI(title="Mantenimiento Service", version="1.0.0")

DATABASE_URL = os.getenv("DATABASE_URL")

POOL = None

@app.on_event("startup")
async def startup_db():
    global POOL
    POOL = await asyncpg.create_pool(DATABASE_URL)

@app.on_event("shutdown")
async def shutdown_db():
    if POOL:
        await POOL.close()

async def get_db_pool():
    return POOL

class MantenimientoCreate(BaseModel):
    equipo_id: int
    tipo: str
    fecha_programada: Optional[date] = None
    tecnico_id: Optional[int] = None
    proveedor_id: Optional[int] = None
    descripcion: Optional[str] = None
    prioridad: str = "media"

class MantenimientoUpdate(BaseModel):
    fecha_realizada: Optional[date] = None
    problema_reportado: Optional[str] = None
    solucion_aplicada: Optional[str] = None
    costo: Optional[float] = None
    tiempo_fuera_servicio_horas: Optional[float] = None
    estado: Optional[str] = None
    observaciones: Optional[str] = None

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "mantenimiento"}

@app.get("/mantenimientos")
async def get_mantenimientos(estado: Optional[str] = None):
    pool = await get_db_pool()
    query = "SELECT * FROM mantenimientos"
    params = []
    if estado:
        query += " WHERE estado = $1"
        params.append(estado)
    query += " ORDER BY fecha_programada DESC"
    
    async with pool.acquire() as conn:
        rows = await conn.fetch(query, *params)
        return [dict(row) for row in rows]

@app.post("/mantenimientos")
async def create_mantenimiento(mantenimiento: MantenimientoCreate):
    pool = await get_db_pool()
    query = """
        INSERT INTO mantenimientos (
            equipo_id, tipo, fecha_programada, tecnico_id, proveedor_id, 
            descripcion, prioridad, estado
        ) VALUES ($1, $2, $3, $4, $5, $6, $7, 'programado')
        RETURNING id
    """
    async with pool.acquire() as conn:
        try:
            mantenimiento_id = await conn.fetchval(
                query,
                mantenimiento.equipo_id,
                mantenimiento.tipo,
                mantenimiento.fecha_programada,
                mantenimiento.tecnico_id,
                mantenimiento.proveedor_id,
                mantenimiento.descripcion,
                mantenimiento.prioridad
            )
            return {"id": mantenimiento_id, "message": "Mantenimiento programado exitosamente"}
        except asyncpg.ForeignKeyViolationError:
             raise HTTPException(status_code=400, detail="ID de equipo, técnico o proveedor inválido")

@app.put("/mantenimientos/{mantenimiento_id}")
async def update_mantenimiento(mantenimiento_id: int, mantenimiento: MantenimientoUpdate):
    pool = await get_db_pool()
    updates = []
    params = []
    param_count = 1
    
    for field, value in mantenimiento.dict(exclude_unset=True).items():
        updates.append(f"{field} = ${param_count}")
        params.append(value)
        param_count += 1
        
    if not updates:
        raise HTTPException(status_code=400, detail="No hay campos para actualizar")
        
    params.append(mantenimiento_id)
    query = f"UPDATE mantenimientos SET {', '.join(updates)} WHERE id = ${param_count}"
    
    async with pool.acquire() as conn:
        result = await conn.execute(query, *params)
        if result == "UPDATE 0":
            raise HTTPException(status_code=404, detail="Mantenimiento no encontrado")
        return {"message": "Mantenimiento actualizado exitosamente"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8003)
