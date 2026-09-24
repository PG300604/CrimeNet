/**
 * TacticalCommandBar.jsx — CrimeNet AI Narrative Ingestion & @feedback Bar
 * High-visibility top command center spanning the entire application header.
 * Allows pasting suspect facts, uploading evidence files, and executing @feedback.
 */

import React, { useState, useRef } from "react";
import { Sparkles, Paperclip, Send, Loader2, ShieldAlert, FileText, CheckCircle2 } from "lucide-react";
import { api } from "../lib/api";

export default function TacticalCommandBar({
  caseId = "CASE-2024-MH-088",
  onGraphUpdate,
  onNotify,
  onToggleGeminiChat,
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
      // 1. Human-in-the-Loop @feedback command
      if (cleanPrompt.toLowerCase().startsWith("@feedback")) {
        setStatusText("Applying human ground truth feedback & re-aligning AI context...");
        const res = await api.submitFeedback(cleanPrompt, caseId);
        onNotify?.(`[Feedback Applied] ${res.message} (Audit: ${res.auditId || "Logged"})`);
        setPrompt("");
        setStatusText("");
        setLoading(false);
        return;
      }

      // 2. Evidence file upload (RAG chunking)
      if (attachedFile) {
        setStatusText(`Chunking & embedding evidence: ${attachedFile.name}...`);
        const uploadRes = await api.uploadEvidence(attachedFile, caseId);
        if (uploadRes?.graph?.nodes) {
          onGraphUpdate?.(uploadRes.graph.nodes, uploadRes.graph.edges);
        }
        onNotify?.(`RAG Indexed ${uploadRes.chunksIndexed} chunks & ${uploadRes.extractedEntities} entities.`);
        setAttachedFile(null);
        if (fileInputRef.current) fileInputRef.current.value = "";
      }

      // 3. Narrative text-to-graph extraction
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
    <header style={{
      display: "flex",
      alignItems: "center",
      justifyContent: "space-between",
      padding: "8px 16px",
      background: "var(--panel, #ffffff)",
      borderBottom: "2px solid var(--border, #e2e8f0)",
      boxShadow: "0 2px 10px rgba(0,0,0,0.06)",
      zIndex: 100,
      flexShrink: 0,
      gap: 14
    }}>
      {/* Brand Badge */}
      <div style={{ display: "flex", alignItems: "center", gap: 8, minWidth: 200 }}>
        <div style={{
          width: 30,
          height: 30,
          borderRadius: 6,
          background: "linear-gradient(135deg, #10b981, #059669)",
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
          color: "#fff",
          boxShadow: "0 2px 6px rgba(16,185,129,0.3)"
        }}>
          <ShieldAlert size={18} />
        </div>
        <div>
          <div style={{ fontSize: 13, fontWeight: 700, letterSpacing: "-0.01em", color: "var(--text-1, #0f172a)", display: "flex", alignItems: "center", gap: 6 }}>
            <span>CrimeNet AI</span>
            <span style={{ fontSize: 9, background: "rgba(16,185,129,0.15)", color: "#10b981", padding: "1px 5px", borderRadius: 4, fontWeight: 700 }}>
              LE EDITION
            </span>
          </div>
          <div style={{ fontSize: 10.5, color: "var(--text-muted, #94a3b8)" }}>
            Indian Criminal Network Intelligence
          </div>
        </div>
      </div>

      {/* Main Command Input */}
      <form onSubmit={handleExecute} style={{ display: "flex", alignItems: "center", gap: 8, flex: 1, maxWidth: 860 }}>
        <div style={{ flex: 1, position: "relative", display: "flex", alignItems: "center" }}>
          <Sparkles size={14} style={{ position: "absolute", left: 11, color: "#f59e0b" }} />
          <input
            type="text"
            value={prompt}
            onChange={(e) => setPrompt(e.target.value)}
            placeholder="Type anything: suspect name, phone, UPI, FIR narrative, or enter @feedback to correct facts…"
            disabled={loading}
            style={{
              width: "100%",
              padding: "8px 12px 8px 34px",
              background: "var(--panel-2, #f8fafc)",
              color: "var(--text-1, #0f172a)",
              border: "1px solid var(--border, #cbd5e1)",
              borderRadius: 6,
              fontSize: 12.5,
              outline: "none",
              transition: "border-color 0.15s, box-shadow 0.15s",
            }}
          />
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
          style={{
            display: "inline-flex",
            alignItems: "center",
            gap: 5,
            padding: "7px 11px",
            fontSize: 11.5,
            fontWeight: 500,
            background: attachedFile ? "rgba(16,185,129,0.15)" : "var(--panel-2, #f8fafc)",
            color: attachedFile ? "#10b981" : "var(--text-2, #475569)",
            border: attachedFile ? "1px solid #10b981" : "1px solid var(--border, #cbd5e1)",
            borderRadius: 6,
            cursor: "pointer",
            whiteSpace: "nowrap"
          }}
          title={attachedFile ? `Attached: ${attachedFile.name}` : "Attach FIR PDF or CDR/Bank CSV"}
        >
          <Paperclip size={13} />
          <span>{attachedFile ? attachedFile.name.slice(0, 14) + "…" : "Attach Evidence"}</span>
        </button>

        {/* Submit Button */}
        <button
          type="submit"
          disabled={loading || (!prompt.trim() && !attachedFile)}
          style={{
            display: "inline-flex",
            alignItems: "center",
            gap: 6,
            padding: "7px 16px",
            fontSize: 12.5,
            fontWeight: 600,
            background: loading ? "#94a3b8" : "linear-gradient(135deg, #10b981, #059669)",
            color: "#ffffff",
            border: "none",
            borderRadius: 6,
            cursor: loading ? "not-allowed" : "pointer",
            boxShadow: "0 2px 6px rgba(16,185,129,0.3)",
            whiteSpace: "nowrap"
          }}
        >
          {loading ? <Loader2 size={13} className="animate-spin" /> : <Send size={13} />}
          <span>{loading ? "Analyzing…" : "Run AI Analysis"}</span>
        </button>
      </form>

      {/* Gemini AI Chat Trigger & Status */}
      <div style={{ display: "flex", alignItems: "center", gap: 10, fontSize: 11, color: "var(--text-muted, #94a3b8)" }}>
        {statusText ? (
          <div style={{ display: "flex", alignItems: "center", gap: 5, color: "#3b82f6", fontWeight: 500 }}>
            <Loader2 size={12} className="animate-spin" />
            <span>{statusText}</span>
          </div>
        ) : (
          <div style={{ display: "flex", alignItems: "center", gap: 5 }}>
            <span style={{ width: 7, height: 7, borderRadius: "50%", background: "#10b981" }} />
            <span>API Online</span>
          </div>
        )}

        <button
          type="button"
          onClick={onToggleGeminiChat}
          style={{
            display: "inline-flex",
            alignItems: "center",
            gap: 6,
            padding: "6px 12px",
            borderRadius: 6,
            border: "1px solid #c7d2fe",
            background: "linear-gradient(135deg, #4285F4 0%, #9B72CF 50%, #D96570 100%)",
            color: "#ffffff",
            fontWeight: 600,
            fontSize: 12,
            cursor: "pointer",
            boxShadow: "0 2px 8px rgba(66, 133, 244, 0.35)",
            whiteSpace: "nowrap"
          }}
        >
          <Sparkles size={13} />
          <span>Gemini AI</span>
        </button>
      </div>
    </header>
  );
}
