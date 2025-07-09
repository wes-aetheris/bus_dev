from pydantic import BaseModel, Field
from typing import Dict, List, Optional, Any
from datetime import datetime
from enum import Enum

class AlertSeverity(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class AlertType(str, Enum):
    SENSOR_OFFLINE = "sensor_offline"
    BATTERY_LOW = "battery_low"
    WEATHER_WARNING = "weather_warning"
    MAINTENANCE_DUE = "maintenance_due"
    CALIBRATION_NEEDED = "calibration_needed"
    ANOMALY_DETECTED = "anomaly_detected"

class Alert(BaseModel):
    id: str
    type: AlertType
    severity: AlertSeverity
    message: str
    timestamp: datetime
    sensor_id: Optional[str] = None
    mission_id: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None
    acknowledged: bool = False
    resolved: bool = False

class AlertRule(BaseModel):
    id: str
    name: str
    type: AlertType
    severity: AlertSeverity
    condition: Dict[str, Any]
    enabled: bool = True
    description: Optional[str] = None
