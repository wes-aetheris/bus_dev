import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import json

# Page configuration
st.set_page_config(
    page_title="Watchtower Drone Dashboard",
    page_icon="🚁",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Sidebar
st.sidebar.title("Watchtower Dashboard")
st.sidebar.markdown("---")

# Navigation
page = st.sidebar.selectbox(
    "Select Dashboard",
    [
        "Pre-Flight",
        "Post-Flight", 
        "Mission Planning",
        "Maintenance",
        "Environment & Context",
        "Camera Sensor Profile",
        "Operational Flight"
    ]
)

# Main content
st.title(f"🚁 {page}")

if page == "Pre-Flight":
    st.header("Pre-Flight Checks")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.subheader("Sensor Status")
        sensor_data = {
            "GPS": {"status": "Online", "calibration": "Good"},
            "IMU": {"status": "Online", "calibration": "Good"},
            "Camera": {"status": "Online", "calibration": "Good"},
            "Barometer": {"status": "Online", "calibration": "Good"}
        }
        
        for sensor, info in sensor_data.items():
            st.metric(
                label=sensor,
                value=info["status"],
                delta=info["calibration"]
            )
    
    with col2:
        st.subheader("System Checks")
        system_data = {
            "Battery": {"level": 95, "status": "Ready"},
            "Propellers": {"status": "Good", "last_check": "2024-01-01"},
            "Motors": {"status": "Good", "last_check": "2024-01-01"},
            "Frame": {"status": "Good", "last_check": "2024-01-01"}
        }
        
        for component, info in system_data.items():
            if "level" in info:
                st.metric(
                    label=component,
                    value=f"{info['level']}%",
                    delta=info["status"]
                )
            else:
                st.metric(
                    label=component,
                    value=info["status"],
                    delta=info["last_check"]
                )
    
    with col3:
        st.subheader("Weather Conditions")
        weather_data = {
            "Wind Speed": 5.2,
            "Wind Direction": 180,
            "Temperature": 22.5,
            "Humidity": 65,
            "Visibility": "Good"
        }
        
        for metric, value in weather_data.items():
            if isinstance(value, (int, float)):
                st.metric(label=metric, value=f"{value}")
            else:
                st.metric(label=metric, value=value)

elif page == "Post-Flight":
    st.header("Post-Flight Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Flight Summary")
        flight_summary = {
            "Duration": "45:30",
            "Distance": "12.5 km",
            "Max Altitude": "120 m",
            "Max Speed": "15.2 m/s",
            "Battery Consumed": "65%"
        }
        
        for metric, value in flight_summary.items():
            st.metric(label=metric, value=value)
    
    with col2:
        st.subheader("Data Collected")
        data_summary = {
            "Total Records": 2700,
            "Sensors Used": "GPS, IMU, Camera, Barometer",
            "Data Size": "45.2 MB"
        }
        
        for metric, value in data_summary.items():
            st.metric(label=metric, value=str(value))
    
    # Flight path visualization
    st.subheader("Flight Path")
    flight_path = pd.DataFrame({
        'latitude': np.random.normal(40.7128, 0.001, 100),
        'longitude': np.random.normal(-74.0060, 0.001, 100),
        'altitude': np.random.normal(100, 10, 100)
    })
    
    fig = px.scatter_mapbox(
        flight_path,
        lat='latitude',
        lon='longitude',
        color='altitude',
        title="Flight Path",
        mapbox_style="open-street-map"
    )
    st.plotly_chart(fig, use_container_width=True)

elif page == "Mission Planning":
    st.header("Mission Planning")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Planned Routes")
        routes = [
            {"name": "Survey Area A", "duration": "30:00", "distance": "8.5 km"},
            {"name": "Survey Area B", "duration": "25:00", "distance": "6.2 km"}
        ]
        
        for route in routes:
            with st.expander(route["name"]):
                st.write(f"**Duration:** {route['duration']}")
                st.write(f"**Distance:** {route['distance']}")
    
    with col2:
        st.subheader("Weather Forecast")
        hours = list(range(24))
        wind_speed = np.random.normal(5.2, 1, 24)
        temperature = np.random.normal(22.5, 2, 24)
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=hours, y=wind_speed, name="Wind Speed (m/s)"))
        fig.add_trace(go.Scatter(x=hours, y=temperature, name="Temperature (°C)", yaxis="y2"))
        
        fig.update_layout(
            title="24-Hour Weather Forecast",
            xaxis_title="Hour",
            yaxis=dict(title="Wind Speed (m/s)"),
            yaxis2=dict(title="Temperature (°C)", overlaying="y", side="right")
        )
        
        st.plotly_chart(fig, use_container_width=True)

