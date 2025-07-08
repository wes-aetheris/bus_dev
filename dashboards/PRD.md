# Watchtower Drone Sensor Dashboard - Complete Project Setup

## Project Overview
Create a full-stack drone operator dashboard for **Watchtower** - a physics-informed sensor monitoring system. The dashboard should showcase real-time sensor health monitoring, cross-sensor correlation analysis, and predictive maintenance capabilities for drone sensors.

## Tech Stack Requirements

### Backend (Python)
- **FastAPI** for REST API and WebSocket support
- **Pandas** for data processing and CSV handling
- **NumPy** for physics-based calculations
- **Pydantic** for data validation
- **SQLAlchemy** for database operations (SQLite for development)
- **Asyncio** for real-time data streaming

### Frontend (React/TypeScript)
- **Next.js 14** with TypeScript
- **Tailwind CSS** for styling
- **Recharts** for sensor visualizations
- **Lucide React** for icons
- **Socket.io-client** for real-time updates
- **React Hook Form** for data upload forms
- **Zustand** for state management

### Additional Tools
- **Docker** for containerization
- **Jupyter notebooks** for data analysis integration
- **Streamlit** as alternative dashboard option

## Project Structure
```
watchtower-dashboard/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py
│   │   ├── models/
│   │   │   ├── __init__.py
│   │   │   ├── sensor_data.py
│   │   │   └── alerts.py
│   │   ├── services/
│   │   │   ├── __init__.py
│   │   │   ├── physics_engine.py
│   │   │   ├── data_processor.py
│   │   │   └── alert_generator.py
│   │   ├── api/
│   │   │   ├── __init__.py
│   │   │   ├── sensors.py
│   │   │   ├── dashboard.py
│   │   │   └── websocket.py
│   │   └── utils/
│   │       ├── __init__.py
│   │       ├── csv_handler.py
│   │       └── physics_models.py
│   ├── data/
│   │   ├── sample_data.csv
│   │   └── templates/
│   ├── notebooks/
│   │   ├── data_analysis.ipynb
│   │   └── sensor_modeling.ipynb
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── dashboard/
│   │   │   │   ├── SensorHealthGauge.tsx
│   │   │   │   ├── CorrelationMatrix.tsx
│   │   │   │   ├── DegradationChart.tsx
│   │   │   │   ├── AlertBanner.tsx
│   │   │   │   ├── MissionStatus.tsx
│   │   │   │   └── EnvironmentalPanel.tsx
│   │   │   ├── data/
│   │   │   │   ├── CSVUploader.tsx
│   │   │   │   └── DataControls.tsx
│   │   │   └── layout/
│   │   │       ├── Header.tsx
│   │   │       ├── Sidebar.tsx
│   │   │       └── Layout.tsx
│   │   ├── hooks/
│   │   │   ├── useWebSocket.ts
│   │   │   ├── useSensorData.ts
│   │   │   └── useAlerts.ts
│   │   ├── stores/
│   │   │   ├── dashboardStore.ts
│   │   │   └── alertStore.ts
│   │   ├── types/
│   │   │   ├── sensor.ts
│   │   │   └── dashboard.ts
│   │   ├── utils/
│   │   │   ├── api.ts
│   │   │   └── physics.ts
│   │   ├── pages/
│   │   │   ├── index.tsx
│   │   │   ├── dashboard.tsx
│   │   │   └── api/
│   │   └── styles/
│   │       └── globals.css
│   ├── package.json
│   ├── tailwind.config.js
│   ├── next.config.js
│   └── Dockerfile
├── streamlit-app/
│   ├── streamlit_dashboard.py
│   ├── components/
│   │   ├── sensor_widgets.py
│   │   └── charts.py
│   └── requirements.txt
├── docker-compose.yml
├── .env.example
└── README.md
```

## Core Features to Implement

### 1. Backend API (FastAPI)
```python
# Key endpoints needed:
- GET /api/sensors/health - Current sensor health status
- POST /api/data/upload - CSV file upload
- GET /api/data/historical - Historical sensor data
- GET /api/alerts/current - Current alerts
- GET /api/physics/predictions - Predictive maintenance
- WebSocket /ws/realtime - Real-time sensor updates
```

### 2. Physics-Informed Models
Implement the physics equations from the technical documents:
- **Thermal Camera**: Arrhenius degradation (dark current doubling every 6-8°C)
- **GPS**: EMI correlation and signal degradation
- **IMU**: Vibration-induced bias drift
- **Cross-sensor correlation**: Environmental factor analysis

