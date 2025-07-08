import numpy as np
from scipy import stats
from datetime import datetime, timedelta
from typing import Dict, Any, Optional
import json

class PhysicsModelService:
    """Service for physics-based sensor degradation modeling"""
    
    def __init__(self):
        self.initialized = False
        self.models = {}
        
    async def initialize(self):
        """Initialize physics models"""
        self.models = {
            "thermal_camera": {
                "name": "Arrhenius Degradation",
                "description": "Dark current doubling every 6-8°C temperature increase",
                "parameters": ["temperature", "time", "initial_health"],
                "equation": "degradation = A * exp(-Ea/(k*T)) * time",
                "constants": {
                    "A": 1e-6,  # Pre-exponential factor
                    "Ea": 0.5,  # Activation energy (eV)
                    "k": 8.617e-5,  # Boltzmann constant (eV/K)
                    "doubling_temp": 7.0  # Temperature for doubling (K)
                }
            },
            "gps": {
                "name": "EMI Correlation",
                "description": "Signal degradation based on electromagnetic interference",
                "parameters": ["emi_level", "signal_strength", "frequency"],
                "equation": "degradation = EMI_factor * signal_strength * frequency",
                "constants": {
                    "emi_threshold": 0.3,
                    "frequency_factor": 1.5,
                    "signal_decay_rate": 0.1
                }
            },
            "imu": {
                "name": "Vibration-Induced Bias Drift",
                "description": "Bias drift caused by mechanical vibration",
                "parameters": ["vibration_level", "frequency", "duration"],
                "equation": "drift = vibration_amplitude * frequency * sqrt(duration)",
                "constants": {
                    "vibration_threshold": 0.2,
                    "frequency_weight": 1.2,
                    "time_factor": 0.5
                }
            },
            "environmental": {
                "name": "Multi-Factor Correlation",
                "description": "Combined effects of temperature, humidity, vibration, and EMI",
                "parameters": ["temperature", "humidity", "vibration", "emi"],
                "equation": "total_effect = Σ(weight_i * factor_i)",
                "constants": {
                    "temp_weight": 0.3,
                    "humidity_weight": 0.2,
                    "vibration_weight": 0.3,
                    "emi_weight": 0.2
                }
            }
        }
        self.initialized = True
    
    def is_initialized(self) -> bool:
        """Check if service is initialized"""
        return self.initialized
    
    def calculate_thermal_degradation(self, temperature: float, time_hours: float = 1.0) -> float:
        """Calculate thermal camera degradation using Arrhenius model"""
        if not self.initialized:
            return 0.0
        
        model = self.models["thermal_camera"]
        constants = model["constants"]
        
        # Convert temperature to Kelvin
        T = temperature + 273.15
        
        # Arrhenius equation for degradation rate
        degradation_rate = constants["A"] * np.exp(-constants["Ea"] / (constants["k"] * T))
        
        # Calculate degradation over time
        degradation = degradation_rate * time_hours * 100  # Convert to percentage
        
        # Apply temperature doubling effect
        if temperature > 25:  # Above room temperature
            temp_factor = 2 ** ((temperature - 25) / constants["doubling_temp"])
            degradation *= temp_factor
        
        return min(degradation, 100.0)  # Cap at 100%
    
    def calculate_gps_degradation(self, emi_level: float, signal_strength: float = 85.0) -> float:
        """Calculate GPS degradation based on EMI levels"""
        if not self.initialized:
            return 0.0
        
        model = self.models["gps"]
        constants = model["constants"]
        
        # Base degradation from EMI
        emi_factor = max(0, emi_level - constants["emi_threshold"])
        base_degradation = emi_factor * constants["frequency_factor"]
        
        # Signal strength effect
        signal_factor = (100 - signal_strength) / 100
        signal_degradation = signal_factor * constants["signal_decay_rate"]
        
        # Combined degradation
        total_degradation = (base_degradation + signal_degradation) * 100
        
        return min(total_degradation, 100.0)
    
    def calculate_imu_degradation(self, vibration_level: float, frequency: float = 50.0, duration_hours: float = 1.0) -> float:
        """Calculate IMU degradation from vibration"""
        if not self.initialized:
            return 0.0
        
        model = self.models["imu"]
        constants = model["constants"]
        
        # Vibration threshold effect
        if vibration_level > constants["vibration_threshold"]:
            vibration_factor = (vibration_level - constants["vibration_threshold"]) / (1 - constants["vibration_threshold"])
        else:
            vibration_factor = 0
        
        # Frequency effect
        freq_factor = frequency / 100  # Normalize frequency
        
        # Time effect (square root relationship)
        time_factor = np.sqrt(duration_hours)
        
        # Calculate drift
        drift = vibration_factor * freq_factor * time_factor * constants["frequency_weight"] * constants["time_factor"]
        
        # Convert to percentage degradation
        degradation = drift * 100
        
        return min(degradation, 100.0)
    
    def calculate_environmental_correlation(self, temperature: float, humidity: float, vibration: float, emi: float) -> float:
        """Calculate combined environmental effects"""
        if not self.initialized:
            return 0.0
        
        model = self.models["environmental"]
        constants = model["constants"]
        
        # Normalize factors to 0-1 range
        temp_factor = max(0, min(1, (temperature - 20) / 40))  # 20-60°C range
        humidity_factor = humidity / 100
        vibration_factor = vibration
        emi_factor = emi
        
        # Weighted combination
        total_effect = (
            constants["temp_weight"] * temp_factor +
            constants["humidity_weight"] * humidity_factor +
            constants["vibration_weight"] * vibration_factor +
            constants["emi_weight"] * emi_factor
        )
        
        return min(total_effect * 100, 100.0)
    
    def predict_sensor_life(self, sensor_id: str, current_health: float, environmental_factors: Dict[str, float]) -> Dict[str, Any]:
        """Predict remaining sensor life based on physics models"""
        if not self.initialized:
            return {"remaining_hours": 0, "confidence": 0}
        
        if sensor_id == "thermal_camera":
            temp = environmental_factors.get("temperature", 25)
            degradation_rate = self.calculate_thermal_degradation(temp, 1.0)
            remaining_hours = max(0, (100 - current_health) / degradation_rate) if degradation_rate > 0 else 1000
            
        elif sensor_id == "gps":
            emi = environmental_factors.get("emi_level", 0.1)
            degradation_rate = self.calculate_gps_degradation(emi)
            remaining_hours = max(0, (100 - current_health) / degradation_rate) if degradation_rate > 0 else 2000
            
        elif sensor_id == "imu":
            vibration = environmental_factors.get("vibration_level", 0.1)
            degradation_rate = self.calculate_imu_degradation(vibration)
            remaining_hours = max(0, (100 - current_health) / degradation_rate) if degradation_rate > 0 else 1500
            
        else:
            remaining_hours = 1000  # Default
            
        # Calculate confidence based on data quality
        confidence = min(0.95, max(0.5, current_health / 100))
        
        return {
            "remaining_hours": round(remaining_hours, 1),
            "confidence": round(confidence, 2),
            "degradation_rate": round(degradation_rate, 3) if 'degradation_rate' in locals() else 0.1
        }
    
    def get_model_info(self, sensor_id: str) -> Optional[Dict[str, Any]]:
        """Get information about a specific physics model"""
        if not self.initialized:
            return None
        
        return self.models.get(sensor_id, None)
    
    def get_all_models(self) -> Dict[str, Any]:
        """Get all physics models information"""
        if not self.initialized:
            return {}
        
        return self.models
    
    def validate_physics_prediction(self, sensor_id: str, actual_health: float, predicted_health: float) -> Dict[str, Any]:
        """Validate physics model predictions against actual measurements"""
        error = abs(actual_health - predicted_health)
        accuracy = max(0, 100 - error)
        
        return {
            "sensor_id": sensor_id,
            "actual_health": actual_health,
            "predicted_health": predicted_health,
            "error": round(error, 2),
            "accuracy": round(accuracy, 2),
            "timestamp": datetime.now().isoformat()
        } 