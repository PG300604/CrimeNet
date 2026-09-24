/**
 * TacticalCommandBar.jsx — CrimeNet AI Top Tactical Navigation Bar
 * Streamlined application header with live case telemetry, model status, and quick shortcuts.
 * AI search, narrative ingestion, and evidence analysis are housed directly in the Left Sidebar.
 */

import React from "react";
import { ShieldAlert, Sparkles, FolderOpen, Sun, Moon, Database, Activity } from "lucide-react";

export default function TacticalCommandBar({
  caseId = "CASE-2024-MH-088",
  nodesCount = 0,
  edgesCount = 0,
  onToggleGeminiChat,
  onToggleTheme,
  theme = "light",
}) {
  return (
    <header
      style={{
        display: "flex",
        alignItems: "center",
        justifyContent: "space-between",
        padding: "8px 18px",
        background: "var(--panel, #ffffff)",
        borderBottom: "1.5px solid var(--border, #e2e8f0)",
        boxShadow: "0 1px 4px rgba(0,0,0,0.04)",
        zIndex: 100,
        flexShrink: 0,
        height: 48,
        gap: 16,
      }}
    >
      {/* ── Left: Brand Badge ──────────────────────────────────────────────── */}
      <div style={{ display: "flex", alignItems: "center", gap: 10, minWidth: 220 }}>
        <div
          style={{
            width: 28,
            height: 28,
            borderRadius: 6,
            background: "linear-gradient(135deg, #10b981, #059669)",
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
            color: "#fff",
            boxShadow: "0 2px 6px rgba(16,185,129,0.3)",
          }}
        >
          <ShieldAlert size={16} />
        </div>
        <div>
          <div
            style={{
              fontSize: 13,
              fontWeight: 700,
              letterSpacing: "-0.01em",
              color: "var(--text-1, #0f172a)",
              display: "flex",
              alignItems: "center",
              gap: 6,
            }}
          >
            <span>CrimeNet AI</span>
            <span
              style={{
                fontSize: 9,
                background: "rgba(16,185,129,0.12)",
                color: "#059669",
                padding: "1px 5px",
                borderRadius: 4,
                fontWeight: 700,
              }}
            >
              LE EDITION
            </span>
          </div>
          <div style={{ fontSize: 10, color: "var(--text-muted, #94a3b8)" }}>
            Indian Criminal Network Intelligence
          </div>
        </div>
      </div>

      {/* ── Center: Active Case Telemetry Badge ─────────────────────────────── */}
      <div
        style={{
          display: "flex",
          alignItems: "center",
          gap: 10,
          background: "var(--panel-2, #f8fafc)",
          border: "1px solid var(--border, #e2e8f0)",
          borderRadius: 20,
          padding: "3px 12px",
        }}
      >
        <span
          style={{
            width: 7,
            height: 7,
            borderRadius: "50%",
            background: "#ef4444",
            boxShadow: "0 0 6px #ef4444",
          }}
        />
        <span style={{ fontSize: 11.5, fontWeight: 600, color: "var(--text-1, #0f172a)" }}>
          Active Case: <span style={{ color: "#2563eb" }}>{caseId}</span>
        </span>
        <span style={{ color: "#cbd5e1" }}>·</span>
        <span style={{ fontSize: 11, color: "var(--text-muted, #64748b)" }}>
          {nodesCount} Entities
        </span>
        <span style={{ color: "#cbd5e1" }}>·</span>
        <span style={{ fontSize: 11, color: "var(--text-muted, #64748b)" }}>
          {edgesCount} Connections
        </span>
      </div>

      {/* ── Right: AI Model Status & Gemini Sidebar Toggle ─────────────────── */}
      <div style={{ display: "flex", alignItems: "center", gap: 10 }}>
        {/* Gemini Online Status Indicator */}
        <div
          style={{
            display: "flex",
            alignItems: "center",
            gap: 6,
            fontSize: 11,
            fontWeight: 500,
            color: "#059669",
            background: "#ecfdf5",
            border: "1px solid #a7f3d0",
            padding: "3px 8px",
            borderRadius: 14,
          }}
        >
          <span style={{ width: 6, height: 6, borderRadius: "50%", background: "#10b981" }} />
          <span>Gemini 2.5 Flash</span>
        </div>

        {/* Gemini AI Sidebar Trigger */}
        <button
          type="button"
          onClick={onToggleGeminiChat}
          title="Toggle Gemini AI Copilot"
          style={{
            display: "inline-flex",
            alignItems: "center",
            gap: 6,
            padding: "5px 12px",
            borderRadius: 6,
            border: "none",
            background: "linear-gradient(135deg, #4285F4 0%, #9B72CF 50%, #D96570 100%)",
            color: "#ffffff",
            fontWeight: 600,
            fontSize: 11.5,
            cursor: "pointer",
            boxShadow: "0 2px 8px rgba(66, 133, 244, 0.3)",
            whiteSpace: "nowrap",
          }}
        >
          <Sparkles size={13} />
          <span>Gemini AI</span>
        </button>

        {/* Theme Toggle Button */}
        {onToggleTheme && (
          <button
            type="button"
            onClick={onToggleTheme}
            title={theme === "light" ? "Switch to Dark Mode" : "Switch to Light Mode"}
            style={{
              background: "transparent",
              border: "1px solid var(--border, #cbd5e1)",
              borderRadius: 6,
              padding: 5,
              cursor: "pointer",
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
              color: "var(--text-1, #475569)",
            }}
          >
            {theme === "light" ? <Moon size={14} /> : <Sun size={14} />}
          </button>
        )}
      </div>
    </header>
  );
}
