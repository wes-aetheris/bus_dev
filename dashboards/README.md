# Watchtower Drone Sensor Dashboard

A comprehensive full-stack dashboard for drone operators to monitor sensor data, plan missions, and analyze flight performance with **physics-informed sensor intelligence**.

## 🚁 Project Overview

Watchtower is a complete drone sensor dashboard system with multiple interfaces:

- **Next.js Frontend**: Modern web dashboard with real-time data visualization and sensor intelligence widgets
- **FastAPI Backend**: RESTful API with WebSocket support for real-time updates
- **Streamlit Alternative**: Rapid prototyping and data exploration interface
- **Jupyter Integration**: Advanced analytics and research capabilities

## 🏗️ Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │   Backend       │    │   Streamlit     │
│   (Next.js)     │◄──►│   (FastAPI)     │◄──►│   (Dashboard)   │
│   Port: 3000    │    │   Port: 8000    │    │   Port: 8501    │
│   + Sensor      │    │   + Physics     │    │   + Analytics   │
│   Intelligence  │    │   Engine        │    │   Tools         │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         │                       │                       │
         └───────────────────────┼───────────────────────┘
                                 │
                    ┌─────────────────┐
                    │   Jupyter       │
                    │   (Analytics)   │
                    │   Port: 8888    │
                    └─────────────────┘
```

## 📊 Dashboard Tabs

1. **Sensor Intelligence**: Physics-informed sensor monitoring and predictive analytics
2. **Pre-Flight**: Sensor calibration, system checks, weather conditions
3. **Post-Flight**: Flight analysis, data collection summary, anomaly detection
4. **Mission Planning**: Route optimization, weather forecasting, no-fly zones
5. **Maintenance**: Component health monitoring, maintenance schedules
6. **Environment & Context**: Environmental conditions, air quality, terrain data
7. **Camera Sensor Profile**: Camera settings, image analysis, recording modes
8. **Live Flight**: Real-time flight monitoring, mission progress

## 🧠 Sensor Intelligence Features

### Mission Capability Assessment
- **Real-time capability scoring** with physics-informed calculations
- **Trend analysis** showing improving/degrading/stable performance
- **Confidence metrics** for prediction reliability
- **30-minute projections** for mission planning
- **Contributing factors** analysis with impact assessment

### Sensor Health Monitoring
- **Current health percentages** with color-coded status indicators
- **1-hour health predictions** using degradation modeling
- **Degradation rate analysis** (%/hour trends)
- **Threshold management** (optimal/warning/critical levels)
- **Individual sensor status** for each component

### Widget System
- **Responsive grid layout** for flexible dashboard organization
- **Real-time data updates** via WebSocket connections
- **Status indicators** with color-coded alerts
- **Refresh functionality** for manual data updates
- **Collapsible widgets** for space optimization

## 🚀 Quick Start

### Prerequisites

- Docker and Docker Compose
- Node.js 18+ (for local development)
- Python 3.11+ (for local development)

### Using Docker (Recommended)

1. **Clone and navigate to the project**:
   ```bash
   cd dashboards
   ```

2. **Start all services**:
   ```bash
   docker-compose up --build
   ```

3. **Access the applications**:
   - Frontend Dashboard: http://localhost:3000
   - Backend API: http://localhost:8000
   - Streamlit Dashboard: http://localhost:8501
   - Jupyter Lab: http://localhost:8888 (token: watchtower)

### Local Development

1. **Backend Setup**:
   ```bash
   cd backend
   pip install -r requirements.txt
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```

2. **Frontend Setup**:
   ```bash
   cd frontend
   npm install
   npm run dev
   ```

3. **Streamlit Setup**:
   ```bash
   cd streamlit
   pip install -r requirements.txt
   streamlit run app.py
   ```

## 📁 Project Structure

```
dashboards/
├── backend/                 # FastAPI backend
│   ├── main.py             # Main application
│   ├── models/             # Pydantic models
│   ├── services/           # Business logic
│   ├── api/                # API endpoints
│   └── utils/              # Utility functions
├── frontend/               # Next.js frontend
│   ├── src/
│   │   ├── components/     # React components
│   │   │   ├── dashboard/  # Dashboard widgets
│   │   │   │   ├── widgets/ # Sensor intelligence widgets
│   │   │   │   └── WidgetGrid.tsx
│   │   │   └── ui/         # UI components
│   │   ├── pages/          # Next.js pages
│   │   ├── stores/         # Zustand state management
│   │   ├── hooks/          # Custom React hooks
│   │   └── data/           # Mock data and types
│   └── public/             # Static assets
├── streamlit/              # Streamlit dashboard
│   ├── app.py              # Main Streamlit app
│   └── requirements.txt    # Python dependencies
├── notebooks/              # Jupyter integration
│   ├── sensor_analysis.ipynb  # Analysis notebook
│   └── ace_tools.py        # Helper utilities
├── data/                   # Sample data
│   └── sample_sensor_data.csv
└── docker-compose.yml      # Multi-service orchestration
```

## 🔧 API Endpoints

### Core Endpoints
- `GET /` - Health check
- `GET /health` - System status
- `GET /api/dashboard/tabs` - Available dashboard tabs

### Sensor Intelligence Endpoints
- `GET /api/sensors/mission-capability` - Mission capability assessment
- `GET /api/sensors/health-detailed` - Detailed sensor health data
- `GET /api/sensors/detection-ranges` - Target detection capabilities
- `GET /api/sensors/resolution` - Resolution and image quality metrics
- `GET /api/sensors/snr` - Signal-to-noise ratio analysis
- `GET /api/environment/atmospheric` - Atmospheric condition data
- `GET /api/sensors/thermal` - Thermal sensor status
- `GET /api/sensors/performance-timeline` - Performance predictions
- `GET /api/intelligence/recommendations` - AI-powered recommendations
- `GET /api/intelligence/threat-detection` - Threat detection analysis
- `GET /api/sensors/multi-sensor-correlation` - Multi-sensor correlation data
- `GET /api/sensors/dynamic-range` - Dynamic range utilization

### Sensor Data
- `GET /api/sensors/status` - Current sensor status
- `POST /api/sensors/upload` - Upload sensor data
- `POST /api/sensors/upload/csv` - Upload CSV data
- `GET /api/sensors/data/{sensor_id}` - Get sensor data
- `GET /api/sensors/anomalies` - Get detected anomalies
- `GET /api/sensors/physics-metrics` - Physics calculations

### Dashboard Data
- `GET /api/dashboard/{tab_id}` - Get tab-specific data
- `GET /api/dashboard/sensor-intelligence` - Sensor intelligence data
- `GET /api/dashboard/pre-flight` - Pre-flight data
- `GET /api/dashboard/post-flight` - Post-flight data
- `GET /api/dashboard/mission-planning` - Mission planning data
- `GET /api/dashboard/maintenance` - Maintenance data
- `GET /api/dashboard/environment` - Environment data
- `GET /api/dashboard/camera-profile` - Camera profile data
- `GET /api/dashboard/live-flight` - Live flight data

### WebSocket Endpoints
- `WS /ws/sensor-data` - Real-time sensor data
- `WS /ws/alerts` - Real-time alerts
- `WS /ws/flight-status` - Real-time flight status
- `WS /ws/sensor-intelligence` - Real-time sensor intelligence updates

## 📈 Features

### Real-time Monitoring
- Live sensor data streaming via WebSockets
- Real-time alert system
- Live flight status updates
- **Physics-informed sensor intelligence**

### Data Analysis
- Anomaly detection using statistical methods
- Physics-based calculations (velocity, acceleration)
- Performance metrics and KPIs
- **Predictive analytics for sensor degradation**
- **Mission capability assessment**

### Visualization
- Interactive flight path maps
- Time series charts
- Performance dashboards
- Anomaly visualization
- **Sensor intelligence widgets**
- **Real-time capability scoring**

### Data Management
- CSV upload and processing
- Sensor data validation
- Data export capabilities
- **Physics model integration**

## 🔍 Usage Examples

### Upload Sensor Data
```python
import requests

