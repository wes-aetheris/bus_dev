import React, { useState } from 'react'
import { DashboardLayout } from '@/components/ui/DashboardLayout'
import { TabNavigation } from '@/components/ui/TabNavigation'
import { DroneCard } from '@/components/ui/DroneCard'
import { StatusGauge } from '@/components/ui/StatusGauge'
import { HUDDisplay } from '@/components/ui/HUDDisplay'
import { useDashboardStore } from '@/stores/dashboardStore'
import { WidgetGrid, WidgetSection } from '@/components/dashboard/WidgetGrid'
import { MissionCapabilityCard, SensorHealthGauge } from '@/components/dashboard/widgets'
import { mockMissionCapabilityData, mockSensorHealthData } from '@/data/mockSensorData'

const Dashboard: React.FC = () => {
  const [activeTab, setActiveTab] = useState('pre-flight')
  const { tabs, loading } = useDashboardStore()

  console.log('DASHBOARD MAIN: activeTab =', activeTab)

  const renderTabContent = () => {
    console.log('RENDER TAB CONTENT: activeTab =', activeTab)
    switch (activeTab) {
      case 'pre-flight':
        return (
          <div className="p-6">
            <h2 className="hud-text text-2xl font-bold mb-6">Pre-Flight Checks</h2>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              <DroneCard title="Sensor Status" status="normal">
                <div className="space-y-4">
                  <div className="flex justify-between items-center">
                    <span className="text-drone-text-dim">GPS</span>
                    <span className="text-drone-green font-mono">ONLINE</span>
                  </div>
                  <div className="flex justify-between items-center">
                    <span className="text-drone-text-dim">IMU</span>
                    <span className="text-drone-green font-mono">ONLINE</span>
                  </div>
                  <div className="flex justify-between items-center">
                    <span className="text-drone-text-dim">Camera</span>
                    <span className="text-drone-green font-mono">ONLINE</span>
                  </div>
                  <div className="flex justify-between items-center">
                    <span className="text-drone-text-dim">Barometer</span>
                    <span className="text-drone-green font-mono">ONLINE</span>
                  </div>
                </div>
              </DroneCard>
              
              <DroneCard title="System Health" status="normal">
                <div className="grid grid-cols-2 gap-4">
                  <StatusGauge value={95} label="Battery" size="sm" />
                  <StatusGauge value={90} label="Motors" size="sm" />
                  <StatusGauge value={85} label="Propellers" size="sm" />
                  <StatusGauge value={95} label="Frame" size="sm" />
                </div>
              </DroneCard>
              
              <DroneCard title="Weather Conditions" status="normal">
                <div className="space-y-4">
                  <HUDDisplay value="5.2" label="Wind Speed" unit="m/s" status="normal" />
                  <HUDDisplay value="22.5" label="Temperature" unit="°C" status="normal" />
                  <HUDDisplay value="65" label="Humidity" unit="%" status="normal" />
                  <HUDDisplay value="10.0" label="Visibility" unit="km" status="normal" />
                </div>
              </DroneCard>
            </div>
          </div>
        )
        
      case 'post-flight':
        return (
          <div className="p-6">
            <h2 className="hud-text text-2xl font-bold mb-6">Post-Flight Analysis</h2>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <DroneCard title="Flight Summary" status="normal">
                <div className="grid grid-cols-2 gap-4">
                  <HUDDisplay value="45:30" label="Duration" status="normal" />
                  <HUDDisplay value="12.5" label="Distance" unit="km" status="normal" />
                  <HUDDisplay value="120" label="Max Altitude" unit="m" status="normal" />
                  <HUDDisplay value="15.2" label="Max Speed" unit="m/s" status="normal" />
                </div>
              </DroneCard>
              
              <DroneCard title="Data Collection" status="normal">
                <div className="space-y-4">
                  <div className="flex justify-between items-center">
                    <span className="text-drone-text-dim">Total Records</span>
                    <span className="text-drone-blue font-mono">2,700</span>
                  </div>
                  <div className="flex justify-between items-center">
                    <span className="text-drone-text-dim">Data Size</span>
                    <span className="text-drone-blue font-mono">45.2 MB</span>
                  </div>
                  <div className="flex justify-between items-center">
                    <span className="text-drone-text-dim">Sensors Used</span>
                    <span className="text-drone-blue font-mono">4</span>
                  </div>
                </div>
              </DroneCard>
            </div>
          </div>
        )
        
      case 'mission-planning':
        return (
          <div className="p-6">
            <h2 className="hud-text text-2xl font-bold mb-6">Mission Planning</h2>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <DroneCard title="Planned Routes" status="normal">
                <div className="space-y-4">
                  <div className="border border-drone-border p-4 rounded">
                    <h4 className="text-drone-blue font-mono font-semibold">Survey Area A</h4>
                    <p className="text-drone-text-dim text-sm">Estimated: 30:00, 8.5 km</p>
                    <div className="mt-2 text-xs text-drone-text-dim">
                      <div>Waypoints: 8</div>
                      <div>Altitude: 100m</div>
                    </div>
                  </div>
                </div>
              </DroneCard>
              
              <DroneCard title="Weather Forecast" status="normal">
                <div className="space-y-4">
                  <HUDDisplay value="5.2" label="Wind Speed" unit="m/s" status="normal" />
                  <HUDDisplay value="22.5" label="Temperature" unit="°C" status="normal" />
                  <HUDDisplay value="10" label="Precipitation" unit="%" status="normal" />
                  <HUDDisplay value="180" label="Wind Direction" unit="°" status="normal" />
                </div>
              </DroneCard>
            </div>
          </div>
        )
        
      case 'maintenance':
        return (
          <div className="p-6">
            <h2 className="hud-text text-2xl font-bold mb-6">Maintenance</h2>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <DroneCard title="Component Health" status="warning">
                <div className="grid grid-cols-2 gap-4">
                  <StatusGauge value={85} label="Motors" size="sm" />
                  <StatusGauge value={90} label="Propellers" size="sm" />
                  <StatusGauge value={75} label="Battery" size="sm" />
                  <StatusGauge value={95} label="Frame" size="sm" />
                </div>
              </DroneCard>
              
              <DroneCard title="Maintenance Schedule" status="normal">
                <div className="space-y-3">
                  <div className="border-l-2 border-drone-red pl-3">
                    <div className="text-drone-red font-mono text-sm font-semibold">Battery Inspection</div>
                    <div className="text-drone-text-dim text-xs">Due: 2024-01-10</div>
                  </div>
                  <div className="border-l-2 border-drone-amber pl-3">
                    <div className="text-drone-amber font-mono text-sm font-semibold">Propeller Replacement</div>
                    <div className="text-drone-text-dim text-xs">Due: 2024-01-15</div>
                  </div>
                  <div className="border-l-2 border-drone-blue pl-3">
                    <div className="text-drone-blue font-mono text-sm font-semibold">Motor Inspection</div>
                    <div className="text-drone-text-dim text-xs">Due: 2024-02-01</div>
                  </div>
                </div>
              </DroneCard>
            </div>
          </div>
        )
        
      case 'environment':
        return (
          <div className="p-6">
            <h2 className="hud-text text-2xl font-bold mb-6">Environment & Context</h2>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <DroneCard title="Current Conditions" status="normal">
                <div className="grid grid-cols-2 gap-4">
                  <HUDDisplay value="22.5" label="Temperature" unit="°C" status="normal" />
                  <HUDDisplay value="65" label="Humidity" unit="%" status="normal" />
                  <HUDDisplay value="1013.25" label="Pressure" unit="hPa" status="normal" />
                  <HUDDisplay value="5.2" label="Wind Speed" unit="m/s" status="normal" />
                </div>
              </DroneCard>
              
              <DroneCard title="Air Quality" status="normal">
                <div className="grid grid-cols-2 gap-4">
                  <HUDDisplay value="12" label="PM2.5" unit="µg/m³" status="normal" />
                  <HUDDisplay value="25" label="PM10" unit="µg/m³" status="normal" />
                  <HUDDisplay value="420" label="CO2" unit="ppm" status="normal" />
                  <HUDDisplay value="150" label="VOC" unit="ppb" status="normal" />
                </div>
              </DroneCard>
            </div>
          </div>
        )
        
      case 'camera-profile':
        return (
          <div className="p-6">
            <h2 className="hud-text text-2xl font-bold mb-6">Camera Sensor Profile</h2>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <DroneCard title="Camera Settings" status="normal">
                <div className="space-y-3">
                  <div className="flex justify-between items-center">
                    <span className="text-drone-text-dim">Resolution</span>
                    <span className="text-drone-blue font-mono">4K</span>
                  </div>
                  <div className="flex justify-between items-center">
                    <span className="text-drone-text-dim">FPS</span>
                    <span className="text-drone-blue font-mono">30</span>
                  </div>
                  <div className="flex justify-between items-center">
                    <span className="text-drone-text-dim">ISO</span>
                    <span className="text-drone-blue font-mono">100</span>
                  </div>
                  <div className="flex justify-between items-center">
                    <span className="text-drone-text-dim">Shutter Speed</span>
                    <span className="text-drone-blue font-mono">1/1000</span>
                  </div>
                </div>
              </DroneCard>
              
              <DroneCard title="Image Quality" status="normal">
                <div className="space-y-4">
                  <div className="flex justify-between items-center">
                    <span className="text-drone-text-dim">Sharpness</span>
                    <span className="text-drone-green font-mono">Excellent</span>
                  </div>
                  <div className="flex justify-between items-center">
                    <span className="text-drone-text-dim">Noise Level</span>
                    <span className="text-drone-green font-mono">Low</span>
                  </div>
                  <div className="flex justify-between items-center">
                    <span className="text-drone-text-dim">Dynamic Range</span>
                    <span className="text-drone-blue font-mono">12.5 stops</span>
                  </div>
                  <div className="flex justify-between items-center">
                    <span className="text-drone-text-dim">Color Accuracy</span>
                    <span className="text-drone-green font-mono">High</span>
                  </div>
                </div>
              </DroneCard>
            </div>
          </div>
        )
        
      case 'live-flight':
        console.log('Entering live-flight case')
        console.log('MissionCapabilityCard:', MissionCapabilityCard)
        console.log('SensorHealthGauge:', SensorHealthGauge)
        console.log('mockMissionCapabilityData:', mockMissionCapabilityData)
        console.log('mockSensorHealthData:', mockSensorHealthData)
        console.log('WidgetSection:', WidgetSection)
        console.log('WidgetGrid:', WidgetGrid)
        
        // Test if components are being rendered
        const testComponent = (
          <div style={{color: 'red', fontSize: '24px', fontWeight: 'bold'}}>
            LIVE FLIGHT TEST COMPONENT RENDERED
          </div>
        )
        console.log('Test component:', testComponent)
        
        return (
          <div className="p-6 space-y-8">
            <div className="mb-6">
              <h2 className="hud-text text-2xl font-bold mb-2">Live Flight Monitoring</h2>
              <p className="text-drone-text-dim">Real-time flight status with physics-informed sensor intelligence</p>
            </div>
            
            {/* Sensor Intelligence Section */}
            <div className="space-y-4">
              <h3 className="text-drone-text font-semibold text-lg">Sensor Intelligence</h3>
              <div className="bg-drone-card border border-drone-border rounded-lg p-4">
                <div className="text-drone-text font-semibold text-sm mb-4">Mission Capability</div>
                <div className="text-drone-text">Capability Score: {mockMissionCapabilityData.capabilityScore}%</div>
                <div className="text-drone-text">Trend: {mockMissionCapabilityData.trend}</div>
                <div className="text-drone-text">Confidence: {mockMissionCapabilityData.confidence}%</div>
              </div>
              <div className="bg-drone-card border border-drone-border rounded-lg p-4">
                <div className="text-drone-text font-semibold text-sm mb-4">Sensor Health</div>
                <div className="text-drone-text">Current Health: {mockSensorHealthData.currentHealth}%</div>
                <div className="text-drone-text">Predicted Health: {mockSensorHealthData.predictedHealth}%</div>
                <div className="text-drone-text">Degradation Rate: {mockSensorHealthData.degradationRate}%/hr</div>
              </div>
            </div>

            {/* Flight Status Section */}
            <div className="space-y-6">
              <h3 className="hud-text text-xl font-bold">Flight Status</h3>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <DroneCard title="Flight Status" status="normal">
                  <div className="space-y-4">
                    <div className="flex justify-between items-center">
                      <span className="text-drone-text-dim">Status</span>
                      <span className="text-drone-green font-mono">IN FLIGHT</span>
                    </div>
                    <div className="flex justify-between items-center">
                      <span className="text-drone-text-dim">Altitude</span>
                      <span className="text-drone-blue font-mono">85.2 m</span>
                    </div>
                    <div className="flex justify-between items-center">
                      <span className="text-drone-text-dim">Speed</span>
                      <span className="text-drone-blue font-mono">12.5 m/s</span>
                    </div>
                    <div className="flex justify-between items-center">
                      <span className="text-drone-text-dim">Battery</span>
                      <span className="text-drone-green font-mono">78%</span>
                    </div>
                  </div>
                </DroneCard>
                
                <DroneCard title="Mission Progress" status="normal">
                  <div className="space-y-4">
                    <div className="flex justify-between items-center">
                      <span className="text-drone-text-dim">Waypoints</span>
                      <span className="text-drone-blue font-mono">3/8</span>
                    </div>
                    <div className="flex justify-between items-center">
                      <span className="text-drone-text-dim">Distance</span>
                      <span className="text-drone-blue font-mono">2.1/8.5 km</span>
                    </div>
                    <div className="flex justify-between items-center">
                      <span className="text-drone-text-dim">Time</span>
                      <span className="text-drone-blue font-mono">12:30/30:00</span>
                    </div>
                    <div className="flex justify-between items-center">
                      <span className="text-drone-text-dim">Data Collected</span>
                      <span className="text-drone-green font-mono">1.2 GB</span>
                    </div>
                  </div>
                </DroneCard>
              </div>
            </div>
          </div>
        )
        
      default:
        console.log('DEFAULT CASE - activeTab value:', activeTab)
        return (
          <div className="p-6">
            <div style={{color: 'purple', fontSize: '24px', fontWeight: 'bold'}}>DEFAULT CASE TEST - activeTab: {activeTab}</div>
            <h2 className="hud-text text-2xl font-bold mb-6">Dashboard</h2>
            <p className="text-drone-text-dim">Select a tab to view specific information.</p>
          </div>
        )
    }
  }

  return (
    <DashboardLayout>
      <TabNavigation 
        activeTab={activeTab}
        onTabChange={setActiveTab}
      />
      {renderTabContent()}
    </DashboardLayout>
  )
}

export default Dashboard
