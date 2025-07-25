import React, { ReactNode } from 'react'

export interface WidgetGridProps {
  children: ReactNode
  className?: string
  columns?: number
}

export const WidgetGrid: React.FC<WidgetGridProps> = ({
  children,
  className = '',
  columns = 4
}) => {
  const gridCols = {
    1: 'grid-cols-1',
    2: 'grid-cols-1 md:grid-cols-2',
    3: 'grid-cols-1 md:grid-cols-2 lg:grid-cols-3',
    4: 'grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4',
    5: 'grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-5',
    6: 'grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-6'
  }

  return (
    <div className={`
      grid gap-6 auto-rows-min
      ${gridCols[columns as keyof typeof gridCols] || gridCols[4]}
      ${className}
    `}>
      {children}
    </div>
  )
}

export interface WidgetSectionProps {
  title: string
  children: ReactNode
  className?: string
}

export const WidgetSection: React.FC<WidgetSectionProps> = ({
  title,
  children,
  className = ''
}) => {
  return (
    <div className={`space-y-4 ${className}`}>
      <h2 className="text-drone-text font-semibold text-lg">{title}</h2>
      <WidgetGrid>
        {children}
      </WidgetGrid>
    </div>
  )
} 