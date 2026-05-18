import Navbar from "../ui/Navbar";
import { motion } from "framer-motion";

export default function PageLayout({ children, className = "" }) {
  return (
    <div className="min-h-screen bg-slate-50">
      <Navbar />
      <motion.main
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ duration: 0.35 }}
        className={["pt-16", className].join(" ")}
      >
        {children}
      </motion.main>
    </div>
  );
}
