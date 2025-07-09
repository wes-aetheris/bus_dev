# Watchtower Dashboard Troubleshooting Guide

This guide provides solutions for common issues encountered when setting up and running the Watchtower Drone Sensor Dashboard.

## 🚨 Common Issues

### 1. Docker Issues

#### Problem: Docker Build Fails
**Symptoms**: Build process fails with errors
```bash
ERROR: failed to build: error building at step X
```

**Solutions**:
```bash
# Clean Docker cache
docker system prune -a

# Rebuild without cache
docker-compose build --no-cache

# Check Docker version
docker --version
docker-compose --version

# Ensure Docker daemon is running
sudo systemctl status docker
```

#### Problem: Port Already in Use
**Symptoms**: Service fails to start with port binding errors
```bash
ERROR: for backend Cannot start service backend: driver failed programming external connectivity
```

**Solutions**:
```bash
# Check port usage
netstat -tulpn | grep :8000
netstat -tulpn | grep :3000

# Kill processes using ports
sudo lsof -ti:8000 | xargs kill -9
sudo lsof -ti:3000 | xargs kill -9

# Or change ports in docker-compose.yml
ports:
  - "8001:8000"  # Change external port
```

#### Problem: Permission Denied
**Symptoms**: Docker commands fail with permission errors
```bash
Got permission denied while trying to connect to the Docker daemon
```

**Solutions**:
```bash
# Add user to docker group
sudo usermod -aG docker $USER

# Logout and login again, or run:
newgrp docker

# Or run Docker with sudo
sudo docker-compose up
```

### 2. Backend Issues

#### Problem: FastAPI Import Errors
**Symptoms**: ModuleNotFoundError when starting backend
```bash
ModuleNotFoundError: No module named 'fastapi'
```

**Solutions**:
```bash
# Install dependencies
cd backend
pip install -r requirements.txt

# Check Python version
python --version  # Should be 3.11+

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

#### Problem: API Connection Refused
**Symptoms**: Frontend can't connect to backend API
```bash
Failed to fetch: http://localhost:8000/api/sensors/status
```

**Solutions**:
```bash
# Check if backend is running
curl http://localhost:8000/health

# Check backend logs
docker-compose logs backend

# Verify CORS settings in backend/main.py
# Ensure frontend URL is in allowed origins
```

#### Problem: WebSocket Connection Fails
**Symptoms**: Real-time updates not working
```bash
WebSocket connection failed
```

**Solutions**:
```bash
# Check WebSocket endpoint
curl -i -N -H "Connection: Upgrade" -H "Upgrade: websocket" \
  -H "Sec-WebSocket-Version: 13" -H "Sec-WebSocket-Key: test" \
  http://localhost:8000/ws/sensor-data

# Verify WebSocket implementation in backend/api/websocket.py
```

### 3. Frontend Issues

#### Problem: Next.js Build Fails
**Symptoms**: npm run build fails with TypeScript errors
```bash
Type error: Cannot find module 'react'
```

**Solutions**:
```bash
# Clear node_modules and reinstall
cd frontend
rm -rf node_modules package-lock.json
npm install

# Check Node.js version
node --version  # Should be 18+

# Install missing dependencies
npm install react react-dom @types/react @types/react-dom
```

#### Problem: Frontend Can't Connect to Backend
**Symptoms**: Dashboard shows loading or error states
```bash
API request failed: Network Error
```

**Solutions**:
```bash
# Check environment variables
cat frontend/.env.local

# Ensure backend is running
curl http://localhost:8000/health

# Check CORS configuration
# Verify NEXT_PUBLIC_API_URL is correct
```

#### Problem: Tailwind CSS Not Working
**Symptoms**: Styles not applied correctly
```bash
CSS classes not working
```

**Solutions**:
```bash
# Check Tailwind configuration
cat frontend/tailwind.config.js

# Rebuild CSS
cd frontend
npm run build

# Check PostCSS configuration
cat frontend/postcss.config.js
```

### 4. Streamlit Issues

#### Problem: Streamlit Won't Start
**Symptoms**: Streamlit fails to start or shows errors
```bash
ModuleNotFoundError: No module named 'streamlit'
```

**Solutions**:
```bash
# Install Streamlit
pip install streamlit

# Check Python environment
python -c "import streamlit; print(streamlit.__version__)"

# Run with explicit port
streamlit run app.py --server.port 8501 --server.address 0.0.0.0
```

#### Problem: Plotly Charts Not Displaying
**Symptoms**: Charts show as blank or error
```bash
Chart rendering failed
```

**Solutions**:
```bash
# Install Plotly
pip install plotly

# Check browser console for JavaScript errors
# Ensure internet connection for map tiles
```

### 5. Jupyter Issues

#### Problem: Jupyter Lab Won't Start
**Symptoms**: Jupyter fails to start or shows errors
```bash
ModuleNotFoundError: No module named 'jupyter'
```

**Solutions**:
```bash
# Install Jupyter
pip install jupyterlab ipykernel

