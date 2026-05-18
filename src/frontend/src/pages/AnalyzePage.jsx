import { useState, useRef, useCallback } from "react";
import { useNavigate } from "react-router-dom";
import { motion, AnimatePresence } from "framer-motion";
import {
  Upload,
  FileText,
  X,
  AlertCircle,
  ArrowRight,
  Loader2,
  CheckCircle2,
  Sparkles,
} from "lucide-react";
import PageLayout from "../components/layout/PageLayout";
import Button from "../components/ui/Button";
import { useAnalyze } from "../hooks/useAnalyze";

const MAX_FILE_BYTES = 5 * 1024 * 1024; // 5 MB
const MIN_JD_CHARS   = 50;

function FileUploadZone({ file, onFileSelect, onFileClear, error }) {
  const inputRef   = useRef(null);
  const [dragging, setDragging] = useState(false);

  const handleDrop = useCallback((e) => {
    e.preventDefault();
    setDragging(false);
    const dropped = e.dataTransfer.files[0];
    if (dropped) onFileSelect(dropped);
  }, [onFileSelect]);

  const handleDragOver = (e) => { e.preventDefault(); setDragging(true); };
  const handleDragLeave = () => setDragging(false);

  return (
    <div>
      {!file ? (
        <div
          id="resume-upload-zone"
          role="button"
          tabIndex={0}
          onClick={() => inputRef.current?.click()}
          onKeyDown={(e) => e.key === "Enter" && inputRef.current?.click()}
          onDrop={handleDrop}
          onDragOver={handleDragOver}
          onDragLeave={handleDragLeave}
          className={[
            "upload-zone",
            dragging ? "drag-over" : "",
            error ? "border-red-300 bg-red-50/30" : "",
          ].join(" ")}
        >
          <input
            ref={inputRef}
            type="file"
            accept=".pdf"
            className="hidden"
            onChange={(e) => e.target.files?.[0] && onFileSelect(e.target.files[0])}
          />
          <div className="flex flex-col items-center gap-3 pointer-events-none select-none">
            <div className={`w-14 h-14 rounded-2xl flex items-center justify-center
              ${dragging ? "bg-brand-100 text-brand-600" : "bg-slate-100 text-slate-400"} transition-colors`}>
              <Upload size={26} />
            </div>
            <div>
              <p className="font-semibold text-slate-700">
                {dragging ? "Drop it here!" : "Drag & drop your resume"}
              </p>
              <p className="text-sm text-slate-400 mt-0.5">
                or <span className="text-brand-600 underline underline-offset-2">browse files</span> — PDF only, max 5 MB
              </p>
            </div>
          </div>
        </div>
      ) : (
        <motion.div
          initial={{ opacity: 0, scale: 0.97 }}
          animate={{ opacity: 1, scale: 1 }}
          className="flex items-center justify-between gap-3 p-4 bg-brand-50 border border-brand-200 rounded-2xl"
        >
          <div className="flex items-center gap-3 min-w-0">
            <div className="w-10 h-10 rounded-xl bg-brand-600 flex items-center justify-center shrink-0">
              <FileText size={18} className="text-white" />
            </div>
            <div className="min-w-0">
              <p className="text-sm font-semibold text-slate-800 truncate">{file.name}</p>
              <p className="text-xs text-slate-400">{(file.size / 1024).toFixed(0)} KB</p>
            </div>
          </div>
          <div className="flex items-center gap-2 shrink-0">
            <CheckCircle2 size={16} className="text-emerald-500" />
            <button
              id="remove-file-btn"
              onClick={onFileClear}
              className="p-1.5 rounded-lg text-slate-400 hover:text-red-500 hover:bg-red-50 transition-colors"
              aria-label="Remove file"
            >
              <X size={16} />
            </button>
          </div>
        </motion.div>
      )}

      <AnimatePresence>
        {error && (
          <motion.p
            initial={{ opacity: 0, y: -4 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0 }}
            className="mt-2 text-sm text-red-600 flex items-center gap-1.5"
          >
            <AlertCircle size={14} /> {error}
          </motion.p>
        )}
      </AnimatePresence>
    </div>
  );
}

