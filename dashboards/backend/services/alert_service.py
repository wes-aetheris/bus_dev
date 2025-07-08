from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
import json

class AlertService:
    """Service for managing sensor alerts and notifications"""
    
    def __init__(self):
        self.initialized = False
        self.alerts = []
        self.alert_history = []
        self.alert_rules = {}
    
    async def initialize(self):
        """Initialize the alert service"""
        self.initialized = True
        
        # Define alert rules based on physics models
        self.alert_rules = {
            "thermal_camera": {
                "health_threshold": 75,
                "temperature_threshold": 50,
                "degradation_rate_threshold": 0.2,
                "severity_levels": {
                    "critical": {"health": 60, "temp": 60},
                    "high": {"health": 70, "temp": 50},
                    "medium": {"health": 80, "temp": 45},
                    "low": {"health": 85, "temp": 40}
                }
            },
            "gps": {
                "health_threshold": 80,
                "emi_threshold": 0.5,
                "signal_strength_threshold": 70,
                "severity_levels": {
                    "critical": {"health": 65, "emi": 0.7, "signal": 50},
                    "high": {"health": 75, "emi": 0.6, "signal": 60},
                    "medium": {"health": 85, "emi": 0.5, "signal": 70},
                    "low": {"health": 90, "emi": 0.4, "signal": 80}
                }
            },
            "imu": {
                "health_threshold": 70,
                "vibration_threshold": 0.6,
                "bias_drift_threshold": 0.3,
                "severity_levels": {
                    "critical": {"health": 55, "vibration": 0.8, "drift": 0.5},
                    "high": {"health": 65, "vibration": 0.7, "drift": 0.4},
                    "medium": {"health": 75, "vibration": 0.6, "drift": 0.3},
                    "low": {"health": 85, "vibration": 0.5, "drift": 0.2}
                }
            },
            "barometer": {
                "health_threshold": 85,
                "pressure_variance_threshold": 0.2,
                "severity_levels": {
                    "critical": {"health": 70, "variance": 0.4},
                    "high": {"health": 80, "variance": 0.3},
                    "medium": {"health": 85, "variance": 0.25},
                    "low": {"health": 90, "variance": 0.2}
                }
            }
        }
        
        # Initialize with some sample alerts
        self._generate_sample_alerts()
    
    def is_initialized(self) -> bool:
        """Check if service is initialized"""
        return self.initialized
    
    def _generate_sample_alerts(self):
        """Generate sample alerts for demonstration"""
        sample_alerts = [
            {
                "id": 1,
                "sensor_id": "thermal_camera",
                "severity": "medium",
                "message": "Thermal camera showing increased degradation rate. Temperature factor contributing to Arrhenius degradation.",
                "timestamp": datetime.now() - timedelta(hours=2),
                "acknowledged": False,
                "physics_model_triggered": True,
                "model_data": {
                    "temperature": 48.5,
                    "degradation_rate": 0.15,
                    "predicted_life_hours": 120
                }
            },
            {
                "id": 2,
                "sensor_id": "imu",
                "severity": "high",
                "message": "IMU experiencing vibration-induced bias drift. Recommend calibration check.",
                "timestamp": datetime.now() - timedelta(hours=1),
                "acknowledged": False,
                "physics_model_triggered": True,
                "model_data": {
                    "vibration_level": 0.65,
                    "bias_drift": 0.35,
                    "frequency": 45.2
                }
            },
            {
                "id": 3,
                "sensor_id": "gps",
                "severity": "low",
                "message": "GPS signal strength fluctuating due to EMI interference.",
                "timestamp": datetime.now() - timedelta(minutes=30),
                "acknowledged": True,
                "physics_model_triggered": True,
                "model_data": {
                    "emi_level": 0.42,
                    "signal_strength": 78.5,
                    "satellites": 7
                }
            }
        ]
        
        self.alerts = sample_alerts
    
    def get_current_alerts(self) -> List[Dict[str, Any]]:
        """Get current active alerts"""
        if not self.initialized:
            return []
        
        # Filter out acknowledged alerts older than 24 hours
        cutoff_time = datetime.now() - timedelta(hours=24)
        active_alerts = [
            alert for alert in self.alerts
            if not alert["acknowledged"] or alert["timestamp"] > cutoff_time
        ]
        
        return active_alerts
    
    def check_sensor_alerts(self, sensor_id: str, sensor_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Check for new alerts based on sensor data"""
        if not self.initialized or sensor_id not in self.alert_rules:
            return []
        
        rules = self.alert_rules[sensor_id]
        new_alerts = []
        
        # Check health threshold
        health = sensor_data.get("health", 100)
        if health < rules["health_threshold"]:
            severity = self._determine_severity(sensor_id, "health", health)
            alert = self._create_alert(sensor_id, severity, f"Health below threshold: {health}%", sensor_data)
            new_alerts.append(alert)
        
        # Check temperature threshold (for thermal camera)
        if sensor_id == "thermal_camera":
            temperature = sensor_data.get("temperature", 25)
            if temperature > rules["temperature_threshold"]:
                severity = self._determine_severity(sensor_id, "temp", temperature)
                alert = self._create_alert(sensor_id, severity, f"Temperature above threshold: {temperature}°C", sensor_data)
                new_alerts.append(alert)
        
        # Check EMI threshold (for GPS)
        if sensor_id == "gps":
            emi_level = sensor_data.get("emi_level", 0)
            if emi_level > rules["emi_threshold"]:
                severity = self._determine_severity(sensor_id, "emi", emi_level)
                alert = self._create_alert(sensor_id, severity, f"EMI level above threshold: {emi_level}", sensor_data)
                new_alerts.append(alert)
        
        # Check vibration threshold (for IMU)
        if sensor_id == "imu":
            vibration = sensor_data.get("vibration", 0)
            if vibration > rules["vibration_threshold"]:
                severity = self._determine_severity(sensor_id, "vibration", vibration)
                alert = self._create_alert(sensor_id, severity, f"Vibration above threshold: {vibration}", sensor_data)
                new_alerts.append(alert)
        
        # Add new alerts to the list
        for alert in new_alerts:
            self.alerts.append(alert)
        
        return new_alerts
    
    def _determine_severity(self, sensor_id: str, metric: str, value: float) -> str:
        """Determine alert severity based on sensor data"""
        if sensor_id not in self.alert_rules:
            return "low"
        
        rules = self.alert_rules[sensor_id]["severity_levels"]
        
        # Check from highest to lowest severity
        for severity in ["critical", "high", "medium", "low"]:
            if severity in rules:
                threshold = rules[severity].get(metric, float('inf'))
                if value <= threshold:
                    return severity
        
        return "low"
    
    def _create_alert(self, sensor_id: str, severity: str, message: str, sensor_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new alert"""
        alert_id = max([alert["id"] for alert in self.alerts], default=0) + 1
        
        return {
            "id": alert_id,
            "sensor_id": sensor_id,
            "severity": severity,
            "message": message,
            "timestamp": datetime.now(),
            "acknowledged": False,
            "physics_model_triggered": True,
            "model_data": sensor_data
        }
    
    def acknowledge_alert(self, alert_id: int) -> bool:
        """Acknowledge an alert"""
        for alert in self.alerts:
            if alert["id"] == alert_id:
                alert["acknowledged"] = True
                return True
        return False
    
    def get_alert_statistics(self) -> Dict[str, Any]:
        """Get alert statistics"""
        if not self.initialized:
            return {}
        
        total_alerts = len(self.alerts)
        active_alerts = len([a for a in self.alerts if not a["acknowledged"]])
        
        severity_counts = {}
        sensor_counts = {}
        
        for alert in self.alerts:
            # Count by severity
            severity = alert["severity"]
            severity_counts[severity] = severity_counts.get(severity, 0) + 1
            
            # Count by sensor
            sensor_id = alert["sensor_id"]
            sensor_counts[sensor_id] = sensor_counts.get(sensor_id, 0) + 1
        
        return {
            "total_alerts": total_alerts,
            "active_alerts": active_alerts,
            "acknowledged_alerts": total_alerts - active_alerts,
            "severity_distribution": severity_counts,
            "sensor_distribution": sensor_counts,
            "physics_model_alerts": len([a for a in self.alerts if a["physics_model_triggered"]])
        }
    
    def get_alerts_by_severity(self, severity: str) -> List[Dict[str, Any]]:
        """Get alerts filtered by severity"""
        return [alert for alert in self.alerts if alert["severity"] == severity]
    
    def get_alerts_by_sensor(self, sensor_id: str) -> List[Dict[str, Any]]:
        """Get alerts filtered by sensor"""
        return [alert for alert in self.alerts if alert["sensor_id"] == sensor_id]
    
    def clear_old_alerts(self, days: int = 7):
        """Clear alerts older than specified days"""
        cutoff_time = datetime.now() - timedelta(days=days)
        self.alerts = [alert for alert in self.alerts if alert["timestamp"] > cutoff_time]
    
    def export_alerts(self, format: str = "json") -> str:
        """Export alerts in specified format"""
        if format == "json":
            return json.dumps(self.alerts, default=str, indent=2)
        elif format == "csv":
            # Convert to CSV format
            csv_lines = ["id,sensor_id,severity,message,timestamp,acknowledged,physics_model_triggered"]
            for alert in self.alerts:
                csv_lines.append(f"{alert['id']},{alert['sensor_id']},{alert['severity']},\"{alert['message']}\",{alert['timestamp']},{alert['acknowledged']},{alert['physics_model_triggered']}")
            return "\n".join(csv_lines)
        else:
            return "Unsupported format" 