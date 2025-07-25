import React from 'react'
import { StatusIndicator } from './StatusIndicator'
import { RefreshCw, ChevronDown, ChevronUp } from 'lucide-react'

export interface WidgetHeaderProps {
  title: string
  icon?: string
  status?: 'optimal' | 'good' | 'warning' | 'critical' | 'offline'
  onRefresh?: () => void
  isLoading?: boolean
  lastUpdated?: Date
  collapsible?: boolean
  isCollapsed?: boolean
  onToggleCollapse?: () => void
}

export const WidgetHeader: React.FC<WidgetHeaderProps> = ({
  title,
  icon,
  status = 'good',
  onRefresh,
  isLoading = false,
  lastUpdated,
  collapsible = false,
  isCollapsed = false,
  onToggleCollapse
}) => {
  const formatLastUpdated = (date: Date) => {
    const now = new Date()
    const diffMs = now.getTime() - date.getTime()
    const diffMins = Math.floor(diffMs / 60000)
    
    if (diffMins < 1) return 'Just now'
    if (diffMins < 60) return `${diffMins}m ago`
    const diffHours = Math.floor(diffMins / 60)
    if (diffHours < 24) return `${diffHours}h ago`
    return date.toLocaleDateString()
  }

  return (
    <div className="flex items-center justify-between">
      <div className="flex items-center space-x-2">
        {icon && (
          <div className="w-5 h-5 text-drone-blue">
            {/* Icon placeholder - you can replace with actual icon component */}
            <div className="w-full h-full bg-drone-blue rounded-sm opacity-60"></div>
          </div>
        )}
        
        <h3 className="text-drone-text font-semibold text-sm">{title}</h3>
        
        <StatusIndicator status={status} />
      </div>
      
      <div className="flex items-center space-x-2">
        {lastUpdated && (
          <span className="text-xs text-drone-text-dim">
            {formatLastUpdated(lastUpdated)}
          </span>
        )}
        
        {onRefresh && (
          <button
            onClick={onRefresh}
            disabled={isLoading}
            className="p-1 text-drone-text-dim hover:text-drone-blue transition-colors disabled:opacity-50"
            title="Refresh data"
          >
            <RefreshCw 
              size={14} 
              className={`${isLoading ? 'animate-spin' : ''}`} 
            />
          </button>
        )}
        
        {collapsible && onToggleCollapse && (
          <button
            onClick={onToggleCollapse}
            className="p-1 text-drone-text-dim hover:text-drone-blue transition-colors"
            title={isCollapsed ? 'Expand' : 'Collapse'}
          >
            {isCollapsed ? <ChevronDown size={14} /> : <ChevronUp size={14} />}
          </button>
        )}
      </div>
    </div>
  )
} 