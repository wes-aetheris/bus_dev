'use client'

import { Battery, Clock, Thermometer, Wind, Compass, Wifi } from 'lucide-react'

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

interface MissionStatusBarProps {
  status: MissionStatus
}

export default function MissionStatusBar({ status }: MissionStatusBarProps) {
  const formatTime = (seconds: number) => {
    const hours = Math.floor(seconds / 3600)
    const minutes = Math.floor((seconds % 3600) / 60)
    return `${hours.toString().padStart(2, '0')}:${minutes.toString().padStart(2, '0')}`
  }

  const getBatteryColor = (battery: number) => {
    if (battery >= 60) return 'text-success-400'
    if (battery >= 30) return 'text-warning-400'
    return 'text-danger-400'
  }

  const getSignalColor = (signal: number) => {
    if (signal >= 80) return 'text-success-400'
    if (signal >= 60) return 'text-warning-400'
    return 'text-danger-400'
  }

  return (
    <div className="mission-status-bar">
      <div className="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-6 gap-4">
        {/* Altitude */}
        <div className="flex items-center space-x-2">
          <Compass className="w-5 h-5 text-primary-400" />
          <div>
            <p className="text-sm text-dark-400">Altitude</p>
            <p className="font-semibold text-white">{status.altitude.toFixed(1)}m</p>
          </div>
        </div>

        {/* Speed */}
        <div className="flex items-center space-x-2">
          <Wind className="w-5 h-5 text-blue-400" />
          <div>
            <p className="text-sm text-dark-400">Speed</p>
            <p className="font-semibold text-white">{status.speed.toFixed(1)}m/s</p>
          </div>
        </div>

        {/* Battery */}
        <div className="flex items-center space-x-2">
          <Battery className="w-5 h-5 text-green-400" />
          <div>
            <p className="text-sm text-dark-400">Battery</p>
            <p className={`font-semibold ${getBatteryColor(status.battery)}`}>
              {status.battery.toFixed(1)}%
            </p>
          </div>
        </div>

        {/* Flight Time */}
        <div className="flex items-center space-x-2">
          <Clock className="w-5 h-5 text-purple-400" />
          <div>
            <p className="text-sm text-dark-400">Flight Time</p>
            <p className="font-semibold text-white">{formatTime(status.flight_time)}</p>
          </div>
        </div>

        {/* GPS Signal */}
        <div className="flex items-center space-x-2">
          <Wifi className="w-5 h-5 text-orange-400" />
          <div>
            <p className="text-sm text-dark-400">GPS Signal</p>
            <p className={`font-semibold ${getSignalColor(status.signal_strength)}`}>
              {status.signal_strength.toFixed(0)}%
            </p>
          </div>
        </div>

        {/* Temperature */}
        <div className="flex items-center space-x-2">
          <Thermometer className="w-5 h-5 text-red-400" />
          <div>
            <p className="text-sm text-dark-400">Temperature</p>
            <p className="font-semibold text-white">{status.temperature.toFixed(1)}°C</p>
          </div>
        </div>
      </div>

      {/* Mission Phase */}
      <div className="mt-4 pt-4 border-t border-dark-600">
        <div className="flex items-center justify-between">
          <div>
            <p className="text-sm text-dark-400">Mission Phase</p>
            <p className="font-semibold text-white capitalize">{status.mission_phase}</p>
          </div>
          <div className="flex items-center space-x-4 text-sm">
            <div>
              <span className="text-dark-400">GPS Satellites: </span>
              <span className="text-white">{status.gps_satellites}</span>
            </div>
            <div>
              <span className="text-dark-400">Humidity: </span>
              <span className="text-white">{status.humidity.toFixed(1)}%</span>
            </div>
            <div>
              <span className="text-dark-400">Wind: </span>
              <span className="text-white">{status.wind_speed.toFixed(1)}m/s</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
} 