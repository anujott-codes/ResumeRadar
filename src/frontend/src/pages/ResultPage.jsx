import { useLocation, useNavigate, Link, Navigate } from "react-router-dom";
import { motion } from "framer-motion";
import {
  CheckCircle2,
  XCircle,
  Lightbulb,
  ArrowLeft,
  RotateCcw,
  FileText,
  TrendingUp,
  Target,
  Users,
  BookOpen,
} from "lucide-react";
import PageLayout from "../components/layout/PageLayout";
import ScoreRing from "../components/ui/ScoreRing";
import Card from "../components/ui/Card";
import Button from "../components/ui/Button";

/* ── Animation variants ── */
const stagger = {
  hidden: {},
  visible: { transition: { staggerChildren: 0.07 } },
};
const fadeUp = {
  hidden: { opacity: 0, y: 14 },
  visible: { opacity: 1, y: 0, transition: { duration: 0.38, ease: "easeOut" } },
};
const chipAnim = {
  hidden: { opacity: 0, scale: 0.8 },
  visible: { opacity: 1, scale: 1, transition: { duration: 0.25 } },
};

/* ── Stat mini-card ── */
function StatCard({ label, value, icon: Icon, color, delay }) {
  const pct = Math.round(value * 100);
  return (
    <motion.div
      initial={{ opacity: 0, y: 16 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.45, delay }}
      className="flex-1 min-w-[140px] bg-white rounded-2xl border border-slate-100 shadow-sm p-5 flex flex-col gap-2"
    >
      <div className={`w-9 h-9 rounded-xl flex items-center justify-center ${color}`}>
        <Icon size={18} />
      </div>
      <p className="text-2xl font-extrabold text-slate-900">{pct}%</p>
      <p className="text-xs font-semibold text-slate-400 uppercase tracking-wider">{label}</p>
      {/* Mini bar */}
      <div className="h-1.5 rounded-full bg-slate-100 overflow-hidden">
        <motion.div
          initial={{ width: 0 }}
          animate={{ width: `${pct}%` }}
          transition={{ duration: 1, delay: delay + 0.3, ease: "easeOut" }}
          className="h-full rounded-full"
          style={{ backgroundColor: color.includes("brand") ? "#2563eb" : color.includes("emerald") ? "#10b981" : "#8b5cf6" }}
        />
      </div>
    </motion.div>
  );
}

/* ── Chip grid ── */
function ChipGrid({ items, variant }) {
  const styles = {
    matched: "chip-matched",
    missing: "chip-missing",
    soft: "chip-soft",
  };

  return (
    <motion.div
      variants={stagger}
      initial="hidden"
      animate="visible"
      className="flex flex-wrap gap-2"
    >
      {items.map((item) => (
        <motion.span
          key={item.jd_skill}
          variants={chipAnim}
          className={styles[variant]}
          title={`Score: ${Math.round((item.score ?? 0) * 100)}%`}
        >
          {variant === "matched" && <CheckCircle2 size={12} />}
          {variant === "missing" && <XCircle size={12} />}
          {item.jd_skill}
        </motion.span>
      ))}
    </motion.div>
  );
}

/* ── Improvement suggestion generator ── */
function buildSuggestions(result) {
  const suggestions = [];

  const allMissing = [
    ...(result.hard_skills?.missing ?? []),
    ...(result.soft_skills?.missing ?? []),
  ];

  if (allMissing.length > 0) {
    suggestions.push(
      `Add explicit mentions of: ${allMissing.slice(0, 4).map((m) => m.jd_skill).join(", ")} to your resume.`
    );
  }

  const hardMissing = result.hard_skills?.missing ?? [];
  if (hardMissing.length > 0) {
    suggestions.push(
      `Consider upskilling or adding project experience in: ${hardMissing.map((m) => m.jd_skill).join(", ")}.`
    );
  }

  if (result.coverage < 0.7) {
    suggestions.push(
      "Your resume covers less than 70% of the JD's skills. Tailor your experience section to better reflect the required competencies."
    );
  }

  if (result.soft_similarity < 0.65) {
    suggestions.push(
      "Soft skills like leadership, communication, or problem-solving were underrepresented. Add concrete examples in your summary or bullet points."
    );
  }

  if (result.final_similarity >= 0.8) {
    suggestions.push(
      "Great match! Focus on quantifying your achievements (e.g., 'Reduced latency by 30%') to stand out further."
    );
  } else {
    suggestions.push(
      "Rewrite your professional summary to mirror the language and priorities of the job description."
    );
  }

  return suggestions;
}

