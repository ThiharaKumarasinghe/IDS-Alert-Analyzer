/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        "darkPurple": "#050C9C",
        "purple": "#3572EF",
        "semiLightPurple": "#3ABEF9",
        "lightPurple": "#DDF2FD",
      }
    },
  },
  plugins: [
    require('daisyui'),
  ],
  daisyui: {
    extends: {},
    themes: [
      {
        mytheme: {
          "primary": "#1a73e8",
          "secondary": "#f6ad55",
          "accent": "#37cdbe",
          "neutral": "#3d4451",
          "base-100": "#ffffff",  // This controls the base background color
        },
      },
    ],
    darkTheme: false, // Disable dark mode completely
  },
}
