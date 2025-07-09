from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from typing import Dict, List, Any
import json
import asyncio
from datetime import datetime

router = APIRouter()

class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            try:
                await connection.send_text(message)
            except:
                # Remove disconnected clients
                self.active_connections.remove(connection)

manager = ConnectionManager()

@router.websocket("/ws/sensor-data")
async def websocket_sensor_data(websocket: WebSocket):
    """WebSocket endpoint for real-time sensor data"""
    await manager.connect(websocket)
    try:
        while True:
            # Send mock real-time sensor data
            sensor_data = {
                "timestamp": datetime.utcnow().isoformat(),
                "sensors": {
                    "gps": {
                        "latitude": 40.7128,
                        "longitude": -74.0060,
                        "altitude": 100,
                        "speed": 12.5
                    },
                    "imu": {
                        "roll": 0.5,
                        "pitch": 1.2,
                        "yaw": 180.0
                    },
                    "battery": {
                        "level": 75,
                        "voltage": 11.8,
                        "current": 2.1
                    }
                }
            }
            
            await manager.send_personal_message(
                json.dumps(sensor_data), websocket
            )
            
            await asyncio.sleep(1)  # Send data every second
            
    except WebSocketDisconnect:
        manager.disconnect(websocket)

@router.websocket("/ws/alerts")
async def websocket_alerts(websocket: WebSocket):
    """WebSocket endpoint for real-time alerts"""
    await manager.connect(websocket)
    try:
        while True:
            # Send mock alerts
            alerts = {
                "timestamp": datetime.utcnow().isoformat(),
                "alerts": [
                    {
                        "id": "alert_001",
                        "type": "battery_low",
                        "severity": "medium",
                        "message": "Battery level below 20%",
                        "timestamp": datetime.utcnow().isoformat()
                    }
                ]
            }
            
            await manager.send_personal_message(
                json.dumps(alerts), websocket
            )
            
            await asyncio.sleep(5)  # Send alerts every 5 seconds
            
    except WebSocketDisconnect:
        manager.disconnect(websocket)

@router.websocket("/ws/flight-status")
async def websocket_flight_status(websocket: WebSocket):
    """WebSocket endpoint for real-time flight status"""
    await manager.connect(websocket)
    try:
        while True:
            # Send mock flight status
            flight_status = {
                "timestamp": datetime.utcnow().isoformat(),
                "status": {
                    "flight_mode": "mission",
                    "altitude": 100,
                    "speed": 12.5,
                    "heading": 180,
                    "battery_level": 75,
                    "signal_strength": 95,
                    "mission_progress": {
                        "waypoints_completed": 3,
                        "total_waypoints": 8,
                        "estimated_completion": "15:30"
                    }
                }
            }
            
            await manager.send_personal_message(
                json.dumps(flight_status), websocket
            )
            
            await asyncio.sleep(2)  # Send status every 2 seconds
            
    except WebSocketDisconnect:
        manager.disconnect(websocket)
