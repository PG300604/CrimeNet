import React, { useState } from "react";
import {
  X, BookOpen, Shield, Network, BrainCircuit, Terminal,
  Search, Check, Copy, ExternalLink, Zap, AlertTriangle, FileText
} from "lucide-react";

export default function UserDocumentationModal({ isOpen, onClose }) {
  const [activeTab, setActiveTab] = useState("overview"); // overview, analytics, ai, shortcuts
  const [copiedText, setCopiedText] = useState(null);
  const [filterQuery, setFilterQuery] = useState("");

  if (!isOpen) return null;

  const handleCopy = (text, id) => {
    navigator.clipboard.writeText(text);
    setCopiedText(id);
    setTimeout(() => setCopiedText(null), 2000);
  };

  return (
    <div className="crimenet-modal-backdrop" onClick={onClose} style={{
      position: "fixed",
      inset: 0,
      background: "rgba(0, 0, 0, 0.75)",
      backdropFilter: "blur(6px)",
      display: "flex",
      alignItems: "center",
      justifyContent: "center",
      zIndex: 1000,
      padding: 16,
    }}>
      <div
        className="crimenet-modal-window crimenet-fade-in"
        onClick={(e) => e.stopPropagation()}
        style={{
          width: 780,
          maxWidth: "95vw",
          maxHeight: "88vh",
          display: "flex",
          flexDirection: "column",
          background: "var(--panel)",
          border: "1px solid var(--border-2)",
          borderRadius: 12,
          boxShadow: "0 20px 50px rgba(0,0,0,0.5), 0 0 0 1px var(--border)",
          overflow: "hidden",
        }}
      >
        {/* Header */}
        <div style={{
          display: "flex",
          alignItems: "center",
          justifyContent: "space-between",
          padding: "14px 20px",
          background: "var(--panel-2)",
          borderBottom: "1px solid var(--border)",
        }}>
          <div style={{ display: "flex", alignItems: "center", gap: 10 }}>
            <div style={{
              width: 32,
              height: 32,
              borderRadius: 8,
              background: "var(--teal)",
              color: "#ffffff",
              display: "grid",
              placeItems: "center",
              boxShadow: "0 4px 12px rgba(79, 195, 247, 0.3)",
            }}>
              <BookOpen size={16} />
            </div>
            <div>
              <div style={{ fontSize: 14, fontWeight: 700, color: "var(--text)" }}>
                CrimeNet Operations Documentation
              </div>
              <div style={{ fontSize: 11, color: "var(--text-muted)" }}>
                Investigator Handbook & Platform Technical Reference
              </div>
            </div>
          </div>
          <button
            onClick={onClose}
            aria-label="Close documentation"
            style={{
              background: "transparent",
              border: "none",
              color: "var(--text-muted)",
              cursor: "pointer",
              padding: 6,
              borderRadius: 6,
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
            }}
          >
            <X size={18} />
          </button>
        </div>

        {/* Tab Navigation */}
        <div style={{
          display: "flex",
          gap: 6,
          padding: "8px 20px",
          background: "var(--panel-3)",
          borderBottom: "1px solid var(--border)",
        }}>
          {[
            { id: "overview", label: "Overview", icon: Shield },
            { id: "analytics", label: "Graph Analytics", icon: Network },
            { id: "ai", label: "AI Intelligence", icon: BrainCircuit },
            { id: "shortcuts", label: "Shortcuts & Actions", icon: Terminal },
          ].map((tab) => {
            const Icon = tab.icon;
            const active = activeTab === tab.id;
            return (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id)}
                style={{
                  display: "flex",
                  alignItems: "center",
                  gap: 6,
                  padding: "6px 12px",
                  borderRadius: 6,
                  border: active ? "1px solid var(--teal)" : "1px solid transparent",
                  background: active ? "var(--teal-s)" : "transparent",
                  color: active ? "var(--teal)" : "var(--text-muted)",
                  fontWeight: active ? 600 : 500,
                  fontSize: 12,
                  cursor: "pointer",
                  transition: "all 150ms ease",
                }}
              >
                <Icon size={14} />
                <span>{tab.label}</span>
              </button>
            );
          })}
        </div>

        {/* Modal Scrollable Body */}
        <div style={{
          padding: "20px 24px",
          overflowY: "auto",
          flex: 1,
          color: "var(--text)",
          fontSize: 13,
          lineHeight: 1.6,
        }}>
          {activeTab === "overview" && (
            <div style={{ display: "flex", flexDirection: "column", gap: 16 }}>
              <div style={{
                padding: "14px 16px",
                background: "var(--panel-2)",
                border: "1px solid var(--border)",
                borderRadius: 8,
              }}>
                <h3 style={{ margin: "0 0 6px 0", fontSize: 14, fontWeight: 700, color: "var(--teal)" }}>
                  What is CrimeNet?
                </h3>
                <p style={{ margin: 0, color: "var(--text-muted)", fontSize: 12.5 }}>
                  CrimeNet is a mission-critical criminal intelligence platform designed for law enforcement agencies.
                  It ingests unstructured police narratives, First Information Reports (FIRs), call detail records (CDRs),
                  and banking ledgers, converting them into multi-tier interactive knowledge graphs with real-time AI reasoning.
                </p>
              </div>

              <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 12 }}>
                <div style={{
                  padding: 12,
                  background: "var(--panel-2)",
                  border: "1px solid var(--border)",
                  borderRadius: 8,
                }}>
                  <div style={{ fontWeight: 600, color: "var(--text)", marginBottom: 4, display: "flex", alignItems: "center", gap: 6 }}>
                    <Shield size={14} color="var(--teal)" /> 1. Operational Graph
                  </div>
                  <div style={{ fontSize: 11.5, color: "var(--text-muted)" }}>
                    Nodes represent entities (Suspects, Phones, Bank Accounts, Vehicles, Locations). Links represent validated transactions, co-occurrences, and communication paths.
                  </div>
                </div>

                <div style={{
                  padding: 12,
                  background: "var(--panel-2)",
                  border: "1px solid var(--border)",
                  borderRadius: 8,
                }}>
                  <div style={{ fontWeight: 600, color: "var(--text)", marginBottom: 4, display: "flex", alignItems: "center", gap: 6 }}>
                    <BrainCircuit size={14} color="var(--teal)" /> 2. AI Intelligence
                  </div>
                  <div style={{ fontSize: 11.5, color: "var(--text-muted)" }}>
                    Integrated AI reasoning engine executing unsupervised anomaly detection, kingpin identification, and statutory legal order drafting.
                  </div>
                </div>
              </div>
            </div>
          )}

          {activeTab === "analytics" && (
            <div style={{ display: "flex", flexDirection: "column", gap: 14 }}>
              <div style={{ fontSize: 13, fontWeight: 700, color: "var(--text)" }}>
                Core Graph Algorithms & Topological Metrics
              </div>

              {[
                {
                  name: "PageRank Centrality",
                  desc: "Measures overall influence and authority within the criminal syndicate. Identifies kingpins and top controllers who operate behind multiple intermediaries.",
                  badge: "HIERARCHY",
                },
                {
                  name: "Betweenness & Cut Vertices (Articulation Points)",
                  desc: "Identifies strategic communication brokers and logistic bridges whose removal immediately fragments the criminal network into disconnected sub-graphs.",
                  badge: "INTERDICTION",
                },
                {
                  name: "Follow-the-Money (3-Hop BFS Tracing)",
                  desc: "Traces financial disbursements across mule accounts, shell companies, and ATM cash withdrawals up to 3 hops away from any flagged account.",
                  badge: "FINANCIAL",
                },
                {
                  name: "Isolation Forest Anomaly Detection",
                  desc: "Unsupervised machine learning model detecting stealthy outlier nodes exhibiting atypical degree-to-transaction ratios and threat scores.",
                  badge: "ML DETECTION",
                },
              ].map((algo, i) => (
                <div key={i} style={{
                  padding: "12px 14px",
                  background: "var(--panel-2)",
                  border: "1px solid var(--border)",
                  borderRadius: 8,
                }}>
                  <div style={{ display: "flex", alignItems: "center", justifyContent: "space-between", marginBottom: 4 }}>
                    <span style={{ fontWeight: 600, color: "var(--text)" }}>{algo.name}</span>
                    <span style={{
                      fontSize: 9.5,
                      fontWeight: 700,
                      padding: "2px 6px",
                      borderRadius: 4,
                      background: "var(--teal-s)",
                      color: "var(--teal)",
                      border: "1px solid var(--teal)",
                    }}>
                      {algo.badge}
                    </span>
                  </div>
                  <div style={{ fontSize: 12, color: "var(--text-muted)" }}>{algo.desc}</div>
                </div>
              ))}
            </div>
          )}

          {activeTab === "ai" && (
            <div style={{ display: "flex", flexDirection: "column", gap: 14 }}>
              <div style={{ fontSize: 13, fontWeight: 700, color: "var(--text)" }}>
                Using the AI Chatbox & Tactical Prompt Chips
              </div>

              <div style={{
                padding: "12px 14px",
                background: "var(--panel-2)",
                border: "1px solid var(--border)",
                borderRadius: 8,
              }}>
                <div style={{ fontWeight: 600, marginBottom: 6 }}>1-Click Quick Action Chips:</div>
                <div style={{ display: "flex", flexWrap: "wrap", gap: 6 }}>
                  {[
                    "Identify syndicate hierarchy & kingpin",
                    "Trace 3-hop money trail & mule accounts",
                    "Run Isolation Forest anomaly detection",
                    "Draft Section 102 CrPC account freeze order",
                    "Find critical communication bridges (cut vertices)",
                    "Summarize GraphRAG evidence citations",
                  ].map((chip, i) => (
                    <div key={i} style={{
                      fontSize: 11,
                      padding: "4px 8px",
                      background: "var(--panel-3)",
                      border: "1px solid var(--border-2)",
                      borderRadius: 14,
                      color: "var(--text)",
                      fontFamily: "var(--font-mono)",
                    }}>
                      {chip}
                    </div>
                  ))}
                </div>
              </div>

              <div style={{
                padding: "12px 14px",
                background: "var(--panel-2)",
                border: "1px solid var(--border)",
                borderRadius: 8,
              }}>
                <div style={{ fontWeight: 600, marginBottom: 4 }}>Statutory Legal Notices (CrPC Section 102):</div>
                <div style={{ fontSize: 12, color: "var(--text-muted)" }}>
                  Clicking "Section 102 freeze order" prompts the AI to synthesize a formal, court-admissible bank account freeze order formatted according to Section 102 of the Code of Criminal Procedure (CrPC), 1973, referencing account numbers and evidence citations from the active case.
                </div>
              </div>
            </div>
          )}

          {activeTab === "shortcuts" && (
            <div style={{ display: "flex", flexDirection: "column", gap: 12 }}>
              <div style={{ fontSize: 13, fontWeight: 700, color: "var(--text)" }}>
                Keyboard Shortcuts & Operational Controls
              </div>

              {[
                { key: "Ctrl + K / ⌘K", desc: "Open global network search & entity scoping modal" },
                { key: "Click Node", desc: "Open Entity Detail Drawer with Dossier & Actions" },
                { key: "Double Click Node", desc: "Center and zoom canvas directly onto target entity" },
                { key: "Right Click Node", desc: "Open context menu (Follow Money, Freeze, Delete)" },
                { key: "Force / LR / TB", desc: "Switch graph layout (Spring force, Left-Right, Top-Bottom)" },
                { key: "Theme Toggle", desc: "Switch between Pitch Black (Dark) and Cream White (Light) modes" },
              ].map((s, idx) => (
                <div key={idx} style={{
                  display: "flex",
                  alignItems: "center",
                  justifyContent: "space-between",
                  padding: "8px 12px",
                  background: "var(--panel-2)",
                  border: "1px solid var(--border)",
                  borderRadius: 6,
                }}>
                  <span style={{ fontSize: 12, color: "var(--text-muted)" }}>{s.desc}</span>
                  <kbd style={{
                    padding: "3px 8px",
                    background: "var(--bg-2)",
                    border: "1px solid var(--border-2)",
                    borderRadius: 4,
                    fontSize: 11,
                    fontFamily: "var(--font-mono)",
                    color: "var(--text)",
                    boxShadow: "0 1px 2px rgba(0,0,0,0.1)",
                  }}>
                    {s.key}
                  </kbd>
                </div>
              ))}
            </div>
          )}
        </div>

        {/* Footer */}
        <div style={{
          display: "flex",
          alignItems: "center",
          justifyContent: "space-between",
          padding: "10px 20px",
          background: "var(--panel-2)",
          borderTop: "1px solid var(--border)",
        }}>
          <div style={{ fontSize: 11, color: "var(--text-dim)", fontFamily: "var(--font-mono)" }}>
            CrimeNet LE v2.0 • Security & Audit Enabled
          </div>
          <button
            onClick={onClose}
            className="crimenet-btn-secondary"
            style={{
              padding: "6px 14px",
              borderRadius: 6,
              border: "1px solid var(--border-2)",
              background: "var(--panel-3)",
              color: "var(--text)",
              fontWeight: 600,
              fontSize: 12,
              cursor: "pointer",
            }}
          >
            Close Documentation
          </button>
        </div>
      </div>
    </div>
  );
}
