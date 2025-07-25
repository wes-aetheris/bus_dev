import React from 'react'
import { BaseWidget } from './BaseWidget'
import { ProgressBar } from './ProgressBar'
import { TrendingDown, AlertTriangle, CheckCircle } from 'lucide-react'

export interface SensorHealthData {
  currentHealth: number // 0-100
  predictedHealth: number // 1-hour prediction
  degradationRate: number // %/hour
  thresholds: {
    optimal: number
    warning: number
    critical: number
  }
  sensors: {
    name: string
    health: number
    status: 'optimal' | 'good' | 'warning' | 'critical' | 'offline'
  }[]
}

export interface SensorHealthGaugeProps {
  data: SensorHealthData
  onRefresh?: () => void
  isLoading?: boolean
  lastUpdated?: Date
}

export const SensorHealthGauge: React.FC<SensorHealthGaugeProps> = ({
  data,
  onRefresh,
  isLoading = false,
  lastUpdated
}) => {
  const getStatusFromHealth = (health: number): 'optimal' | 'good' | 'warning' | 'critical' => {
    if (health >= data.thresholds.optimal) return 'optimal'
    if (health >= data.thresholds.warning) return 'good'
    if (health >= data.thresholds.critical) return 'warning'
    return 'critical'
  }

  const getDegradationColor = (rate: number) => {
    if (rate <= 2) return 'text-drone-green'
    if (rate <= 5) return 'text-drone-amber'
    return 'text-drone-red'
  }

  const getDegradationIcon = (rate: number) => {
    if (rate <= 2) return <CheckCircle className="w-4 h-4 text-drone-green" />
    if (rate <= 5) return <AlertTriangle className="w-4 h-4 text-drone-amber" />
    return <TrendingDown className="w-4 h-4 text-drone-red" />
  }

  return (
    <BaseWidget
      title="Sensor Health"
      icon="activity"
      status={getStatusFromHealth(data.currentHealth)}
      onRefresh={onRefresh}
      isLoading={isLoading}
      lastUpdated={lastUpdated}
      size="medium"
    >
      <div className="space-y-4">
        {/* Main Health Gauge */}
        <div className="space-y-2">
          <div className="flex items-center justify-between">
            <span className="text-drone-text-dim text-xs">Current Health</span>
            <span className="text-drone-text font-mono text-lg">
              {data.currentHealth.toFixed(1)}%
            </span>
          </div>
          <ProgressBar
            value={data.currentHealth}
            color={getStatusFromHealth(data.currentHealth) === 'optimal' ? 'green' : 
                   getStatusFromHealth(data.currentHealth) === 'good' ? 'blue' : 
                   getStatusFromHealth(data.currentHealth) === 'warning' ? 'amber' : 'red'}
            size="lg"
            showValue={false}
          />
        </div>

        {/* Prediction and Degradation */}
        <div className="grid grid-cols-2 gap-4">
          <div className="bg-drone-panel rounded p-3">
            <div className="text-drone-text-dim text-xs mb-1">1hr Prediction</div>
            <div className="text-drone-blue font-mono text-sm">
              {data.predictedHealth.toFixed(1)}%
            </div>
          </div>
          <div className="bg-drone-panel rounded p-3">
            <div className="text-drone-text-dim text-xs mb-1">Degradation</div>
            <div className="flex items-center space-x-1">
              {getDegradationIcon(data.degradationRate)}
              <span className={`font-mono text-sm ${getDegradationColor(data.degradationRate)}`}>
                {data.degradationRate.toFixed(1)}%/hr
              </span>
            </div>
          </div>
        </div>

        {/* Thresholds */}
        <div className="space-y-2">
          <div className="text-drone-text-dim text-xs font-medium">Thresholds</div>
          <div className="grid grid-cols-3 gap-2 text-xs">
            <div className="text-center">
              <div className="text-drone-green font-mono">{data.thresholds.optimal}%</div>
              <div className="text-drone-text-dim">Optimal</div>
            </div>
            <div className="text-center">
              <div className="text-drone-amber font-mono">{data.thresholds.warning}%</div>
              <div className="text-drone-text-dim">Warning</div>
            </div>
            <div className="text-center">
              <div className="text-drone-red font-mono">{data.thresholds.critical}%</div>
              <div className="text-drone-text-dim">Critical</div>
            </div>
          </div>
        </div>

        {/* Individual Sensors */}
        {data.sensors.length > 0 && (
          <div className="space-y-2">
            <div className="text-drone-text-dim text-xs font-medium">Sensor Status</div>
            <div className="space-y-1">
              {data.sensors.slice(0, 4).map((sensor, index) => (
                <div key={index} className="flex items-center justify-between text-xs">
                  <span className="text-drone-text-dim">{sensor.name}</span>
                  <div className="flex items-center space-x-2">
                    <span className="font-mono">{sensor.health.toFixed(1)}%</span>
                    <div className={`w-2 h-2 rounded-full ${
                      sensor.status === 'optimal' ? 'bg-drone-green' :
                      sensor.status === 'good' ? 'bg-drone-blue' :
                      sensor.status === 'warning' ? 'bg-drone-amber' :
                      sensor.status === 'critical' ? 'bg-drone-red' :
                      'bg-gray-500'
                    }`} />
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>
    </BaseWidget>
  )
} 