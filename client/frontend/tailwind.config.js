/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/**/*.{js,jsx,ts,tsx}",
  ],  theme: {
    extend: {
      fontFamily: {
        'Futura' : 'Futura Book BT', 
        'Futura-bold' : 'Futura bold',
        'avantgarde': ['ITC Avant Garde Gothic', 'sans-serif'],
      },
      colors :{
        'navBg':'#1E1E1E',
      }
    },
  },
  plugins: [],
}