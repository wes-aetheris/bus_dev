import pandas as pd
import numpy as np
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
import json

class DataProcessor:
    """Service for processing sensor data"""
    
    def __init__(self):
        self.processed_data = {}
        self.statistics = {}
    
    def process_sensor_data(self, data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Process raw sensor data"""
        if not data:
            return {"error": "No data provided"}
        
        df = pd.DataFrame(data)
        
        # Basic statistics
        stats = {
            "total_records": len(df),
            "time_range": {
                "start": df['timestamp'].min() if 'timestamp' in df.columns else None,
                "end": df['timestamp'].max() if 'timestamp' in df.columns else None
            },
            "sensors": df['sensor_id'].unique().tolist() if 'sensor_id' in df.columns else []
        }
        
        # Calculate basic metrics for numeric columns
        numeric_columns = df.select_dtypes(include=[np.number]).columns
        for col in numeric_columns:
            if col in df.columns:
                stats[f"{col}_stats"] = {
                    "mean": float(df[col].mean()),
                    "std": float(df[col].std()),
                    "min": float(df[col].min()),
                    "max": float(df[col].max())
                }
        
        return {
            "processed": True,
            "statistics": stats,
            "record_count": len(df)
        }
    
    def detect_anomalies(self, data: List[Dict[str, Any]], threshold: float = 2.0) -> List[Dict[str, Any]]:
        """Detect anomalies in sensor data"""
        if not data:
            return []
        
        df = pd.DataFrame(data)
        anomalies = []
        
        # Simple anomaly detection using z-score
        numeric_columns = df.select_dtypes(include=[np.number]).columns
        
        for col in numeric_columns:
            if col in df.columns and len(df[col].dropna()) > 0:
                z_scores = np.abs((df[col] - df[col].mean()) / df[col].std())
                anomaly_indices = z_scores > threshold
                
                if anomaly_indices.any():
                    anomaly_data = df[anomaly_indices][col].to_dict()
                    anomalies.append({
                        "column": col,
                        "anomaly_indices": list(anomaly_data.keys()),
                        "anomaly_values": list(anomaly_data.values()),
                        "threshold": threshold
                    })
        
        return anomalies
    
    def calculate_physics_metrics(self, data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Calculate physics-based metrics"""
        if not data:
            return {}
        
        df = pd.DataFrame(data)
        metrics = {}
        
        # Calculate velocity if position data is available
        if all(col in df.columns for col in ['latitude', 'longitude', 'timestamp']):
            # Simple velocity calculation (placeholder)
            metrics["velocity"] = {
                "average_speed": 0.0,  # Placeholder
                "max_speed": 0.0,      # Placeholder
                "speed_variance": 0.0   # Placeholder
            }
        
        # Calculate acceleration if velocity data is available
        if 'speed' in df.columns:
            metrics["acceleration"] = {
                "average_acceleration": 0.0,  # Placeholder
                "max_acceleration": 0.0,      # Placeholder
                "acceleration_variance": 0.0   # Placeholder
            }
        
        return metrics
