/** @type {import('tailwindcss').Config} */
const plugin = require("tailwindcss/plugin");

module.exports = {
  content: [
    "./static/css/*.css",
    "./static/js/*.js",
    "./templates/*.html"
  ],
  theme: {
    extend: {
      textShadow: {
        sm: "0 1px 2px var(--tw-shadow-color)",
        DEFAULT: "0 2px 4px var(--tw-shadow-color)",
        lg: "0 8px 16px var(--tw-shadow-color)",
      },
      boxShadow: {
        "3xl": "0 10px 15px 10px rgba(0, 0, 0, 0.3)",
        "inner-xl": "inset 0px -5px 10px 5px rgba(0, 0, 0, 0.3)",
      },
    },
  },
  plugins: [
    plugin(function ({ matchUtilities, theme }) {
      matchUtilities(
        {
          "text-shadow": (value) => ({
            textShadow: value,
          }),
        },
        { values: theme("textShadow") }
      );
    }),
  ],
}

