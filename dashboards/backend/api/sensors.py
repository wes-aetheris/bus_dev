from fastapi import APIRouter, HTTPException, UploadFile, File
from typing import Dict, List, Any, Optional
import pandas as pd
import json
from datetime import datetime

from ..models.sensor_data import SensorData, SensorUpload
from ..services.data_processor import DataProcessor

router = APIRouter(prefix="/api/sensors", tags=["sensors"])

data_processor = DataProcessor()

@router.get("/status")
async def get_sensor_status():
    """Get current sensor status"""
    return {
        "sensors": [
            {"id": "gps", "status": "online", "last_update": "2024-01-01T12:00:00Z"},
            {"id": "imu", "status": "online", "last_update": "2024-01-01T12:00:00Z"},
            {"id": "camera", "status": "online", "last_update": "2024-01-01T12:00:00Z"},
            {"id": "barometer", "status": "online", "last_update": "2024-01-01T12:00:00Z"},
            {"id": "temperature", "status": "online", "last_update": "2024-01-01T12:00:00Z"}
        ]
    }

@router.post("/upload")
async def upload_sensor_data(data: SensorUpload):
    """Upload sensor data"""
    try:
        # Process the uploaded data
        raw_data = [reading.dict() for reading in data.sensor_readings]
        processed_result = data_processor.process_sensor_data(raw_data)
        
        return {
            "message": "Data uploaded successfully",
            "mission_id": data.mission_id,
            "records_processed": len(data.sensor_readings),
            "processing_result": processed_result
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error processing data: {str(e)}")

@router.post("/upload/csv")
async def upload_csv_data(file: UploadFile = File(...)):
    """Upload CSV sensor data"""
    try:
        if not file.filename.endswith('.csv'):
            raise HTTPException(status_code=400, detail="File must be a CSV")
        
        # Read CSV data
        df = pd.read_csv(file.file)
        data = df.to_dict('records')
        
        # Process the data
        processed_result = data_processor.process_sensor_data(data)
        
        return {
            "message": "CSV data uploaded successfully",
            "filename": file.filename,
            "records_processed": len(data),
            "processing_result": processed_result
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error processing CSV: {str(e)}")

@router.get("/data/{sensor_id}")
async def get_sensor_data(sensor_id: str, limit: int = 100):
    """Get sensor data for a specific sensor"""
    # Placeholder - would connect to database
    return {
        "sensor_id": sensor_id,
        "data": [],
        "total_records": 0,
        "limit": limit
    }

@router.get("/anomalies")
async def get_anomalies(threshold: float = 2.0):
    """Get detected anomalies"""
    # Placeholder - would use actual data
    sample_data = [
        {"timestamp": "2024-01-01T12:00:00Z", "value": 100},
        {"timestamp": "2024-01-01T12:01:00Z", "value": 150},
        {"timestamp": "2024-01-01T12:02:00Z", "value": 200}
    ]
    
    anomalies = data_processor.detect_anomalies(sample_data, threshold)
    
    return {
        "anomalies": anomalies,
        "threshold": threshold,
        "total_anomalies": len(anomalies)
    }

@router.get("/physics-metrics")
async def get_physics_metrics():
    """Get physics-based metrics"""
    # Placeholder - would use actual data
    sample_data = [
        {"timestamp": "2024-01-01T12:00:00Z", "latitude": 40.7128, "longitude": -74.0060, "speed": 10.0},
        {"timestamp": "2024-01-01T12:01:00Z", "latitude": 40.7129, "longitude": -74.0061, "speed": 12.0}
    ]
    
    metrics = data_processor.calculate_physics_metrics(sample_data)
    
    return {
        "physics_metrics": metrics,
        "calculation_timestamp": datetime.utcnow().isoformat()
    }
