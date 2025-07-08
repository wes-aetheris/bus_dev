from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
from datetime import datetime
from enum import Enum

class SensorType(str, Enum):
    THERMAL = "thermal"
    NAVIGATION = "navigation"
    ENVIRONMENTAL = "environmental"
    IMAGING = "imaging"

class AlertSeverity(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class MissionPhase(str, Enum):
    PREFLIGHT = "preflight"
    TAKEOFF = "takeoff"
    ACTIVE = "active"
    LANDING = "landing"
    COMPLETE = "complete"

class SensorData(BaseModel):
    sensor_id: str
    timestamp: datetime
    health: float = Field(..., ge=0, le=100)
    temperature: Optional[float] = None
    humidity: Optional[float] = None
    vibration: Optional[float] = None
    emi_level: Optional[float] = None
    degradation_rate: float = Field(..., ge=0)
    physics_model_data: Optional[Dict[str, Any]] = None

class Alert(BaseModel):
    sensor_id: str
    severity: AlertSeverity
    message: str
    timestamp: datetime
    acknowledged: bool = False
    physics_model_triggered: bool = False

class MissionStatus(BaseModel):
    timestamp: datetime
    altitude: float = Field(..., ge=0)
    speed: float = Field(..., ge=0)
    battery: float = Field(..., ge=0, le=100)
    flight_time: int = Field(..., ge=0)
    mission_phase: MissionPhase
    gps_satellites: int = Field(..., ge=0)
    signal_strength: float = Field(..., ge=0, le=100)
    temperature: Optional[float] = None
    humidity: Optional[float] = None
    wind_speed: Optional[float] = None

class PhysicsModel(BaseModel):
    model_name: str
    description: str
    parameters: List[str]
    equation: str
    sensor_id: str

class SensorHealth(BaseModel):
    sensor_id: str
    health: float
    timestamp: datetime
    physics_model: Optional[PhysicsModel] = None

class CorrelationMatrix(BaseModel):
    sensors: List[str]
    correlation_matrix: List[List[float]]
    timestamp: datetime

class UploadResponse(BaseModel):
    message: str
    filename: str
    rows: int
    columns: List[str]
    processed_data: Dict[str, Any]

class ExportResponse(BaseModel):
    format: str
    data: Dict[str, Any]
    timestamp: datetime

class WebSocketMessage(BaseModel):
    type: str
    timestamp: datetime
    data: Dict[str, Any] 