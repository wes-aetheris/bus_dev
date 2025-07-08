'use client'

import { useEffect, useState } from 'react'

interface SensorHealthGaugeProps {
  health: number
}

export default function SensorHealthGauge({ health }: SensorHealthGaugeProps) {
  const [animatedHealth, setAnimatedHealth] = useState(0)

  useEffect(() => {
    const timer = setTimeout(() => {
      setAnimatedHealth(health)
    }, 100)
    return () => clearTimeout(timer)
  }, [health])

  const getHealthColor = (value: number) => {
    if (value >= 80) return '#22d47b' // success
    if (value >= 60) return '#fbbf24' // warning
    return '#ef4444' // danger
  }

  // SVG gauge constants
  const size = 120
  const strokeWidth = 10
  const radius = (size - strokeWidth) / 2
  const circumference = Math.PI * radius
  // Only half the circle (semi-circle)
  const arcLength = Math.PI * radius
  // Health as a fraction (0-1)
  const healthFraction = Math.max(0, Math.min(1, animatedHealth / 100))
  // Arc offset for SVG stroke-dasharray
  const offset = arcLength * (1 - healthFraction)

  return (
    <div style={{ width: size, height: size / 2, position: 'relative', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
      <svg width={size} height={size / 2} viewBox={`0 0 ${size} ${size / 2}`} style={{ position: 'absolute', top: 0, left: 0 }}>
        {/* Background arc */}
        <path
          d={`M ${strokeWidth / 2},${size / 2} A ${radius},${radius} 0 0 1 ${size - strokeWidth / 2},${size / 2}`}
          fill="none"
          stroke="#222a36"
          strokeWidth={strokeWidth}
        />
        {/* Foreground arc (health) */}
        <path
          d={`M ${strokeWidth / 2},${size / 2} A ${radius},${radius} 0 0 1 ${size - strokeWidth / 2},${size / 2}`}
          fill="none"
          stroke={getHealthColor(animatedHealth)}
          strokeWidth={strokeWidth}
          strokeDasharray={`${arcLength} ${circumference}`}
          strokeDashoffset={offset}
          strokeLinecap="round"
          style={{ transition: 'stroke-dashoffset 1s ease-out' }}
        />
      </svg>
      <div style={{
        position: 'absolute',
        top: 0,
        left: 0,
        width: size,
        height: size / 2,
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        fontSize: 28,
        fontWeight: 700,
        color: getHealthColor(animatedHealth),
        userSelect: 'none',
      }}>
        {Math.round(animatedHealth)}%
      </div>
    </div>
  )
} 