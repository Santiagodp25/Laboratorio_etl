from sqlalchemy import Column, Integer, String, Text, DateTime, JSON
from sqlalchemy.ext.declarative import declarative_base
import datetime

Base = declarative_base()

class PersonajeSQL(Base):
    """Modelo SQL para la tabla personajes_master basado en Rick & Morty API"""
    __tablename__ = "personajes_master"
    
    # Primary Key (usaremos el id de la API como PK)
    id = Column(Integer, primary_key=True)  # id de la API
    
    # Columnas principales de la API Rick & Morty
    name = Column(String(200), nullable=False)
    status = Column(String(50), nullable=False)  # Alive, Dead, unknown
    species = Column(String(100), nullable=False)
    type = Column(String(100), default="")
    gender = Column(String(50), nullable=False)  # Male, Female, Genderless, unknown
    
    # Información de ubicación (aplanada)
    origin_name = Column(String(200), default="Unknown")
    origin_url = Column(String(500), nullable=True)
    location_name = Column(String(200), default="Unknown")
    location_url = Column(String(500), nullable=True)
    
    # Información multimedia
    image = Column(String(500), nullable=False)
    
    # Episodios (podemos guardar como JSON o contar)
    episode_count = Column(Integer, default=0)
    
    # Metadata
    url = Column(String(500), nullable=True)
    created = Column(String(100), nullable=True)  # Fecha de creación en la API
    fecha_carga = Column(DateTime, default=datetime.datetime.utcnow)  # Cuando lo cargamos
    
    def __repr__(self):
        return f"<Personaje(id={self.id}, name='{self.name}')>"