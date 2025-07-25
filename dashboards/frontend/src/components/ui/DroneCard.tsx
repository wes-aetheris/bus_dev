import React from 'react';
import { motion } from 'framer-motion';

interface DroneCardProps {
  children: React.ReactNode;
  title?: string;
  status?: 'normal' | 'warning' | 'error';
  className?: string;
}

export const DroneCard: React.FC<DroneCardProps> = ({
  children, title, status = 'normal', className = ''
}) => {
  const statusColors = {
    normal: 'border-drone-blue',
    warning: 'border-drone-amber', 
    error: 'border-drone-red'
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      className={`bg-drone-card border ${statusColors[status]} rounded-lg p-6 shadow-glow ${className}`}
    >
      {title && (
        <h3 className="hud-text text-sm font-semibold mb-4 uppercase tracking-wider">
          {title}
        </h3>
      )}
      {children}
    </motion.div>
  );
}; 