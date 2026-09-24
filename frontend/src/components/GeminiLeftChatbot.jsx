/**
 * GeminiLeftChatbot.jsx — Embedded Google Gemini 2.5 Flash AI Chatbot
 * Housed directly inside the Left Sidebar alongside the Control Boxes.
 * 
 * Features:
 * - Direct execution of 6 Core Tactical Intelligence Tasks:
 *   1. 🎯 Identify syndicate hierarchy & kingpin
 *   2. 💸 Trace 3-hop money trail & mule accounts
 *   3. 🌲 Run Isolation Forest anomaly detection
 *   4. ⚖️ Draft Section 102 CrPC account freeze order
 *   5. 💥 Find critical communication bridges (cut vertices)
 *   6. 📜 Summarize GraphRAG evidence citations
 * - Natural Language Narrative Ingestion (extracts nodes & edges directly into active graph)
 * - Evidence attachment upload (PDF, CSV, TXT)
 * - 1-Click Copy, markdown formatting, and interactive clickable entity chips
 */

import React, { useState, useRef, useEffect } from "react";
import {
  Sparkles, Send, Bot, User, Trash2, Copy, Check, Paperclip,
  ArrowUpRight, Loader2, ShieldAlert, FileText, CheckCircle2
} from "lucide-react";
import { api } from "../lib/api";

const SUGGESTED_PROMPTS = [
  { label: "🎯 Syndicate Hierarchy & Kingpin", prompt: "Identify syndicate hierarchy & kingpin" },
  { label: "💸 3-Hop Money Trail & Mules", prompt: "Trace 3-hop money trail & mule accounts" },
  { label: "🌲 Isolation Forest Anomalies", prompt: "Run Isolation Forest anomaly detection" },
  { label: "⚖️ Section 102 CrPC Freeze Order", prompt: "Draft Section 102 CrPC account freeze order" },
  { label: "💥 Critical Bridges (Cut Vertices)", prompt: "Find critical communication bridges (cut vertices)" },
  { label: "📜 GraphRAG Evidence Citations", prompt: "Summarize GraphRAG evidence citations" },
];

