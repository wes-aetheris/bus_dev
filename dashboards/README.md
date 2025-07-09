# Watchtower Drone Sensor Dashboard

A comprehensive full-stack dashboard for drone operators to monitor sensor data, plan missions, and analyze flight performance.

## 🚁 Project Overview

Watchtower is a complete drone sensor dashboard system with multiple interfaces:

- **Next.js Frontend**: Modern web dashboard with real-time data visualization
- **FastAPI Backend**: RESTful API with WebSocket support for real-time updates
- **Streamlit Alternative**: Rapid prototyping and data exploration interface
- **Jupyter Integration**: Advanced analytics and research capabilities

## 🏗️ Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │   Backend       │    │   Streamlit     │
│   (Next.js)     │◄──►│   (FastAPI)     │◄──►│   (Dashboard)   │
│   Port: 3000    │    │   Port: 8000    │    │   Port: 8501    │
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

1. **Pre-Flight**: Sensor calibration, system checks, weather conditions
2. **Post-Flight**: Flight analysis, data collection summary, anomaly detection
3. **Mission Planning**: Route optimization, weather forecasting, no-fly zones
4. **Maintenance**: Component health monitoring, maintenance schedules
5. **Environment & Context**: Environmental conditions, air quality, terrain data
6. **Camera Sensor Profile**: Camera settings, image analysis, recording modes
7. **Operational Flight**: Real-time flight monitoring, mission progress

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
│   │   ├── pages/          # Next.js pages
│   │   ├── stores/         # Zustand state management
│   │   └── hooks/          # Custom React hooks
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

### Sensor Data
- `GET /api/sensors/status` - Current sensor status
- `POST /api/sensors/upload` - Upload sensor data
- `POST /api/sensors/upload/csv` - Upload CSV data
- `GET /api/sensors/data/{sensor_id}` - Get sensor data
- `GET /api/sensors/anomalies` - Get detected anomalies
- `GET /api/sensors/physics-metrics` - Physics calculations

### Dashboard Data
- `GET /api/dashboard/{tab_id}` - Get tab-specific data
- `GET /api/dashboard/pre-flight` - Pre-flight data
- `GET /api/dashboard/post-flight` - Post-flight data
- `GET /api/dashboard/mission-planning` - Mission planning data
- `GET /api/dashboard/maintenance` - Maintenance data
- `GET /api/dashboard/environment` - Environment data
- `GET /api/dashboard/camera-profile` - Camera profile data
- `GET /api/dashboard/operational-flight` - Operational flight data

### WebSocket Endpoints
- `WS /ws/sensor-data` - Real-time sensor data
- `WS /ws/alerts` - Real-time alerts
- `WS /ws/flight-status` - Real-time flight status

## 📈 Features

### Real-time Monitoring
- Live sensor data streaming via WebSockets
- Real-time alert system
- Live flight status updates

### Data Analysis
- Anomaly detection using statistical methods
- Physics-based calculations (velocity, acceleration)
- Performance metrics and KPIs

### Visualization
- Interactive flight path maps
- Time series charts
- Performance dashboards
- Anomaly visualization

### Data Management
- CSV upload and processing
- Sensor data validation
- Data export capabilities

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

### Jupyter Analysis
```python
from ace_tools import SensorDataProcessor, generate_sample_data

# Load and analyze data
processor = SensorDataProcessor()
data = generate_sample_data(1000)
processor.load_data(data)

# Detect anomalies
anomalies = processor.detect_anomalies(['altitude', 'roll', 'pitch'])

# Calculate metrics
metrics = processor.calculate_flight_metrics()
```

## 🧪 Testing

### Backend Tests
```bash
cd backend
python -m pytest tests/
```

### Frontend Tests
```bash
cd frontend
npm test
```

### Integration Tests
```bash
# Test API endpoints
curl http://localhost:8000/health
curl http://localhost:8000/api/sensors/status
```

## 🚨 Troubleshooting

### Common Issues

1. **Port conflicts**: Ensure ports 3000, 8000, 8501, 8888 are available
2. **Docker build failures**: Check Docker logs with `docker-compose logs`
3. **API connection errors**: Verify backend is running on port 8000
4. **Frontend build issues**: Clear node_modules and reinstall dependencies

### Health Checks
- Backend: http://localhost:8000/health
- Frontend: http://localhost:3000
- Streamlit: http://localhost:8501/_stcore/health
- Jupyter: http://localhost:8888/api/status

## 📚 Documentation

- [API Documentation](http://localhost:8000/docs) - Interactive API docs
- [Project Summary](PROJECT_SUMMARY.md) - Detailed project overview
- [Setup Guide](SETUP.md) - Detailed setup instructions
- [Troubleshooting](TROUBLESHOOTING.md) - Common issues and solutions

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For support and questions:
- Create an issue in the repository
- Check the troubleshooting guide
- Review the API documentation

---

**Watchtower Dashboard** - Empowering drone operators with comprehensive sensor monitoring and analysis capabilities.
