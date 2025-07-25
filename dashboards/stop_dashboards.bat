@echo off
setlocal enabledelayedexpansion

echo ========================================
echo Watchtower Dashboard Stop Script
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

:: Check if Docker is available
docker --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Docker is not installed or not in PATH!
    echo.
    pause
    exit /b 1
)

:: Check if containers are running
echo Checking current container status...
docker-compose ps --services --filter "status=running" | findstr /c:"backend" /c:"frontend" /c:"streamlit" /c:"jupyter" >nul
if %errorlevel% neq 0 (
    echo No dashboard containers are currently running.
    echo.
    pause
    exit /b 0
)

:: Show current status
echo Current container status:
docker-compose ps
echo.

:: Ask for confirmation
set /p choice="Do you want to stop all dashboard containers? (y/N): "
if /i "!choice!"=="y" (
    echo.
    echo Stopping all dashboard containers...
    docker-compose down
    
    if %errorlevel% equ 0 (
        echo.
        echo ✓ All containers stopped successfully!
        echo.
        echo Container status after stopping:
        docker-compose ps
    ) else (
        echo.
        echo ERROR: Failed to stop containers!
        echo Please check the error messages above.
    )
) else (
    echo.
    echo Operation cancelled. Containers remain running.
)

echo.
pause 