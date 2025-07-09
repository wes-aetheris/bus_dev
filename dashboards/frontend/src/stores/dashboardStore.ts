import { create } from 'zustand'

interface Tab {
  id: string
  name: string
  icon: string
  description: string
}

interface DashboardState {
  tabs: Tab[]
  loading: boolean
  activeTab: string
  setActiveTab: (tabId: string) => void
  setLoading: (loading: boolean) => void
  fetchTabs: () => Promise<void>
}

export const useDashboardStore = create<DashboardState>((set, get) => ({
  tabs: [
    { id: 'pre-flight', name: 'Pre-Flight', icon: 'airplane', description: 'Pre-flight checks and sensor calibration' },
    { id: 'post-flight', name: 'Post-Flight', icon: 'landing', description: 'Post-flight analysis and data review' },
    { id: 'mission-planning', name: 'Mission Planning', icon: 'map', description: 'Mission planning and route optimization' },
    { id: 'maintenance', name: 'Maintenance', icon: 'wrench', description: 'Maintenance schedules and component health' },
    { id: 'environment', name: 'Environment & Context', icon: 'globe', description: 'Environmental conditions and context data' },
    { id: 'camera-profile', name: 'Camera Sensor Profile', icon: 'camera', description: 'Camera settings and image analysis' },
    { id: 'operational-flight', name: 'Operational Flight', icon: 'flight', description: 'Real-time flight monitoring' }
  ],
  loading: false,
  activeTab: 'pre-flight',
  setActiveTab: (tabId: string) => set({ activeTab: tabId }),
  setLoading: (loading: boolean) => set({ loading }),
  fetchTabs: async () => {
    set({ loading: true })
    try {
      // In a real app, this would fetch from the API
      // const response = await fetch('/api/dashboard/tabs')
      // const data = await response.json()
      // set({ tabs: data.tabs })
      await new Promise(resolve => setTimeout(resolve, 1000)) // Simulate API call
    } catch (error) {
      console.error('Failed to fetch tabs:', error)
    } finally {
      set({ loading: false })
    }
  }
}))
