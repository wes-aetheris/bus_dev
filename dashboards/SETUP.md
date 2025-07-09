# Watchtower Dashboard Setup Guide

This guide provides detailed instructions for setting up the Watchtower Drone Sensor Dashboard using different deployment methods.

## 📋 Prerequisites

### System Requirements
- **Operating System**: Windows 10/11, macOS 10.15+, or Linux (Ubuntu 18.04+)
- **RAM**: Minimum 4GB, Recommended 8GB+
- **Storage**: 2GB free space
- **Network**: Internet connection for package downloads

### Required Software
- **Docker**: Version 20.10+ with Docker Compose
- **Node.js**: Version 18+ (for local development)
- **Python**: Version 3.11+ (for local development)
- **Git**: Version 2.30+ (for cloning repository)

## 🚀 Quick Start with Docker (Recommended)

### Step 1: Install Docker
1. **Windows/macOS**: Download and install Docker Desktop
   ```bash
   # Download from https://www.docker.com/products/docker-desktop
   ```

2. **Linux**: Install Docker and Docker Compose
   ```bash
   # Ubuntu/Debian
   sudo apt update
   sudo apt install docker.io docker-compose
   sudo usermod -aG docker $USER
   ```

### Step 2: Clone Repository
```bash
git clone <repository-url>
cd dashboards
```

### Step 3: Start Services
```bash
# Build and start all services
docker-compose up --build

# Or run in background
docker-compose up --build -d
```

### Step 4: Access Applications
- **Frontend Dashboard**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **Streamlit Dashboard**: http://localhost:8501
- **Jupyter Lab**: http://localhost:8888 (token: watchtower)

### Step 5: Verify Installation
```bash
# Check service status
docker-compose ps

# View logs
docker-compose logs

# Test API health
curl http://localhost:8000/health
```

## 🔧 Local Development Setup

### Backend Setup

#### Step 1: Python Environment
```bash
# Create virtual environment
python -m venv watchtower_env

# Activate environment
# Windows
watchtower_env\Scripts\activate
# macOS/Linux
source watchtower_env/bin/activate
```

#### Step 2: Install Dependencies
```bash
cd backend
pip install -r requirements.txt
```

#### Step 3: Run Backend
```bash
# Development mode with auto-reload
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Production mode
uvicorn main:app --host 0.0.0.0 --port 8000
```

#### Step 4: Test Backend
```bash
# Test health endpoint
curl http://localhost:8000/health

# Test API documentation
# Open http://localhost:8000/docs in browser
```

### Frontend Setup

#### Step 1: Install Node.js Dependencies
```bash
cd frontend
npm install
```

#### Step 2: Configure Environment
```bash
# Create .env.local file
echo "NEXT_PUBLIC_API_URL=http://localhost:8000" > .env.local
```

#### Step 3: Run Frontend
```bash
# Development mode
npm run dev

# Production build
npm run build
npm start
```

#### Step 4: Test Frontend
- Open http://localhost:3000 in browser
- Verify dashboard loads correctly
- Test tab navigation

### Streamlit Setup

#### Step 1: Install Dependencies
```bash
cd streamlit
pip install -r requirements.txt
```

#### Step 2: Run Streamlit
```bash
streamlit run app.py --server.port 8501 --server.address 0.0.0.0
```

#### Step 3: Test Streamlit
- Open http://localhost:8501 in browser
- Test navigation between tabs
- Verify data visualization

### Jupyter Setup

#### Step 1: Install Jupyter
```bash
pip install jupyterlab ipykernel
```

#### Step 2: Setup Kernel
```bash
python -m ipykernel install --user --name watchtower_env --display-name "Watchtower"
```

#### Step 3: Run Jupyter
```bash
cd notebooks
jupyter lab --ip 0.0.0.0 --port 8888 --no-browser --allow-root
```

#### Step 4: Test Jupyter
- Open http://localhost:8888 in browser
- Enter token: watchtower
- Open sensor_analysis.ipynb notebook

## 🐳 Docker Configuration

### Custom Docker Compose

Create custom `docker-compose.override.yml` for development:

```yaml
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

  streamlit:
    volumes:
      - ./streamlit:/app
    environment:
      - STREAMLIT_SERVER_HEADLESS=false

  jupyter:
    volumes:
      - ./notebooks:/home/jovyan/work
    environment:
      - JUPYTER_ENABLE_LAB=yes
```

