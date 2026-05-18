import { useEffect, useRef } from "react";
import { motion } from "framer-motion";

const SIZE = 160;
const STROKE = 10;
const R = (SIZE - STROKE) / 2;
const CIRCUMFERENCE = 2 * Math.PI * R;

function getColor(score) {
  if (score >= 0.75) return "#10b981"; // emerald
  if (score >= 0.5)  return "#f59e0b"; // amber
  return "#ef4444";                    // red
}

function getLabel(score) {
  if (score >= 0.75) return "Strong Match";
  if (score >= 0.5)  return "Moderate Match";
  return "Weak Match";
}

export default function ScoreRing({ score = 0 }) {
  const pct = Math.round(score * 100);
  const dashOffset = CIRCUMFERENCE * (1 - score);
  const color = getColor(score);

  return (
    <div className="flex flex-col items-center gap-3">
      <div className="relative" style={{ width: SIZE, height: SIZE }}>
        <svg width={SIZE} height={SIZE} viewBox={`0 0 ${SIZE} ${SIZE}`}>
          {/* Track */}
          <circle
            cx={SIZE / 2}
            cy={SIZE / 2}
            r={R}
            className="score-ring-track"
          />
          {/* Animated fill */}
          <motion.circle
            cx={SIZE / 2}
            cy={SIZE / 2}
            r={R}
            className="score-ring-fill"
            stroke={color}
            strokeDasharray={CIRCUMFERENCE}
            initial={{ strokeDashoffset: CIRCUMFERENCE }}
            animate={{ strokeDashoffset: dashOffset }}
            transition={{ duration: 1.4, ease: "easeOut", delay: 0.3 }}
            style={{ transformOrigin: "50% 50%", transform: "rotate(-90deg)" }}
          />
        </svg>

        {/* Center label */}
        <div className="absolute inset-0 flex flex-col items-center justify-center">
          <motion.span
            initial={{ opacity: 0, scale: 0.6 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ delay: 0.6, duration: 0.4 }}
            className="text-4xl font-extrabold tracking-tight"
            style={{ color }}
          >
            {pct}
            <span className="text-xl">%</span>
          </motion.span>
        </div>
      </div>

      <div className="text-center">
        <p className="text-sm font-semibold text-slate-500 uppercase tracking-widest">
          ATS Match Score
        </p>
        <p className="text-base font-bold mt-0.5" style={{ color }}>
          {getLabel(score)}
        </p>
      </div>
    </div>
  );
}
