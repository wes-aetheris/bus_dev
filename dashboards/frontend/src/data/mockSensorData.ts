import { MissionCapabilityData, SensorHealthData } from '@/components/dashboard/widgets'

export const mockMissionCapabilityData: MissionCapabilityData = {
  capabilityScore: 87.5,
  trend: 'improving',
  confidence: 92.3,
  projectedScore: 89.1,
  factors: [
    { name: 'Atmospheric Conditions', impact: 'positive', value: 5.2 },
    { name: 'Sensor Calibration', impact: 'positive', value: 3.1 },
    { name: 'Thermal Stability', impact: 'negative', value: -1.8 },
    { name: 'Lighting Quality', impact: 'positive', value: 2.4 }
  ]
}

export const mockSensorHealthData: SensorHealthData = {
  currentHealth: 94.2,
  predictedHealth: 91.8,
  degradationRate: 2.4,
  thresholds: {
    optimal: 85,
    warning: 70,
    critical: 50
  },
  sensors: [
    { name: 'Visible Camera', health: 96.5, status: 'optimal' },
    { name: 'Thermal Camera', health: 92.1, status: 'optimal' },
    { name: 'GPS Module', health: 98.3, status: 'optimal' },
    { name: 'IMU Sensor', health: 89.7, status: 'good' },
    { name: 'Barometer', health: 95.2, status: 'optimal' }
  ]
} 