export default function GeminiLeftChatbot({
  nodes = [],
  edges = [],
  caseId = "CASE-2024-MH-088",
  onGraphUpdate,
  onSelectNode,
  onToast,
}) {
  const [messages, setMessages] = useState([
    {
      id: "m0",
      sender: "gemini",
      text: `### 🛡️ CrimeNet Gemini 2.5 Flash Active\n\nI am your tactical AI intelligence partner grounded in active network topology (**${nodes.length} entities**, **${edges.length} edges**), **scikit-learn Isolation Forest**, and **GraphRAG** evidence.\n\nChoose an inquiry below, ask any tactical question, or paste suspect facts to build the graph:`,
      timestamp: "Just now",
      model: "Google Gemini 2.5 Flash",
    },
  ]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const [copiedId, setCopiedId] = useState(null);
  const [attachedFile, setAttachedFile] = useState(null);
  const messagesEndRef = useRef(null);
  const fileInputRef = useRef(null);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, loading]);

  const handleFileChange = (e) => {
    if (e.target.files && e.target.files[0]) {
      const file = e.target.files[0];
      setAttachedFile(file);
      onToast?.(`Evidence attached: ${file.name}`);
    }
  };

  const handleSend = async (overridePrompt) => {
    const query = (overridePrompt || input).trim();
    if (!query && !attachedFile) return;

    const userText = query || (attachedFile ? `Uploaded evidence file: ${attachedFile.name}` : "");
    const userMsgId = `usr_${Date.now()}`;
    const userMsg = {
      id: userMsgId,
      sender: "user",
      text: userText,
      timestamp: new Date().toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" }),
    };

    setMessages((prev) => [...prev, userMsg]);
    setInput("");
    setLoading(true);

    try {
      // 1. If file attached, upload and index via RAG
      if (attachedFile) {
        onToast?.(`Indexing evidence: ${attachedFile.name}...`);
        const uploadRes = await api.uploadEvidence(attachedFile, caseId);
        if (uploadRes?.graph?.nodes) {
          onGraphUpdate?.(uploadRes.graph.nodes, uploadRes.graph.edges);
        }
        setAttachedFile(null);
        if (fileInputRef.current) fileInputRef.current.value = "";
      }

      // 2. Query Gemini Agent with contextual grounding
      const historyPayload = messages.slice(-6).map((m) => ({
        role: m.sender === "user" ? "user" : "model",
        text: m.text,
      }));

      const res = await api.geminiChat({
        message: query || "Analyze the attached evidence document",
        caseId,
        history: historyPayload,
        nodes,
        edges,
      });

      const geminiMsg = {
        id: `gem_${Date.now()}`,
        sender: "gemini",
        text: res.reply || "No response received.",
        timestamp: new Date().toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" }),
        model: res.model || "Gemini 2.5 Flash",
        extractedCount: res.extractedCount || 0,
        newNodes: res.newNodes || [],
      };

      setMessages((prev) => [...prev, geminiMsg]);

      // If narrative ingestion yielded new nodes/edges, notify canvas!
      if (res.newNodes && res.newNodes.length > 0) {
        onToast?.(`[Gemini Extraction] Added ${res.newNodes.length} entities to operational graph.`);
        if (onGraphUpdate) {
          const mergedNodes = [...nodes];
          const existIds = new Set(nodes.map((n) => n.id));
          res.newNodes.forEach((n) => {
            if (!existIds.has(n.id)) mergedNodes.push(n);
          });
          const mergedEdges = [...edges, ...(res.newEdges || [])];
          onGraphUpdate(mergedNodes, mergedEdges);
        }
      }
    } catch (err) {
      console.error("Gemini Left Chatbot Error:", err);
      setMessages((prev) => [
        ...prev,
        {
          id: `err_${Date.now()}`,
          sender: "gemini",
          text: `⚠️ **Service Notice**: ${err.message || "Backend offline"}. Please verify connection to port 8000.`,
          timestamp: new Date().toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" }),
          model: "System Notice",
        },
      ]);
    } finally {
      setLoading(false);
    }
  };

  const handleCopy = (id, text) => {
    navigator.clipboard.writeText(text);
    setCopiedId(id);
    setTimeout(() => setCopiedId(null), 2000);
  };

  const handleClearChat = () => {
    setMessages([
      {
        id: `m_${Date.now()}`,
        sender: "gemini",
        text: "🧹 Chat cleared. Operational graph context and GraphRAG knowledge base remain loaded.",
        timestamp: "Just now",
        model: "Google Gemini 2.5 Flash",
      },
    ]);
  };

  return (
    <div
      style={{
        display: "flex",
        flexDirection: "column",
        height: "100%",
        minHeight: 0,
        background: "var(--panel, #ffffff)",
        borderRadius: 6,
        overflow: "hidden",
      }}
    >
      {/* ── Subheader / Telemetry Bar ───────────────────────────────────────── */}
      <div
        style={{
          display: "flex",
          alignItems: "center",
          justifyContent: "space-between",
          padding: "7px 10px",
          background: "linear-gradient(90deg, #f8fafc 0%, #f1f5f9 100%)",
          borderBottom: "1px solid var(--border, #e2e8f0)",
          flexShrink: 0,
        }}
      >
        <div style={{ display: "flex", alignItems: "center", gap: 6 }}>
          <div
            style={{
              width: 22,
              height: 22,
              borderRadius: "50%",
              background: "linear-gradient(135deg, #4285F4 0%, #9B72CF 50%, #D96570 100%)",
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
              boxShadow: "0 1px 4px rgba(66, 133, 244, 0.3)",
            }}
          >
            <Sparkles size={12} color="#ffffff" />
          </div>
          <div>
            <span style={{ fontSize: 11.5, fontWeight: 700, color: "var(--text-1, #0f172a)" }}>
              Gemini 2.5 Flash
            </span>
            <span style={{ fontSize: 10, color: "#10b981", marginLeft: 6, fontWeight: 600 }}>
              ● Live API
            </span>
          </div>
        </div>

        <button
          onClick={handleClearChat}
          title="Clear Chat History"
          style={{
            background: "transparent",
            border: "none",
            color: "#94a3b8",
            cursor: "pointer",
            padding: 4,
            borderRadius: 4,
          }}
        >
          <Trash2 size={13} />
        </button>
      </div>

      {/* ── Quick Tactical Prompt Chips ─────────────────────────────────────── */}
      <div
        style={{
          padding: "6px 8px",
          background: "#ffffff",
          borderBottom: "1px solid #f1f5f9",
          display: "flex",
          gap: 4,
          overflowX: "auto",
          whiteSpace: "nowrap",
          scrollbarWidth: "none",
          flexShrink: 0,
        }}
      >
        {SUGGESTED_PROMPTS.map((item, idx) => (
          <button
            key={idx}
            onClick={() => handleSend(item.prompt)}
            disabled={loading}
            style={{
              padding: "3px 8px",
              borderRadius: 12,
              border: "1px solid #e2e8f0",
              background: "#f8fafc",
              color: "#334155",
              fontSize: 10.5,
              fontWeight: 500,
              cursor: "pointer",
              flexShrink: 0,
              transition: "all 0.15s ease",
            }}
            onMouseEnter={(e) => {
              e.currentTarget.style.background = "#eef2ff";
              e.currentTarget.style.borderColor = "#c7d2fe";
            }}
            onMouseLeave={(e) => {
              e.currentTarget.style.background = "#f8fafc";
              e.currentTarget.style.borderColor = "#e2e8f0";
            }}
          >
            {item.label}
          </button>
        ))}
      </div>

      {/* ── Chat Messages Scroll Area ───────────────────────────────────────── */}
      <div
        style={{
          flex: 1,
          overflowY: "auto",
          padding: "10px",
          display: "flex",
          flexDirection: "column",
          gap: 12,
          background: "#f8fafc",
        }}
      >
        {messages.map((m) => {
          const isUser = m.sender === "user";
          return (
            <div
              key={m.id}
              style={{
                display: "flex",
                flexDirection: "column",
                alignItems: isUser ? "flex-end" : "flex-start",
                maxWidth: "100%",
              }}
            >
              <div
                style={{
                  display: "flex",
                  alignItems: "flex-start",
                  gap: 6,
                  flexDirection: isUser ? "row-reverse" : "row",
                  maxWidth: "96%",
                }}
              >
                {!isUser ? (
                  <div
                    style={{
                      width: 22,
                      height: 22,
                      borderRadius: "50%",
                      background: "linear-gradient(135deg, #4285F4, #9B72CF)",
                      display: "flex",
                      alignItems: "center",
                      justifyContent: "center",
                      flexShrink: 0,
                      marginTop: 2,
                    }}
                  >
                    <Sparkles size={12} color="#ffffff" />
                  </div>
                ) : (
                  <div
                    style={{
                      width: 22,
                      height: 22,
                      borderRadius: "50%",
                      background: "#334155",
                      display: "flex",
                      alignItems: "center",
                      justifyContent: "center",
                      flexShrink: 0,
                      marginTop: 2,
                    }}
                  >
                    <User size={12} color="#ffffff" />
                  </div>
                )}

                <div
                  style={{
                    background: isUser ? "#1e293b" : "#ffffff",
                    color: isUser ? "#f8fafc" : "#0f172a",
                    padding: isUser ? "8px 12px" : "10px 12px",
                    borderRadius: isUser ? "14px 14px 3px 14px" : "14px 14px 14px 3px",
                    border: isUser ? "none" : "1px solid #e2e8f0",
                    boxShadow: "0 1px 2px rgba(0,0,0,0.04)",
                    fontSize: 12,
                    lineHeight: 1.5,
                    whiteSpace: "pre-wrap",
                    wordBreak: "break-word",
                  }}
                >
                  {m.text}

                  {m.newNodes && m.newNodes.length > 0 && (
                    <div style={{ marginTop: 6, display: "flex", flexWrap: "wrap", gap: 4 }}>
                      {m.newNodes.map((nn) => (
                        <button
                          key={nn.id}
                          onClick={() => onSelectNode?.(nn.id)}
                          style={{
                            display: "inline-flex",
                            alignItems: "center",
                            gap: 3,
                            padding: "2px 6px",
                            borderRadius: 10,
                            background: "#ecfdf5",
                            color: "#059669",
                            border: "1px solid #a7f3d0",
                            fontSize: 10.5,
                            cursor: "pointer",
                            fontWeight: 600,
                          }}
                        >
                          <span>{nn.label}</span>
                          <ArrowUpRight size={10} />
                        </button>
                      ))}
                    </div>
                  )}
                </div>
              </div>

              {/* Message metadata & copy button */}
              <div
                style={{
                  display: "flex",
                  alignItems: "center",
                  gap: 6,
                  marginTop: 3,
                  marginRight: isUser ? 28 : 0,
                  marginLeft: !isUser ? 28 : 0,
                  fontSize: 9.5,
                  color: "#94a3b8",
                }}
              >
                <span>{m.timestamp}</span>
                {!isUser && (
                  <>
                    <span>·</span>
                    <button
                      onClick={() => handleCopy(m.id, m.text)}
                      style={{
                        background: "none",
                        border: "none",
                        color: "#94a3b8",
                        cursor: "pointer",
                        display: "flex",
                        alignItems: "center",
                        gap: 2,
                        padding: 0,
                      }}
                    >
                      {copiedId === m.id ? (
                        <>
                          <Check size={10} color="#16a34a" /> <span style={{ color: "#16a34a" }}>Copied</span>
                        </>
                      ) : (
                        <>
                          <Copy size={10} /> Copy
                        </>
                      )}
                    </button>
                  </>
                )}
              </div>
            </div>
          );
        })}

        {loading && (
          <div style={{ display: "flex", alignItems: "center", gap: 6 }}>
            <div
              style={{
                width: 22,
                height: 22,
                borderRadius: "50%",
                background: "linear-gradient(135deg, #4285F4, #9B72CF)",
                display: "flex",
                alignItems: "center",
                justifyContent: "center",
              }}
            >
              <Sparkles size={12} color="#ffffff" />
            </div>
            <div
              style={{
                background: "#ffffff",
                border: "1px solid #e2e8f0",
                padding: "6px 10px",
                borderRadius: "14px 14px 14px 3px",
                display: "flex",
                alignItems: "center",
                gap: 6,
                fontSize: 11,
                color: "#64748b",
              }}
            >
              <Loader2 size={12} className="spin" />
              <span>Gemini 2.5 Flash is analyzing network & statutes...</span>
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      {/* ── Attached File Indicator ─────────────────────────────────────────── */}
      {attachedFile && (
        <div
          style={{
            padding: "4px 10px",
            background: "#eff6ff",
            borderTop: "1px solid #bfdbfe",
            display: "flex",
            alignItems: "center",
            justifyContent: "space-between",
            fontSize: 11,
            color: "#1d4ed8",
          }}
        >
          <div style={{ display: "flex", alignItems: "center", gap: 5 }}>
            <FileText size={12} />
            <span>Attached: {attachedFile.name}</span>
          </div>
          <button
            onClick={() => setAttachedFile(null)}
            style={{
              background: "none",
              border: "none",
              color: "#6b7280",
              cursor: "pointer",
              fontSize: 12,
            }}
          >
            ✕
          </button>
        </div>
      )}

      {/* ── Bottom Input & Action Bar ───────────────────────────────────────── */}
      <div
        style={{
          padding: "8px 10px",
          background: "#ffffff",
          borderTop: "1px solid #e2e8f0",
          flexShrink: 0,
        }}
      >
        <form
          onSubmit={(e) => {
            e.preventDefault();
            handleSend();
          }}
          style={{
            display: "flex",
            alignItems: "center",
            background: "#f1f5f9",
            borderRadius: 20,
            padding: "3px 6px 3px 10px",
            border: "1px solid #cbd5e1",
          }}
        >
          {/* File Attachment Input */}
          <input
            type="file"
            ref={fileInputRef}
            style={{ display: "none" }}
            accept=".pdf,.csv,.txt"
            onChange={handleFileChange}
          />
          <button
            type="button"
            onClick={() => fileInputRef.current?.click()}
            title="Attach FIR PDF / CDR CSV"
            style={{
              background: "none",
              border: "none",
              color: attachedFile ? "#2563eb" : "#64748b",
              cursor: "pointer",
              padding: 4,
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
              marginRight: 4,
            }}
          >
            <Paperclip size={14} />
          </button>

          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Ask Gemini or paste suspect narrative..."
            disabled={loading}
            style={{
              flex: 1,
              border: "none",
              background: "transparent",
              outline: "none",
              fontSize: 11.5,
              color: "#0f172a",
            }}
          />

          <button
            type="submit"
            disabled={(!input.trim() && !attachedFile) || loading}
            style={{
              width: 28,
              height: 28,
              borderRadius: "50%",
              border: "none",
              background: (input.trim() || attachedFile) && !loading
                ? "linear-gradient(135deg, #4285F4 0%, #9B72CF 100%)"
                : "#cbd5e1",
              color: "#ffffff",
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
              cursor: (input.trim() || attachedFile) && !loading ? "pointer" : "default",
              transition: "transform 0.15s ease",
            }}
          >
            <Send size={12} />
          </button>
        </form>
      </div>
    </div>
  );
}
