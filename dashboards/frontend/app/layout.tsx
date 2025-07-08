import type { Metadata } from 'next'
import { Inter } from 'next/font/google'
import './globals.css'

const inter = Inter({ subsets: ['latin'] })

export const metadata: Metadata = {
  title: 'Watchtower - Drone Operator Dashboard',
  description: 'Physics-informed sensor monitoring system for drone operations',
  keywords: 'drone, sensor monitoring, physics, aviation, thermal camera, GPS, IMU',
  authors: [{ name: 'Watchtower Team' }],
  viewport: 'width=device-width, initial-scale=1',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en" className="dark">
      <body className={`${inter.className} bg-dark-950 text-white antialiased`}>
        <div className="min-h-screen bg-gradient-to-br from-dark-950 via-dark-900 to-dark-800">
          {children}
        </div>
      </body>
    </html>
  )
} 