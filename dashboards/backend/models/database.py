from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, Text, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# Database URL from environment variable or default
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./watchtower.db")

# Create engine
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

# Create SessionLocal class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create Base class
Base = declarative_base()

# Database models
class SensorData(Base):
    __tablename__ = "sensor_data"
    
    id = Column(Integer, primary_key=True, index=True)
    sensor_id = Column(String, index=True)
    timestamp = Column(DateTime)
    health = Column(Float)
    temperature = Column(Float)
    humidity = Column(Float)
    vibration = Column(Float)
    emi_level = Column(Float)
    degradation_rate = Column(Float)
    physics_model_data = Column(Text)  # JSON string

class Alert(Base):
    __tablename__ = "alerts"
    
    id = Column(Integer, primary_key=True, index=True)
    sensor_id = Column(String, index=True)
    severity = Column(String)  # low, medium, high, critical
    message = Column(Text)
    timestamp = Column(DateTime)
    acknowledged = Column(Boolean, default=False)
    physics_model_triggered = Column(Boolean, default=False)

class MissionStatus(Base):
    __tablename__ = "mission_status"
    
    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime)
    altitude = Column(Float)
    speed = Column(Float)
    battery = Column(Float)
    flight_time = Column(Integer)
    mission_phase = Column(String)
    gps_satellites = Column(Integer)
    signal_strength = Column(Float)

# Create tables
Base.metadata.create_all(bind=engine) 