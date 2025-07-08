@echo off
echo Starting Watchtower Dashboard...
echo.

echo Building and starting all services...
docker-compose up --build

echo.
echo Dashboard should be available at:
echo - Frontend: http://localhost:3000
echo - Streamlit: http://localhost:8501
echo - Backend API: http://localhost:8000
echo - Jupyter: http://localhost:8888 (token: watchtower)
echo.
pause 