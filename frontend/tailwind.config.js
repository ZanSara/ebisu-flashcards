module.exports = {
  purge: [],
  darkMode: false, // or 'media' or 'class'
  theme: {
    boxShadow: {
      sm: "0.25rem 0.25rem rgba(107, 114, 128)",
      md: "0.5rem 0.5rem rgba(107, 114, 128)",
      DEFAULT: "1.5rem 1.5rem #5a5c69",
    },
    extend: {
      keyframes: {
        swim: {
          "0%, 100%": {
            transform: "rotate(0deg) translateY(0)",
          },
          "25%": {
            transform: "rotate(-5deg) translateY(-25%)",
          },
          "50%": {
            transform: "rotate(0deg) translateY(-50%)",
            // animationTimingFunction: "cubic-bezier(0.8, 0, 1, 1)",
          },
          "75%": {
            transform: "rotate(5deg) translateY(-25%)",
          },
        },
      },
      animation: {
        swim: "swim 1s linear infinite",
      },
    },
  },
  variants: {
    extend: {},
  },
  plugins: [],
};
