import { motion } from "framer-motion";

export default function Card({
  children,
  className = "",
  hover = false,
  delay = 0,
  ...props
}) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 16 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.45, delay, ease: "easeOut" }}
      whileHover={hover ? { y: -3, boxShadow: "0 20px 40px -12px rgba(37,99,235,0.15)" } : undefined}
      className={[
        "bg-white rounded-2xl border border-slate-100 shadow-md p-6 transition-shadow",
        className,
      ].join(" ")}
      {...props}
    >
      {children}
    </motion.div>
  );
}
