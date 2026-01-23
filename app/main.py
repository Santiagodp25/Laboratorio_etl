from fastapi import FastAPI
from app.controllers.etl_controller import router as etl_router
from app.database import get_mysql_engine
from sqlalchemy import text

app = FastAPI(
    title="ETL Pipeline API",
    description="Laboratorio Final - Pipeline ETL con FastAPI",
    version="1.0.0"
)

# Incluir rutas
app.include_router(etl_router, prefix="/api/v1/etl", tags=["ETL"])

@app.on_event("startup")
async def startup_event():
    """Inicializar conexiones al iniciar la app"""
    try:
        engine = get_mysql_engine()
        # Probar conexión (forma correcta para SQLAlchemy 2.0)
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
            conn.commit()
        print("✅ Conexión a MySQL inicializada correctamente")
    except Exception as e:
        print(f"❌ Error en conexión MySQL: {e}")

@app.get("/")
async def root():
    return {
        "message": "ETL Pipeline API - Laboratorio Final",
        "endpoints": {
            "extraer": "POST /api/v1/etl/extraer - Extraer datos de API a MongoDB",
            "transformar": "POST /api/v1/etl/transformar - Transformar a MySQL", 
            "reset": "DELETE /api/v1/etl/reset - Limpiar sistema"
        },
        "integrantes": ["Tu Nombre", "Santiago"]
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "etl-pipeline"}