### Production Configuration

Create `docker-compose.prod.yml`:

```yaml
version: '3.8'

services:
  backend:
    environment:
      - ENVIRONMENT=production
    restart: unless-stopped

  frontend:
    environment:
      - NODE_ENV=production
    restart: unless-stopped

  streamlit:
    restart: unless-stopped

  jupyter:
    restart: unless-stopped
```

## 🔧 Configuration

### Environment Variables

#### Backend (.env)
```bash
ENVIRONMENT=development
DEBUG=true
API_HOST=0.0.0.0
API_PORT=8000
CORS_ORIGINS=http://localhost:3000,http://localhost:8501
```

#### Frontend (.env.local)
```bash
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_WS_URL=ws://localhost:8000
NODE_ENV=development
```

#### Streamlit (.streamlit/config.toml)
```toml
[server]
port = 8501
address = "0.0.0.0"
headless = true

[browser]
gatherUsageStats = false
```

### Port Configuration

Default ports (can be changed in docker-compose.yml):
- **Backend**: 8000
- **Frontend**: 3000
- **Streamlit**: 8501
- **Jupyter**: 8888

## 🧪 Testing Setup

### Backend Testing
```bash
cd backend
pip install pytest pytest-asyncio
pytest tests/
```

### Frontend Testing
```bash
cd frontend
npm test
npm run test:watch
```

### Integration Testing
```bash
# Test API endpoints
curl -X GET http://localhost:8000/health
curl -X GET http://localhost:8000/api/sensors/status
curl -X GET http://localhost:8000/api/dashboard/tabs

# Test WebSocket connection
# Use WebSocket client or browser console
```

## 🔍 Troubleshooting

### Common Issues

#### 1. Port Conflicts
```bash
# Check port usage
netstat -tulpn | grep :8000
netstat -tulpn | grep :3000

# Kill processes using ports
sudo kill -9 <PID>
```

#### 2. Docker Build Failures
```bash
# Clean Docker cache
docker system prune -a

# Rebuild without cache
docker-compose build --no-cache
```

#### 3. Permission Issues
```bash
# Fix file permissions
sudo chown -R $USER:$USER .

# Fix Docker permissions
sudo usermod -aG docker $USER
```

#### 4. Network Issues
```bash
# Check Docker network
docker network ls
docker network inspect dashboards_watchtower-network

# Restart Docker
sudo systemctl restart docker
```

### Debug Commands

#### Docker Debugging
```bash
# View service logs
docker-compose logs backend
docker-compose logs frontend

# Access container shell
docker-compose exec backend bash
docker-compose exec frontend sh

# Check service status
docker-compose ps
```

#### Application Debugging
```bash
# Backend debugging
cd backend
python -m pdb main.py

# Frontend debugging
cd frontend
npm run dev -- --inspect
```

## 📊 Monitoring

### Health Checks
```bash
# Backend health
curl http://localhost:8000/health

# Frontend health
curl http://localhost:3000

# Streamlit health
curl http://localhost:8501/_stcore/health

# Jupyter health
curl http://localhost:8888/api/status
```

### Log Monitoring
```bash
# View all logs
docker-compose logs -f

# View specific service logs
docker-compose logs -f backend
docker-compose logs -f frontend
```

### Performance Monitoring
```bash
# Check resource usage
docker stats

# Monitor API performance
curl -w "@curl-format.txt" -o /dev/null -s http://localhost:8000/health
```

## 🔒 Security Configuration

### Development Security
```bash
# Generate secure tokens
openssl rand -hex 32

# Set secure environment variables
export JWT_SECRET_KEY=$(openssl rand -hex 32)
export API_KEY=$(openssl rand -hex 16)
```

### Production Security
```bash
# Use HTTPS in production
# Configure SSL certificates
# Set up proper CORS origins
# Implement rate limiting
```

## 📚 Additional Resources

### Documentation
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Next.js Documentation](https://nextjs.org/docs)
- [Streamlit Documentation](https://docs.streamlit.io/)
- [Jupyter Documentation](https://jupyter.org/documentation)

### Community Support
- [GitHub Issues](https://github.com/your-repo/issues)
- [Discord Community](https://discord.gg/your-community)
- [Stack Overflow](https://stackoverflow.com/questions/tagged/watchtower)

---

**Next Steps**: After successful setup, proceed to the [User Guide](USER_GUIDE.md) for detailed usage instructions.
