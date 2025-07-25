@echo off
setlocal enabledelayedexpansion

echo ========================================
echo Frontend Build Debug Script
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

echo This script will build the frontend with detailed output to debug the issue.
echo.

:: Stop frontend container if running
echo Step 1: Stopping frontend container...
docker-compose stop frontend
docker-compose rm -f frontend
echo.

:: Remove frontend image
echo Step 2: Removing frontend image...
docker rmi dashboards_frontend 2>nul
echo.

:: Build with detailed output
echo Step 3: Building frontend with detailed output...
echo This will show all build steps and any errors...
echo.

docker-compose build --no-cache --progress=plain frontend

echo.
echo ========================================
echo Build completed. Checking results...
echo ========================================
echo.

:: Check if container starts
echo Step 4: Starting container to test...
docker-compose up frontend -d

:: Wait a moment
timeout /t 5 /nobreak >nul

:: Check container status
echo Step 5: Checking container status...
docker-compose ps frontend
echo.

:: Check if .next directory exists in container
echo Step 6: Checking if build files exist in container...
docker-compose exec frontend ls -la .next 2>nul || echo "Cannot exec into container - checking logs instead"
echo.

:: Show recent logs
echo Step 7: Recent container logs...
docker-compose logs --tail=10 frontend
echo.

:: Test if frontend responds
echo Step 8: Testing frontend accessibility...
curl -f http://localhost:3000 >nul 2>&1
if %errorlevel% equ 0 (
    echo ✓ Frontend is responding at http://localhost:3000
) else (
    echo ❌ Frontend is not responding
    echo.
    echo Let's check the detailed logs...
    docker-compose logs frontend
)

echo.
echo ========================================
echo Debug Complete!
echo ========================================
echo.
pause 