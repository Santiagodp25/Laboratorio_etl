#  Laboratorio ETL - Pipeline con FastAPI

**Universidad de Antioquia**  
**Bases de Datos para Ciencia de Datos**  
**Docente: Miguel Ramos García**  
**Entrega: Jueves 29 de Enero, 11:59 p.m.**  
**Modalidad: Parejas**

##  Integrantes
- **Camilo Melo** - [camilo.melo@udea.edu.co]
- **Santiago Duque** - [santiago.duquep1@udea.edu.co]

##  Descripción
Implementación de un pipeline ETL completo que expone una API REST con FastAPI. El sistema orquesta un proceso ETL que extrae datos de una API pública, los almacena en MongoDB (staging), los transforma y carga a MySQL (data warehouse).

##  Objetivo
Desarrollar una aplicación de Ingeniería de Datos (Backend) que orqueste un proceso ETL completo mediante tres endpoints REST.

##  Arquitectura

### Flujo de Datos


### Tecnologías Utilizadas
- **Backend**: FastAPI, Uvicorn
- **Base de Datos NoSQL**: MongoDB (Staging Area)
- **Base de Datos SQL**: MySQL (Data Warehouse)
- **Procesamiento**: Pandas, SQLAlchemy
- **Validación**: Pydantic
- **Control de Versiones**: Git, GitHub

### Estructura del Proyecto (Patrón MVC + Services)  

- **laboratorio_etl/** (raíz del proyecto)
  - **app/** (código de la aplicación)
    - `main.py` - Punto de entrada FastAPI
    - `config.py` - Configuración
    - `database.py` - Conexiones a bases de datos
    - **controllers/** - Controladores de endpoints
      - `etl_controller.py` - Endpoints ETL
    - **models/** - Modelos de datos
      - `personajes_sql.py` - Modelo SQLAlchemy
    - **services/** - Lógica de negocio
      - `etl_service.py` - Servicio ETL
    - **views/** - Esquemas de validación
      - `schemas.py` - Esquemas Pydantic
  - `requirements.txt` - Dependencias de Python
  - `.env` - Variables de entorno
  - `README.md` - Este archivo

##  Endpoints API

### 1. `DELETE /api/v1/etl/reset`
**Descripción**: Limpia todo el sistema (MongoDB y MySQL).  
**Response**:
```json
{
  "mensaje": "Sistema reseteado correctamente",
  "mongo_docs_eliminados": 0,
  "mysql_rows_eliminadas": 0,
  "status": 200
}
```

### 2. `POST /api/v1/etl/extraer`
**Descripción**: Extrae datos de Rick & Morty API y guarda en MongoDB.  
**Response**:
```json
{
  "mensaje": "Datos extraídos exitosamente",
  "status": 200
}
```

### 3. `POST /api/v1/etl/transformar`
**Descripción**: Transforma datos de MongoDB y carga a MySQL.  
**Response**:
```json
{
  "mensaje": "Pipeline finalizado",
  "registros_procesados": 10,
  "tabla_destino": "personajes_master",
  "status": 200
}
```
## Instalación y configuración
### 1. Clonar repositorio
```bash
git clone https://github.com/Santiagodp25/Laboratorio_etl.git
cd Laboratorio_etl
```
### 2. Crear entorno virtual
```bash
python -m venv venv
.\venv\Scripts\activate
```
### 3. Instalar dependencias
```bash
pip install -r requirements.txt
```
### 4. Configurar archivo .env
```bash
MONGO_URI=mongodb://localhost:27017
MONGO_DB=etl_staging
MYSQL_HOST=localhost
MYSQL_USER=root
MYSQL_PASSWORD=tu_contraseña
MYSQL_DB=etl_warehouse
```
### 5. Ejecutar la apliación
```bash
uvicorn app.main:app --reload
```
