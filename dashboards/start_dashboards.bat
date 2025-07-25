@echo off
setlocal enabledelayedexpansion

echo ========================================
echo Watchtower Dashboard Startup Script
echo ========================================
echo.

:: Check if we're in the correct directory
if not exist "docker-compose.yml" (
    echo ERROR: docker-compose.yml not found!
    echo Please run this script from the dashboards directory.
    echo.
    pause
    exit /b 1
)

:: Check if Docker Desktop is installed
docker --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Docker is not installed or not in PATH!
    echo Please install Docker Desktop from https://www.docker.com/products/docker-desktop
    echo.
    pause
    exit /b 1
)

echo ✓ Docker is installed
echo.

:: Check if Docker Desktop is running
echo Checking if Docker Desktop is running...
docker info >nul 2>&1
if %errorlevel% neq 0 (
    echo Docker Desktop is not running. Starting it now...
    echo.
    echo Please wait while Docker Desktop starts up...
    echo This may take a minute or two on first startup.
    echo.
    
    :: Try to start Docker Desktop
    start "" "C:\Program Files\Docker\Docker\Docker Desktop.exe"
    
    :: Wait for Docker to be ready
    echo Waiting for Docker to be ready...
    :wait_for_docker
    timeout /t 5 /nobreak >nul
    docker info >nul 2>&1
    if %errorlevel% neq 0 (
        echo Still waiting for Docker to start...
        goto wait_for_docker
    )
    echo ✓ Docker Desktop is now running
) else (
    echo ✓ Docker Desktop is already running
)

echo.

:: Check if containers are already running
echo Checking current container status...
docker-compose ps --services --filter "status=running" | findstr /c:"backend" /c:"frontend" /c:"streamlit" /c:"jupyter" >nul
if %errorlevel% equ 0 (
    echo Some containers are already running.
    echo.
    set /p choice="Do you want to restart all containers? (y/N): "
    if /i "!choice!"=="y" (
        echo Stopping existing containers...
        docker-compose down
        echo.
    ) else (
        echo Keeping existing containers running.
        echo.
        goto show_status
    )
)

:: Build and start containers
echo Building and starting all dashboard containers...
echo This may take several minutes on first run.
echo.

docker-compose up --build -d

if %errorlevel% neq 0 (
    echo.
    echo ERROR: Failed to start containers!
    echo Please check the error messages above.
    echo.
    pause
    exit /b 1
)

echo.
echo ✓ All containers started successfully!
echo.

:show_status
:: Show container status
echo Current container status:
docker-compose ps
echo.

:: Wait a moment for services to fully start
echo Waiting for services to be ready...
timeout /t 10 /nobreak >nul

:: Show service URLs
echo ========================================
echo Dashboard Services Available At:
echo ========================================
echo.
echo Frontend Dashboard:    http://localhost:3000
echo Backend API:          http://localhost:8000
echo API Documentation:     http://localhost:8000/docs
echo Streamlit Dashboard:   http://localhost:8501
echo Jupyter Lab:          http://localhost:8888 (token: watchtower)
echo.
echo ========================================
echo.

:: Check if services are responding
echo Checking service health...
echo.

:: Check backend
echo Checking backend API...
curl -f http://localhost:8000/health >nul 2>&1
if %errorlevel% equ 0 (
    echo ✓ Backend API is responding
) else (
    echo ⚠ Backend API may still be starting up
)

:: Check frontend
echo Checking frontend...
curl -f http://localhost:3000 >nul 2>&1
if %errorlevel% equ 0 (
    echo ✓ Frontend is responding
) else (
    echo ⚠ Frontend may still be starting up
)

:: Check streamlit
echo Checking streamlit...
curl -f http://localhost:8501/_stcore/health >nul 2>&1
if %errorlevel% equ 0 (
    echo ✓ Streamlit is responding
) else (
    echo ⚠ Streamlit may still be starting up
)

echo.
echo ========================================
echo Setup Complete!
echo ========================================
echo.
echo If any services show as "starting up", please wait a few more minutes
echo and refresh your browser. The services may take time to fully initialize.
echo.
echo To stop all containers, run: docker-compose down
echo To view logs, run: docker-compose logs -f
echo.
pause 