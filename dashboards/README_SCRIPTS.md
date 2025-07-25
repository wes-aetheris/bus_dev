# Dashboard Container Management Scripts

This document explains how to use the automated scripts to start and stop the Watchtower Dashboard containers with **physics-informed sensor intelligence**.

## 📋 Prerequisites

Before using these scripts, ensure you have:

- **Windows 10/11** operating system
- **Docker Desktop** installed and configured
- **Git** (for cloning the repository)
- **PowerShell** or **Command Prompt**

## 🚀 Quick Start

### Starting the Dashboards

1. **Navigate to the dashboards directory:**
   ```cmd
   cd dashboards
   ```

2. **Run the startup script:**
   ```cmd
   start_dashboards.bat
   ```

3. **Wait for the script to complete** - it will:
   - Check if Docker Desktop is running
   - Start Docker Desktop if needed
   - Build and start all containers
   - Verify services are responding
   - Display access URLs

### Stopping the Dashboards

1. **Navigate to the dashboards directory:**
   ```cmd
   cd dashboards
   ```

2. **Run the stop script:**
   ```cmd
   stop_dashboards.bat
   ```

3. **Confirm the action** when prompted

## 📊 Available Services

Once started, you can access these services:

| Service | URL | Description |
|---------|-----|-------------|
| **Frontend Dashboard** | http://localhost:3000 | Main React/Next.js dashboard with sensor intelligence widgets |
| **Backend API** | http://localhost:8000 | FastAPI backend service with physics engine |
| **API Documentation** | http://localhost:8000/docs | Interactive API docs (Swagger) |
| **Streamlit Dashboard** | http://localhost:8501 | Data visualization dashboard |
| **Jupyter Lab** | http://localhost:8888 | Jupyter notebooks (token: `watchtower`) |

## 🧠 New Sensor Intelligence Features

The dashboard now includes advanced sensor intelligence capabilities:

### Mission Capability Assessment
- **Real-time capability scoring** with physics-informed calculations
- **Trend analysis** showing improving/degrading/stable performance
- **Confidence metrics** for prediction reliability
- **30-minute projections** for mission planning

### Sensor Health Monitoring
- **Current health percentages** with color-coded status indicators
- **1-hour health predictions** using degradation modeling
- **Degradation rate analysis** (%/hour trends)
- **Threshold management** (optimal/warning/critical levels)

### Widget System
- **Responsive grid layout** for flexible dashboard organization
- **Real-time data updates** via WebSocket connections
- **Status indicators** with color-coded alerts
- **Refresh functionality** for manual data updates

## 🔧 Script Details

### `start_dashboards.bat`

This script performs the following operations:

1. **Environment Check**
   - Verifies you're in the correct directory
   - Checks if Docker is installed
   - Ensures `docker-compose.yml` exists

2. **Docker Desktop Management**
   - Checks if Docker Desktop is running
   - Automatically starts Docker Desktop if needed
   - Waits for Docker to be ready

3. **Container Management**
   - Checks for existing running containers
   - Offers to restart containers if already running
   - Builds and starts all services in detached mode

4. **Health Verification**
   - Tests backend API health endpoint
   - Checks frontend accessibility
   - Verifies Streamlit service
   - Reports service status

5. **User Information**
   - Displays all service URLs
   - Shows container status
   - Provides helpful commands

### `stop_dashboards.bat`

This script performs the following operations:

1. **Environment Check**
   - Verifies you're in the correct directory
   - Checks if Docker is available

2. **Status Check**
   - Shows current container status
   - Checks if any containers are running

3. **Safe Shutdown**
   - Asks for confirmation before stopping
   - Gracefully stops all containers
   - Shows final status

## 🛠️ Troubleshooting

### Common Issues

#### Docker Desktop Not Starting
```
ERROR: Docker is not installed or not in PATH!
```
**Solution:** Install Docker Desktop from https://www.docker.com/products/docker-desktop

#### Containers Fail to Start
```
ERROR: Failed to start containers!
```
**Solutions:**
1. Check if ports 3000, 8000, 8501, or 8888 are already in use
2. Ensure Docker Desktop has enough resources allocated
3. Try running `docker-compose down` first, then restart

#### Services Not Responding
If services show as "starting up" for too long:
1. Wait a few more minutes for full initialization
2. Check logs: `docker-compose logs -f`
3. Restart specific service: `docker-compose restart [service-name]`

#### Sensor Intelligence Widgets Not Loading
If the new sensor intelligence widgets don't appear:
1. Clear browser cache (Ctrl+Shift+R)
2. Check browser console for errors (F12)
3. Verify the frontend container built successfully
4. Check that mock data is being loaded correctly

### Manual Commands

If the scripts don't work, you can run these commands manually:

