/** @type {import('tailwindcss').Config} */
module.exports = {

  content: ["./src/**/*.{js,jsx,ts,tsx}"],

  theme: {
    extend: {
      gradientColorStops: (theme) => ({
        f6b237: theme("colors.yellow1"),
        "6b30e4": theme("colors.purple"),
        "3635ce": theme("colors.blue"),
        f6b2372: theme("colors.yellow2"),
        "6b30e42": theme("colors.purple2"),
        "3635ce2": theme("colors.blue2"),
      }),
      screens: {
        s: "500px",
      },
    },
    borderRadius: {
      'rd': '6px',
    },
    fontFamily: {
      Futura: "Futura Book BT",
      "Futura-bold": "Futura bold",
      "ITC Avant Garde Std Bold": "ITC",
    },
    Futura: "Futura Book BT",
    "Futura-bold": "Futura bold",
    avantgarde: ["ITC Avant Garde Gothic", "sans-serif"],
    colors: {
      navBg: "#1E1E1E",
      yellow: " #F6B237",
      yellow1: "rgba(54, 53, 206, 0.72)",
      purple: "rgba(107, 48, 228, 0.72)",
      blue: "rgba(246, 178, 55, 0.72)",
      "rgba-54-53-206-1": "rgba(54, 53, 206, 1)",
      yellow2: "rgba(54, 53, 206, 0.9)",
      purple2: "rgba(107, 48, 228, 0.86)",
      blue2: "rgba(246, 178, 55, 0.9)",
      'purple-600': '#8A88E2',
      'purple-300':'#bdbdec',
      white: "#FFFFFF",
      "gray-800": "#1E1E1E",

    },
  },
  plugins: [],
};
