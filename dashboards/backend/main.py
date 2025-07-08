from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException, Depends, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse, FileResponse
import asyncio
import json
import os
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
import pandas as pd
import numpy as np
from scipy import stats
import plotly.graph_objects as go
import plotly.express as px
from io import BytesIO
import base64

from models.database import engine, SessionLocal
from models.schemas import SensorData, Alert, MissionStatus, PhysicsModel
from services.physics_models import PhysicsModelService
from services.websocket_manager import WebSocketManager
from services.data_processor import DataProcessor
from services.alert_service import AlertService

app = FastAPI(title="Watchtower API", version="1.0.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files (only if directory exists)
import os
if os.path.exists("static"):
    app.mount("/static", StaticFiles(directory="static"), name="static")

# Initialize services
websocket_manager = WebSocketManager()
physics_service = PhysicsModelService()
data_processor = DataProcessor()
alert_service = AlertService()

# Database dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.on_event("startup")
async def startup_event():
    """Initialize services on startup"""
    await physics_service.initialize()
    await data_processor.initialize()
    await alert_service.initialize()

@app.get("/")
async def root():
    """Root endpoint"""
    return {"message": "Watchtower API", "version": "1.0.0"}

@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "services": {
            "physics_models": physics_service.is_initialized(),
            "data_processor": data_processor.is_initialized(),
            "alert_service": alert_service.is_initialized()
        }
    }

@app.get("/api/sensors")
async def get_sensors():
    """Get all sensor information"""
    sensors = [
        {
            "id": "thermal_camera",
            "name": "Thermal Camera",
            "type": "thermal",
            "health": 85,
            "degradation_rate": 0.12,
            "last_calibration": "2024-01-15T10:30:00Z",
            "next_calibration": "2024-04-15T10:30:00Z"
        },
        {
            "id": "gps",
            "name": "GPS Module",
            "type": "navigation",
            "health": 92,
            "degradation_rate": 0.08,
            "last_calibration": "2024-01-10T14:20:00Z",
            "next_calibration": "2024-04-10T14:20:00Z"
        },
        {
            "id": "imu",
            "name": "Inertial Measurement Unit",
            "type": "navigation",
            "health": 78,
            "degradation_rate": 0.15,
            "last_calibration": "2024-01-05T09:15:00Z",
            "next_calibration": "2024-04-05T09:15:00Z"
        },
        {
            "id": "barometer",
            "name": "Barometric Altimeter",
            "type": "environmental",
            "health": 95,
            "degradation_rate": 0.05,
            "last_calibration": "2024-01-20T11:45:00Z",
            "next_calibration": "2024-04-20T11:45:00Z"
        }
    ]
    return {"sensors": sensors}

@app.get("/api/sensors/{sensor_id}/health")
async def get_sensor_health(sensor_id: str):
    """Get detailed health information for a specific sensor"""
    # Simulate physics-based health calculation
    base_health = {
        "thermal_camera": 85,
        "gps": 92,
        "imu": 78,
        "barometer": 95
    }
    
    health = base_health.get(sensor_id, 50)
    
    # Apply physics models
    if sensor_id == "thermal_camera":
        # Arrhenius degradation model
        temperature = 45  # Current temperature in Celsius
        degradation = physics_service.calculate_thermal_degradation(temperature)
        health = max(0, health - degradation)
    elif sensor_id == "gps":
        # EMI correlation model
        emi_level = 0.3  # EMI level (0-1)
        degradation = physics_service.calculate_gps_degradation(emi_level)
        health = max(0, health - degradation)
    elif sensor_id == "imu":
        # Vibration model
        vibration_level = 0.4  # Vibration level (0-1)
        degradation = physics_service.calculate_imu_degradation(vibration_level)
        health = max(0, health - degradation)
    
    return {
        "sensor_id": sensor_id,
        "health": round(health, 2),
        "timestamp": datetime.now().isoformat(),
        "physics_model": physics_service.get_model_info(sensor_id)
    }

@app.get("/api/correlation-matrix")
async def get_correlation_matrix():
    """Get cross-sensor correlation matrix"""
    # Generate realistic correlation data
    sensors = ["thermal_camera", "gps", "imu", "barometer"]
    correlation_data = []
    
    for i, sensor1 in enumerate(sensors):
        row = []
        for j, sensor2 in enumerate(sensors):
            if i == j:
                correlation = 1.0
            else:
                # Generate realistic correlations
                correlations = {
                    ("thermal_camera", "gps"): 0.15,
                    ("thermal_camera", "imu"): 0.25,
                    ("thermal_camera", "barometer"): 0.10,
                    ("gps", "imu"): 0.35,
                    ("gps", "barometer"): 0.20,
                    ("imu", "barometer"): 0.30
                }
                key = tuple(sorted([sensor1, sensor2]))
                correlation = correlations.get(key, 0.05)
            row.append(round(correlation, 3))
        correlation_data.append(row)
    
    return {
        "sensors": sensors,
        "correlation_matrix": correlation_data,
        "timestamp": datetime.now().isoformat()
    }

