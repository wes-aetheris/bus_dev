import React, { useState } from 'react'
import { Layout } from '@/components/layout/Layout'
import { Header } from '@/components/layout/Header'
import { useDashboardStore } from '@/stores/dashboardStore'

const Dashboard: React.FC = () => {
  const [activeTab, setActiveTab] = useState('pre-flight')
  const { tabs, loading } = useDashboardStore()

  const renderTabContent = () => {
    switch (activeTab) {
      case 'pre-flight':
        return (
          <div className="p-6">
            <h2 className="text-2xl font-bold mb-4">Pre-Flight Checks</h2>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              <div className="bg-white p-6 rounded-lg shadow">
                <h3 className="text-lg font-semibold mb-2">Sensor Status</h3>
                <div className="space-y-2">
                  <div className="flex justify-between">
                    <span>GPS</span>
                    <span className="text-green-600">Online</span>
                  </div>
                  <div className="flex justify-between">
                    <span>IMU</span>
                    <span className="text-green-600">Online</span>
                  </div>
                  <div className="flex justify-between">
                    <span>Camera</span>
                    <span className="text-green-600">Online</span>
                  </div>
                </div>
              </div>
              <div className="bg-white p-6 rounded-lg shadow">
                <h3 className="text-lg font-semibold mb-2">System Checks</h3>
                <div className="space-y-2">
                  <div className="flex justify-between">
                    <span>Battery</span>
                    <span className="text-green-600">Ready</span>
                  </div>
                  <div className="flex justify-between">
                    <span>Propellers</span>
                    <span className="text-green-600">Good</span>
                  </div>
                </div>
              </div>
              <div className="bg-white p-6 rounded-lg shadow">
                <h3 className="text-lg font-semibold mb-2">Weather</h3>
                <div className="space-y-2">
                  <div className="flex justify-between">
                    <span>Wind Speed</span>
                    <span>5.2 m/s</span>
                  </div>
                  <div className="flex justify-between">
                    <span>Temperature</span>
                    <span>22.5°C</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        )
      case 'post-flight':
        return (
          <div className="p-6">
            <h2 className="text-2xl font-bold mb-4">Post-Flight Analysis</h2>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div className="bg-white p-6 rounded-lg shadow">
                <h3 className="text-lg font-semibold mb-2">Flight Summary</h3>
                <div className="space-y-2">
                  <div className="flex justify-between">
                    <span>Duration</span>
                    <span>45:30</span>
                  </div>
                  <div className="flex justify-between">
                    <span>Distance</span>
                    <span>12.5 km</span>
                  </div>
                  <div className="flex justify-between">
                    <span>Max Altitude</span>
                    <span>120 m</span>
                  </div>
                </div>
              </div>
              <div className="bg-white p-6 rounded-lg shadow">
                <h3 className="text-lg font-semibold mb-2">Data Collected</h3>
                <div className="space-y-2">
                  <div className="flex justify-between">
                    <span>Records</span>
                    <span>2,700</span>
                  </div>
                  <div className="flex justify-between">
                    <span>Data Size</span>
                    <span>45.2 MB</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        )
      case 'mission-planning':
        return (
          <div className="p-6">
            <h2 className="text-2xl font-bold mb-4">Mission Planning</h2>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div className="bg-white p-6 rounded-lg shadow">
                <h3 className="text-lg font-semibold mb-2">Planned Routes</h3>
                <div className="space-y-4">
                  <div className="border p-4 rounded">
                    <h4 className="font-semibold">Survey Area A</h4>
                    <p className="text-sm text-gray-600">Estimated: 30:00, 8.5 km</p>
                  </div>
                </div>
              </div>
              <div className="bg-white p-6 rounded-lg shadow">
                <h3 className="text-lg font-semibold mb-2">Weather Forecast</h3>
                <div className="space-y-2">
                  <div className="flex justify-between">
                    <span>Wind Speed</span>
                    <span>5.2 m/s</span>
                  </div>
                  <div className="flex justify-between">
                    <span>Temperature</span>
                    <span>22.5°C</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        )
      case 'maintenance':
        return (
          <div className="p-6">
            <h2 className="text-2xl font-bold mb-4">Maintenance</h2>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div className="bg-white p-6 rounded-lg shadow">
                <h3 className="text-lg font-semibold mb-2">Component Health</h3>
                <div className="space-y-2">
                  <div className="flex justify-between">
                    <span>Motors</span>
                    <span className="text-yellow-600">85%</span>
                  </div>
                  <div className="flex justify-between">
                    <span>Propellers</span>
                    <span className="text-green-600">90%</span>
                  </div>
                  <div className="flex justify-between">
                    <span>Battery</span>
                    <span className="text-red-600">75%</span>
                  </div>
                </div>
              </div>
              <div className="bg-white p-6 rounded-lg shadow">
                <h3 className="text-lg font-semibold mb-2">Maintenance Schedule</h3>
                <div className="space-y-2">
                  <div className="text-sm">
                    <div className="font-semibold">Battery Inspection</div>
                    <div className="text-gray-600">Due: 2024-01-10</div>
                  </div>
                  <div className="text-sm">
                    <div className="font-semibold">Propeller Replacement</div>
                    <div className="text-gray-600">Due: 2024-01-15</div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        )
      case 'environment':
        return (
          <div className="p-6">
            <h2 className="text-2xl font-bold mb-4">Environment & Context</h2>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div className="bg-white p-6 rounded-lg shadow">
                <h3 className="text-lg font-semibold mb-2">Current Conditions</h3>
                <div className="space-y-2">
                  <div className="flex justify-between">
                    <span>Temperature</span>
                    <span>22.5°C</span>
                  </div>
                  <div className="flex justify-between">
                    <span>Humidity</span>
                    <span>65%</span>
                  </div>
                  <div className="flex justify-between">
                    <span>Wind Speed</span>
                    <span>5.2 m/s</span>
                  </div>
                </div>
              </div>
              <div className="bg-white p-6 rounded-lg shadow">
                <h3 className="text-lg font-semibold mb-2">Air Quality</h3>
                <div className="space-y-2">
                  <div className="flex justify-between">
                    <span>PM2.5</span>
                    <span>12 µg/m³</span>
                  </div>
                  <div className="flex justify-between">
                    <span>CO2</span>
                    <span>420 ppm</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        )
      case 'camera-profile':
        return (
          <div className="p-6">
            <h2 className="text-2xl font-bold mb-4">Camera Sensor Profile</h2>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div className="bg-white p-6 rounded-lg shadow">
                <h3 className="text-lg font-semibold mb-2">Camera Settings</h3>
                <div className="space-y-2">
                  <div className="flex justify-between">
                    <span>Resolution</span>
                    <span>4K</span>
                  </div>
                  <div className="flex justify-between">
                    <span>FPS</span>
                    <span>30</span>
                  </div>
                  <div className="flex justify-between">
                    <span>ISO</span>
                    <span>100</span>
                  </div>
                </div>
              </div>
              <div className="bg-white p-6 rounded-lg shadow">
                <h3 className="text-lg font-semibold mb-2">Image Analysis</h3>
                <div className="space-y-2">
                  <div className="flex justify-between">
                    <span>Sharpness</span>
                    <span>85%</span>
                  </div>
                  <div className="flex justify-between">
                    <span>Exposure</span>
                    <span>Good</span>
                  </div>
                  <div className="flex justify-between">
                    <span>Color Accuracy</span>
                    <span>90%</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        )
      case 'operational-flight':
        return (
          <div className="p-6">
            <h2 className="text-2xl font-bold mb-4">Operational Flight</h2>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div className="bg-white p-6 rounded-lg shadow">
                <h3 className="text-lg font-semibold mb-2">Current Status</h3>
                <div className="space-y-2">
                  <div className="flex justify-between">
                    <span>Flight Mode</span>
                    <span>Mission</span>
                  </div>
                  <div className="flex justify-between">
                    <span>Altitude</span>
                    <span>100 m</span>
                  </div>
                  <div className="flex justify-between">
                    <span>Speed</span>
                    <span>12.5 m/s</span>
                  </div>
                  <div className="flex justify-between">
                    <span>Battery</span>
                    <span>75%</span>
                  </div>
                </div>
              </div>
              <div className="bg-white p-6 rounded-lg shadow">
                <h3 className="text-lg font-semibold mb-2">Mission Progress</h3>
                <div className="space-y-2">
                  <div className="flex justify-between">
                    <span>Waypoints</span>
                    <span>3/8</span>
                  </div>
                  <div className="flex justify-between">
                    <span>Distance Remaining</span>
                    <span>2.5 km</span>
                  </div>
                  <div className="flex justify-between">
                    <span>ETA</span>
                    <span>15:30</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        )
      default:
        return <div className="p-6">Select a tab to view content</div>
    }
  }

  return (
    <Layout>
      <Header />
      <div className="flex-1">
        <div className="border-b border-gray-200">
          <nav className="-mb-px flex space-x-8 px-6">
            {tabs.map((tab) => (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id)}
                className={`py-2 px-1 border-b-2 font-medium text-sm ${
                  activeTab === tab.id
                    ? 'border-primary-500 text-primary-600'
                    : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                }`}
              >
                {tab.name}
              </button>
            ))}
          </nav>
        </div>
        {loading ? (
          <div className="flex items-center justify-center h-64">
            <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary-500"></div>
          </div>
        ) : (
          renderTabContent()
        )}
      </div>
    </Layout>
  )
}

export default Dashboard
