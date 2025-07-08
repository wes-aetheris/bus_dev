'use client'

import { AlertTriangle, CheckCircle, Clock } from 'lucide-react'

interface Alert {
  id: number
  sensor_id: string
  severity: string
  message: string
  timestamp: string
  acknowledged: boolean
  physics_model_triggered: boolean
}

interface AlertPanelProps {
  alerts: Alert[]
}

export default function AlertPanel({ alerts }: AlertPanelProps) {
  const getSeverityColor = (severity: string) => {
    switch (severity) {
      case 'critical':
        return 'alert-critical'
      case 'high':
        return 'alert-high'
      case 'medium':
        return 'alert-medium'
      case 'low':
        return 'alert-low'
      default:
        return 'alert-low'
    }
  }

  const getSeverityIcon = (severity: string) => {
    switch (severity) {
      case 'critical':
        return <AlertTriangle className="w-4 h-4 text-danger-400" />
      case 'high':
        return <AlertTriangle className="w-4 h-4 text-warning-400" />
      default:
        return <AlertTriangle className="w-4 h-4 text-primary-400" />
    }
  }

  const formatTimestamp = (timestamp: string) => {
    return new Date(timestamp).toLocaleTimeString()
  }

  return (
    <div className="card">
      <div className="flex items-center space-x-2 mb-4">
        <AlertTriangle className="w-5 h-5 text-warning-400" />
        <h3 className="font-semibold">Alerts & Notifications</h3>
        <span className="alert-badge alert-high">{alerts.length}</span>
      </div>

      <div className="space-y-3 max-h-64 overflow-y-auto">
        {alerts.length === 0 ? (
          <div className="text-center py-8 text-dark-400">
            <CheckCircle className="w-8 h-8 mx-auto mb-2 text-success-400" />
            <p>No active alerts</p>
          </div>
        ) : (
          alerts.map((alert) => (
            <div
              key={alert.id}
              className={`p-3 rounded-lg border ${
                alert.acknowledged ? 'bg-dark-700/50 border-dark-600' : 'bg-dark-700 border-dark-500'
              }`}
            >
              <div className="flex items-start justify-between">
                <div className="flex items-start space-x-3 flex-1">
                  {getSeverityIcon(alert.severity)}
                  <div className="flex-1">
                    <div className="flex items-center space-x-2 mb-1">
                      <span className={`alert-badge ${getSeverityColor(alert.severity)}`}>
                        {alert.severity.toUpperCase()}
                      </span>
                      {alert.physics_model_triggered && (
                        <span className="text-xs text-secondary-400">Physics Model</span>
                      )}
                    </div>
                    <p className="text-sm text-white mb-1">{alert.message}</p>
                    <p className="text-xs text-dark-400">
                      Sensor: {alert.sensor_id.replace('_', ' ')}
                    </p>
                  </div>
                </div>
                <div className="flex items-center space-x-2 text-xs text-dark-400">
                  <Clock className="w-3 h-3" />
                  <span>{formatTimestamp(alert.timestamp)}</span>
                </div>
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  )
} 