import { Link } from "react-router-dom";
import { motion } from "framer-motion";
import {
  ArrowRight,
  Zap,
  Target,
  Brain,
  CheckCircle2,
  Upload,
  BarChart3,
  Sparkles,
  ExternalLink,
  Radar,
} from "lucide-react";
import PageLayout from "../components/layout/PageLayout";
import Badge from "../components/ui/Badge";

/* ── Animation variants ── */
const fadeUp = {
  hidden: { opacity: 0, y: 24 },
  visible: (i = 0) => ({
    opacity: 1,
    y: 0,
    transition: { duration: 0.55, delay: i * 0.1, ease: "easeOut" },
  }),
};

const stagger = {
  hidden: {},
  visible: { transition: { staggerChildren: 0.12 } },
};

/* ── Feature cards data ── */
const FEATURES = [
  {
    icon: Brain,
    title: "Hard Skill Matching",
    desc: "Semantic NLP engine compares your technical skills — Python, SQL, Docker — against the JD with sentence-level precision.",
    color: "bg-brand-50 text-brand-600",
  },
  {
    icon: Target,
    title: "Soft Skill Analysis",
    desc: "Detects leadership, communication, and collaboration signals in your resume and cross-references them with the JD's expectations.",
    color: "bg-violet-50 text-violet-600",
  },
  {
    icon: BarChart3,
    title: "ATS Match Score",
    desc: "Get a real-time overall match score combining skill coverage and semantic similarity — exactly what recruiters' ATS systems look for.",
    color: "bg-emerald-50 text-emerald-600",
  },
];

/* ── How it works steps ── */
const STEPS = [
  { icon: Upload,      label: "Upload Resume",      desc: "Drop your PDF resume — we parse it instantly." },
  { icon: Zap,         label: "Paste Job Description", desc: "Paste the JD text from any job posting." },
  { icon: Sparkles,    label: "Get Insights",        desc: "Receive a detailed match score, skill gaps, and suggestions." },
];

/* ── Social proof stats ── */
const STATS = [
  { value: "98%", label: "Parsing Accuracy" },
  { value: "<2s", label: "Analysis Time" },
  { value: "5MB", label: "Max Resume Size" },
  { value: "Free", label: "No Sign-up Needed" },
];

