from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import uvicorn
from typing import Dict, List, Any
import json

# Import models and services (to be implemented)
# from models import *
# from services import *
# from api import *

app = FastAPI(
    title="Watchtower Drone Sensor Dashboard API",
    description="Backend API for Watchtower drone operator dashboard",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
async def root():
    """Root endpoint"""
    return {"message": "Watchtower Drone Sensor Dashboard API", "version": "1.0.0"}

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "watchtower-api"}

@app.get("/api/dashboard/tabs")
async def get_dashboard_tabs():
    """Get available dashboard tabs"""
    return {
        "tabs": [
            {"id": "pre-flight", "name": "Pre-Flight", "icon": "airplane"},
            {"id": "post-flight", "name": "Post-Flight", "icon": "landing"},
            {"id": "mission-planning", "name": "Mission Planning", "icon": "map"},
            {"id": "maintenance", "name": "Maintenance", "icon": "wrench"},
            {"id": "environment", "name": "Environment & Context", "icon": "globe"},
            {"id": "camera-profile", "name": "Camera Sensor Profile", "icon": "camera"},
            {"id": "live-flight", "name": "Live Flight", "icon": "flight"}
        ]
    }

@app.get("/api/sensors/status")
async def get_sensor_status():
    """Get current sensor status"""
    return {
        "sensors": [
            {"id": "gps", "status": "online", "last_update": "2024-01-01T12:00:00Z"},
            {"id": "imu", "status": "online", "last_update": "2024-01-01T12:00:00Z"},
            {"id": "camera", "status": "online", "last_update": "2024-01-01T12:00:00Z"}
        ]
    }

@app.post("/api/data/upload")
async def upload_sensor_data(data: Dict[str, Any]):
    """Upload sensor data"""
    # Placeholder for data processing
    return {"message": "Data uploaded successfully", "records": len(data)}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