export default function ResultPage() {
  const location = useLocation();
  const navigate  = useNavigate();

  const result   = location.state?.result;
  const fileName  = location.state?.fileName ?? "resume.pdf";

  if (!result) {
    return <Navigate to="/analyze" replace />;
  }

  const suggestions = buildSuggestions(result);

  const allMatched = [
    ...(result.hard_skills?.matched ?? []),
    ...(result.soft_skills?.matched ?? []).map((s) => ({ ...s, soft: true })),
  ];
  const allMissing = [
    ...(result.hard_skills?.missing ?? []),
    ...(result.soft_skills?.missing ?? []),
  ];
  const softMatched = result.soft_skills?.matched ?? [];

  return (
    <PageLayout>
      <div className="max-w-5xl mx-auto px-4 sm:px-6 py-12 space-y-8">

        {/* Top row: file info + back */}
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          className="flex items-center justify-between flex-wrap gap-3"
        >
          <div className="flex items-center gap-2 text-sm text-slate-500">
            <FileText size={15} className="text-brand-500" />
            <span className="font-medium text-slate-700">{fileName}</span>
          </div>
          <div className="flex gap-2">
            <Button variant="outline" size="sm" onClick={() => navigate("/analyze")}>
              <RotateCcw size={14} /> Re-analyze
            </Button>
            <Link to="/">
              <Button variant="ghost" size="sm">
                <ArrowLeft size={14} /> Home
              </Button>
            </Link>
          </div>
        </motion.div>

        {/* Main score card + stats */}
        <div className="grid grid-cols-1 md:grid-cols-[auto_1fr] gap-6">
          {/* Score ring */}
          <Card className="flex items-center justify-center p-10" delay={0}>
            <ScoreRing score={result.final_similarity} />
          </Card>

          {/* Stats */}
          <div className="flex flex-col gap-4">
            <h2 className="text-xl font-bold text-slate-900">Match Breakdown</h2>
            <div className="flex flex-wrap gap-4">
              <StatCard
                label="Coverage"
                value={result.coverage}
                icon={Target}
                color="bg-brand-50 text-brand-600"
                delay={0.1}
              />
              <StatCard
                label="Hard Skills"
                value={result.hard_similarity}
                icon={TrendingUp}
                color="bg-emerald-50 text-emerald-600"
                delay={0.18}
              />
              <StatCard
                label="Soft Skills"
                value={result.soft_similarity}
                icon={Users}
                color="bg-violet-50 text-violet-600"
                delay={0.26}
              />
            </div>
          </div>
        </div>

        {/* Matched Skills */}
        <Card delay={0.15}>
          <div className="flex items-center gap-2 mb-4">
            <div className="w-8 h-8 rounded-lg bg-emerald-50 text-emerald-600 flex items-center justify-center">
              <CheckCircle2 size={16} />
            </div>
            <div>
              <h3 className="font-bold text-slate-900">Matched Skills</h3>
              <p className="text-xs text-slate-400">Skills found in your resume that align with the JD</p>
            </div>
            <span className="ml-auto text-xs font-semibold px-2.5 py-1 rounded-full bg-emerald-50 text-emerald-700 border border-emerald-100">
              {allMatched.length} skills
            </span>
          </div>

          <ChipGrid items={allMatched.filter((s) => !s.soft)} variant="matched" />

          {softMatched.length > 0 && (
            <div className="mt-4">
              <p className="text-xs font-semibold text-slate-400 uppercase tracking-widest mb-2">Soft Skills</p>
              <ChipGrid items={softMatched} variant="soft" />
            </div>
          )}
        </Card>

        {/* Missing Skills */}
        <Card delay={0.2}>
          <div className="flex items-center gap-2 mb-4">
            <div className="w-8 h-8 rounded-lg bg-red-50 text-red-500 flex items-center justify-center">
              <XCircle size={16} />
            </div>
            <div>
              <h3 className="font-bold text-slate-900">Missing Skills</h3>
              <p className="text-xs text-slate-400">JD requirements not found in your resume</p>
            </div>
            <span className="ml-auto text-xs font-semibold px-2.5 py-1 rounded-full bg-red-50 text-red-700 border border-red-100">
              {allMissing.length} gaps
            </span>
          </div>

          {allMissing.length === 0 ? (
            <p className="text-emerald-600 text-sm font-medium flex items-center gap-2">
              <CheckCircle2 size={16} /> No critical skill gaps detected — excellent match!
            </p>
          ) : (
            <ChipGrid items={allMissing} variant="missing" />
          )}
        </Card>

        {/* Improvement Suggestions */}
        <Card delay={0.25}>
          <div className="flex items-center gap-2 mb-5">
            <div className="w-8 h-8 rounded-lg bg-amber-50 text-amber-500 flex items-center justify-center">
              <Lightbulb size={16} />
            </div>
            <div>
              <h3 className="font-bold text-slate-900">Improvement Suggestions</h3>
              <p className="text-xs text-slate-400">AI-generated tips to strengthen your application</p>
            </div>
          </div>

          <motion.ul
            variants={stagger}
            initial="hidden"
            animate="visible"
            className="space-y-3"
          >
            {suggestions.map((s, i) => (
              <motion.li
                key={i}
                variants={fadeUp}
                className="flex items-start gap-3 p-3.5 rounded-xl bg-slate-50 border border-slate-100"
              >
                <span className="w-5 h-5 rounded-full bg-brand-600 text-white text-xs flex items-center justify-center font-bold shrink-0 mt-0.5">
                  {i + 1}
                </span>
                <p className="text-sm text-slate-700 leading-relaxed">{s}</p>
              </motion.li>
            ))}
          </motion.ul>
        </Card>

        {/* CTA bottom */}
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.5 }}
          className="flex flex-col sm:flex-row items-center justify-center gap-4 pt-4 pb-10"
        >
          <Button variant="primary" size="lg" onClick={() => navigate("/analyze")}>
            <RotateCcw size={16} /> Analyze Another Resume
          </Button>
          <Link to="/">
            <Button variant="outline" size="lg">
              <ArrowLeft size={16} /> Back to Home
            </Button>
          </Link>
        </motion.div>
      </div>
    </PageLayout>
  );
}
