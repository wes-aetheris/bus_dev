from fastapi import APIRouter, HTTPException
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
import json

router = APIRouter(prefix="/api/dashboard", tags=["dashboard"])

@router.get("/tabs")
async def get_dashboard_tabs():
    """Get available dashboard tabs"""
    return {
        "tabs": [
            {"id": "pre-flight", "name": "Pre-Flight", "icon": "airplane", "description": "Pre-flight checks and sensor calibration"},
            {"id": "post-flight", "name": "Post-Flight", "icon": "landing", "description": "Post-flight analysis and data review"},
            {"id": "mission-planning", "name": "Mission Planning", "icon": "map", "description": "Mission planning and route optimization"},
            {"id": "maintenance", "name": "Maintenance", "icon": "wrench", "description": "Maintenance schedules and component health"},
            {"id": "environment", "name": "Environment & Context", "icon": "globe", "description": "Environmental conditions and context data"},
            {"id": "camera-profile", "name": "Camera Sensor Profile", "icon": "camera", "description": "Camera settings and image analysis"},
            {"id": "operational-flight", "name": "Operational Flight", "icon": "flight", "description": "Real-time flight monitoring"}
        ]
    }

@router.get("/pre-flight")
async def get_preflight_data():
    """Get pre-flight data"""
    return {
        "sensor_status": {
            "gps": {"status": "online", "calibration": "good"},
            "imu": {"status": "online", "calibration": "good"},
            "camera": {"status": "online", "calibration": "good"},
            "barometer": {"status": "online", "calibration": "good"}
        },
        "system_checks": {
            "battery": {"level": 95, "status": "ready"},
            "propellers": {"status": "good", "last_check": "2024-01-01T10:00:00Z"},
            "motors": {"status": "good", "last_check": "2024-01-01T10:00:00Z"},
            "frame": {"status": "good", "last_check": "2024-01-01T10:00:00Z"}
        },
        "weather_conditions": {
            "wind_speed": 5.2,
            "wind_direction": 180,
            "temperature": 22.5,
            "humidity": 65,
            "visibility": "good"
        }
    }

@router.get("/post-flight")
async def get_postflight_data():
    """Get post-flight data"""
    return {
        "flight_summary": {
            "duration": "45:30",
            "distance": 12.5,
            "max_altitude": 120,
            "max_speed": 15.2,
            "battery_consumed": 65
        },
        "data_collected": {
            "total_records": 2700,
            "sensors_used": ["gps", "imu", "camera", "barometer"],
            "data_size": "45.2 MB"
        },
        "anomalies_detected": [
            {"type": "wind_gust", "timestamp": "2024-01-01T12:15:00Z", "severity": "medium"},
            {"type": "battery_drain", "timestamp": "2024-01-01T12:30:00Z", "severity": "low"}
        ]
    }

@router.get("/mission-planning")
async def get_mission_planning_data():
    """Get mission planning data"""
    return {
        "planned_routes": [
            {
                "id": "route_001",
                "name": "Survey Area A",
                "waypoints": [
                    {"lat": 40.7128, "lng": -74.0060, "alt": 100},
                    {"lat": 40.7129, "lng": -74.0061, "alt": 120},
                    {"lat": 40.7130, "lng": -74.0062, "alt": 100}
                ],
                "estimated_duration": "30:00",
                "estimated_distance": 8.5
            }
        ],
        "weather_forecast": {
            "wind_speed": [5.2, 6.1, 4.8, 5.5],
            "wind_direction": [180, 185, 175, 180],
            "temperature": [22.5, 23.1, 22.8, 23.5],
            "precipitation_chance": [10, 15, 5, 20]
        },
        "no_fly_zones": [
            {"lat": 40.7150, "lng": -74.0080, "radius": 500, "reason": "airport"},
            {"lat": 40.7100, "lng": -74.0040, "radius": 300, "reason": "hospital"}
        ]
    }

@router.get("/maintenance")
async def get_maintenance_data():
    """Get maintenance data"""
    return {
        "component_health": {
            "motors": {"health": 85, "last_service": "2024-01-01T00:00:00Z", "next_service": "2024-02-01T00:00:00Z"},
            "propellers": {"health": 90, "last_service": "2024-01-01T00:00:00Z", "next_service": "2024-01-15T00:00:00Z"},
            "battery": {"health": 75, "last_service": "2024-01-01T00:00:00Z", "next_service": "2024-01-10T00:00:00Z"},
            "frame": {"health": 95, "last_service": "2024-01-01T00:00:00Z", "next_service": "2024-03-01T00:00:00Z"}
        },
        "maintenance_schedule": [
            {"component": "battery", "due_date": "2024-01-10T00:00:00Z", "type": "inspection"},
            {"component": "propellers", "due_date": "2024-01-15T00:00:00Z", "type": "replacement"},
            {"component": "motors", "due_date": "2024-02-01T00:00:00Z", "type": "inspection"}
        ],
        "service_history": [
            {"component": "battery", "date": "2024-01-01T00:00:00Z", "type": "inspection", "technician": "John Doe"},
            {"component": "propellers", "date": "2024-01-01T00:00:00Z", "type": "replacement", "technician": "Jane Smith"}
        ]
    }

@router.get("/environment")
async def get_environment_data():
    """Get environment and context data"""
    return {
        "current_conditions": {
            "temperature": 22.5,
            "humidity": 65,
            "pressure": 1013.25,
            "wind_speed": 5.2,
            "wind_direction": 180,
            "visibility": 10.0,
            "uv_index": 3
        },
        "air_quality": {
            "pm25": 12,
            "pm10": 25,
            "co2": 420,
            "voc": 150
        },
        "terrain_data": {
            "elevation": 50,
            "terrain_type": "urban",
            "obstacles": [
                {"type": "building", "height": 100, "distance": 200},
                {"type": "tree", "height": 15, "distance": 150}
            ]
        }
    }

@router.get("/camera-profile")
async def get_camera_profile_data():
    """Get camera sensor profile data"""
    return {
        "camera_settings": {
            "resolution": "4K",
            "fps": 30,
            "iso": 100,
            "shutter_speed": "1/1000",
            "aperture": "f/2.8",
            "white_balance": "auto"
        },
        "lens_info": {
            "focal_length": "24mm",
            "aperture_range": "f/2.8-f/22",
            "focus_mode": "auto"
        },
        "image_analysis": {
            "sharpness": 85,
            "exposure": "good",
            "color_accuracy": 90,
            "noise_level": "low"
        },
        "recording_modes": [
            {"mode": "photo", "resolution": "4K", "format": "JPEG"},
            {"mode": "video", "resolution": "4K", "format": "MP4"},
            {"mode": "timelapse", "resolution": "1080p", "format": "MP4"}
        ]
    }

@router.get("/operational-flight")
async def get_operational_flight_data():
    """Get operational flight data"""
    return {
        "current_status": {
            "flight_mode": "mission",
            "altitude": 100,
            "speed": 12.5,
            "heading": 180,
            "battery_level": 75,
            "signal_strength": 95
        },
        "mission_progress": {
            "waypoints_completed": 3,
            "total_waypoints": 8,
            "estimated_completion": "15:30",
            "distance_remaining": 2.5
        },
        "real_time_metrics": {
            "vertical_speed": 0.5,
            "ground_speed": 12.5,
            "wind_speed": 5.2,
            "temperature": 22.5
        }
    }
