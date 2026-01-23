from pymongo import MongoClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.config import config

# MongoDB Connection
def get_mongo_client():
    """Conexión a MongoDB para staging"""
    client = MongoClient(config.MONGO_URI)
    return client[config.MONGO_DB]

# MySQL Connection (SQLAlchemy)
def get_mysql_engine():
    """Conexión a MySQL para data warehouse"""
    connection_string = f"mysql+pymysql://{config.MYSQL_USER}:{config.MYSQL_PASSWORD}@{config.MYSQL_HOST}/{config.MYSQL_DB}"
    engine = create_engine(connection_string, echo=True)
    return engine

def get_mysql_session():
    """Sesión para operaciones en MySQL"""
    engine = get_mysql_engine()
    Session = sessionmaker(bind=engine)
    return Session()