/**
 * api.js — CrimeNet AI Backend REST Client
 * Connects the React frontend to the FastAPI RAG & Agentic backend.
 */

const BASE_URL = import.meta.env.VITE_API_URL || "http://localhost:8000/api";

export const api = {
  // Check health
  checkHealth: async () => {
    try {
      const res = await fetch("http://localhost:8000/");
      return await res.json();
    } catch (err) {
      console.warn("Backend not reachable:", err);
      return null;
    }
  },

  // 1. Cases
  getCases: async () => {
    const res = await fetch(`${BASE_URL}/cases`);
    if (!res.ok) throw new Error("Failed to fetch cases");
    return await res.json();
  },

  createCase: async (caseData) => {
    const res = await fetch(`${BASE_URL}/cases`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(caseData),
    });
    if (!res.ok) throw new Error("Failed to create case");
    return await res.json();
  },

  // 2. Graph
  getGraph: async (caseId) => {
    const res = await fetch(`${BASE_URL}/graph/${caseId}`);
    if (!res.ok) throw new Error("Failed to fetch graph");
    return await res.json();
  },

  // 3. Narrative Ingestion (Text-to-Graph)
  submitNarrative: async (narrative, caseId = "CASE-2024-MH-088") => {
    const res = await fetch(`${BASE_URL}/investigate/narrative`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ narrative, case_id: caseId }),
    });
    if (!res.ok) throw new Error("Failed to process narrative");
    return await res.json();
  },

  // 4. Evidence File Upload (RAG)
  uploadEvidence: async (file, caseId = "CASE-2024-MH-088") => {
    const formData = new FormData();
    formData.append("file", file);
    formData.append("case_id", caseId);
    formData.append("officer_badge", "INSP-4409");

    const res = await fetch(`${BASE_URL}/investigate/upload`, {
      method: "POST",
      body: formData,
    });
    if (!res.ok) throw new Error("Failed to upload evidence");
    return await res.json();
  },

  // 5. Entity Dossier (Agentic Synthesis + Citations)
  getEntityDossier: async (nodeId, caseId = "CASE-2024-MH-088") => {
    const res = await fetch(`${BASE_URL}/entity/${encodeURIComponent(nodeId)}/dossier?case_id=${encodeURIComponent(caseId)}`);
    if (!res.ok) throw new Error("Failed to generate dossier");
    return await res.json();
  },

  // 6. Follow the Money (3-hop BFS)
  followTheMoney: async (seedNodeId, caseId = "CASE-2024-MH-088", maxHops = 3) => {
    const res = await fetch(`${BASE_URL}/analytics/follow-money`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ seed_node_id: seedNodeId, case_id: caseId, max_hops: maxHops }),
    });
    if (!res.ok) throw new Error("Failed to trace financial flow");
    return await res.json();
  },

  // 7. Human-in-the-Loop Feedback (@feedback)
  submitFeedback: async (feedbackPrompt, caseId = "CASE-2024-MH-088") => {
    const res = await fetch(`${BASE_URL}/feedback`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ feedback_prompt: feedbackPrompt, case_id: caseId }),
    });
    if (!res.ok) throw new Error("Failed to submit feedback");
    return await res.json();
  },

  // 8. Action Dispatch (LOC, Freeze Account, Summons)
  dispatchAction: async (actionId, entityId, caseId = "CASE-2024-MH-088", parameters = {}) => {
    const res = await fetch(`${BASE_URL}/actions/dispatch`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        action_id: actionId,
        entity_id: entityId,
        case_id: caseId,
        parameters,
      }),
    });
    if (!res.ok) throw new Error("Failed to dispatch action");
    return await res.json();
  },

  // 9. Timeline & Alerts
  getTimeline: async (caseId = "CASE-2024-MH-088") => {
    const res = await fetch(`${BASE_URL}/cases/${caseId}/timeline`);
    if (!res.ok) throw new Error("Failed to fetch timeline");
    return await res.json();
  },

  getAlerts: async (caseId = "CASE-2024-MH-088") => {
    const res = await fetch(`${BASE_URL}/alerts?case_id=${caseId}`);
    if (!res.ok) throw new Error("Failed to fetch alerts");
    return await res.json();
  },

  // 10. Prosecutor Report
  getProsecutorReport: async (caseId = "CASE-2024-MH-088") => {
    const res = await fetch(`${BASE_URL}/cases/${caseId}/report`);
    if (!res.ok) throw new Error("Failed to generate report");
    return await res.json();
  },
};
