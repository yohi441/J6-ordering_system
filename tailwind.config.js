/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './templates/**/*.html',
    './ordering/forms.py',
  ],
  theme: {
    extend: {
      colors: {
        j6primary: '#1c9941',
        j6secondary: '#3b4441',
      }
    },
  },
  plugins: [
    
  ],
}
