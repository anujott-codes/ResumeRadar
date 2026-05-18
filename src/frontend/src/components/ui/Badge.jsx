export default function Badge({ children, variant = "default", className = "" }) {
  const variants = {
    default: "bg-slate-100 text-slate-700",
    blue: "bg-brand-100 text-brand-700",
    green: "bg-emerald-100 text-emerald-700",
    red: "bg-red-100 text-red-700",
    amber: "bg-amber-100 text-amber-700",
    violet: "bg-violet-100 text-violet-700",
  };

  return (
    <span
      className={[
        "inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full text-xs font-semibold",
        variants[variant] ?? variants.default,
        className,
      ].join(" ")}
    >
      {children}
    </span>
  );
}