# Create kernel
python -m ipykernel install --user --name watchtower_env

# Start Jupyter
jupyter lab --ip 0.0.0.0 --port 8888 --no-browser --allow-root
```

#### Problem: Notebook Import Errors
**Symptoms**: Import errors in Jupyter notebook
```bash
ModuleNotFoundError: No module named 'pandas'
```

**Solutions**:
```bash
# Install required packages
pip install pandas numpy matplotlib plotly scipy scikit-learn

# Check kernel selection in notebook
# Ensure correct kernel is selected
```

## 🔍 Diagnostic Commands

### System Diagnostics
```bash
# Check system resources
free -h
df -h
top

# Check network connectivity
ping localhost
curl -I http://localhost:8000

# Check Docker status
docker info
docker-compose ps
```

### Service Diagnostics
```bash
# Check all service logs
docker-compose logs

# Check specific service logs
docker-compose logs backend
docker-compose logs frontend

# Check service health
docker-compose exec backend curl http://localhost:8000/health
```

### Network Diagnostics
```bash
# Check port usage
netstat -tulpn | grep -E ':(3000|8000|8501|8888)'

# Check Docker network
docker network ls
docker network inspect dashboards_watchtower-network

# Test inter-service communication
docker-compose exec frontend curl http://backend:8000/health
```

## 🛠️ Debugging Tools

### Backend Debugging
```bash
# Run with debug mode
cd backend
uvicorn main:app --reload --host 0.0.0.0 --port 8000 --log-level debug

# Test API endpoints
curl -X GET http://localhost:8000/health
curl -X GET http://localhost:8000/api/sensors/status
curl -X GET http://localhost:8000/api/dashboard/tabs
```

### Frontend Debugging
```bash
# Run with debug mode
cd frontend
npm run dev -- --inspect

# Check browser console
# Open Developer Tools (F12)
# Check Network tab for failed requests
```

### Database Debugging
```bash
# Check data files
ls -la data/
cat data/sample_sensor_data.csv

# Test data processing
cd backend
python -c "from services.data_processor import DataProcessor; print('OK')"
```

## 🔧 Configuration Fixes

### Environment Variables
```bash
# Backend environment
cat > backend/.env << EOF
ENVIRONMENT=development
DEBUG=true
API_HOST=0.0.0.0
API_PORT=8000
CORS_ORIGINS=http://localhost:3000,http://localhost:8501
EOF

# Frontend environment
cat > frontend/.env.local << EOF
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_WS_URL=ws://localhost:8000
NODE_ENV=development
EOF
```

### Docker Configuration
```bash
# Create development override
cat > docker-compose.override.yml << EOF
version: '3.8'
services:
  backend:
    volumes:
      - ./backend:/app
    environment:
      - ENVIRONMENT=development
      - DEBUG=true
  frontend:
    volumes:
      - ./frontend:/app
      - /app/node_modules
    environment:
      - NODE_ENV=development
EOF
```

## 📊 Performance Issues

### High Memory Usage
**Symptoms**: System becomes slow or crashes
```bash
# Check memory usage
docker stats

# Limit container resources
services:
  backend:
    deploy:
      resources:
        limits:
          memory: 512M
```

### Slow API Responses
**Symptoms**: Dashboard loads slowly
```bash
# Check API response times
curl -w "@curl-format.txt" -o /dev/null -s http://localhost:8000/health

# Optimize backend
# Add caching
# Use async operations
```

### Frontend Performance
**Symptoms**: Dashboard is slow to load
```bash
# Check bundle size
cd frontend
npm run build
# Look for large bundle warnings

# Optimize imports
# Use code splitting
# Lazy load components
```

## 🔒 Security Issues

### CORS Errors
**Symptoms**: Browser blocks requests
```bash
# Check CORS configuration in backend/main.py
# Ensure frontend URL is in allowed origins
# Add proper CORS headers
```

### Authentication Issues
**Symptoms**: API calls fail with auth errors
```bash
# Check API key configuration
# Verify authentication headers
# Test with Postman or curl
```

## 📞 Getting Help

### Before Asking for Help
1. **Check logs**: `docker-compose logs`
2. **Test endpoints**: `curl http://localhost:8000/health`
3. **Verify setup**: Follow setup guide step by step
4. **Check versions**: Ensure all software versions match requirements

### When Asking for Help
Include the following information:
- **Operating System**: Windows/macOS/Linux version
- **Docker Version**: `docker --version`
- **Node.js Version**: `node --version`
- **Python Version**: `python --version`
- **Error Messages**: Complete error output
- **Steps Taken**: What you've already tried
- **Logs**: Relevant log output

### Useful Commands for Debugging
```bash
# System information
uname -a
docker version
node --version
python --version

# Service status
docker-compose ps
docker-compose logs --tail=50

# Network connectivity
curl -v http://localhost:8000/health
curl -v http://localhost:3000

# Resource usage
docker stats --no-stream
```

---

**Remember**: Most issues can be resolved by following the setup guide carefully and checking the logs for specific error messages.