elif page == "Maintenance":
    st.header("Maintenance Dashboard")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Component Health")
        components = {
            "Motors": 85,
            "Propellers": 90,
            "Battery": 75,
            "Frame": 95
        }
        
        for component, health in components.items():
            st.metric(
                label=component,
                value=f"{health}%",
                delta="Good" if health > 80 else "Needs Attention"
            )
    
    with col2:
        st.subheader("Maintenance Schedule")
        maintenance_items = [
            {"component": "Battery", "due_date": "2024-01-10", "type": "Inspection"},
            {"component": "Propellers", "due_date": "2024-01-15", "type": "Replacement"},
            {"component": "Motors", "due_date": "2024-02-01", "type": "Inspection"}
        ]
        
        for item in maintenance_items:
            with st.expander(f"{item['component']} - {item['type']}"):
                st.write(f"**Due Date:** {item['due_date']}")
                st.write(f"**Type:** {item['type']}")

elif page == "Environment & Context":
    st.header("Environment & Context")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Current Conditions")
        conditions = {
            "Temperature": "22.5°C",
            "Humidity": "65%",
            "Pressure": "1013.25 hPa",
            "Wind Speed": "5.2 m/s",
            "Wind Direction": "180°",
            "Visibility": "10.0 km",
            "UV Index": "3"
        }
        
        for metric, value in conditions.items():
            st.metric(label=metric, value=value)
    
    with col2:
        st.subheader("Air Quality")
        air_quality = {
            "PM2.5": "12 µg/m³",
            "PM10": "25 µg/m³",
            "CO2": "420 ppm",
            "VOC": "150 ppb"
        }
        
        for metric, value in air_quality.items():
            st.metric(label=metric, value=value)

elif page == "Camera Sensor Profile":
    st.header("Camera Sensor Profile")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Camera Settings")
        settings = {
            "Resolution": "4K",
            "FPS": "30",
            "ISO": "100",
            "Shutter Speed": "1/1000",
            "Aperture": "f/2.8",
            "White Balance": "Auto"
        }
        
        for setting, value in settings.items():
            st.metric(label=setting, value=value)
    
    with col2:
        st.subheader("Image Analysis")
        analysis = {
            "Sharpness": "85%",
            "Exposure": "Good",
            "Color Accuracy": "90%",
            "Noise Level": "Low"
        }
        
        for metric, value in analysis.items():
            st.metric(label=metric, value=value)

elif page == "Operational Flight":
    st.header("Operational Flight")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Current Status")
        status = {
            "Flight Mode": "Mission",
            "Altitude": "100 m",
            "Speed": "12.5 m/s",
            "Heading": "180°",
            "Battery Level": "75%",
            "Signal Strength": "95%"
        }
        
        for metric, value in status.items():
            st.metric(label=metric, value=value)
    
    with col2:
        st.subheader("Mission Progress")
        progress = {
            "Waypoints Completed": "3/8",
            "Distance Remaining": "2.5 km",
            "Estimated Completion": "15:30"
        }
        
        for metric, value in progress.items():
            st.metric(label=metric, value=value)
    
    # Real-time metrics chart
    st.subheader("Real-time Metrics")
    time_points = pd.date_range(start=datetime.now() - timedelta(minutes=30), periods=30, freq='1min')
    altitude_data = np.random.normal(100, 5, 30)
    speed_data = np.random.normal(12.5, 2, 30)
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=time_points, y=altitude_data, name="Altitude (m)"))
    fig.add_trace(go.Scatter(x=time_points, y=speed_data, name="Speed (m/s)", yaxis="y2"))
    
    fig.update_layout(
        title="Real-time Flight Metrics",
        xaxis_title="Time",
        yaxis=dict(title="Altitude (m)"),
        yaxis2=dict(title="Speed (m/s)", overlaying="y", side="right")
    )
    
    st.plotly_chart(fig, use_container_width=True)

# Footer
st.markdown("---")
st.markdown("*Watchtower Drone Sensor Dashboard - Streamlit Version*")
