/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ['./src/**/*.{js,ts,jsx,tsx,mdx}'],
  theme: {
    extend: {
      colors: {
        drone: {
          'bg': '#0B0E1A',
          'panel': '#1A1F2E', 
          'card': '#252B3D',
          'border': '#2D3548',
          'blue': '#00D4FF',
          'amber': '#FFB800',
          'green': '#00FF88',
          'red': '#FF4444',
          'text': '#E8E8E8',
          'text-dim': '#A0A0A0',
        }
      },
      fontFamily: {
        'mono': ['JetBrains Mono', 'monospace'],
      },
      boxShadow: {
        'glow': '0 0 20px rgba(0, 212, 255, 0.3)',
      }
    },
  },
  plugins: [],
}
