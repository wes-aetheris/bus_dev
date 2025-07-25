import React from 'react';
import { CircularProgressbar, buildStyles } from 'react-circular-progressbar';
import 'react-circular-progressbar/dist/styles.css';

interface StatusGaugeProps {
  value: number;
  label: string;
  size?: 'sm' | 'md' | 'lg';
}

export const StatusGauge: React.FC<StatusGaugeProps> = ({
  value, label, size = 'md'
}) => {
  const sizeClasses = {
    sm: 'w-16 h-16',
    md: 'w-24 h-24', 
    lg: 'w-32 h-32'
  };

  const getColor = () => {
    if (value < 30) return '#FF4444';
    if (value < 70) return '#FFB800';
    return '#00FF88';
  };

  return (
    <div className="text-center">
      <div className={`${sizeClasses[size]} mx-auto mb-2`}>
        <CircularProgressbar
          value={value}
          text={`${value}%`}
          styles={buildStyles({
            textColor: '#E8E8E8',
            pathColor: getColor(),
            trailColor: '#2D3548',
          })}
        />
      </div>
      <div className="text-drone-text-dim text-xs font-mono uppercase">
        {label}
      </div>
    </div>
  );
}; 