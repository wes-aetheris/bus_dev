import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
import requests
import json
import time
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configuration
API_URL = os.getenv("API_URL", "http://localhost:8000")
WEBSOCKET_URL = os.getenv("WEBSOCKET_URL", "ws://localhost:8001")

# Page configuration
st.set_page_config(
    page_title="Watchtower Dashboard",
    page_icon="🚁",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for dark theme
st.markdown("""
<style>
    .main {
        background-color: #0f172a;
        color: white;
    }
    .stApp {
        background-color: #0f172a;
    }
    .stButton > button {
        background-color: #1e293b;
        color: white;
        border: 1px solid #334155;
    }
    .stButton > button:hover {
        background-color: #334155;
    }
    .metric-container {
        background-color: #1e293b;
        padding: 1rem;
        border-radius: 0.5rem;
        border: 1px solid #334155;
    }
    .alert-critical {
        background-color: #7f1d1d;
        color: #fca5a5;
        padding: 0.5rem;
        border-radius: 0.25rem;
        margin: 0.5rem 0;
    }
    .alert-high {
        background-color: #78350f;
        color: #fbbf24;
        padding: 0.5rem;
        border-radius: 0.25rem;
        margin: 0.5rem 0;
    }
    .alert-medium {
        background-color: #713f12;
        color: #fde047;
        padding: 0.5rem;
        border-radius: 0.25rem;
        margin: 0.5rem 0;
    }
    .alert-low {
        background-color: #1e3a8a;
        color: #93c5fd;
        padding: 0.5rem;
        border-radius: 0.25rem;
        margin: 0.5rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'sensors' not in st.session_state:
    st.session_state.sensors = []
if 'mission_status' not in st.session_state:
    st.session_state.mission_status = {}
if 'alerts' not in st.session_state:
    st.session_state.alerts = []
if 'correlation_matrix' not in st.session_state:
    st.session_state.correlation_matrix = {}

def fetch_api_data(endpoint):
    """Fetch data from API"""
    try:
        response = requests.get(f"{API_URL}/api/{endpoint}")
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Error fetching {endpoint}: {response.status_code}")
            return None
    except Exception as e:
        st.error(f"Error connecting to API: {str(e)}")
        return None

def create_gauge_chart(value, title, color="blue"):
    """Create a gauge chart using Plotly"""
    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=value,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': title},
        delta={'reference': 100},
        gauge={
            'axis': {'range': [None, 100]},
            'bar': {'color': color},
            'steps': [
                {'range': [0, 60], 'color': "lightgray"},
                {'range': [60, 80], 'color': "yellow"},
                {'range': [80, 100], 'color': "green"}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': 90
            }
        }
    ))
    fig.update_layout(
        height=200,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font={'color': 'white'}
    )
    return fig

def create_correlation_heatmap(data):
    """Create correlation matrix heatmap"""
    if not data or 'correlation_matrix' not in data:
        return None
    
    sensors = data['sensors']
    correlation_matrix = data['correlation_matrix']
    
    fig = px.imshow(
        correlation_matrix,
        x=sensors,
        y=sensors,
        color_continuous_scale='RdBu',
        aspect="auto"
    )
    
    fig.update_layout(
        title="Cross-Sensor Correlation Matrix",
        height=400,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font={'color': 'white'}
    )
    
    return fig

def physics_model_card(title, model, description, health):
    """Create a physics model card"""
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.markdown(f"**{title}**")
        st.markdown(f"*{model}*")
        st.markdown(f"<small>{description}</small>", unsafe_allow_html=True)
    
    with col2:
        st.metric("Health", f"{health:.1f}%")

def main():
    st.title("🚁 Watchtower - Physics-Informed Sensor Monitoring")
    st.markdown("### Real-time drone sensor health monitoring with physics-based degradation models")
    
    # Sidebar
    st.sidebar.title("Navigation")
    page = st.sidebar.selectbox(
        "Choose a page",
        ["Dashboard", "Sensor Details", "Physics Models", "Data Upload", "Analytics"]
    )
    
    # Auto-refresh
    if st.sidebar.checkbox("Auto-refresh", value=True):
        time.sleep(1)
        st.rerun()
    
    if page == "Dashboard":
        show_dashboard()
    elif page == "Sensor Details":
        show_sensor_details()
    elif page == "Physics Models":
        show_physics_models()
    elif page == "Data Upload":
        show_data_upload()
    elif page == "Analytics":
        show_analytics()

def show_dashboard():
    """Main dashboard view"""
    
    # Fetch data
    sensors_data = fetch_api_data("sensors")
    mission_data = fetch_api_data("mission-status")
    alerts_data = fetch_api_data("alerts")
    
    if sensors_data:
        st.session_state.sensors = sensors_data.get('sensors', [])
    if mission_data:
        st.session_state.mission_status = mission_data
    if alerts_data:
        st.session_state.alerts = alerts_data.get('alerts', [])
    
    # Mission Status Bar
    st.subheader("🎯 Mission Status")
    if st.session_state.mission_status:
        status = st.session_state.mission_status
        
        col1, col2, col3, col4, col5, col6 = st.columns(6)
        
        with col1:
            st.metric("Altitude", f"{status.get('altitude', 0):.1f}m")
        with col2:
            st.metric("Speed", f"{status.get('speed', 0):.1f}m/s")
        with col3:
            st.metric("Battery", f"{status.get('battery', 0):.1f}%")
        with col4:
            st.metric("Flight Time", f"{status.get('flight_time', 0)//60:.0f}min")
        with col5:
            st.metric("GPS Signal", f"{status.get('signal_strength', 0):.0f}%")
        with col6:
            st.metric("Temperature", f"{status.get('temperature', 0):.1f}°C")
    
    # Sensor Health Grid
    st.subheader("📊 Sensor Health")
    if st.session_state.sensors:
        cols = st.columns(len(st.session_state.sensors))
        
        for i, sensor in enumerate(st.session_state.sensors):
            with cols[i]:
                st.markdown(f"**{sensor['name']}**")
                fig = create_gauge_chart(
                    sensor['health'],
                    f"{sensor['health']:.1f}%",
                    "green" if sensor['health'] >= 80 else "yellow" if sensor['health'] >= 60 else "red"
                )
                st.plotly_chart(fig, use_container_width=True)
                
                st.markdown(f"**Degradation Rate:** {sensor['degradation_rate']*100:.1f}%/hr")
                st.markdown(f"**Type:** {sensor['type'].title()}")
    
    # Alerts
    st.subheader("🚨 Alerts & Notifications")
    if st.session_state.alerts:
        for alert in st.session_state.alerts:
            alert_class = f"alert-{alert['severity']}"
            st.markdown(f"""
            <div class="{alert_class}">
                <strong>{alert['severity'].upper()}</strong> - {alert['message']}<br>
                <small>Sensor: {alert['sensor_id']} | Time: {alert['timestamp']}</small>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.success("No active alerts")
    
    # Correlation Matrix
    st.subheader("🔗 Cross-Sensor Correlation")
    correlation_data = fetch_api_data("correlation-matrix")
    if correlation_data:
        fig = create_correlation_heatmap(correlation_data)
        if fig:
            st.plotly_chart(fig, use_container_width=True)

def show_sensor_details():
    """Detailed sensor information"""
    st.subheader("🔍 Sensor Details")
    
    if st.session_state.sensors:
        sensor_id = st.selectbox(
            "Select Sensor",
            [sensor['id'] for sensor in st.session_state.sensors]
        )
        
        sensor = next((s for s in st.session_state.sensors if s['id'] == sensor_id), None)
        
        if sensor:
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown(f"**Sensor:** {sensor['name']}")
                st.markdown(f"**Type:** {sensor['type'].title()}")
                st.markdown(f"**Health:** {sensor['health']:.1f}%")
                st.markdown(f"**Degradation Rate:** {sensor['degradation_rate']*100:.1f}%/hr")
            
            with col2:
                st.markdown(f"**Last Calibration:** {sensor['last_calibration']}")
                st.markdown(f"**Next Calibration:** {sensor['next_calibration']}")
                
                # Health trend simulation
                dates = pd.date_range(start='2024-01-01', periods=30, freq='D')
                health_trend = [sensor['health'] - i * sensor['degradation_rate'] * 24 for i in range(30)]
                health_trend = [max(0, h) for h in health_trend]
                
                fig = px.line(
                    x=dates,
                    y=health_trend,
                    title="Predicted Health Trend",
                    labels={'x': 'Date', 'y': 'Health (%)'}
                )
                fig.update_layout(
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)',
                    font={'color': 'white'}
                )
                st.plotly_chart(fig, use_container_width=True)

def show_physics_models():
    """Physics models information"""
    st.subheader("⚡ Physics Models")
    
    models_data = fetch_api_data("physics-models")
    
    if models_data and 'physics_models' in models_data:
        models = models_data['physics_models']
        
        for sensor_id, model_info in models.items():
            with st.expander(f"{sensor_id.replace('_', ' ').title()}"):
                st.markdown(f"**Model:** {model_info['name']}")
                st.markdown(f"**Description:** {model_info['description']}")
                st.markdown(f"**Parameters:** {', '.join(model_info['parameters'])}")
                st.markdown(f"**Equation:** `{model_info['equation']}`")
                
                # Find corresponding sensor health
                sensor = next((s for s in st.session_state.sensors if s['id'] == sensor_id), None)
                if sensor:
                    physics_model_card(
                        sensor['name'],
                        model_info['name'],
                        model_info['description'],
                        sensor['health']
                    )

def show_data_upload():
    """Data upload functionality"""
    st.subheader("📤 Data Upload")
    
    uploaded_file = st.file_uploader(
        "Choose a CSV file",
        type=['csv'],
        help="Upload sensor data in CSV format"
    )
    
    if uploaded_file is not None:
        try:
            df = pd.read_csv(uploaded_file)
            st.success(f"Successfully loaded {len(df)} rows")
            
            st.markdown("**Data Preview:**")
            st.dataframe(df.head())
            
            if st.button("Upload to System"):
                # Simulate upload
                st.success("Data uploaded successfully!")
                
        except Exception as e:
            st.error(f"Error reading file: {str(e)}")
    
    st.markdown("""
    **Required CSV Format:**
    - timestamp: ISO datetime format
    - sensor_id: sensor identifier
    - health: sensor health percentage (0-100)
    - Optional: temperature, humidity, vibration, emi_level
    """)

def show_analytics():
    """Analytics and reporting"""
    st.subheader("📈 Analytics")
    
    # Export options
    st.markdown("**Export Data:**")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("Export CSV"):
            st.info("CSV export functionality would be implemented here")
    
    with col2:
        if st.button("Export JSON"):
            st.info("JSON export functionality would be implemented here")
    
    with col3:
        if st.button("Generate Report"):
            st.info("PDF report generation would be implemented here")
    
    # Sample analytics
    st.markdown("**Sensor Health Distribution:**")
    if st.session_state.sensors:
        health_values = [s['health'] for s in st.session_state.sensors]
        sensor_names = [s['name'] for s in st.session_state.sensors]
        
        fig = px.bar(
            x=sensor_names,
            y=health_values,
            title="Sensor Health Comparison",
            labels={'x': 'Sensor', 'y': 'Health (%)'}
        )
        fig.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font={'color': 'white'}
        )
        st.plotly_chart(fig, use_container_width=True)

if __name__ == "__main__":
    main() 