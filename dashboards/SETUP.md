# Watchtower Dashboard Setup Guide

This guide will help you set up and run the complete Watchtower drone operator dashboard with physics-informed sensor monitoring.

## 🚀 Quick Start with Docker

The easiest way to run the entire system is using Docker Compose:

```bash
# Navigate to the dashboards directory
cd dashboards

# Start all services
docker-compose up --build

# Access the applications:
# - Frontend Dashboard: http://localhost:3000
# - Streamlit Dashboard: http://localhost:8501
# - Backend API: http://localhost:8000
# - Jupyter Notebooks: http://localhost:8888 (token: watchtower)
```

## 📁 Project Structure

```
dashboards/
├── backend/                 # FastAPI backend with physics models
│   ├── main.py             # Main API application
│   ├── models/             # Database models and schemas
│   ├── services/           # Physics models and business logic
│   ├── requirements.txt    # Python dependencies
│   └── Dockerfile         # Backend container
├── frontend/              # Next.js dashboard
│   ├── app/               # React components
│   ├── package.json       # Node.js dependencies
│   └── Dockerfile         # Frontend container
├── streamlit/             # Streamlit alternative
│   ├── app.py             # Streamlit application
│   ├── requirements.txt   # Python dependencies
│   └── Dockerfile         # Streamlit container
├── data/                  # Sample data and CSV files
│   └── sample_sensor_data.csv
├── notebooks/             # Jupyter notebooks for analysis
│   ├── sensor_analysis.ipynb
│   └── Dockerfile
├── docker-compose.yml     # Container orchestration
└── README.md             # Project documentation
```

## 🔧 Manual Setup

### Backend Setup

```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

### Streamlit Setup

```bash
cd streamlit
pip install -r requirements.txt
streamlit run app.py
```

## 🎯 Key Features

### Physics Models Implemented

1. **Thermal Camera - Arrhenius Degradation**
   - Dark current doubling every 6-8°C temperature increase
   - Temperature-dependent degradation modeling

2. **GPS - EMI Correlation**
   - Signal degradation based on electromagnetic interference
   - Frequency and signal strength correlation

3. **IMU - Vibration-Induced Bias Drift**
   - Bias drift caused by mechanical vibration
   - Frequency and duration effects

4. **Environmental Correlation**
   - Multi-factor analysis (temperature, humidity, vibration, EMI)
   - Cross-sensor correlation modeling

### Dashboard Features

- **Real-time Monitoring**: Live sensor health gauges with WebSocket updates
- **Mission Status**: Altitude, speed, battery, flight time tracking
- **Alert System**: Multi-severity alerts with physics model triggers
- **Data Upload**: CSV file processing with validation
- **Correlation Analysis**: Cross-sensor correlation matrix visualization
- **Export Functionality**: CSV, JSON, and PDF report generation
- **Dark Theme**: Military/aviation themed interface

## 📊 Sample Data

The system includes realistic sample data with physics-based degradation patterns:

- **Thermal Camera**: Shows Arrhenius degradation with temperature correlation
- **GPS**: Demonstrates EMI-based signal degradation
- **IMU**: Illustrates vibration-induced bias drift
- **Barometer**: Environmental factor correlation

## 🔌 API Endpoints

### Core Endpoints
- `GET /api/sensors` - Get all sensor information
- `GET /api/sensors/{id}/health` - Get detailed sensor health
- `GET /api/mission-status` - Get current mission status
- `GET /api/alerts` - Get current alerts
- `GET /api/correlation-matrix` - Get cross-sensor correlations

### Data Management
- `POST /api/upload-csv` - Upload and process CSV data
- `GET /api/export/{format}` - Export data (CSV, JSON, PDF)

### Physics Models
- `GET /api/physics-models` - Get physics model information

### Real-time
- `WS /ws` - WebSocket endpoint for real-time updates

## 🎨 UI Components

### Frontend (Next.js)
- **SensorHealthGauge**: Animated health gauges with color coding
- **MissionStatusBar**: Real-time mission parameters display
- **CorrelationMatrix**: Interactive correlation heatmap
- **AlertPanel**: Multi-severity alert display
- **PhysicsModelCard**: Physics model information cards
- **DataUpload**: Drag-and-drop CSV upload

### Streamlit Alternative
- **Dashboard**: Main monitoring interface
- **Sensor Details**: Detailed sensor analysis
- **Physics Models**: Physics model explanations
- **Data Upload**: File upload interface
- **Analytics**: Advanced data analysis

## 🔒 Security Features

- JWT-based authentication (ready for implementation)
- Input validation and sanitization
- CORS configuration
- Rate limiting on API endpoints

## 📈 Performance Optimizations

- Real-time WebSocket updates
- Optimized database queries
- Caching for static data
- Efficient physics model calculations

## 🐛 Troubleshooting

### Common Issues

1. **Port Conflicts**
   ```bash
   # Check if ports are in use
   netstat -tulpn | grep :8000
   netstat -tulpn | grep :3000
   netstat -tulpn | grep :8501
   ```

2. **Docker Issues**
   ```bash
   # Clean up containers
   docker-compose down
   docker system prune -f
   docker-compose up --build
   ```

3. **API Connection Issues**
   - Check if backend is running on port 8000
   - Verify environment variables in docker-compose.yml
   - Check WebSocket connection on port 8001

4. **Frontend Build Issues**
   ```bash
   # Clear npm cache
   npm cache clean --force
   rm -rf node_modules package-lock.json
   npm install
   ```

## 🚀 Production Deployment

For production deployment, consider:

1. **Environment Variables**
   ```bash
   DATABASE_URL=postgresql://user:pass@host:port/db
   JWT_SECRET=your-secret-key
   WEBSOCKET_PORT=8001
   ```

2. **Reverse Proxy**
   - Use Nginx for load balancing
   - Configure SSL certificates
   - Set up proper CORS headers

3. **Database**
   - Use PostgreSQL for production
   - Implement proper backup strategy
   - Set up connection pooling

4. **Monitoring**
   - Add health check endpoints
   - Implement logging
   - Set up metrics collection

## 📚 Additional Resources

- **Physics Models**: See `backend/services/physics_models.py` for detailed implementations
- **API Documentation**: Available at `http://localhost:8000/docs` when backend is running
- **Sample Data**: Use `data/sample_sensor_data.csv` for testing
- **Jupyter Analysis**: Run `notebooks/sensor_analysis.ipynb` for advanced analysis

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

---

**Watchtower**: Physics-Informed Sensor Monitoring for Drone Operations

For support or questions, please refer to the main README.md file. 