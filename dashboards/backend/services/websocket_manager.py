from fastapi import WebSocket
from typing import List, Dict, Any
import json
import asyncio
from datetime import datetime

class WebSocketManager:
    """Manages WebSocket connections for real-time updates"""
    
    def __init__(self):
        self.active_connections: List[WebSocket] = []
        self.connection_data: Dict[str, Any] = {}
    
    async def connect(self, websocket: WebSocket):
        """Connect a new WebSocket client"""
        await websocket.accept()
        self.active_connections.append(websocket)
        connection_id = id(websocket)
        self.connection_data[connection_id] = {
            "connected_at": datetime.now(),
            "last_activity": datetime.now(),
            "subscriptions": []
        }
        print(f"WebSocket connected: {connection_id}")
    
    def disconnect(self, websocket: WebSocket):
        """Disconnect a WebSocket client"""
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)
            connection_id = id(websocket)
            if connection_id in self.connection_data:
                del self.connection_data[connection_id]
            print(f"WebSocket disconnected: {connection_id}")
    
    async def send_personal_message(self, message: str, websocket: WebSocket):
        """Send a message to a specific WebSocket client"""
        try:
            await websocket.send_text(message)
            connection_id = id(websocket)
            if connection_id in self.connection_data:
                self.connection_data[connection_id]["last_activity"] = datetime.now()
        except Exception as e:
            print(f"Error sending message: {e}")
            self.disconnect(websocket)
    
    async def broadcast(self, message: str):
        """Broadcast a message to all connected WebSocket clients"""
        disconnected = []
        for connection in self.active_connections:
            try:
                await connection.send_text(message)
                connection_id = id(connection)
                if connection_id in self.connection_data:
                    self.connection_data[connection_id]["last_activity"] = datetime.now()
            except Exception as e:
                print(f"Error broadcasting message: {e}")
                disconnected.append(connection)
        
        # Remove disconnected clients
        for connection in disconnected:
            self.disconnect(connection)
    
    async def send_sensor_update(self, sensor_data: Dict[str, Any]):
        """Send sensor health update to all clients"""
        message = {
            "type": "sensor_update",
            "timestamp": datetime.now().isoformat(),
            "data": sensor_data
        }
        await self.broadcast(json.dumps(message))
    
    async def send_alert(self, alert_data: Dict[str, Any]):
        """Send alert to all clients"""
        message = {
            "type": "alert",
            "timestamp": datetime.now().isoformat(),
            "data": alert_data
        }
        await self.broadcast(json.dumps(message))
    
    async def send_mission_status(self, status_data: Dict[str, Any]):
        """Send mission status update to all clients"""
        message = {
            "type": "mission_status",
            "timestamp": datetime.now().isoformat(),
            "data": status_data
        }
        await self.broadcast(json.dumps(message))
    
    async def send_physics_model_update(self, model_data: Dict[str, Any]):
        """Send physics model update to all clients"""
        message = {
            "type": "physics_model_update",
            "timestamp": datetime.now().isoformat(),
            "data": model_data
        }
        await self.broadcast(json.dumps(message))
    
    def get_connection_count(self) -> int:
        """Get number of active connections"""
        return len(self.active_connections)
    
    def get_connection_stats(self) -> Dict[str, Any]:
        """Get connection statistics"""
        now = datetime.now()
        stats = {
            "total_connections": len(self.active_connections),
            "connection_details": []
        }
        
        for connection_id, data in self.connection_data.items():
            duration = (now - data["connected_at"]).total_seconds()
            last_activity = (now - data["last_activity"]).total_seconds()
            
            stats["connection_details"].append({
                "connection_id": connection_id,
                "duration_seconds": round(duration, 1),
                "last_activity_seconds": round(last_activity, 1),
                "subscriptions": data["subscriptions"]
            })
        
        return stats
    
    async def cleanup_inactive_connections(self):
        """Remove inactive connections"""
        now = datetime.now()
        inactive_threshold = 300  # 5 minutes
        
        inactive_connections = []
        for connection in self.active_connections:
            connection_id = id(connection)
            if connection_id in self.connection_data:
                last_activity = self.connection_data[connection_id]["last_activity"]
                if (now - last_activity).total_seconds() > inactive_threshold:
                    inactive_connections.append(connection)
        
        for connection in inactive_connections:
            self.disconnect(connection)
            print(f"Removed inactive connection: {id(connection)}")
    
    async def start_cleanup_task(self):
        """Start periodic cleanup of inactive connections"""
        while True:
            await asyncio.sleep(60)  # Check every minute
            await self.cleanup_inactive_connections() 