# Upload sensor data
data = {
    "mission_id": "mission_001",
    "sensor_readings": [
        {
            "sensor_id": "gps",
            "sensor_type": "gps",
            "timestamp": "2024-01-01T12:00:00Z",
            "value": {"latitude": 40.7128, "longitude": -74.0060}
        }
    ]
}

response = requests.post("http://localhost:8000/api/sensors/upload", json=data)
```

### Access Sensor Intelligence Data
```python
import requests

# Get mission capability assessment
capability = requests.get("http://localhost:8000/api/sensors/mission-capability").json()
print(f"Mission Capability: {capability['capabilityScore']}%")

# Get sensor health data
health = requests.get("http://localhost:8000/api/sensors/health-detailed").json()
print(f"Current Health: {health['currentHealth']}%")
```

### Jupyter Analysis
```python
from ace_tools import SensorDataProcessor, generate_sample_data

# Load and analyze data
processor = SensorDataProcessor()
```

## 🧠 Sensor Intelligence Widgets

### Mission Capability Card
- **Overall capability score** (0-100%)
- **Trend analysis** (improving/degrading/stable)
- **Confidence metrics** for predictions
- **30-minute projections** for planning
- **Contributing factors** with impact analysis

### Sensor Health Gauge
- **Current health percentage** with status indicators
- **1-hour health predictions** using degradation models
- **Degradation rate analysis** (%/hour)
- **Threshold management** (optimal/warning/critical)
- **Individual sensor status** for each component

### Widget Features
- **Responsive design** for all screen sizes
- **Real-time updates** via WebSocket connections
- **Color-coded status indicators** for quick assessment
- **Refresh functionality** for manual updates
- **Collapsible sections** for space optimization

## 🚀 Performance Considerations

### Real-time Updates
- WebSocket connections for live data streaming
- Optimized widget rendering for 60fps performance
- Efficient data processing for physics calculations

### Memory Management
- Automatic cleanup of WebSocket subscriptions
- Efficient state management with Zustand
- Optimized re-rendering with React.memo

### Network Efficiency
- Batched updates for non-critical data
- Prioritized critical alerts and warnings
- Graceful degradation for offline scenarios
