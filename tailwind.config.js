/** @type {import('tailwindcss').Config} */
module.exports = {
  mode: 'jit',
  purge: ["./src/**/*.{html,js}", "./docs/**/*.{html,js}"],
  content: ["./src/**/*.{html,js}", "./docs/**/*.{html,js}"],
  theme: {
    extend: {},
  },
  plugins: [],
}
