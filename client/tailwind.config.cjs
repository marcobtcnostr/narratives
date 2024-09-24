// tailwind.config.cjs
/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ['./src/**/*.{html,js,svelte,ts}'],
  theme: {
    extend: {
      screens: {
        'xs': '100px',
        'sm': '640px',
        'md': '768px',
        'lg': '1024px',
        'xl': '1280px',
        '2xl': '1536px'
      },
      fontSize: {
        xs: ['1rem', '1.5'],
        sm: ['1rem', '1.5'],
        md: ['1rem', '1.5'],
        lg: ['1rem', '1.5'],
        xl: ['1rem', '1.5']
      }
    },
  },
  plugins: [
    require('daisyui')
  ],
  daisyui: {
    themes: [
      {
        light: {
          "--logo-color": "#69b3a2",
          "--logo-color-hover": "#56a085",
          "--bg-color": "white",
          "--text-color": "#333",
          "--text-color-hover": "white",
          "--button-bg-color": "#474747",
          "--button-bg-color-hover": "#dae0e5",
          "--button-text-color": "#f6f8fa",
          "--button-text-color-hover": "#474747",
          "--navbar-bg-color": "#f6f8fa",
          "--navbar-bg-color-hover": "#333",
          "--navbar-text-color-hover": "white",
          "--modal-bg-color": "#f6f8fa",
          "--event-card-bg-color": "#f6f8fa",
          "--separator-line-color": "#dae0e5",
          "--event-card-connector-color": "#dae0e5",
        },
        dark: {
          "--logo-color": "#69b3a2",
          "--logo-color-hover": "#56a085",
          "--bg-color": "#474747",
          "--text-color": "#f6f8fa",
          "--text-color-hover": "#474747",
          "--button-bg-color": "white",
          "--button-bg-color-hover": "#dae0e5",
          "--button-text-color": "#474747",
          "--button-text-color-hover": "#474747",
          "--navbar-bg-color": "#333",
          "--navbar-bg-color-hover": "#f6f8fa",
          "--navbar-text-color-hover": "#474747",
          "--modal-bg-color": "#333",
          "--event-card-bg-color": "#333",
          "--separator-line-color": "#dae0e5",
          "--event-card-connector-color": "#dae0e5",
        },
        custom: {
          "--logo-color": "#800080",  // Purple color for logo
          "--logo-color-hover": "#a020f0",  // Lighter purple color for hover
          "--bg-color": "#474747",
          "--text-color": "#f6f8fa",
          "--text-color-hover": "#474747",
          "--button-bg-color": "white",
          "--button-bg-color-hover": "#dae0e5",
          "--button-text-color": "#474747",
          "--button-text-color-hover": "#474747",
          "--navbar-bg-color": "#333",
          "--navbar-bg-color-hover": "#f6f8fa",
          "--navbar-text-color-hover": "#474747",
          "--modal-bg-color": "#333",
          "--event-card-bg-color": "#333",
          "--separator-line-color": "#dae0e5",
          "--event-card-connector-color": "#dae0e5",
        }
      }
    ],
    styled: true,
    themesEnabled: true,
  }
};