export default function AnalyzePage() {
  const navigate = useNavigate();
  const { analyze, loading, error: apiError } = useAnalyze();

  const [file,    setFile]    = useState(null);
  const [jdText,  setJdText]  = useState("");
  const [fileErr, setFileErr] = useState("");
  const [jdErr,   setJdErr]   = useState("");

  /* ── Validation ── */
  const validateFile = (f) => {
    if (!f) return "Please upload a PDF resume.";
    if (!f.name.toLowerCase().endsWith(".pdf")) return "Only PDF files are supported.";
    if (f.size > MAX_FILE_BYTES) return "File size exceeds 5 MB limit.";
    return "";
  };

  const handleFileSelect = (f) => {
    const err = validateFile(f);
    setFileErr(err);
    if (!err) setFile(f);
  };

  const handleFileClear = () => { setFile(null); setFileErr(""); };

  const jdCharCount = jdText.length;
  const jdValid     = jdCharCount >= MIN_JD_CHARS;
  const canSubmit   = file && jdValid && !fileErr && !loading;

  /* ── Submit ── */
  const handleSubmit = async (e) => {
    e.preventDefault();

    // Validate
    const fe = validateFile(file);
    if (fe) { setFileErr(fe); return; }
    if (!jdValid) { setJdErr(`Job description must be at least ${MIN_JD_CHARS} characters.`); return; }


    const result = await analyze(file, jdText);
    if (result) {
      navigate("/result", { state: { result, fileName: file.name } });
    }
  };

  return (
    <PageLayout>
      <div className="max-w-4xl mx-auto px-4 sm:px-6 py-16">
        {/* Header */}
        <motion.div
          initial={{ opacity: 0, y: 16 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.45 }}
          className="text-center mb-12"
        >
          <span className="inline-flex items-center gap-2 px-3.5 py-1.5 rounded-full bg-brand-50 border border-brand-100
            text-brand-700 text-xs font-semibold mb-4">
            <Sparkles size={12} />
            AI Analysis Engine
          </span>
          <h1 className="text-4xl sm:text-5xl font-extrabold text-slate-900 tracking-tight">
            Analyze Your Resume
          </h1>
          <p className="mt-4 text-slate-500 text-lg max-w-xl mx-auto">
            Upload your PDF resume and paste the job description below.
            Our NLP engine will score your match in seconds.
          </p>
        </motion.div>

        {/* Form card */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5, delay: 0.1 }}
          className="bg-white rounded-3xl border border-slate-100 shadow-xl p-8 sm:p-10"
        >
          <form onSubmit={handleSubmit} className="flex flex-col gap-8" noValidate>
            {/* Step 1: Resume Upload */}
            <div>
              <label className="block text-sm font-semibold text-slate-700 mb-3">
                <span className="inline-flex items-center gap-2">
                  <span className="w-6 h-6 rounded-full bg-brand-600 text-white text-xs flex items-center justify-center font-bold">1</span>
                  Upload Resume PDF
                </span>
              </label>
              <FileUploadZone
                file={file}
                onFileSelect={handleFileSelect}
                onFileClear={handleFileClear}
                error={fileErr}
              />
            </div>

            {/* Step 2: JD Text */}
            <div>
              <div className="flex items-center justify-between mb-3">
                <label htmlFor="jd-text" className="text-sm font-semibold text-slate-700">
                  <span className="inline-flex items-center gap-2">
                    <span className="w-6 h-6 rounded-full bg-brand-600 text-white text-xs flex items-center justify-center font-bold">2</span>
                    Paste Job Description
                  </span>
                </label>
                <span className={`text-xs font-medium ${jdValid ? "text-emerald-600" : "text-slate-400"}`}>
                  {jdCharCount} / {MIN_JD_CHARS}+ chars
                </span>
              </div>
              <textarea
                id="jd-text"
                rows={9}
                value={jdText}
                onChange={(e) => { setJdText(e.target.value); if (jdErr) setJdErr(""); }}
                placeholder="Paste the full job description here — the more detail, the better the analysis…"
                className={[
                  "w-full px-4 py-3 rounded-2xl border text-sm text-slate-800 placeholder-slate-300 resize-none",
                  "focus:outline-none focus:ring-2 focus:ring-brand-500 focus:border-transparent transition-all",
                  jdErr ? "border-red-300 bg-red-50/30" : "border-slate-200 bg-slate-50/50",
                ].join(" ")}
              />
              <AnimatePresence>
                {jdErr && (
                  <motion.p
                    initial={{ opacity: 0, y: -4 }}
                    animate={{ opacity: 1, y: 0 }}
                    exit={{ opacity: 0 }}
                    className="mt-1.5 text-sm text-red-600 flex items-center gap-1.5"
                  >
                    <AlertCircle size={14} /> {jdErr}
                  </motion.p>
                )}
              </AnimatePresence>
            </div>

            {/* API error */}
            <AnimatePresence>
              {apiError && (
                <motion.div
                  initial={{ opacity: 0, y: -8 }}
                  animate={{ opacity: 1, y: 0 }}
                  exit={{ opacity: 0 }}
                  className="flex items-start gap-3 p-4 rounded-xl bg-red-50 border border-red-200 text-red-700"
                >
                  <AlertCircle size={18} className="shrink-0 mt-0.5" />
                  <div>
                    <p className="font-semibold text-sm">Analysis failed</p>
                    <p className="text-sm mt-0.5 text-red-600">{apiError}</p>
                  </div>
                </motion.div>
              )}
            </AnimatePresence>


            {/* Submit */}
            <div className="flex flex-col sm:flex-row items-center justify-between gap-4 pt-2 border-t border-slate-100">
              <p className="text-xs text-slate-400 max-w-xs">
                Your resume is analyzed locally and never stored. Results are discarded after the session.
              </p>
              <Button
                id="analyze-submit-btn"
                type="submit"
                size="lg"
                loading={loading}
                disabled={!canSubmit}
                className="w-full sm:w-auto"
              >
                {loading ? "Analyzing…" : "Analyze Resume"}
                {!loading && <ArrowRight size={18} />}
              </Button>
            </div>
          </form>
        </motion.div>
      </div>
    </PageLayout>
  );
}
