/** @type {import('tailwindcss').Config} */
export default {
  darkMode: 'class',
  content: ['./index.html', './src/**/*.{js,jsx,ts,tsx}'],
  theme: {
    extend: {
      colors: {
        // Base backgrounds
        background: {
          light: '#F5F5F4', // stone-100
          dark: '#0B1220',
        },

        surface: {
          light: '#FAFAF9', // stone-50
          dark: '#111B2E',
        },

        border: {
          light: '#E7E5E4', // stone-200
          dark: '#1F2A44',
        },

        // Text
        text: {
          primary: {
            light: '#111827', // gray-900
            dark: '#E5E7EB',
          },
          muted: {
            light: '#6B7280', // gray-500
            dark: '#94A3B8',
          },
        },

        // Brand colors
        brand: {
          primary: '#2563EB', // blue-600
          accent: '#FBBF24', // yellow-400
        },

        // Status colors
        success: '#10B981',
        warning: '#F59E0B',
        error: '#EF4444',
        info: '#3B82F6',
      },

      fontFamily: {
        sans: ['Poppins', 'ui-sans-serif', 'system-ui'],
        display: ['Poppins', 'ui-sans-serif'],
      },

      boxShadow: {
        soft: '0 2px 12px rgba(0,0,0,0.08)',
        medium: '0 6px 20px rgba(0,0,0,0.15)',
        strong: '0 12px 36px rgba(0,0,0,0.2)',
      },

      borderRadius: {
        xl: '14px',
        '2xl': '20px',
      },

      keyframes: {
        fadeIn: {
          '0%': {
            opacity: 0,
            transform: 'translateY(8px)',
          },
          '100%': {
            opacity: 1,
            transform: 'translateY(0)',
          },
        },

        slideIn: {
          '0%': {
            opacity: 0,
            transform: 'translateX(-10px)',
          },
          '100%': {
            opacity: 1,
            transform: 'translateX(0)',
          },
        },
      },

      animation: {
        fadeIn: 'fadeIn 0.25s ease-out',
        slideIn: 'slideIn 0.25s ease-out',
      },
    },
  },
  plugins: [],
};
