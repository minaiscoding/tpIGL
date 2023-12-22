/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/**/*.{js,jsx,ts,tsx}",
  ],  theme: {
    extend: {
      
      fontFamily: {
        'Futura' : 'Futura Book BT', 
        'Futura-bold' : 'Futura bold',
        'ITC Avant Garde Std Bold' : 'ITC',
      }
    },
  },
  plugins: [],
}

