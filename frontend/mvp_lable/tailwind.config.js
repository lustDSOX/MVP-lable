/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./index.html",
    "./src/**/*.{vue,js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      fontFamily:{
        'planet': ['"Planet Kosmos"', 'sans-serif'],
        'LTWave': ['"LTWave"', 'sans-serif'],
      },

      colors:{
        chrome: {
          dark: '#393939',      // Базовый темный
          base: '#929292',      // Средний тон
          light: '#A9A9A9',     // Светлый тон
          
          'hover-dark': '#424242', 
          'hover-light': '#B8B8B8',
        }
      }

      
    },
  },
  plugins: [],
}