/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
        "./templates/*.html",
        "./templates/**/*.html",
    ],
  theme: {
    extend: {
      colors: {
        "terminus-gray": "#393939",
        "terminus-maroon": "#931a00",
      }
    },
  },
  plugins: [],
}
