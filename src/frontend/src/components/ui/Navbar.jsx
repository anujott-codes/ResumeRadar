import { Link, useLocation } from "react-router-dom";
import { Radar, ExternalLink, ArrowRight } from "lucide-react";
import { motion } from "framer-motion";

export default function Navbar() {
  const { pathname } = useLocation();

  return (
    <motion.nav
      initial={{ y: -20, opacity: 0 }}
      animate={{ y: 0, opacity: 1 }}
      transition={{ duration: 0.4 }}
      className="fixed top-0 left-0 right-0 z-50 bg-white/80 backdrop-blur-md border-b border-slate-100 shadow-sm"
    >
      <div className="max-w-6xl mx-auto px-4 sm:px-6 h-16 flex items-center justify-between">
        {/* Logo */}
        <Link to="/" className="flex items-center gap-2 group">
          <div className="p-1.5 rounded-lg bg-brand-600 text-white shadow-sm group-hover:bg-brand-700 transition-colors">
            <Radar size={18} />
          </div>
          <span className="font-bold text-slate-900 text-lg tracking-tight">
            Resume<span className="text-brand-600">Radar</span>
          </span>
        </Link>

        {/* Nav links */}
        <div className="flex items-center gap-3">
          <a
            href="https://github.com/anujott-codes/ResumeRadar"
            target="_blank"
            rel="noopener noreferrer"
            className="p-2 rounded-lg text-slate-500 hover:text-slate-900 hover:bg-slate-100 transition-all"
            aria-label="GitHub"
          >
            <ExternalLink size={18} />
          </a>

          {pathname !== "/analyze" && (
            <Link
              to="/analyze"
              className="flex items-center gap-1.5 px-4 py-2 rounded-xl bg-brand-600 text-white text-sm font-semibold
                hover:bg-brand-700 active:scale-95 transition-all shadow-sm shadow-brand-200"
            >
              Try it free
              <ArrowRight size={14} />
            </Link>
          )}
        </div>
      </div>
    </motion.nav>
  );
}
