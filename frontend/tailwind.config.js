/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./src/**/*.{js,jsx,ts,tsx}"],
  theme: {
    extend: {
      fontFamily: {
        display: ["'Syne'", "sans-serif"],
        body: ["'DM Sans'", "sans-serif"],
        mono: ["'JetBrains Mono'", "monospace"],
      },
      colors: {
        obsidian: {
          950: "#050508",
          900: "#0a0a0f",
          800: "#111118",
          700: "#18181f",
          600: "#1e1e28",
          500: "#26263a",
        },
        jade: {
          400: "#34d399",
          500: "#10b981",
          600: "#059669",
        },
        crimson: {
          400: "#f87171",
          500: "#ef4444",
          600: "#dc2626",
        },
        aurelius: {
          400: "#fbbf24",
          500: "#f59e0b",
        },
        azure: {
          400: "#60a5fa",
          500: "#3b82f6",
        },
        violet: {
          400: "#a78bfa",
          500: "#8b5cf6",
        },
      },
      backgroundImage: {
        "mesh-dark": "radial-gradient(at 40% 20%, hsla(228,50%,8%,1) 0px, transparent 50%), radial-gradient(at 80% 0%, hsla(240,30%,5%,1) 0px, transparent 50%), radial-gradient(at 0% 50%, hsla(220,40%,6%,1) 0px, transparent 50%)",
        "glow-jade": "radial-gradient(ellipse at center, rgba(16,185,129,0.15) 0%, transparent 70%)",
        "glow-crimson": "radial-gradient(ellipse at center, rgba(239,68,68,0.15) 0%, transparent 70%)",
      },
      animation: {
        "fade-in": "fadeIn 0.5s ease-out",
        "slide-up": "slideUp 0.4s ease-out",
        "pulse-slow": "pulse 3s infinite",
        "shimmer": "shimmer 1.5s infinite",
      },
      keyframes: {
        fadeIn: { "0%": { opacity: "0" }, "100%": { opacity: "1" } },
        slideUp: { "0%": { opacity: "0", transform: "translateY(16px)" }, "100%": { opacity: "1", transform: "translateY(0)" } },
        shimmer: { "0%": { backgroundPosition: "-200% 0" }, "100%": { backgroundPosition: "200% 0" } },
      },
      boxShadow: {
        "glow-jade": "0 0 30px rgba(16,185,129,0.2)",
        "glow-crimson": "0 0 30px rgba(239,68,68,0.2)",
        "card": "0 4px 24px rgba(0,0,0,0.4), inset 0 1px 0 rgba(255,255,255,0.04)",
      },
    },
  },
  plugins: [],
};
