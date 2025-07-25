import React from 'react';

interface HUDDisplayProps {
  value: string | number;
  label: string;
  unit?: string;
  status?: 'normal' | 'warning' | 'critical';
}

export const HUDDisplay: React.FC<HUDDisplayProps> = ({
  value, label, unit, status = 'normal'
}) => {
  const statusColors = {
    normal: 'text-drone-blue',
    warning: 'text-drone-amber',
    critical: 'text-drone-red',
  };

  return (
    <div className="text-center">
      <div className="text-drone-text-dim text-xs font-mono uppercase mb-1">
        {label}
      </div>
      <div className={`font-mono font-bold text-2xl ${statusColors[status]}`}>
        {value}
        {unit && <span className="text-sm text-drone-text-dim ml-1">{unit}</span>}
      </div>
    </div>
  );
}; 