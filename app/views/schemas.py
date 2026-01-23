from pydantic import BaseModel, Field
from typing import Optional

# Esquema para la solicitud de extracción (Endpoint A)
class ExtractRequest(BaseModel):
    cantidad: int = Field(..., gt=0, description="Cantidad de registros a extraer (mayor que 0)")

# Esquema para la respuesta de extracción
class ExtractResponse(BaseModel):
    mensaje: str
    registros_guardados: int
    fuente: str
    status: int

# Esquema para la respuesta de transformación
class TransformResponse(BaseModel):
    mensaje: str
    registros_procesados: int
    tabla_destino: str
    status: int

# Esquema para la respuesta de reset
class ResetResponse(BaseModel):
    mensaje: str
    mongo_docs_eliminados: int
    mysql_rows_eliminadas: int
    status: int