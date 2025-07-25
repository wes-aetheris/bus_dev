import React, { ReactNode } from 'react'
import { WidgetHeader } from './WidgetHeader'
import { StatusIndicator } from './StatusIndicator'

export interface BaseWidgetProps {
  title: string
  icon?: string
  status?: 'optimal' | 'good' | 'warning' | 'critical' | 'offline'
  children: ReactNode
  className?: string
  onRefresh?: () => void
  isLoading?: boolean
  lastUpdated?: Date
  size?: 'small' | 'medium' | 'large'
  collapsible?: boolean
  defaultCollapsed?: boolean
}

export const BaseWidget: React.FC<BaseWidgetProps> = ({
  title,
  icon,
  status = 'good',
  children,
  className = '',
  onRefresh,
  isLoading = false,
  lastUpdated,
  size = 'medium',
  collapsible = false,
  defaultCollapsed = false
}) => {
  const [isCollapsed, setIsCollapsed] = React.useState(defaultCollapsed)

  const sizeClasses = {
    small: 'col-span-1 row-span-1',
    medium: 'col-span-2 row-span-2',
    large: 'col-span-3 row-span-3'
  }

  return (
    <div className={`
      bg-drone-card border border-drone-border rounded-lg p-4
      hover:border-drone-blue transition-all duration-200
      ${sizeClasses[size]}
      ${className}
    `}>
      <WidgetHeader
        title={title}
        icon={icon}
        status={status}
        onRefresh={onRefresh}
        isLoading={isLoading}
        lastUpdated={lastUpdated}
        collapsible={collapsible}
        isCollapsed={isCollapsed}
        onToggleCollapse={() => setIsCollapsed(!isCollapsed)}
      />
      
      {!isCollapsed && (
        <div className="mt-4">
          {isLoading ? (
            <div className="flex items-center justify-center h-32">
              <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-drone-blue"></div>
            </div>
          ) : (
            children
          )}
        </div>
      )}
    </div>
  )
} 