# Watchtower Drone Operator Dashboard - Project Summary

## 🚁 Project Overview

Watchtower is a comprehensive physics-informed sensor monitoring system for drone operations. This full-stack dashboard provides real-time monitoring, predictive maintenance, and advanced analytics for drone sensor health.

## 🏗️ Architecture

### Tech Stack
- **Backend**: FastAPI (Python) with WebSocket support
- **Frontend**: Next.js 14 with TypeScript and Tailwind CSS
- **Alternative UI**: Streamlit for rapid prototyping
- **Database**: SQLite with SQLAlchemy ORM
- **Real-time**: WebSocket connections for live updates
- **Containerization**: Docker with docker-compose
- **Analytics**: Jupyter notebooks for advanced analysis

### Services
1. **Backend API** (Port 8000): Core API with physics models
2. **Frontend Dashboard** (Port 3000): Main operator interface
3. **Streamlit Dashboard** (Port 8501): Alternative rapid interface
4. **Jupyter Notebook** (Port 8888): Advanced analytics

## 🔬 Physics Models Implemented

### 1. Thermal Camera (Arrhenius Degradation)
- Models thermal sensor degradation based on temperature exposure
- Predicts remaining sensor life using Arrhenius equation
- Accounts for thermal cycling effects

### 2. GPS EMI Correlation
- Monitors GPS signal quality vs electromagnetic interference
- Correlates position accuracy with EMI levels
- Provides interference mitigation recommendations

### 3. IMU Vibration-Induced Bias Drift
- Tracks accelerometer/gyroscope bias drift from vibrations
- Models vibration frequency effects on sensor accuracy
- Predicts calibration requirements

### 4. Environmental Correlations
- Cross-sensor environmental impact analysis
- Temperature, humidity, and pressure correlations
- Weather condition impact on sensor performance

## 🎯 Core Features

### Real-time Monitoring
- Live sensor health gauges with color-coded status
- Mission status bar with altitude, speed, and battery
- WebSocket-powered real-time updates
- Alert system for critical sensor issues

### Data Management
- CSV upload and processing
- Automatic sensor data parsing
- Historical data visualization
- Export functionality (CSV, JSON, PDF)

### Analytics Dashboard
- Cross-sensor correlation matrix
- Physics model performance metrics
- Predictive maintenance alerts
- Trend analysis and forecasting

### Professional UI
- Dark military/aviation theme
- Responsive design for various screen sizes
- Intuitive navigation and controls
- Professional-grade visualizations

## 📊 Sample Data

The system includes realistic sensor data with:
- 8 different sensor types (GPS, IMU, Thermal, etc.)
- Physics-based degradation patterns
- Environmental correlation effects
- Mission simulation data
- Historical performance metrics

## 🚀 Quick Start

### Prerequisites
- Docker Desktop installed and running
- At least 4GB RAM available
- Ports 3000, 8000, 8501, 8888 available

### Installation
```bash
cd dashboards
docker-compose up --build
```

### Access Points
- **Main Dashboard**: http://localhost:3000
- **Streamlit Alternative**: http://localhost:8501
- **API Documentation**: http://localhost:8000/docs
- **Jupyter Analytics**: http://localhost:8888 (token: watchtower)

## 🧪 Testing

### API Testing
```bash
# Python test
python test_api.py

# PowerShell test
powershell -ExecutionPolicy Bypass -File test_api.ps1
```

### Health Checks
- Backend: http://localhost:8000/api/health
- Sensors: http://localhost:8000/api/sensors
- Mission Status: http://localhost:8000/api/mission-status

## 📁 Project Structure

```
dashboards/
├── backend/                 # FastAPI application
│   ├── app/
│   │   ├── models/         # Database models
│   │   ├── services/       # Business logic
│   │   ├── physics/        # Physics models
│   │   └── api/           # API routes
│   └── data/              # Sample data
├── frontend/               # Next.js application
│   ├── components/         # React components
│   ├── pages/             # Next.js pages
│   └── styles/            # Tailwind CSS
├── streamlit/             # Streamlit dashboard
├── notebooks/             # Jupyter notebooks
├── data/                  # Database and uploads
└── docker-compose.yml     # Container orchestration
```

## 🔧 Development

### Adding New Sensors
1. Add sensor model in `backend/app/models/`
2. Create physics model in `backend/app/physics/`
3. Add API endpoints in `backend/app/api/`
4. Update frontend components
5. Add to sample data

### Customizing Physics Models
- Models are in `backend/app/physics/`
- Each model implements degradation prediction
- Can be extended for new sensor types
- Supports parameter tuning

### UI Customization
- Frontend uses Tailwind CSS for styling
- Dark theme defined in `frontend/styles/`
- Components are modular and reusable
- Responsive design for mobile/tablet

## 📈 Performance

### Optimization Features
- WebSocket for real-time updates
- Efficient database queries with SQLAlchemy
- Optimized frontend rendering
- Docker containerization for scalability

### Monitoring
- Built-in health checks
- Performance metrics
- Error logging and alerting
- Resource usage monitoring

## 🔒 Security

### Features
- Input validation on all endpoints
- SQL injection protection via SQLAlchemy
- CORS configuration for frontend
- Secure WebSocket connections

### Best Practices
- Environment variables for configuration
- No hardcoded secrets
- Input sanitization
- Error handling without information leakage

## 🎨 UI/UX Design

### Design Principles
- Military/aviation aesthetic
- High contrast for readability
- Intuitive navigation
- Responsive design
- Accessibility considerations

### Color Scheme
- Dark background (#0f1419)
- Green accents for good status
- Red for critical alerts
- Blue for information
- Yellow for warnings

## 📚 Documentation

- **API Docs**: Auto-generated at `/docs`
- **Troubleshooting**: See `TROUBLESHOOTING.md`
- **Physics Models**: Documented in code comments
- **Component Guide**: Frontend component documentation

## 🚀 Future Enhancements

### Planned Features
- Machine learning integration
- Advanced predictive analytics
- Mobile app companion
- Cloud deployment options
- Additional sensor types
- Advanced visualization options

### Scalability
- Microservices architecture ready
- Database migration to PostgreSQL
- Redis for caching
- Load balancing support
- Kubernetes deployment

## 🤝 Contributing

### Development Workflow
1. Fork the repository
2. Create feature branch
3. Implement changes
4. Add tests
5. Submit pull request

### Code Standards
- Python: PEP 8 compliance
- TypeScript: ESLint configuration
- React: Component best practices
- Documentation: Inline comments

## 📞 Support

For issues and questions:
1. Check `TROUBLESHOOTING.md`
2. Review API documentation
3. Test with provided scripts
4. Check Docker logs

---

**Watchtower Dashboard** - Advanced drone sensor monitoring with physics-informed analytics 