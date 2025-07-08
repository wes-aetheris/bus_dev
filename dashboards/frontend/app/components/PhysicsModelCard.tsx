'use client'

import { Zap, TrendingDown } from 'lucide-react'

interface PhysicsModelCardProps {
  title: string
  model: string
  description: string
  health: number
}

export default function PhysicsModelCard({ title, model, description, health }: PhysicsModelCardProps) {
  const getHealthColor = (value: number) => {
    if (value >= 80) return 'text-success-400'
    if (value >= 60) return 'text-warning-400'
    return 'text-danger-400'
  }

  return (
    <div className="physics-model-card">
      <div className="flex items-center justify-between mb-2">
        <div className="flex items-center space-x-2">
          <Zap className="w-4 h-4 text-secondary-400" />
          <h4 className="font-medium text-white">{title}</h4>
        </div>
        <div className="flex items-center space-x-1">
          <TrendingDown className="w-4 h-4 text-dark-400" />
          <span className={`text-sm font-mono ${getHealthColor(health)}`}>
            {health.toFixed(1)}%
          </span>
        </div>
      </div>
      
      <div className="space-y-1">
        <p className="text-xs text-secondary-400 font-medium">{model}</p>
        <p className="text-xs text-dark-400">{description}</p>
      </div>
    </div>
  )
} 