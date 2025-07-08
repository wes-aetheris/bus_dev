# Watchtower Dashboard Troubleshooting Guide

## Common Issues and Solutions

### 1. Docker Daemon Not Running
**Error**: `Cannot connect to the Docker daemon`
**Solution**: 
- Start Docker Desktop
- Wait for Docker to fully initialize
- Run `docker ps` to verify it's working

### 2. Port Already in Use
**Error**: `Bind for 0.0.0.0:3000 failed: port is already allocated`
**Solution**:
- Check what's using the port: `netstat -ano | findstr :3000`
- Stop the process or change ports in `docker-compose.yml`

### 3. Build Failures
**Error**: `npm install` fails
**Solution**:
- Clear Docker cache: `docker system prune -a`
- Rebuild: `docker-compose up --build --force-recreate`

### 4. Frontend Not Loading
**Symptoms**: White screen or connection refused
**Solutions**:
- Check if backend is running: `http://localhost:8000/api/health`
- Check frontend logs: `docker-compose logs frontend`
- Verify WebSocket connection in browser console

### 5. Database Issues
**Error**: SQLite database not found
**Solution**:
- Check if `data/` directory exists
- Ensure proper file permissions
- Restart containers: `docker-compose restart`

### 6. Memory Issues
**Error**: Container killed due to memory
**Solution**:
- Increase Docker memory limit in Docker Desktop settings
- Close other applications
- Use `docker-compose down` then `docker-compose up`

## Quick Commands

```bash
# Check container status
docker-compose ps

# View logs
docker-compose logs backend
docker-compose logs frontend
docker-compose logs streamlit

# Restart specific service
docker-compose restart backend

# Full reset
docker-compose down -v
docker-compose up --build

# Test API
python test_api.py
# or
powershell -ExecutionPolicy Bypass -File test_api.ps1
```

## Health Check URLs

- **Backend API**: http://localhost:8000/api/health
- **Frontend**: http://localhost:3000
- **Streamlit**: http://localhost:8501
- **Jupyter**: http://localhost:8888 (token: watchtower)
- **API Docs**: http://localhost:8000/docs

## Performance Tips

1. **Close unused containers**: `docker-compose down` when not using
2. **Monitor resources**: Use Docker Desktop's resource monitor
3. **Clear cache**: `docker system prune` periodically
4. **Use volume mounts**: For development, mount source code as volumes

## Development Mode

For development, you can run services individually:

```bash
# Backend only
cd backend && uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Frontend only
cd frontend && npm run dev

# Streamlit only
cd streamlit && streamlit run app.py
```

## Data Persistence

- Sensor data is stored in `data/sensor_data.db`
- Uploaded files are stored in `data/uploads/`
- Jupyter notebooks are in `notebooks/`

## Support

If issues persist:
1. Check Docker Desktop logs
2. Verify system requirements
3. Try running services individually
4. Check firewall/antivirus settings 