'use client'

import { useState } from 'react'
import { Upload, FileText, CheckCircle, AlertCircle } from 'lucide-react'

export default function DataUpload() {
  const [isUploading, setIsUploading] = useState(false)
  const [uploadStatus, setUploadStatus] = useState<'idle' | 'success' | 'error'>('idle')
  const [uploadMessage, setUploadMessage] = useState('')

  const handleFileUpload = async (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0]
    if (!file) return

    setIsUploading(true)
    setUploadStatus('idle')

    const formData = new FormData()
    formData.append('file', file)

    try {
      const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/upload-csv`, {
        method: 'POST',
        body: formData,
      })

      const data = await response.json()

      if (response.ok) {
        setUploadStatus('success')
        setUploadMessage(`Successfully uploaded ${data.rows} rows with ${data.columns.length} columns`)
      } else {
        setUploadStatus('error')
        setUploadMessage(data.detail || 'Upload failed')
      }
    } catch (error) {
      setUploadStatus('error')
      setUploadMessage('Network error during upload')
    } finally {
      setIsUploading(false)
    }
  }

  return (
    <div className="card">
      <div className="flex items-center space-x-2 mb-4">
        <Upload className="w-5 h-5 text-primary-400" />
        <h3 className="font-semibold">Data Upload</h3>
      </div>

      <div className="space-y-4">
        <div className="border-2 border-dashed border-dark-600 rounded-lg p-6 text-center hover:border-primary-500 transition-colors">
          <input
            type="file"
            accept=".csv"
            onChange={handleFileUpload}
            disabled={isUploading}
            className="hidden"
            id="csv-upload"
          />
          <label htmlFor="csv-upload" className="cursor-pointer">
            <div className="space-y-2">
              <Upload className="w-8 h-8 mx-auto text-dark-400" />
              <div>
                <p className="text-sm text-dark-300">
                  {isUploading ? 'Uploading...' : 'Click to upload CSV file'}
                </p>
                <p className="text-xs text-dark-400 mt-1">
                  Supports sensor data with timestamp, sensor_id, and health columns
                </p>
              </div>
            </div>
          </label>
        </div>

        {uploadStatus !== 'idle' && (
          <div className={`flex items-center space-x-2 p-3 rounded-lg ${
            uploadStatus === 'success' 
              ? 'bg-success-900/20 border border-success-700' 
              : 'bg-danger-900/20 border border-danger-700'
          }`}>
            {uploadStatus === 'success' ? (
              <CheckCircle className="w-4 h-4 text-success-400" />
            ) : (
              <AlertCircle className="w-4 h-4 text-danger-400" />
            )}
            <span className={`text-sm ${
              uploadStatus === 'success' ? 'text-success-300' : 'text-danger-300'
            }`}>
              {uploadMessage}
            </span>
          </div>
        )}

        <div className="text-xs text-dark-400 space-y-1">
          <p><strong>Required CSV format:</strong></p>
          <p>• timestamp: ISO datetime format</p>
          <p>• sensor_id: sensor identifier</p>
          <p>• health: sensor health percentage (0-100)</p>
          <p>• Optional: temperature, humidity, vibration, emi_level</p>
        </div>
      </div>
    </div>
  )
} 