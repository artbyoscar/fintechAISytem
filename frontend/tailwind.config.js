/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  darkMode: 'class',
  theme: {
    extend: {
      colors: {
        // Bloomberg Terminal inspired color palette
        'terminal': {
          'bg': '#000000',
          'bg-light': '#0a0a0a',
          'border': '#1a1a1a',
          'text': '#f5f5f5',
          'text-dim': '#999999',
          'orange': '#ff6b35',
          'orange-light': '#ff8966',
          'blue': '#004e89',
          'blue-light': '#1a659e',
          'green': '#00c853',
          'green-light': '#00e676',
          'red': '#ff1744',
          'red-light': '#ff5252',
          'yellow': '#ffc400',
          'yellow-light': '#ffea00',
        },
        // Modern Fintech color palette (Robinhood + Bloomberg hybrid)
        'fintech': {
          'bg': '#0D1117',        // Main background
          'card': '#161B22',      // Card backgrounds
          'border': 'rgba(255, 255, 255, 0.1)', // Subtle borders
          'green': '#00D09C',     // Bull/Positive
          'red': '#FF4D4D',       // Bear/Negative
          'orange': '#FF6B35',    // Neutral/Action
        }
      },
      fontFamily: {
        'mono': ['Consolas', 'Monaco', 'Courier New', 'monospace'],
        'sans': ['Inter', 'system-ui', 'sans-serif'],
      },
      animation: {
        'pulse-slow': 'pulse 3s cubic-bezier(0.4, 0, 0.6, 1) infinite',
        'fade-in': 'fadeIn 0.5s ease-in-out',
      },
      keyframes: {
        fadeIn: {
          '0%': { opacity: '0', transform: 'translateY(10px)' },
          '100%': { opacity: '1', transform: 'translateY(0)' },
        }
      }
    },
  },
  plugins: [],
}
