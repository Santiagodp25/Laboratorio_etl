import requests
import pandas as pd
from typing import Dict, List, Any
from datetime import datetime
from pymongo import UpdateOne
from sqlalchemy.exc import SQLAlchemyError

from app.database import get_mongo_client, get_mysql_engine
from app.models.personajes_sql import PersonajeSQL, Base

class ETLService:
    def __init__(self):
        self.api_url = "https://rickandmortyapi.com/api/character"
        self.mongo_db = get_mongo_client()
        self.mysql_engine = get_mysql_engine()
        self.collection_name = "personajes_raw"
        
    async def extraer_datos_api(self, cantidad: int) -> Dict[str, Any]:
        """
        Endpoint A: Extraer datos de Rick & Morty API
        Requisito: Idempotencia (no duplicar en MongoDB)
        """
        try:
            # Validar cantidad
            if cantidad <= 0:
                return {
                    "mensaje": "La cantidad debe ser mayor a 0",
                    "registros_guardados": 0,
                    "fuente": "Rick & Morty API",
                    "status": 400
                }
            
            print(f"📥 Iniciando extracción de {cantidad} personajes...")
            
            registros_guardados = 0
            pagina = 1
            collection = self.mongo_db[self.collection_name]
            
            while registros_guardados < cantidad:
                # Hacer request a la API con paginación
                response = requests.get(f"{self.api_url}?page={pagina}", timeout=30)
                response.raise_for_status()
                
                data = response.json()
                personajes = data.get("results", [])
                
                if not personajes:
                    break  # No hay más personajes
                
                # Preparar operaciones bulk con idempotencia
                operaciones = []
                for personaje in personajes:
                    if registros_guardados >= cantidad:
                        break
                    
                    # Usar el ID de la API como _id en MongoDB para idempotencia
                    personaje_id = personaje.get("id")
                    
                    operacion = UpdateOne(
                        {"_id": personaje_id},  # Buscar por ID único
                        {"$set": personaje},    # Actualizar o insertar
                        upsert=True              # Insertar si no existe
                    )
                    operaciones.append(operacion)
                    registros_guardados += 1
                
                # Ejecutar operaciones en bulk
                if operaciones:
                    result = collection.bulk_write(operaciones)
                    print(f"   Página {pagina}: {len(operaciones)} personajes procesados")
                
                pagina += 1
            
            print(f"✅ Extracción completada: {registros_guardados} registros")
            
            return {
                "mensaje": "Datos extraídos exitosamente",
                "registros_guardados": registros_guardados,
                "fuente": "Rick & Morty API",
                "status": 201
            }
            
        except requests.exceptions.RequestException as e:
            raise Exception(f"Error de conexión con la API: {str(e)}")
        except Exception as e:
            raise Exception(f"Error en extracción: {str(e)}")
    
    async def transformar_cargar_datos(self) -> Dict[str, Any]:
        """
        Endpoint B: Transformar de MongoDB y cargar a MySQL
        Requisito: No duplicar en SQL
        """
        try:
            # Aquí implementaremos la lógica de transformación
            # Por ahora estructura base
            return {
                "mensaje": "Transformación implementada parcialmente",
                "registros_procesados": 0,
                "tabla_destino": "personajes_master",
                "status": 200
            }
            
        except Exception as e:
            raise Exception(f"Error en transformación: {str(e)}")
    
    async def reset_sistema(self) -> Dict[str, Any]:
        """
        Endpoint C: Limpiar MongoDB y MySQL
        """
        try:
            # Aquí implementaremos la lógica de reset
            # Por ahora estructura base
            return {
                "mensaje": "Reset implementado parcialmente",
                "mongo_docs_eliminados": 0,
                "mysql_rows_eliminadas": 0,
                "status": 200
            }
            
        except Exception as e:
            raise Exception(f"Error en reset: {str(e)}")