# Watchtower Dashboard Test Script
Write-Host "🚁 Testing Watchtower Dashboard..." -ForegroundColor Green
Write-Host "=" * 50

# Wait for containers to start
Write-Host "Waiting for services to start..." -ForegroundColor Yellow
Start-Sleep -Seconds 10

# Test API endpoints
$baseUrl = "http://localhost:8000"

try {
    # Test health endpoint
    $response = Invoke-RestMethod -Uri "$baseUrl/api/health" -Method Get
    Write-Host "✅ Health check passed" -ForegroundColor Green
    Write-Host "   Status: $($response.status)" -ForegroundColor Cyan
    Write-Host "   Services: $($response.services -join ', ')" -ForegroundColor Cyan
} catch {
    Write-Host "❌ Health check failed: $($_.Exception.Message)" -ForegroundColor Red
}

try {
    # Test sensors endpoint
    $response = Invoke-RestMethod -Uri "$baseUrl/api/sensors" -Method Get
    Write-Host "✅ Sensors endpoint working" -ForegroundColor Green
    $sensors = $response.sensors
    Write-Host "   Found $($sensors.Count) sensors:" -ForegroundColor Cyan
    foreach ($sensor in $sensors) {
        Write-Host "   - $($sensor.name): $($sensor.health)% health" -ForegroundColor White
    }
} catch {
    Write-Host "❌ Sensors endpoint failed: $($_.Exception.Message)" -ForegroundColor Red
}

try {
    # Test mission status
    $response = Invoke-RestMethod -Uri "$baseUrl/api/mission-status" -Method Get
    Write-Host "✅ Mission status working" -ForegroundColor Green
    Write-Host "   Altitude: $($response.altitude)m" -ForegroundColor Cyan
    Write-Host "   Speed: $($response.speed)m/s" -ForegroundColor Cyan
    Write-Host "   Battery: $($response.battery)%" -ForegroundColor Cyan
} catch {
    Write-Host "❌ Mission status failed: $($_.Exception.Message)" -ForegroundColor Red
}

Write-Host ""
Write-Host "=" * 50 -ForegroundColor Green
Write-Host "🎯 Dashboard URLs:" -ForegroundColor Green
Write-Host ""
Write-Host "Frontend Dashboard: http://localhost:3000" -ForegroundColor Yellow
Write-Host "Streamlit Dashboard: http://localhost:8501" -ForegroundColor Yellow
Write-Host "API Documentation: http://localhost:8000/docs" -ForegroundColor Yellow
Write-Host "Jupyter Notebook: http://localhost:8888 (token: watchtower)" -ForegroundColor Yellow
Write-Host ""
Write-Host "Press any key to open the frontend dashboard..." -ForegroundColor Cyan
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")

# Open the frontend dashboard
Start-Process "http://localhost:3000" 