/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,jsx}",
  ],
  theme: {
    extend: {
      colors: {
        dark: {
          900: "#0a0a0a",
          800: "#1a1a1a",
        },
        primary: {
          500: "#6366f1",
        },
      },
    },
  },
  plugins: [],
}