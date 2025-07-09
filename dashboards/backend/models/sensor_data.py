from pydantic import BaseModel, Field
from typing import Dict, List, Optional, Any
from datetime import datetime
from enum import Enum

class SensorType(str, Enum):
    GPS = "gps"
    IMU = "imu"
    CAMERA = "camera"
    BAROMETER = "barometer"
    TEMPERATURE = "temperature"

class SensorStatus(str, Enum):
    ONLINE = "online"
    OFFLINE = "offline"
    ERROR = "error"
    CALIBRATING = "calibrating"

class SensorData(BaseModel):
    sensor_id: str
    sensor_type: SensorType
    timestamp: datetime
    value: Dict[str, Any]
    status: SensorStatus = SensorStatus.ONLINE
    metadata: Optional[Dict[str, Any]] = None

class SensorReading(BaseModel):
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    altitude: Optional[float] = None
    heading: Optional[float] = None
    speed: Optional[float] = None
    roll: Optional[float] = None
    pitch: Optional[float] = None
    yaw: Optional[float] = None
    temperature: Optional[float] = None
    pressure: Optional[float] = None
    humidity: Optional[float] = None

class SensorUpload(BaseModel):
    mission_id: str
    sensor_readings: List[SensorData]
    upload_timestamp: datetime = Field(default_factory=datetime.utcnow)