export default function LandingPage() {
  return (
    <PageLayout>
      {/* ── HERO ── */}
      <section className="relative overflow-hidden">
        {/* Background blobs */}
        <div
          aria-hidden
          className="absolute top-0 -left-32 w-[700px] h-[700px] rounded-full
            bg-gradient-to-br from-brand-100 to-blue-50 opacity-60 blur-3xl pointer-events-none"
        />
        <div
          aria-hidden
          className="absolute top-20 -right-32 w-[500px] h-[500px] rounded-full
            bg-gradient-to-br from-violet-100 to-purple-50 opacity-40 blur-3xl pointer-events-none"
        />

        <div className="relative max-w-6xl mx-auto px-4 sm:px-6 pt-24 pb-32 flex flex-col items-center text-center gap-8">
          {/* Badge */}
          <motion.div variants={fadeUp} initial="hidden" animate="visible" custom={0}>
            <span className="inline-flex items-center gap-2 px-4 py-1.5 rounded-full bg-brand-50 border border-brand-100
              text-brand-700 text-sm font-semibold shadow-sm">
              <Sparkles size={14} className="text-brand-500" />
              AI-Powered ATS Resume Analyzer
            </span>
          </motion.div>

          {/* Headline */}
          <motion.h1
            variants={fadeUp}
            initial="hidden"
            animate="visible"
            custom={1}
            className="text-5xl sm:text-6xl lg:text-7xl font-extrabold text-slate-900 leading-[1.08] tracking-tight text-balance max-w-4xl"
          >
            Land more interviews with a{" "}
            <span className="gradient-text">smarter resume</span>
          </motion.h1>

          {/* Sub */}
          <motion.p
            variants={fadeUp}
            initial="hidden"
            animate="visible"
            custom={2}
            className="text-lg sm:text-xl text-slate-500 max-w-2xl leading-relaxed"
          >
            ResumeRadar uses state-of-the-art NLP to match your resume against
            any job description — showing you exactly which skills you have,
            which you're missing, and how to close the gap.
          </motion.p>

          {/* CTAs */}
          <motion.div
            variants={fadeUp}
            initial="hidden"
            animate="visible"
            custom={3}
            className="flex flex-col sm:flex-row items-center gap-3"
          >
            <Link
              to="/analyze"
              id="hero-cta-analyze"
              className="flex items-center gap-2 px-7 py-3.5 rounded-xl bg-brand-600 text-white font-bold text-base
                hover:bg-brand-700 active:scale-95 transition-all shadow-lg shadow-brand-200"
            >
              Analyze My Resume
              <ArrowRight size={18} />
            </Link>
            <a
              href="https://github.com/anujott-codes/ResumeRadar"
              target="_blank"
              rel="noopener noreferrer"
              className="flex items-center gap-2 px-7 py-3.5 rounded-xl border border-slate-200 bg-white text-slate-700
                font-semibold text-base hover:bg-slate-50 active:scale-95 transition-all shadow-sm"
            >
              <ExternalLink size={18} />
              View on GitHub
            </a>
          </motion.div>

          {/* Stats row */}
          <motion.div
            variants={stagger}
            initial="hidden"
            animate="visible"
            className="flex flex-wrap justify-center gap-8 mt-6"
          >
            {STATS.map((s) => (
              <motion.div key={s.label} variants={fadeUp} className="text-center">
                <p className="text-2xl font-extrabold text-slate-900">{s.value}</p>
                <p className="text-sm text-slate-400 font-medium">{s.label}</p>
              </motion.div>
            ))}
          </motion.div>
        </div>
      </section>

      {/* ── FEATURES ── */}
      <section id="features" className="bg-white py-24">
        <div className="max-w-6xl mx-auto px-4 sm:px-6">
          <motion.div
            variants={stagger}
            initial="hidden"
            whileInView="visible"
            viewport={{ once: true, margin: "-80px" }}
            className="text-center mb-14"
          >
            <motion.p variants={fadeUp} className="text-brand-600 font-semibold text-sm uppercase tracking-widest mb-2">
              What We Do
            </motion.p>
            <motion.h2 variants={fadeUp} className="text-4xl font-extrabold text-slate-900 tracking-tight">
              Everything you need to get hired faster
            </motion.h2>
            <motion.p variants={fadeUp} className="mt-4 text-slate-500 text-lg max-w-xl mx-auto">
              Our NLP pipeline goes beyond keyword matching — it understands context,
              semantics, and skill relationships.
            </motion.p>
          </motion.div>

          <motion.div
            variants={stagger}
            initial="hidden"
            whileInView="visible"
            viewport={{ once: true, margin: "-60px" }}
            className="grid grid-cols-1 md:grid-cols-3 gap-6"
          >
            {FEATURES.map((f, i) => (
              <motion.div
                key={f.title}
                variants={fadeUp}
                custom={i}
                whileHover={{ y: -6, boxShadow: "0 24px 40px -12px rgba(0,0,0,0.12)" }}
                className="group relative bg-white rounded-2xl border border-slate-100 p-8 shadow-sm transition-shadow cursor-default"
              >
                <div className={`w-12 h-12 rounded-xl flex items-center justify-center mb-5 ${f.color}`}>
                  <f.icon size={22} />
                </div>
                <h3 className="text-lg font-bold text-slate-900 mb-2">{f.title}</h3>
                <p className="text-slate-500 text-sm leading-relaxed">{f.desc}</p>
              </motion.div>
            ))}
          </motion.div>
        </div>
      </section>

      {/* ── HOW IT WORKS ── */}
      <section className="py-24 bg-slate-50">
        <div className="max-w-5xl mx-auto px-4 sm:px-6">
          <motion.div
            variants={stagger}
            initial="hidden"
            whileInView="visible"
            viewport={{ once: true, margin: "-80px" }}
            className="text-center mb-16"
          >
            <motion.p variants={fadeUp} className="text-brand-600 font-semibold text-sm uppercase tracking-widest mb-2">
              How It Works
            </motion.p>
            <motion.h2 variants={fadeUp} className="text-4xl font-extrabold text-slate-900 tracking-tight">
              Three steps to clarity
            </motion.h2>
          </motion.div>

          <motion.div
            variants={stagger}
            initial="hidden"
            whileInView="visible"
            viewport={{ once: true }}
            className="relative flex flex-col md:flex-row items-start gap-8"
          >
            {/* Connector line */}
            <div
              aria-hidden
              className="hidden md:block absolute top-8 left-[13%] right-[13%] h-0.5 bg-gradient-to-r from-brand-200 via-brand-400 to-brand-200"
            />

            {STEPS.map((step, i) => (
              <motion.div
                key={step.label}
                variants={fadeUp}
                custom={i}
                className="relative flex-1 flex flex-col items-center text-center gap-4"
              >
                <div className="relative w-16 h-16 rounded-2xl bg-white border-2 border-brand-200 shadow-md
                  flex items-center justify-center text-brand-600 z-10">
                  <step.icon size={26} />
                  <span className="absolute -top-2.5 -right-2.5 w-6 h-6 rounded-full bg-brand-600 text-white text-xs font-bold flex items-center justify-center shadow-sm">
                    {i + 1}
                  </span>
                </div>
                <div>
                  <h3 className="font-bold text-slate-900 text-base">{step.label}</h3>
                  <p className="text-slate-500 text-sm mt-1">{step.desc}</p>
                </div>
              </motion.div>
            ))}
          </motion.div>
        </div>
      </section>

      {/* ── CTA BANNER ── */}
      <section className="py-24 bg-gradient-to-br from-brand-700 via-brand-600 to-blue-500">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.6 }}
          className="max-w-3xl mx-auto px-4 sm:px-6 text-center flex flex-col items-center gap-6"
        >
          <div className="w-14 h-14 rounded-2xl bg-white/15 flex items-center justify-center text-white">
            <Radar size={28} />
          </div>
          <h2 className="text-4xl font-extrabold text-white leading-tight">
            Ready to optimize your resume?
          </h2>
          <p className="text-blue-100 text-lg">
            Upload your PDF and paste a job description — get results in seconds.
            No account required.
          </p>
          <Link
            to="/analyze"
            id="cta-banner-analyze"
            className="flex items-center gap-2 px-8 py-3.5 rounded-xl bg-white text-brand-700 font-bold text-base
              hover:bg-blue-50 active:scale-95 transition-all shadow-xl"
          >
            Start Analyzing Free
            <ArrowRight size={18} />
          </Link>
        </motion.div>
      </section>

      {/* ── FOOTER ── */}
      <footer className="bg-slate-900 text-slate-400 py-10">
        <div className="max-w-6xl mx-auto px-4 sm:px-6 flex flex-col sm:flex-row items-center justify-between gap-4">
          <div className="flex items-center gap-2">
            <div className="p-1 rounded-md bg-brand-600 text-white">
              <Radar size={14} />
            </div>
            <span className="font-bold text-white text-sm">
              Resume<span className="text-brand-400">Radar</span>
            </span>
          </div>
          <p className="text-sm">
            Built with FastAPI + Sentence-Transformers + React &mdash; Open Source
          </p>
          <div className="flex items-center gap-4 text-sm">
            <a href="#features" className="hover:text-white transition-colors">Features</a>
            <Link to="/analyze" className="hover:text-white transition-colors">Try it</Link>
            <a href="https://github.com/anujott-codes/ResumeRadar" target="_blank" rel="noopener noreferrer" className="hover:text-white transition-colors">GitHub</a>
          </div>
        </div>
      </footer>
    </PageLayout>
  );
}
