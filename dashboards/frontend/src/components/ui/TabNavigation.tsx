import React from 'react';
import { motion } from 'framer-motion';
import { 
  RocketLaunchIcon, ChartBarIcon, MapIcon, 
  WrenchScrewdriverIcon, GlobeAltIcon, CameraIcon, SignalIcon,
  CpuChipIcon
} from '@heroicons/react/24/outline';

const defaultTabs = [
  { id: 'pre-flight', name: 'Pre-Flight', icon: RocketLaunchIcon },
  { id: 'post-flight', name: 'Post-Flight', icon: ChartBarIcon },
  { id: 'mission-planning', name: 'Mission Planning', icon: MapIcon },
  { id: 'maintenance', name: 'Maintenance', icon: WrenchScrewdriverIcon },
  { id: 'environment', name: 'Environment', icon: GlobeAltIcon },
  { id: 'camera-profile', name: 'Camera Profile', icon: CameraIcon },
  { id: 'live-flight', name: 'Live Flight', icon: SignalIcon },
];

interface Tab {
  id: string;
  name: string;
  icon: React.ComponentType<{ className?: string }>;
}

interface TabNavigationProps {
  activeTab: string;
  onTabChange: (tabId: string) => void;
  tabs?: Tab[];
}

export const TabNavigation: React.FC<TabNavigationProps> = ({
  activeTab, onTabChange, tabs = defaultTabs
}) => {
  return (
    <nav className="bg-drone-panel border-b border-drone-border">
      <div className="flex overflow-x-auto">
        {tabs.map((tab) => {
          const Icon = tab.icon;
          const isActive = activeTab === tab.id;
          
          return (
            <button
              key={tab.id}
              onClick={() => { console.log('TAB CLICKED:', tab.id); onTabChange(tab.id); }}
              className={`
                relative flex items-center space-x-2 px-6 py-4 text-sm
                ${isActive 
                  ? 'text-drone-blue border-b-2 border-drone-blue bg-drone-card/30' 
                  : 'text-drone-text-dim hover:text-drone-text hover:bg-drone-card/20'
                }
              `}
            >
              <Icon className="w-5 h-5" />
              <span className="font-mono">{tab.name}</span>
              
              {isActive && (
                <motion.div
                  layoutId="activeTab"
                  className="absolute inset-0 bg-drone-blue/10"
                />
              )}
            </button>
          );
        })}
      </div>
    </nav>
  );
}; 