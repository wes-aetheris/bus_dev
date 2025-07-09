import { useState, useEffect } from 'react'

interface DashboardData {
  [key: string]: any
}

interface MockData {
  'pre-flight': {
    sensor_status: {
      gps: { status: string; calibration: string };
      imu: { status: string; calibration: string };
      camera: { status: string; calibration: string };
    };
  };
  'post-flight': {
    flight_summary: {
      duration: string;
      distance: number;
      max_altitude: number;
    };
  };
}

export const useDashboardData = (tabId: string) => {
  const [data, setData] = useState<DashboardData | null>(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const fetchData = async () => {
    setLoading(true)
    setError(null)
    
    try {
      // In a real app, this would fetch from the API
      // const response = await fetch(`/api/dashboard/${tabId}`)
      // const result = await response.json()
      
      // Mock data for now
      await new Promise(resolve => setTimeout(resolve, 1000))
      const mockData: MockData = {
        'pre-flight': {
          sensor_status: {
            gps: { status: 'online', calibration: 'good' },
            imu: { status: 'online', calibration: 'good' },
            camera: { status: 'online', calibration: 'good' }
          }
        },
        'post-flight': {
          flight_summary: {
            duration: '45:30',
            distance: 12.5,
            max_altitude: 120
          }
        }
      }
      
      setData((mockData as any)[tabId] || {})
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to fetch data')
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    if (tabId) {
      fetchData()
    }
  }, [tabId])

  return { data, loading, error, refetch: fetchData }
}
