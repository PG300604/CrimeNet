/**
 * TacticalCommandBar.jsx — restrained operations header.
 *
 * The visual language is intentionally quiet: a simple network mark, compact
 * case telemetry, and two controls that remain useful during an investigation.
 */

import React from "react";
import { MessageSquare, Sun, Moon } from "lucide-react";

function CrimeNetMark() {
  return (
    <svg width="19" height="19" viewBox="0 0 24 24" fill="none" aria-hidden="true">
      <path d="M5 18.5 12 5l7 13.5M5 18.5h14M8.2 13h7.6" stroke="currentColor" strokeWidth="1.35" strokeLinecap="round" strokeLinejoin="round" />
      <circle cx="5" cy="18.5" r="1.7" fill="currentColor" />
      <circle cx="12" cy="5" r="1.7" fill="currentColor" />
      <circle cx="19" cy="18.5" r="1.7" fill="currentColor" />
    </svg>
  );
}

export default function TacticalCommandBar({
  caseId = "CASE-2024-MH-088",
  nodesCount = 0,
  edgesCount = 0,
  onToggleGeminiChat,
  onToggleTheme,
  theme = "dark",
}) {
  return (
    <header className="tactical-command-bar">
      <div className="command-brand">
        <div className="command-brand-mark">
          <CrimeNetMark />
        </div>
        <div className="command-brand-copy">
          <div className="command-brand-name">CRIMENET</div>
          <div className="command-brand-subtitle">Network intelligence system</div>
        </div>
      </div>

      <div className="command-telemetry" aria-label="Active investigation telemetry">
        <span className="command-telemetry-label">CASE</span>
        <span className="command-case-id" title={caseId}>{caseId}</span>
        <span className="command-divider" aria-hidden="true" />
        <span><strong>{nodesCount}</strong> ENTITIES</span>
        <span className="command-divider" aria-hidden="true" />
        <span><strong>{edgesCount}</strong> LINKS</span>
      </div>

      <div className="command-actions">
        <div className="command-provider" title="Copilot service status">
          <span className="command-provider-dot" aria-hidden="true" />
          <span className="command-provider-copy">
            <strong>SYSTEM READY</strong>
            <small>LOCAL COPILOT</small>
          </span>
        </div>

        <button
          type="button"
          className="command-ai-button"
          onClick={onToggleGeminiChat}
          title="Open the investigative copilot"
        >
          <MessageSquare size={13} />
          Copilot
        </button>

        <button
          type="button"
          className="command-theme-button"
          onClick={onToggleTheme}
          title={theme === "dark" ? "Switch to light mode" : "Switch to dark mode"}
          aria-label={theme === "dark" ? "Switch to light mode" : "Switch to dark mode"}
        >
          {theme === "dark" ? <Sun size={14} /> : <Moon size={14} />}
        </button>
      </div>
    </header>
  );
}
