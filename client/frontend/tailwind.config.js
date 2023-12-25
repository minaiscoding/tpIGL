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
      },
      borderRadius: {
      '14': '14px',
      },
      colors: {
      'purple-600': '#8A88E2',
      'purple-300':'#bdbdec',
      },
    },
  },
  plugins: [],
}


