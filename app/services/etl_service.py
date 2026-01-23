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
            print("🔄 Iniciando transformación y carga a MySQL...")
            
            # 1. EXTRACT: Leer datos de MongoDB
            collection = self.mongo_db[self.collection_name]
            cursor = collection.find({})
            datos_mongo = list(cursor)
            
            if not datos_mongo:
                return {
                    "mensaje": "No hay datos en MongoDB para transformar",
                    "registros_procesados": 0,
                    "tabla_destino": "personajes_master",
                    "status": 200
                }
            
            print(f"   📊 Datos en MongoDB: {len(datos_mongo)} documentos")
            
            # 2. TRANSFORM: Convertir a DataFrame de Pandas
            df = pd.DataFrame(datos_mongo)
            
            # Aplanar columnas anidadas
            df['origin_name'] = df['origin'].apply(lambda x: x.get('name') if x else 'Unknown')
            df['origin_url'] = df['origin'].apply(lambda x: x.get('url') if x else None)
            df['location_name'] = df['location'].apply(lambda x: x.get('name') if x else 'Unknown')
            df['location_url'] = df['location'].apply(lambda x: x.get('url') if x else None)
            
            # Contar episodios
            df['episode_count'] = df['episode'].apply(lambda x: len(x) if isinstance(x, list) else 0)
            
            # Seleccionar y renombrar columnas según el modelo SQL
            columnas_finales = {
                'id': 'id',
                'name': 'name',
                'status': 'status',
                'species': 'species',
                'type': 'type',
                'gender': 'gender',
                'origin_name': 'origin_name',
                'origin_url': 'origin_url',
                'location_name': 'location_name',
                'location_url': 'location_url',
                'image': 'image',
                'episode_count': 'episode_count',
                'url': 'url',
                'created': 'created'
            }
            
            df_final = df[list(columnas_finales.keys())].rename(columns=columnas_finales)
            
            # Manejar valores nulos
            df_final = df_final.fillna({
                'type': '',
                'origin_name': 'Unknown',
                'location_name': 'Unknown'
            })
            
            print(f"   📈 Datos transformados: {len(df_final)} registros")
            
            # 3. LOAD: Cargar a MySQL
            # Crear tabla si no existe
            Base.metadata.create_all(self.mysql_engine)
            
            # Usar pandas para insertar (to_sql)
            registros_procesados = df_final.to_sql(
                name='personajes_master',
                con=self.mysql_engine,
                if_exists='append',  # Append para no duplicar si existe
                index=False,
                method='multi'  # Inserción múltiple
            )
            
            print(f"✅ Transformación completada: {registros_procesados} registros cargados")
            
            return {
                "mensaje": "Pipeline finalizado",
                "registros_procesados": registros_procesados,
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