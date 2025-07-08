import pandas as pd
import numpy as np
from typing import Dict, Any, List, Optional
import json
import os
from datetime import datetime
import plotly.graph_objects as go
import plotly.express as px
from io import StringIO
import base64

class DataProcessor:
    """Service for processing CSV data and generating reports"""
    
    def __init__(self):
        self.initialized = False
        self.processed_data = {}
        self.upload_history = []
    
    async def initialize(self):
        """Initialize the data processor"""
        self.initialized = True
        # Create data directory if it doesn't exist
        os.makedirs("data", exist_ok=True)
    
    def is_initialized(self) -> bool:
        """Check if service is initialized"""
        return self.initialized
    
    def process_csv_data(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Process uploaded CSV data"""
        if not self.initialized:
            return {"error": "Data processor not initialized"}
        
        try:
            # Basic data validation
            required_columns = ["timestamp", "sensor_id", "health"]
            missing_columns = [col for col in required_columns if col not in df.columns]
            
            if missing_columns:
                return {
                    "error": f"Missing required columns: {missing_columns}",
                    "available_columns": list(df.columns)
                }
            
            # Convert timestamp column
            if "timestamp" in df.columns:
                df["timestamp"] = pd.to_datetime(df["timestamp"])
            
            # Calculate statistics
            stats = {
                "total_rows": len(df),
                "unique_sensors": df["sensor_id"].nunique() if "sensor_id" in df.columns else 0,
                "date_range": {
                    "start": df["timestamp"].min().isoformat() if "timestamp" in df.columns else None,
                    "end": df["timestamp"].max().isoformat() if "timestamp" in df.columns else None
                },
                "health_stats": {
                    "mean": df["health"].mean() if "health" in df.columns else 0,
                    "std": df["health"].std() if "health" in df.columns else 0,
                    "min": df["health"].min() if "health" in df.columns else 0,
                    "max": df["health"].max() if "health" in df.columns else 0
                }
            }
            
            # Generate correlation matrix if multiple sensors
            if "sensor_id" in df.columns and df["sensor_id"].nunique() > 1:
                pivot_df = df.pivot(index="timestamp", columns="sensor_id", values="health")
                correlation_matrix = pivot_df.corr().fillna(0).to_dict()
                stats["correlation_matrix"] = correlation_matrix
            
            # Detect anomalies
            if "health" in df.columns:
                health_series = df["health"]
                mean_health = health_series.mean()
                std_health = health_series.std()
                
                # Anomaly detection (values outside 2 standard deviations)
                anomalies = health_series[abs(health_series - mean_health) > 2 * std_health]
                stats["anomalies"] = {
                    "count": len(anomalies),
                    "indices": anomalies.index.tolist(),
                    "values": anomalies.tolist()
                }
            
            # Store processed data
            filename = f"processed_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            self.processed_data[filename] = {
                "dataframe": df,
                "statistics": stats,
                "processed_at": datetime.now().isoformat()
            }
            
            return {
                "success": True,
                "filename": filename,
                "statistics": stats,
                "processed_at": datetime.now().isoformat()
            }
            
        except Exception as e:
            return {
                "error": f"Error processing CSV data: {str(e)}",
                "success": False
            }
    
    def convert_to_csv(self, data: Dict[str, Any]) -> str:
        """Convert data to CSV format"""
        try:
            # Extract sensor data
            sensors = data.get("sensors", {}).get("sensors", [])
            
            # Create DataFrame
            df_data = []
            for sensor in sensors:
                df_data.append({
                    "sensor_id": sensor["id"],
                    "name": sensor["name"],
                    "type": sensor["type"],
                    "health": sensor["health"],
                    "degradation_rate": sensor["degradation_rate"],
                    "last_calibration": sensor["last_calibration"],
                    "next_calibration": sensor["next_calibration"]
                })
            
            df = pd.DataFrame(df_data)
            
            # Convert to CSV string
            csv_buffer = StringIO()
            df.to_csv(csv_buffer, index=False)
            return csv_buffer.getvalue()
            
        except Exception as e:
            return f"Error converting to CSV: {str(e)}"
    
    def generate_pdf_report(self, data: Dict[str, Any]) -> str:
        """Generate PDF report (simulated)"""
        try:
            # In a real implementation, this would use a library like reportlab
            # For now, we'll return a JSON representation of the report structure
            
            report = {
                "title": "Watchtower Sensor Health Report",
                "generated_at": datetime.now().isoformat(),
                "sections": [
                    {
                        "title": "Executive Summary",
                        "content": f"Report generated for {len(data.get('sensors', {}).get('sensors', []))} sensors"
                    },
                    {
                        "title": "Sensor Health Overview",
                        "content": "Detailed sensor health analysis with physics-based modeling"
                    },
                    {
                        "title": "Correlation Analysis",
                        "content": "Cross-sensor correlation matrix and analysis"
                    },
                    {
                        "title": "Mission Status",
                        "content": "Current mission parameters and status"
                    },
                    {
                        "title": "Alerts and Recommendations",
                        "content": "Active alerts and maintenance recommendations"
                    }
                ]
            }
            
            return json.dumps(report, indent=2)
            
        except Exception as e:
            return f"Error generating PDF report: {str(e)}"
    
    def generate_sample_data(self) -> pd.DataFrame:
        """Generate realistic sample sensor data with physics-based patterns"""
        np.random.seed(42)  # For reproducible results
        
        # Generate time series
        start_date = datetime.now() - pd.Timedelta(days=30)
        timestamps = pd.date_range(start=start_date, end=datetime.now(), freq='H')
        
        data = []
        
        for timestamp in timestamps:
            # Thermal camera - Arrhenius degradation pattern
            temp_factor = 1 + 0.1 * np.sin(2 * np.pi * timestamp.hour / 24)  # Daily temperature cycle
            thermal_health = 95 - 0.5 * (timestamp - start_date).total_seconds() / 3600 * temp_factor
            thermal_health = max(60, thermal_health + np.random.normal(0, 2))
            
            # GPS - EMI correlation pattern
            emi_factor = 0.3 + 0.2 * np.sin(2 * np.pi * timestamp.hour / 12)  # EMI cycle
            gps_health = 92 - 0.3 * (timestamp - start_date).total_seconds() / 3600 * emi_factor
            gps_health = max(70, gps_health + np.random.normal(0, 1.5))
            
            # IMU - Vibration pattern
            vibration_factor = 0.4 + 0.3 * np.sin(2 * np.pi * timestamp.hour / 6)  # Vibration cycle
            imu_health = 88 - 0.4 * (timestamp - start_date).total_seconds() / 3600 * vibration_factor
            imu_health = max(65, imu_health + np.random.normal(0, 2.5))
            
            # Barometer - Environmental correlation
            env_factor = 0.2 + 0.1 * np.sin(2 * np.pi * timestamp.hour / 24)
            barometer_health = 96 - 0.2 * (timestamp - start_date).total_seconds() / 3600 * env_factor
            barometer_health = max(80, barometer_health + np.random.normal(0, 1))
            
            data.extend([
                {
                    "timestamp": timestamp,
                    "sensor_id": "thermal_camera",
                    "health": round(thermal_health, 2),
                    "temperature": 25 + 15 * np.sin(2 * np.pi * timestamp.hour / 24),
                    "humidity": 45 + 20 * np.sin(2 * np.pi * timestamp.hour / 12),
                    "vibration": 0.1 + 0.2 * np.sin(2 * np.pi * timestamp.hour / 6),
                    "emi_level": 0.2 + 0.1 * np.sin(2 * np.pi * timestamp.hour / 8)
                },
                {
                    "timestamp": timestamp,
                    "sensor_id": "gps",
                    "health": round(gps_health, 2),
                    "temperature": 25 + 10 * np.sin(2 * np.pi * timestamp.hour / 24),
                    "humidity": 40 + 15 * np.sin(2 * np.pi * timestamp.hour / 12),
                    "vibration": 0.15 + 0.25 * np.sin(2 * np.pi * timestamp.hour / 6),
                    "emi_level": 0.3 + 0.2 * np.sin(2 * np.pi * timestamp.hour / 8)
                },
                {
                    "timestamp": timestamp,
                    "sensor_id": "imu",
                    "health": round(imu_health, 2),
                    "temperature": 26 + 12 * np.sin(2 * np.pi * timestamp.hour / 24),
                    "humidity": 42 + 18 * np.sin(2 * np.pi * timestamp.hour / 12),
                    "vibration": 0.4 + 0.3 * np.sin(2 * np.pi * timestamp.hour / 6),
                    "emi_level": 0.25 + 0.15 * np.sin(2 * np.pi * timestamp.hour / 8)
                },
                {
                    "timestamp": timestamp,
                    "sensor_id": "barometer",
                    "health": round(barometer_health, 2),
                    "temperature": 24 + 8 * np.sin(2 * np.pi * timestamp.hour / 24),
                    "humidity": 38 + 12 * np.sin(2 * np.pi * timestamp.hour / 12),
                    "vibration": 0.05 + 0.1 * np.sin(2 * np.pi * timestamp.hour / 6),
                    "emi_level": 0.1 + 0.05 * np.sin(2 * np.pi * timestamp.hour / 8)
                }
            ])
        
        return pd.DataFrame(data)
    
    def save_sample_data(self, filename: str = "sample_sensor_data.csv"):
        """Save sample data to CSV file"""
        if not self.initialized:
            return {"error": "Data processor not initialized"}
        
        try:
            df = self.generate_sample_data()
            filepath = os.path.join("data", filename)
            df.to_csv(filepath, index=False)
            
            return {
                "success": True,
                "filename": filename,
                "filepath": filepath,
                "rows": len(df),
                "columns": list(df.columns)
            }
        except Exception as e:
            return {"error": f"Error saving sample data: {str(e)}"}
    
    def get_processed_data(self, filename: str) -> Optional[Dict[str, Any]]:
        """Get processed data by filename"""
        return self.processed_data.get(filename)
    
    def get_all_processed_data(self) -> Dict[str, Any]:
        """Get all processed data"""
        return self.processed_data 