@app.get("/api/alerts")
async def get_alerts():
    """Get current alerts"""
    alerts = alert_service.get_current_alerts()
    return {"alerts": alerts}

@app.get("/api/mission-status")
async def get_mission_status():
    """Get current mission status"""
    status = {
        "altitude": 1250.5,  # meters
        "speed": 15.2,  # m/s
        "battery": 78.5,  # percentage
        "flight_time": 1245,  # seconds
        "mission_phase": "active",
        "gps_satellites": 8,
        "signal_strength": 85,
        "temperature": 23.4,  # Celsius
        "humidity": 45.2,  # percentage
        "wind_speed": 3.1,  # m/s
        "timestamp": datetime.now().isoformat()
    }
    return status

@app.post("/api/upload-csv")
async def upload_csv(file: UploadFile = File(...)):
    """Upload and process CSV data"""
    if not file.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="File must be a CSV")
    
    try:
        # Read CSV data
        content = await file.read()
        df = pd.read_csv(BytesIO(content))
        
        # Process data
        processed_data = data_processor.process_csv_data(df)
        
        # Save to database or file system
        filename = f"upload_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        filepath = f"data/{filename}"
        os.makedirs("data", exist_ok=True)
        df.to_csv(filepath, index=False)
        
        return {
            "message": "CSV uploaded successfully",
            "filename": filename,
            "rows": len(df),
            "columns": list(df.columns),
            "processed_data": processed_data
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing CSV: {str(e)}")

@app.get("/api/export/{format}")
async def export_data(format: str):
    """Export data in various formats"""
    if format not in ["csv", "json", "pdf"]:
        raise HTTPException(status_code=400, detail="Unsupported format")
    
    # Generate sample data for export
    data = {
        "sensors": await get_sensors(),
        "correlation_matrix": await get_correlation_matrix(),
        "mission_status": await get_mission_status(),
        "alerts": await get_alerts(),
        "export_timestamp": datetime.now().isoformat()
    }
    
    if format == "json":
        return JSONResponse(content=data)
    elif format == "csv":
        # Convert to CSV format
        csv_data = data_processor.convert_to_csv(data)
        return JSONResponse(content={"csv_data": csv_data})
    elif format == "pdf":
        # Generate PDF report
        pdf_data = data_processor.generate_pdf_report(data)
        return JSONResponse(content={"pdf_data": pdf_data})

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket endpoint for real-time updates"""
    await websocket_manager.connect(websocket)
    try:
        while True:
            # Send real-time updates
            data = {
                "type": "sensor_update",
                "timestamp": datetime.now().isoformat(),
                "sensors": await get_sensors(),
                "mission_status": await get_mission_status(),
                "alerts": await get_alerts()
            }
            await websocket.send_text(json.dumps(data))
            await asyncio.sleep(5)  # Update every 5 seconds
    except WebSocketDisconnect:
        websocket_manager.disconnect(websocket)

@app.get("/api/physics-models")
async def get_physics_models():
    """Get information about implemented physics models"""
    models = {
        "thermal_camera": {
            "model": "Arrhenius Degradation",
            "description": "Dark current doubling every 6-8°C temperature increase",
            "parameters": ["temperature", "time", "initial_health"],
            "equation": "degradation = A * exp(-Ea/(k*T)) * time"
        },
        "gps": {
            "model": "EMI Correlation",
            "description": "Signal degradation based on electromagnetic interference",
            "parameters": ["emi_level", "signal_strength", "frequency"],
            "equation": "degradation = EMI_factor * signal_strength * frequency"
        },
        "imu": {
            "model": "Vibration-Induced Bias Drift",
            "description": "Bias drift caused by mechanical vibration",
            "parameters": ["vibration_level", "frequency", "duration"],
            "equation": "drift = vibration_amplitude * frequency * sqrt(duration)"
        },
        "environmental": {
            "model": "Multi-Factor Correlation",
            "description": "Combined effects of temperature, humidity, vibration, and EMI",
            "parameters": ["temperature", "humidity", "vibration", "emi"],
            "equation": "total_effect = Σ(weight_i * factor_i)"
        }
    }
    return {"physics_models": models}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 