### 3. Frontend Dashboard Components
- **Real-time sensor health gauges** (0-100% with color coding)
- **Degradation timeline charts** showing physics-based predictions
- **Cross-sensor correlation matrix** heatmap
- **Alert system** with critical/warning/info levels
- **Environmental context panel** (temperature, humidity, vibration, EMI)
- **Mission status bar** (altitude, speed, battery, flight time)
- **Predictive maintenance recommendations**

### 4. Data Management
- **CSV upload and validation**
- **Real-time data streaming**
- **Historical data storage and retrieval**
- **Data export functionality**
- **Jupyter notebook integration**

### 5. Styling Requirements
- **Dark theme** with drone operator aesthetics
- **Military/aviation color scheme**: Dark blues, amber alerts, green status indicators
- **Responsive design** for different screen sizes
- **Animated elements**: Pulsing alerts, smooth chart updates
- **Professional typography** and spacing

## Physics-Based Data Generation
Implement realistic sensor degradation patterns:

### Thermal Camera Degradation
```python
# Arrhenius relationship for dark current
dark_current = I_0 * exp(-E_g / (2*k*T))
# Health degrades as dark current increases
thermal_health = 100 - (dark_current_ratio - 1) * scaling_factor
```

### GPS EMI Correlation
```python
# GPS health affected by EMI levels
gps_health = base_health - emi_correlation_factor * emi_strength
```

### Environmental Context
- Temperature cycling effects on all sensors
- Vibration impact on IMU drift
- Humidity effects on optical sensors
- EMI interference patterns

## Real-Time Features
- **WebSocket connections** for live data updates
- **Streaming alerts** based on threshold crossings
- **Live correlation analysis** between sensors
- **Real-time physics model updates**

## Sample Data Requirements
Create realistic CSV templates with:
- Timestamp column (ISO format)
- Sensor health percentages (0-100)
- Environmental data (temperature, humidity, vibration, EMI)
- Mission telemetry (altitude, speed, battery)
- Physics parameters (dark current, bias stability, etc.)

## UI/UX Requirements
- **Professional drone operator interface**
- **Intuitive navigation** between dashboard views
- **Clear visual hierarchy** for alerts and status
- **Contextual help** and tooltips
- **Keyboard shortcuts** for common actions
- **Print-friendly** maintenance reports

## Integration Points
- **Jupyter notebook** data analysis workflows
- **CSV file** drag-and-drop upload
- **REST API** for external system integration
- **WebSocket** real-time data feeds
- **Export capabilities** (CSV, JSON, PDF reports)

## Development Priorities
1. **Backend API with physics models**
2. **React dashboard with core components**
3. **WebSocket real-time updates**
4. **CSV upload and data management**
5. **Streamlit alternative interface**
6. **Jupyter notebook integration**
7. **Docker containerization**
8. **Documentation and examples**

## Environment Variables
```env
# Backend
DATABASE_URL=sqlite:///./watchtower.db
CORS_ORIGINS=http://localhost:3000,http://localhost:8501
DEBUG=true

# Frontend
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_WS_URL=ws://localhost:8000/ws

# Streamlit
STREAMLIT_SERVER_PORT=8501
```

## Key Dependencies

### Backend (requirements.txt)
```txt
fastapi==0.104.1
uvicorn==0.24.0
pandas==2.1.4
numpy==1.24.3
pydantic==2.5.0
sqlalchemy==2.0.23
python-multipart==0.0.6
python-socketio==5.10.0
plotly==5.17.0
scipy==1.11.4
```

### Frontend (package.json key deps)
```json
{
  "dependencies": {
    "next": "14.0.4",
    "react": "18.2.0",
    "typescript": "5.3.3",
    "tailwindcss": "3.3.6",
    "recharts": "2.8.0",
    "lucide-react": "0.294.0",
    "socket.io-client": "4.7.4",
    "zustand": "4.4.7",
    "react-hook-form": "7.48.2"
  }
}
```

## Success Criteria
- ✅ Real-time sensor monitoring with physics-based health calculations
- ✅ CSV file upload and processing
- ✅ Cross-sensor correlation analysis
- ✅ Predictive maintenance alerts
- ✅ Professional drone operator interface
- ✅ Jupyter notebook integration
- ✅ Responsive design across devices
- ✅ Real-time WebSocket updates
- ✅ Export functionality for reports
- ✅ Docker containerization

## Additional Notes
- Use **Watchtower branding** (shield/tower icon, amber/blue color scheme)
- Include **physics equations** in tooltips and help text
- Implement **realistic failure scenarios** for demo purposes
- Add **confidence metrics** for all predictions
- Create **sample mission scenarios** for testing
- Document **API endpoints** for external integration