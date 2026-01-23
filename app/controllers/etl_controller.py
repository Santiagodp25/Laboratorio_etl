from fastapi import APIRouter, HTTPException, status
from app.services.etl_service import ETLService
from app.views.schemas import ExtractRequest

router = APIRouter()
etl_service = ETLService()

@router.post("/extraer", status_code=status.HTTP_201_CREATED)
async def extraer_datos(request: ExtractRequest):
    """
    Endpoint A: Extraer datos de la API externa y guardar en MongoDB
    """
    try:
        result = await etl_service.extraer_datos_api(request.cantidad)
        return result
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error en extracción: {str(e)}"
        )

@router.post("/transformar", status_code=status.HTTP_200_OK)
async def transformar_cargar():
    """
    Endpoint B: Transformar datos de MongoDB y cargar a MySQL
    """
    try:
        result = await etl_service.transformar_cargar_datos()
        return result
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error en transformación: {str(e)}"
        )

@router.delete("/reset", status_code=status.HTTP_200_OK)
async def reset_sistema():
    """
    Endpoint C: Limpiar toda la información (MongoDB y MySQL)
    """
    try:
        result = await etl_service.reset_sistema()
        return result
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error en reset: {str(e)}"
        )