```cmd
# Start all services
docker-compose up --build -d

# Stop all services
docker-compose down

# View logs
docker-compose logs -f

# Restart specific service
docker-compose restart backend

# Check status
docker-compose ps

# Rebuild frontend with new sensor intelligence features
docker-compose up --build frontend
```

## 📝 Script Output Examples

### Successful Startup
```
========================================
Watchtower Dashboard Startup Script
========================================

✓ Docker is installed

Checking if Docker Desktop is running...
✓ Docker Desktop is already running

Building and starting all dashboard containers...
This may take several minutes on first run.

✓ All containers started successfully!

Current container status:
Name                    Command               State           Ports
--------------------------------------------------------------------------------
dashboards_backend_1   uvicorn main:app ... Up      0.0.0.0:8000->8000/tcp
dashboards_frontend_1  npm run dev          Up      0.0.0.0:3000->3000/tcp
dashboards_jupyter_1   tini -- jupyter ...  Up      0.0.0.0:8888->8888/tcp
dashboards_streamlit_1 streamlit run app.py Up      0.0.0.0:8501->8501/tcp

========================================
Dashboard Services Available At:
========================================

Frontend Dashboard:    http://localhost:3000
Backend API:          http://localhost:8000
API Documentation:     http://localhost:8000/docs
Streamlit Dashboard:   http://localhost:8501
Jupyter Lab:          http://localhost:8888 (token: watchtower)

========================================

Checking service health...

Checking backend API...
✓ Backend API is responding
Checking frontend...
✓ Frontend is responding
Checking streamlit...
✓ Streamlit is responding

========================================
Setup Complete!
========================================

New Features Available:
- Sensor Intelligence Dashboard with physics-informed widgets
- Mission Capability Assessment with real-time scoring
- Sensor Health Monitoring with predictive analytics
- Responsive widget grid system
```

### Successful Shutdown
```
========================================
Watchtower Dashboard Stop Script
========================================

Checking current container status...
Current container status:
Name                    Command               State           Ports
--------------------------------------------------------------------------------
dashboards_backend_1   uvicorn main:app ... Up      0.0.0.0:8000->8000/tcp
dashboards_frontend_1  npm run dev          Up      0.0.0.0:3000->3000/tcp
dashboards_jupyter_1   tini -- jupyter ...  Up      0.0.0.0:8888->8888/tcp
dashboards_streamlit_1 streamlit run app.py Up      0.0.0.0:8501->8501/tcp

Do you want to stop all dashboard containers? (y/N): y

Stopping all dashboard containers...
Stopping dashboards_streamlit_1 ... done
Stopping dashboards_jupyter_1   ... done
Stopping dashboards_frontend_1  ... done
Stopping dashboards_backend_1   ... done
Removing dashboards_streamlit_1 ... done
Removing dashboards_jupyter_1   ... done
Removing dashboards_frontend_1  ... done
Removing dashboards_backend_1   ... done
Removing network dashboards_watchtower-network

✓ All containers stopped successfully!

Container status after stopping:
Name   Command   State   Ports
----   -------   -----   -----
```

## 🔄 Development Workflow

### Typical Development Session

1. **Start development:**
   ```cmd
   start_dashboards.bat
   ```

2. **Access services:**
   - Open http://localhost:3000 for frontend development
   - Navigate to "Sensor Intelligence" tab for new widgets
   - Use http://localhost:8000/docs for API testing
   - Access http://localhost:8501 for data analysis
   - Use http://localhost:8888 for notebook work

3. **Stop when done:**
   ```cmd
   stop_dashboards.bat
   ```

### Continuous Development

The containers are configured with volume mounts, so code changes will automatically reload:
- **Frontend**: Changes to `frontend/` files auto-reload
- **Backend**: Changes to `backend/` files auto-reload (with uvicorn --reload)
- **Streamlit**: Changes to `streamlit/` files auto-reload

### Sensor Intelligence Development

For developing new sensor intelligence widgets:
1. Add new widget components to `frontend/src/components/dashboard/widgets/`
2. Update mock data in `frontend/src/data/mockSensorData.ts`
3. Add new API endpoints in the backend
4. Test with the existing widget grid system

## 📚 Additional Resources

- **Main Setup Guide**: See `SETUP.md` for detailed installation instructions
- **Troubleshooting**: See `TROUBLESHOOTING.md` for common issues
- **Project Documentation**: See `README.md` for project overview
- **API Documentation**: http://localhost:8000/docs (when running)
- **Sensor Intelligence Guide**: See the main README.md for widget documentation

## 🤝 Contributing

If you encounter issues with these scripts:

1. Check the troubleshooting section above
2. Review the logs: `docker-compose logs -f`
3. Try manual commands to isolate the issue
4. Report bugs with the full script output and error messages 