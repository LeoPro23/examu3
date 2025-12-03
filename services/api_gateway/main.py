import os
import httpx
from fastapi import FastAPI, HTTPException, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional

app = FastAPI(title="API Gateway", version="1.0.0")

# Configuración CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# URLs de los microservicios
EQUIPOS_SERVICE_URL = os.getenv("EQUIPOS_SERVICE_URL", "http://equipos-service:8001")
PROVEEDORES_SERVICE_URL = os.getenv("PROVEEDORES_SERVICE_URL", "http://proveedores-service:8002")
MANTENIMIENTO_SERVICE_URL = os.getenv("MANTENIMIENTO_SERVICE_URL", "http://mantenimiento-service:8003")
REPORTES_SERVICE_URL = os.getenv("REPORTES_SERVICE_URL", "http://reportes-service:8004")
AGENT_SERVICE_URL = os.getenv("AGENT_SERVICE_URL", "http://agent-service:8005")

async def forward_request(method: str, url: str, params: dict = None, json_data: dict = None):
    async with httpx.AsyncClient() as client:
        try:
            response = await client.request(method, url, params=params, json=json_data, timeout=30.0)
            return response
        except httpx.RequestError as exc:
            raise HTTPException(status_code=503, detail=f"Error connecting to service: {exc}")

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "api-gateway"}

@app.on_event("startup")
async def startup_db():
    try:
        import asyncpg
        DATABASE_URL = os.getenv("DATABASE_URL")
        if not DATABASE_URL:
            print("DATABASE_URL not set, skipping init")
            return
            
        # Wait for DB? depends_on handles it mostly.
        # Read schema
        schema_path = "/app/database/schema.sql"
        if os.path.exists(schema_path):
            with open(schema_path, "r") as f:
                schema_sql = f.read()
            
            conn = await asyncpg.connect(DATABASE_URL)
            try:
                await conn.execute(schema_sql)
                print("Database initialized successfully from schema.sql")
            except Exception as e:
                print(f"Error initializing database: {e}")
            finally:
                await conn.close()
        else:
            print(f"Schema file not found at {schema_path}")
    except Exception as e:
        print(f"Startup error: {e}")

# --- Rutas Equipos ---
@app.api_route("/api/equipos/{path:path}", methods=["GET", "POST", "PUT", "DELETE"])
async def equipos_proxy(path: str, request: Request):
    url = f"{EQUIPOS_SERVICE_URL}/equipos/{path}" if path else f"{EQUIPOS_SERVICE_URL}/equipos"
    # Ajuste para rutas que no empiezan con /equipos en el servicio destino si fuera necesario,
    # pero asumiendo que el servicio destino maneja /equipos o la raíz.
    # Revisando equipos_service/main.py, las rutas son /equipos, /equipos/{id}, etc.
    # Si el path viene vacío, es /equipos. Si viene "1", es /equipos/1.
    
    # Sin embargo, el gateway recibe /api/equipos...
    # Si la ruta es /api/equipos, path es "" -> url = .../equipos
    # Si la ruta es /api/equipos/1, path es "1" -> url = .../equipos/1
    
    # Pero el servicio equipos tiene rutas como /categorias y /ubicaciones también.
    # Necesitamos un proxy más genérico o rutas específicas.
    
    # Vamos a hacer un proxy más inteligente o mapear rutas específicas.
    pass

# Mejor enfoque: Proxy genérico por prefijo
async def proxy(service_url: str, path: str, request: Request):
    url = f"{service_url}/{path}"
    body = await request.json() if request.method in ["POST", "PUT", "PATCH"] else None
    params = dict(request.query_params)
    
    response = await forward_request(request.method, url, params, body)
    return Response(content=response.content, status_code=response.status_code, media_type=response.headers.get("content-type"))

@app.api_route("/api/equipos/{path:path}", methods=["GET", "POST", "PUT", "DELETE"])
async def service_equipos(path: str, request: Request):
    # El servicio equipos tiene endpoints: /equipos, /categorias, /ubicaciones, /movimientos
    # Si el path empieza con 'categorias', 'ubicaciones', 'movimientos', se manda directo.
    # Si no, se asume que es parte de 'equipos'.
    
    # Pero espera, el frontend llama a /api/equipos...
    # Si el frontend llama a /api/equipos/categorias, path es "categorias".
    # El servicio espera /categorias.
    # Entonces la URL destino es SERVICE_URL/categorias.
    
    # Si el frontend llama a /api/equipos (para listar), path es "".
    # El servicio espera /equipos.
    # Entonces si path es vacio, url es SERVICE_URL/equipos.
    
    # Esto es confuso. Lo mejor es que el gateway exponga las rutas tal cual el servicio las tiene,
    # o que el frontend sepa llamar a /api/equipos/equipos (feo).
    
    # Vamos a asumir que el gateway mapea:
    # /api/equipos -> servicio equipos
    # /api/proveedores -> servicio proveedores
    
    # Si el path es "categorias", vamos a SERVICE_URL/categorias.
    # Si el path es "", vamos a SERVICE_URL/equipos (default) o SERVICE_URL/ (si el servicio tiene root).
    
    # Revisando equipos_service:
    # @app.get("/equipos")
    # @app.get("/categorias")
    # @app.get("/ubicaciones")
    
    # Entonces:
    # /api/equipos/equipos -> SERVICE/equipos
    # /api/equipos/categorias -> SERVICE/categorias
    
    # Voy a simplificar: El gateway redirige todo lo que venga despues de /api/equipos/ al servicio.
    # El frontend tendrá que ajustarse o el gateway hacer rewrite.
    # El frontend actual llama a:
    # /api/reportes/dashboard
    # /api/agents/notificaciones
    
    # No veo llamadas a equipos en el frontend_app.py (solo dashboard).
    # Pero en frontend_equipos.py (que moví) seguro hay.
    
    return await proxy(EQUIPOS_SERVICE_URL, path, request)

@app.api_route("/api/proveedores/{path:path}", methods=["GET", "POST", "PUT", "DELETE"])
async def service_proveedores(path: str, request: Request):
    return await proxy(PROVEEDORES_SERVICE_URL, path, request)

@app.api_route("/api/mantenimientos/{path:path}", methods=["GET", "POST", "PUT", "DELETE"])
async def service_mantenimientos(path: str, request: Request):
    return await proxy(MANTENIMIENTO_SERVICE_URL, path, request)

@app.api_route("/api/reportes/{path:path}", methods=["GET", "POST", "PUT", "DELETE"])
async def service_reportes(path: str, request: Request):
    return await proxy(REPORTES_SERVICE_URL, path, request)

@app.api_route("/api/agents/{path:path}", methods=["GET", "POST", "PUT", "DELETE"])
async def service_agents(path: str, request: Request):
    return await proxy(AGENT_SERVICE_URL, path, request)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
