/**
 * TacticalCommandBar.jsx — CrimeNet AI Narrative Ingestion & @feedback Bar
 * Placed prominently at the top of the investigative canvas.
 * Allows pasting suspect facts, uploading evidence files, and executing @feedback.
 */

import React, { useState, useRef } from "react";
import { Sparkles, Paperclip, Send, Loader2, CheckCircle2, ShieldAlert } from "lucide-react";
import { api } from "../lib/api";

export default function TacticalCommandBar({
  caseId = "CASE-2024-MH-088",
  onGraphUpdate,
  onNotify,
}) {
  const [prompt, setPrompt] = useState("");
  const [loading, setLoading] = useState(false);
  const [statusText, setStatusText] = useState("");
  const [attachedFile, setAttachedFile] = useState(null);
  const fileInputRef = useRef(null);

  const handleFileChange = (e) => {
    if (e.target.files && e.target.files[0]) {
      setAttachedFile(e.target.files[0]);
      onNotify?.(`Attached evidence: ${e.target.files[0].name}`);
    }
  };

  const handleExecute = async (e) => {
    e?.preventDefault();
    if (!prompt.trim() && !attachedFile) return;

    setLoading(true);
    const cleanPrompt = prompt.trim();

    try {
      // 1. Check if user is issuing a Human-in-the-Loop @feedback command
      if (cleanPrompt.toLowerCase().startsWith("@feedback")) {
        setStatusText("Applying human ground truth feedback & re-aligning AI context...");
        const res = await api.submitFeedback(cleanPrompt, caseId);
        onNotify?.(`[Feedback Applied] ${res.message} (Audit: ${res.auditId || "Logged"})`);
        setPrompt("");
        setStatusText("");
        setLoading(false);
        return;
      }

      // 2. If evidence file is attached, upload & chunk via RAG
      if (attachedFile) {
        setStatusText(`Ingesting & chunking evidence: ${attachedFile.name}...`);
        const uploadRes = await api.uploadEvidence(attachedFile, caseId);
        if (uploadRes?.graph?.nodes) {
          onGraphUpdate?.(uploadRes.graph.nodes, uploadRes.graph.edges);
        }
        onNotify?.(`Indexed ${uploadRes.chunksIndexed} evidence chunks & ${uploadRes.extractedEntities} entities.`);
        setAttachedFile(null);
        if (fileInputRef.current) fileInputRef.current.value = "";
      }

      // 3. If narrative text is present, extract entities & relationships
      if (cleanPrompt) {
        setStatusText("CrimeNet AI cross-referencing narrative against criminal database...");
        const narrativeRes = await api.submitNarrative(cleanPrompt, caseId);
        if (narrativeRes?.graph?.nodes) {
          onGraphUpdate?.(narrativeRes.graph.nodes, narrativeRes.graph.edges);
        }
        onNotify?.(`Extracted ${narrativeRes.extractedCount} entities from narrative.`);
        setPrompt("");
      }
    } catch (err) {
      console.error("AI Analysis error:", err);
      onNotify?.(`Analysis failed: ${err.message || "Backend offline"}`);
    } finally {
      setLoading(false);
      setStatusText("");
    }
  };

  return (
    <div style={{
      display: "flex",
      flexDirection: "column",
      gap: 6,
      padding: "8px 14px",
      background: "var(--bg-secondary, #1e293b)",
      borderBottom: "1px solid var(--border-color, #334155)",
      boxShadow: "0 2px 8px rgba(0,0,0,0.15)"
    }}>
      <form onSubmit={handleExecute} style={{ display: "flex", alignItems: "center", gap: 10 }}>
        <div style={{ display: "flex", alignItems: "center", gap: 6, color: "#f59e0b", fontWeight: 600, fontSize: 13 }}>
          <Sparkles size={16} />
          <span>AI Command</span>
        </div>

        <div style={{ flex: 1, position: "relative", display: "flex", alignItems: "center" }}>
          <input
            type="text"
            value={prompt}
            onChange={(e) => setPrompt(e.target.value)}
            placeholder="Type anything: suspect name, phone, FIR narrative, or enter @feedback to correct facts…"
            disabled={loading}
            style={{
              width: "100%",
              padding: "7px 12px 7px 32px",
              background: "var(--bg-primary, #0f172a)",
              color: "var(--text-primary, #f8fafc)",
              border: "1px solid var(--border-color, #475569)",
              borderRadius: 6,
              fontSize: 13,
              outline: "none",
            }}
          />
          <span style={{ position: "absolute", left: 10, color: "var(--text-muted, #94a3b8)", fontSize: 12 }}>
            ❯
          </span>
        </div>

        {/* Hidden file input */}
        <input
          type="file"
          ref={fileInputRef}
          onChange={handleFileChange}
          style={{ display: "none" }}
          accept=".pdf,.csv,.txt,.json"
        />

        {/* Attach File Button */}
        <button
          type="button"
          onClick={() => fileInputRef.current?.click()}
          className="btn"
          style={{
            display: "flex",
            alignItems: "center",
            gap: 6,
            padding: "6px 12px",
            fontSize: 12,
            background: attachedFile ? "#059669" : "var(--bg-tertiary, #334155)",
            color: "#fff",
            border: "1px solid #475569",
            borderRadius: 6,
            cursor: "pointer"
          }}
          title={attachedFile ? `Attached: ${attachedFile.name}` : "Attach FIR PDF or CDR/Bank CSV"}
        >
          <Paperclip size={14} />
          <span>{attachedFile ? attachedFile.name.slice(0, 12) + "…" : "Attach Evidence"}</span>
        </button>

        {/* Submit Button */}
        <button
          type="submit"
          disabled={loading || (!prompt.trim() && !attachedFile)}
          style={{
            display: "flex",
            alignItems: "center",
            gap: 6,
            padding: "6px 16px",
            fontSize: 13,
            fontWeight: 600,
            background: loading ? "#64748b" : "linear-gradient(135deg, #2563eb, #1d4ed8)",
            color: "#fff",
            border: "none",
            borderRadius: 6,
            cursor: loading ? "not-allowed" : "pointer",
            boxShadow: "0 2px 4px rgba(37,99,235,0.3)"
          }}
        >
          {loading ? <Loader2 size={14} className="animate-spin" /> : <Send size={14} />}
          <span>{loading ? "Analyzing…" : "Run AI Analysis"}</span>
        </button>
      </form>

      {/* Real-time Status Notification Bar */}
      {statusText && (
        <div style={{
          fontSize: 12,
          color: "#38bdf8",
          display: "flex",
          alignItems: "center",
          gap: 6,
          paddingLeft: 4
        }}>
          <Loader2 size={12} className="animate-spin" />
          <span>{statusText}</span>
        </div>
      )}
    </div>
  );
}
