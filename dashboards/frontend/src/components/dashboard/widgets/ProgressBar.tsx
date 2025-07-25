import React from 'react'

export interface ProgressBarProps {
  value: number // 0-100
  maxValue?: number
  label?: string
  unit?: string
  color?: 'blue' | 'green' | 'amber' | 'red' | 'custom'
  customColor?: string
  size?: 'sm' | 'md' | 'lg'
  showValue?: boolean
  animated?: boolean
  className?: string
}

export const ProgressBar: React.FC<ProgressBarProps> = ({
  value,
  maxValue = 100,
  label,
  unit,
  color = 'blue',
  customColor,
  size = 'md',
  showValue = true,
  animated = true,
  className = ''
}) => {
  const percentage = Math.min(Math.max((value / maxValue) * 100, 0), 100)
  
  const colorClasses = {
    blue: 'bg-drone-blue',
    green: 'bg-drone-green',
    amber: 'bg-drone-amber',
    red: 'bg-drone-red',
    custom: customColor || 'bg-drone-blue'
  }

  const sizeClasses = {
    sm: 'h-2',
    md: 'h-3',
    lg: 'h-4'
  }

  const getStatusColor = (val: number) => {
    if (val >= 80) return 'green'
    if (val >= 60) return 'blue'
    if (val >= 40) return 'amber'
    return 'red'
  }

  const statusColor = getStatusColor(percentage)
  const finalColor = color === 'custom' ? customColor : colorClasses[statusColor as keyof typeof colorClasses]

  return (
    <div className={`space-y-1 ${className}`}>
      {(label || showValue) && (
        <div className="flex justify-between items-center text-xs">
          {label && (
            <span className="text-drone-text-dim font-medium">{label}</span>
          )}
          {showValue && (
            <span className="text-drone-text font-mono">
              {value.toFixed(1)}{unit && ` ${unit}`}
            </span>
          )}
        </div>
      )}
      
      <div className={`
        bg-drone-panel rounded-full overflow-hidden
        ${sizeClasses[size]}
      `}>
        <div
          className={`
            ${finalColor} transition-all duration-500 ease-out
            ${animated ? 'animate-pulse' : ''}
            h-full rounded-full
          `}
          style={{ width: `${percentage}%` }}
        />
      </div>
    </div>
  )
}

export interface CircularProgressProps {
  value: number // 0-100
  size?: number
  strokeWidth?: number
  label?: string
  color?: 'blue' | 'green' | 'amber' | 'red'
  showValue?: boolean
  className?: string
}

export const CircularProgress: React.FC<CircularProgressProps> = ({
  value,
  size = 60,
  strokeWidth = 4,
  label,
  color = 'blue',
  showValue = true,
  className = ''
}) => {
  const radius = (size - strokeWidth) / 2
  const circumference = radius * 2 * Math.PI
  const percentage = Math.min(Math.max(value, 0), 100)
  const strokeDasharray = circumference
  const strokeDashoffset = circumference - (percentage / 100) * circumference

  const colorClasses = {
    blue: 'stroke-drone-blue',
    green: 'stroke-drone-green',
    amber: 'stroke-drone-amber',
    red: 'stroke-drone-red'
  }

  return (
    <div className={`flex flex-col items-center ${className}`}>
      <div className="relative" style={{ width: size, height: size }}>
        <svg
          width={size}
          height={size}
          className="transform -rotate-90"
        >
          {/* Background circle */}
          <circle
            cx={size / 2}
            cy={size / 2}
            r={radius}
            stroke="currentColor"
            strokeWidth={strokeWidth}
            fill="none"
            className="text-drone-panel"
          />
          {/* Progress circle */}
          <circle
            cx={size / 2}
            cy={size / 2}
            r={radius}
            stroke="currentColor"
            strokeWidth={strokeWidth}
            fill="none"
            strokeLinecap="round"
            strokeDasharray={strokeDasharray}
            strokeDashoffset={strokeDashoffset}
            className={`transition-all duration-500 ease-out ${colorClasses[color]}`}
          />
        </svg>
        
        {showValue && (
          <div className="absolute inset-0 flex items-center justify-center">
            <span className="text-drone-text font-mono text-sm font-bold">
              {value.toFixed(0)}%
            </span>
          </div>
        )}
      </div>
      
      {label && (
        <span className="text-drone-text-dim text-xs mt-1 text-center">
          {label}
        </span>
      )}
    </div>
  )
} 