import React from 'react'

export type StatusType = 'optimal' | 'good' | 'warning' | 'critical' | 'offline'

export interface StatusIndicatorProps {
  status: StatusType
  size?: 'sm' | 'md' | 'lg'
  showLabel?: boolean
  pulse?: boolean
}

export const StatusIndicator: React.FC<StatusIndicatorProps> = ({
  status,
  size = 'md',
  showLabel = false,
  pulse = false
}) => {
  const statusConfig = {
    optimal: {
      color: 'bg-drone-green',
      textColor: 'text-drone-green',
      label: 'Optimal',
      pulse: false
    },
    good: {
      color: 'bg-drone-blue',
      textColor: 'text-drone-blue',
      label: 'Good',
      pulse: false
    },
    warning: {
      color: 'bg-drone-amber',
      textColor: 'text-drone-amber',
      label: 'Warning',
      pulse: true
    },
    critical: {
      color: 'bg-drone-red',
      textColor: 'text-drone-red',
      label: 'Critical',
      pulse: true
    },
    offline: {
      color: 'bg-gray-500',
      textColor: 'text-gray-400',
      label: 'Offline',
      pulse: false
    }
  }

  const sizeClasses = {
    sm: 'w-2 h-2',
    md: 'w-3 h-3',
    lg: 'w-4 h-4'
  }

  const config = statusConfig[status]
  const shouldPulse = pulse || config.pulse

  return (
    <div className="flex items-center space-x-1">
      <div
        className={`
          ${config.color} ${sizeClasses[size]} rounded-full
          ${shouldPulse ? 'animate-pulse' : ''}
        `}
        title={config.label}
      />
      {showLabel && (
        <span className={`text-xs font-mono ${config.textColor}`}>
          {config.label}
        </span>
      )}
    </div>
  )
} 