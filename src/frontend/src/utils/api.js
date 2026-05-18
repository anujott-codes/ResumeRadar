import axios from "axios";

const api = axios.create({
  baseURL: "/api",
  timeout: 60000,
});

/**
 * Analyze a resume against a job description.
 * @param {File} resumeFile - PDF file object
 * @param {string} jdText - Job description text
 * @returns {Promise<PredictionResponse>}
 */
export async function analyzeResume(resumeFile, jdText) {
  const form = new FormData();
  form.append("resume", resumeFile);
  form.append("jd_text", jdText);

  const { data } = await api.post("/analyze", form, {
    headers: { "Content-Type": "multipart/form-data" },
  });
  return data;
}

export default api;
