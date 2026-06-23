import { useContext } from "react";
import ThemeContext from "@/core/store/ThemeContext";

export default function SectionHeading({
  title,
  subtitle,
  align = "center",
  className = "",

  // 👇 NEW: allow explicit control (IMPORTANT)
  variant, // "dark" | "light" | undefined (auto)
}) {
  const context = useContext(ThemeContext);
  const theme = context?.theme || "dark";

  // final mode = prop overrides context
  const mode = variant || theme;

  const alignStyles = {
    center: "text-center mx-auto",
    left: "text-left",
  };

  const titleColor = mode === "dark" ? "text-white" : "text-gray-900";

  const subtitleColor = mode === "dark" ? "text-gray-300" : "text-gray-600";

  return (
    <div className={`max-w-3xl mb-16 ${alignStyles[align]} ${className}`}>
      {/* TITLE */}
      <h2
        className={`text-4xl font-bold relative inline-block ${titleColor}`}
        style={{
          textShadow:
            mode === "dark"
              ? "0 6px 16px rgba(0,0,0,0.5)"
              : "0 2px 8px rgba(0,0,0,0.12)",
        }}
      >
        {title}

        {/* underline */}
        <span
          className="
          block h-[4px] w-16 mt-3 rounded-full mx-auto
          bg-gradient-to-r from-blue-500 to-indigo-500
        "
        />
      </h2>

      {/* SUBTITLE */}
      {subtitle && (
        <p className={`mt-5 text-lg leading-relaxed ${subtitleColor}`}>
          {subtitle}
        </p>
      )}
    </div>
  );
}
