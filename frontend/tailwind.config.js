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
        // Modern Fintech 2025/2026 Design System
        'fintech': {
          'bg': '#0a0e1a',        // Main background (darker)
          'card': 'rgba(22, 27, 34, 0.6)',      // Glass card backgrounds
          'card-solid': '#161B22',  // Solid card backgrounds
          'border': 'rgba(255, 255, 255, 0.1)', // Subtle borders
          'border-glow': 'rgba(0, 212, 255, 0.2)', // Accent borders
          'green': '#00D09C',     // Bull/Positive
          'red': '#FF4D4D',       // Bear/Negative
          'orange': '#FF6B35',    // Neutral/Action
          'cyan': '#00d4ff',      // Primary accent
          'cyan-glow': 'rgba(0, 212, 255, 0.3)', // Glow effect
          'purple': '#a855f7',    // Secondary accent
          'purple-dark': '#764ba2', // Dark purple for gradients
          'indigo': '#667eea',    // Gradient color
        }
      },
      fontFamily: {
        'mono': ['JetBrains Mono', 'Consolas', 'Monaco', 'Courier New', 'monospace'],
        'sans': ['Inter', 'system-ui', '-apple-system', 'sans-serif'],
      },
      animation: {
        'pulse-slow': 'pulse 3s cubic-bezier(0.4, 0, 0.6, 1) infinite',
        'fade-in': 'fadeIn 0.5s ease-in-out',
        'slide-up': 'slideUp 0.3s cubic-bezier(0.4, 0, 0.2, 1)',
        'glow': 'glow 2s ease-in-out infinite',
      },
      keyframes: {
        fadeIn: {
          '0%': { opacity: '0', transform: 'translateY(10px)' },
          '100%': { opacity: '1', transform: 'translateY(0)' },
        },
        slideUp: {
          '0%': { opacity: '0', transform: 'translateY(20px)' },
          '100%': { opacity: '1', transform: 'translateY(0)' },
        },
        glow: {
          '0%, 100%': { boxShadow: '0 0 20px rgba(0, 212, 255, 0.3)' },
          '50%': { boxShadow: '0 0 30px rgba(0, 212, 255, 0.6)' },
        }
      },
      backgroundImage: {
        'gradient-primary': 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
        'gradient-accent': 'linear-gradient(135deg, #00d4ff 0%, #a855f7 100%)',
        'glass': 'linear-gradient(135deg, rgba(255, 255, 255, 0.1) 0%, rgba(255, 255, 255, 0.05) 100%)',
      },
      backdropBlur: {
        'glass': '20px',
      }
    },
  },
  plugins: [],
}
