import React from 'react'
import { BaseWidget } from './BaseWidget'
import { CircularProgress } from './ProgressBar'
import { TrendingUp, TrendingDown, Minus } from 'lucide-react'

export interface MissionCapabilityData {
  capabilityScore: number // 0-100
  trend: 'improving' | 'degrading' | 'stable'
  confidence: number // 0-100
  projectedScore: number // 30-minute prediction
  factors: {
    name: string
    impact: 'positive' | 'negative' | 'neutral'
    value: number
  }[]
}

export interface MissionCapabilityCardProps {
  data: MissionCapabilityData
  onRefresh?: () => void
  isLoading?: boolean
  lastUpdated?: Date
}

export const MissionCapabilityCard: React.FC<MissionCapabilityCardProps> = ({
  data,
  onRefresh,
  isLoading = false,
  lastUpdated
}) => {
  const getStatusFromScore = (score: number): 'optimal' | 'good' | 'warning' | 'critical' => {
    if (score >= 85) return 'optimal'
    if (score >= 70) return 'good'
    if (score >= 50) return 'warning'
    return 'critical'
  }

  const getTrendIcon = (trend: string) => {
    switch (trend) {
      case 'improving':
        return <TrendingUp className="w-4 h-4 text-drone-green" />
      case 'degrading':
        return <TrendingDown className="w-4 h-4 text-drone-red" />
      default:
        return <Minus className="w-4 h-4 text-drone-text-dim" />
    }
  }

  const getTrendColor = (trend: string) => {
    switch (trend) {
      case 'improving':
        return 'text-drone-green'
      case 'degrading':
        return 'text-drone-red'
      default:
        return 'text-drone-text-dim'
    }
  }

  return (
    <BaseWidget
      title="Mission Capability"
      icon="target"
      status={getStatusFromScore(data.capabilityScore)}
      onRefresh={onRefresh}
      isLoading={isLoading}
      lastUpdated={lastUpdated}
      size="medium"
    >
      <div className="space-y-4">
        {/* Main Score Display */}
        <div className="flex items-center justify-center">
          <CircularProgress
            value={data.capabilityScore}
            size={80}
            strokeWidth={6}
            color={getStatusFromScore(data.capabilityScore) === 'optimal' ? 'green' : 
                   getStatusFromScore(data.capabilityScore) === 'good' ? 'blue' : 
                   getStatusFromScore(data.capabilityScore) === 'warning' ? 'amber' : 'red'}
            showValue={true}
          />
        </div>

        {/* Trend and Confidence */}
        <div className="flex items-center justify-between text-sm">
          <div className="flex items-center space-x-2">
            {getTrendIcon(data.trend)}
            <span className={`font-mono ${getTrendColor(data.trend)}`}>
              {data.trend.charAt(0).toUpperCase() + data.trend.slice(1)}
            </span>
          </div>
          <div className="text-right">
            <div className="text-drone-text-dim text-xs">Confidence</div>
            <div className="text-drone-text font-mono">{data.confidence}%</div>
          </div>
        </div>

        {/* Projected Score */}
        <div className="bg-drone-panel rounded p-3">
          <div className="flex items-center justify-between">
            <span className="text-drone-text-dim text-xs">30min Projection</span>
            <span className="text-drone-blue font-mono text-sm">
              {data.projectedScore.toFixed(1)}%
            </span>
          </div>
        </div>

        {/* Contributing Factors */}
        {data.factors.length > 0 && (
          <div className="space-y-2">
            <div className="text-drone-text-dim text-xs font-medium">Contributing Factors</div>
            <div className="space-y-1">
              {data.factors.slice(0, 3).map((factor, index) => (
                <div key={index} className="flex items-center justify-between text-xs">
                  <span className="text-drone-text-dim">{factor.name}</span>
                  <span className={`font-mono ${
                    factor.impact === 'positive' ? 'text-drone-green' :
                    factor.impact === 'negative' ? 'text-drone-red' :
                    'text-drone-text-dim'
                  }`}>
                    {factor.impact === 'positive' ? '+' : factor.impact === 'negative' ? '-' : ''}
                    {factor.value.toFixed(1)}%
                  </span>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>
    </BaseWidget>
  )
} 