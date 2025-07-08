'use client'

import { useState, useEffect } from 'react'
import { 
  Activity, 
  AlertTriangle, 
  BarChart3, 
  Camera, 
  Compass, 
  Download, 
  Gauge, 
  Globe, 
  Upload, 
  Wifi, 
  Zap,
  Battery,
  Clock,
  Thermometer,
  Wind
} from 'lucide-react'
import SensorHealthGauge from './components/SensorHealthGauge'
import MissionStatusBar from './components/MissionStatusBar'
import CorrelationMatrix from './components/CorrelationMatrix'
import AlertPanel from './components/AlertPanel'
import PhysicsModelCard from './components/PhysicsModelCard'
import DataUpload from './components/DataUpload'

interface Sensor {
  id: string
  name: string
  type: string
  health: number
  degradation_rate: number
  last_calibration: string
  next_calibration: string
}

interface MissionStatus {
  altitude: number
  speed: number
  battery: number
  flight_time: number
  mission_phase: string
  gps_satellites: number
  signal_strength: number
  temperature: number
  humidity: number
  wind_speed: number
}

interface Alert {
  id: number
  sensor_id: string
  severity: string
  message: string
  timestamp: string
  acknowledged: boolean
  physics_model_triggered: boolean
}

export default function Dashboard() {
  const [sensors, setSensors] = useState<Sensor[]>([])
  const [missionStatus, setMissionStatus] = useState<MissionStatus | null>(null)
  const [alerts, setAlerts] = useState<Alert[]>([])
  const [correlationMatrix, setCorrelationMatrix] = useState<any>(null)
  const [isConnected, setIsConnected] = useState(false)

  // Fetch initial data
  useEffect(() => {
    fetchSensors()
    fetchMissionStatus()
    fetchAlerts()
    fetchCorrelationMatrix()
    setupWebSocket()
  }, [])

  const fetchSensors = async () => {
    try {
      const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/sensors`)
      const data = await response.json()
      setSensors(data.sensors)
    } catch (error) {
      console.error('Error fetching sensors:', error)
    }
  }

  const fetchMissionStatus = async () => {
    try {
      const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/mission-status`)
      const data = await response.json()
      setMissionStatus(data)
    } catch (error) {
      console.error('Error fetching mission status:', error)
    }
  }

  const fetchAlerts = async () => {
    try {
      const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/alerts`)
      const data = await response.json()
      setAlerts(data.alerts)
    } catch (error) {
      console.error('Error fetching alerts:', error)
    }
  }

  const fetchCorrelationMatrix = async () => {
    try {
      const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/correlation-matrix`)
      const data = await response.json()
      setCorrelationMatrix(data)
    } catch (error) {
      console.error('Error fetching correlation matrix:', error)
    }
  }

  const setupWebSocket = () => {
    const ws = new WebSocket(process.env.NEXT_PUBLIC_WEBSOCKET_URL || 'ws://localhost:8001')
    
    ws.onopen = () => {
      setIsConnected(true)
      console.log('WebSocket connected')
    }
    
    ws.onmessage = (event) => {
      const data = JSON.parse(event.data)
      
      switch (data.type) {
        case 'sensor_update':
          setSensors(data.data.sensors)
          break
        case 'mission_status':
          setMissionStatus(data.data)
          break
        case 'alert':
          setAlerts(prev => [data.data, ...prev])
          break
      }
    }
    
    ws.onclose = () => {
      setIsConnected(false)
      console.log('WebSocket disconnected')
      // Reconnect after 5 seconds
      setTimeout(setupWebSocket, 5000)
    }
    
    ws.onerror = (error) => {
      console.error('WebSocket error:', error)
      setIsConnected(false)
    }
  }

  const getSensorIcon = (sensorType: string) => {
    switch (sensorType) {
      case 'thermal':
        return <Camera className="w-6 h-6 text-orange-400" />
      case 'navigation':
        return <Compass className="w-6 h-6 text-blue-400" />
      case 'environmental':
        return <Thermometer className="w-6 h-6 text-green-400" />
      default:
        return <Activity className="w-6 h-6 text-gray-400" />
    }
  }

  const getHealthColor = (health: number) => {
    if (health >= 80) return 'text-success-400'
    if (health >= 60) return 'text-warning-400'
    return 'text-danger-400'
  }

  return (
    <div className="min-h-screen bg-dark-950 text-white">
      {/* Header */}
      <header className="bg-dark-900/50 backdrop-blur-sm border-b border-dark-700 p-4">
        <div className="max-w-7xl mx-auto flex items-center justify-between">
          <div className="flex items-center space-x-4">
            <div className="flex items-center space-x-2">
              <div className="w-8 h-8 bg-gradient-to-r from-primary-500 to-secondary-500 rounded-lg flex items-center justify-center">
                <Zap className="w-5 h-5 text-white" />
              </div>
              <h1 className="text-2xl font-bold text-gradient">Watchtower</h1>
            </div>
            <div className="text-sm text-dark-400">Physics-Informed Sensor Monitoring</div>
          </div>
          
          <div className="flex items-center space-x-4">
            <div className={`flex items-center space-x-2 px-3 py-1 rounded-full text-sm ${
              isConnected ? 'bg-success-900 text-success-200' : 'bg-danger-900 text-danger-200'
            }`}>
              <div className={`w-2 h-2 rounded-full ${isConnected ? 'bg-success-400' : 'bg-danger-400'}`} />
              {isConnected ? 'Connected' : 'Disconnected'}
            </div>
            <button className="p-2 hover:bg-dark-700 rounded-lg transition-colors">
              <Download className="w-5 h-5" />
            </button>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto p-6 space-y-6">
        {/* Mission Status Bar */}
        {missionStatus && (
          <MissionStatusBar status={missionStatus} />
        )}

        {/* Sensor Health Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          {sensors.map((sensor) => (
            <div key={sensor.id} className="sensor-card">
              <div className="flex items-center justify-between mb-4">
                <div className="flex items-center space-x-3">
                  {getSensorIcon(sensor.type)}
                  <div>
                    <h3 className="font-semibold text-white">{sensor.name}</h3>
                    <p className="text-sm text-dark-400 capitalize">{sensor.type}</p>
                  </div>
                </div>
                <div className={`status-indicator ${
                  sensor.health >= 80 ? 'status-healthy' : 
                  sensor.health >= 60 ? 'status-warning' : 'status-critical'
                }`} />
              </div>
              
              <SensorHealthGauge health={sensor.health} />
              
              <div className="mt-4 space-y-2 text-sm">
                <div className="flex justify-between">
                  <span className="text-dark-400">Degradation Rate:</span>
                  <span className={getHealthColor(sensor.health)}>
                    {(sensor.degradation_rate * 100).toFixed(1)}%/hr
                  </span>
                </div>
                <div className="flex justify-between">
                  <span className="text-dark-400">Last Calibration:</span>
                  <span className="text-white">
                    {new Date(sensor.last_calibration).toLocaleDateString()}
                  </span>
                </div>
              </div>
            </div>
          ))}
        </div>

        {/* Analytics Section */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {/* Correlation Matrix */}
          <div className="correlation-heatmap">
            <div className="flex items-center space-x-2 mb-4">
              <BarChart3 className="w-5 h-5 text-primary-400" />
              <h3 className="font-semibold">Cross-Sensor Correlation</h3>
            </div>
            {correlationMatrix && (
              <CorrelationMatrix data={correlationMatrix} />
            )}
          </div>

          {/* Physics Models */}
          <div className="space-y-4">
            <div className="flex items-center space-x-2 mb-4">
              <Zap className="w-5 h-5 text-secondary-400" />
              <h3 className="font-semibold">Physics Models</h3>
            </div>
            <div className="grid grid-cols-1 gap-4">
              <PhysicsModelCard 
                title="Thermal Camera"
                model="Arrhenius Degradation"
                description="Dark current doubling every 6-8°C"
                health={sensors.find(s => s.id === 'thermal_camera')?.health || 0}
              />
              <PhysicsModelCard 
                title="GPS Module"
                model="EMI Correlation"
                description="Signal degradation from electromagnetic interference"
                health={sensors.find(s => s.id === 'gps')?.health || 0}
              />
              <PhysicsModelCard 
                title="IMU"
                model="Vibration-Induced Bias Drift"
                description="Bias drift from mechanical vibration"
                health={sensors.find(s => s.id === 'imu')?.health || 0}
              />
            </div>
          </div>
        </div>

        {/* Alerts and Data Upload */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          <AlertPanel alerts={alerts} />
          <DataUpload />
        </div>
      </main>
    </div>
  )
} 