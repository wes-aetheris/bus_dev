'use client'

interface CorrelationMatrixProps {
  data: {
    sensors: string[]
    correlation_matrix: number[][]
  }
}

export default function CorrelationMatrix({ data }: CorrelationMatrixProps) {
  const getCorrelationColor = (value: number) => {
    if (value >= 0.7) return 'bg-success-500'
    if (value >= 0.4) return 'bg-warning-500'
    if (value >= 0.1) return 'bg-primary-500'
    return 'bg-dark-600'
  }

  const getCorrelationTextColor = (value: number) => {
    if (value >= 0.7) return 'text-success-100'
    if (value >= 0.4) return 'text-warning-100'
    if (value >= 0.1) return 'text-primary-100'
    return 'text-dark-300'
  }

  return (
    <div className="overflow-x-auto">
      <div className="min-w-max">
        {/* Header row with sensor names */}
        <div className="grid grid-cols-5 gap-1 mb-2">
          <div className="h-8"></div> {/* Empty corner */}
          {data.sensors.map((sensor, index) => (
            <div key={index} className="h-8 flex items-center justify-center text-xs font-medium text-dark-300">
              {sensor.replace('_', ' ').toUpperCase()}
            </div>
          ))}
        </div>

        {/* Correlation matrix */}
        {data.correlation_matrix.map((row, rowIndex) => (
          <div key={rowIndex} className="grid grid-cols-5 gap-1 mb-1">
            {/* Row header */}
            <div className="h-8 flex items-center justify-center text-xs font-medium text-dark-300">
              {data.sensors[rowIndex].replace('_', ' ').toUpperCase()}
            </div>
            
            {/* Correlation values */}
            {row.map((value, colIndex) => (
              <div
                key={colIndex}
                className={`h-8 flex items-center justify-center text-xs font-mono ${getCorrelationColor(value)} ${getCorrelationTextColor(value)}`}
                title={`${data.sensors[rowIndex]} vs ${data.sensors[colIndex]}: ${value.toFixed(3)}`}
              >
                {value.toFixed(2)}
              </div>
            ))}
          </div>
        ))}
      </div>

      {/* Legend */}
      <div className="mt-4 flex items-center justify-center space-x-4 text-xs">
        <div className="flex items-center space-x-1">
          <div className="w-3 h-3 bg-success-500 rounded"></div>
          <span className="text-dark-300">High (≥0.7)</span>
        </div>
        <div className="flex items-center space-x-1">
          <div className="w-3 h-3 bg-warning-500 rounded"></div>
          <span className="text-dark-300">Medium (≥0.4)</span>
        </div>
        <div className="flex items-center space-x-1">
          <div className="w-3 h-3 bg-primary-500 rounded"></div>
          <span className="text-dark-300">Low (≥0.1)</span>
        </div>
        <div className="flex items-center space-x-1">
          <div className="w-3 h-3 bg-dark-600 rounded"></div>
          <span className="text-dark-300">None (&lt;0.1)</span>
        </div>
      </div>
    </div>
  )
} 