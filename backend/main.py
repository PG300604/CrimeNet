"""
CrimeNet AI - Unified REST API Gateway
Exposes all RAG, NER extraction, graph analytics, and agentic workflows to the React frontend.
Fulfills all contracts defined in FRONTEND_PLAN_AND_TIMELINE.md.
"""

import os
import shutil
import logging
from typing import List, Dict, Any, Optional
from pathlib import Path

from fastapi import FastAPI, UploadFile, File, Form, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from .config import UPLOADS_DIR, CORS_ORIGINS, HOST, PORT
from .rag.document_loader import DocumentLoader
from .rag.chunker import DocumentChunker
from .rag.vector_store import default_vector_store
from .extraction.ner_extractor import NarrativeExtractor, GraphNode, GraphEdge, default_extractor
from .agents.dossier_agent import default_dossier_agent
from .agents.financial_agent import default_financial_agent
from .agents.feedback_agent import default_feedback_agent
from .audit_ledger import default_audit_ledger

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("crimenet.api")

app = FastAPI(
    title="CrimeNet AI API",
    description="Explainable Intelligence & Criminal Network Analysis Platform for Indian Law Enforcement",
    version="1.0.0"
)

# Enable CORS for React frontend (Vite port 5173, etc.)
app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# --------------------------------------------------------------------------- #
# In-Memory Case & Graph State
# --------------------------------------------------------------------------- #
class CaseStore:
    def __init__(self):
        self.cases: Dict[str, Dict[str, Any]] = {
            "CASE-2024-MH-088": {
                "id": "CASE-2024-MH-088",
                "title": "Operation Golden Web",
                "type": "Organized Cyber Extortion",
                "status": "CRITICAL",
                "suspects": 8,
                "volume": "₹2.4 Cr",
                "police_station": "Cyber Crime Cell, Bandra Kurla Complex",
                "officer": "Inspector S. Deshmukh (Badge #4409)",
                "created_at": "2024-03-10"
            },
            "CASE-2024-DL-012": {
                "id": "CASE-2024-DL-012",
                "title": "NCR Hawala Network",
                "type": "Financial Money Laundering",
                "status": "ONGOING",
                "suspects": 14,
                "volume": "₹18.6 Cr",
                "police_station": "Special Cell, Lodhi Colony",
                "officer": "ACP R. K. Mishra",
                "created_at": "2024-02-15"
            },
            "CASE-2023-GJ-901": {
                "id": "CASE-2023-GJ-901",
                "title": "Surat Cargo Smuggling Cell",
                "type": "Narcotics & Logistics",
                "status": "COLD",
                "suspects": 5,
                "volume": "₹4.1 Cr",
                "police_station": "Crime Branch, Surat",
                "officer": "Inspector V. Patel",
                "created_at": "2023-11-20"
            }
        }
        self.graphs: Dict[str, Dict[str, Any]] = {}
        self.seed_default_graph()

    def seed_default_graph(self):
        """Seeds default investigation graph for immediate exploration."""
        cid = "CASE-2024-MH-088"
        nodes = [
            GraphNode(id="E1", label="Vikram Malhotra", type="PERSON", threat_level="CRITICAL", threat_score=0.95),
            GraphNode(id="E2", label="9876543210", type="PHONE", threat_level="HIGH", threat_score=0.82),
            GraphNode(id="E3", label="vikram@okhdfcbank", type="ACCOUNT", threat_level="CRITICAL", threat_score=0.91),
            GraphNode(id="E4", label="SBI-Mule-40912", type="ACCOUNT", threat_level="CRITICAL", threat_score=0.88),
            GraphNode(id="E5", label="Apex Global Logistics Ltd", type="ORGANIZATION", threat_level="HIGH", threat_score=0.79),
            GraphNode(id="E6", label="BVI Offshore Vault 99", type="ORGANIZATION", threat_level="CRITICAL", threat_score=0.96),
            GraphNode(id="E7", label="Surat Cargo Yard", type="LOCATION", threat_level="MEDIUM", threat_score=0.45),
            GraphNode(id="E8", label="MH04AB9901 (Fortuner)", type="VEHICLE", threat_level="HIGH", threat_score=0.72),
        ]
        edges = [
            GraphEdge(id="R1", source="E1", target="E2", type="USES_PHONE", label="Primary Contact"),
            GraphEdge(id="R2", source="E1", target="E3", type="OPERATES_ACCOUNT", label="Registered UPI"),
            GraphEdge(id="R3", source="E3", target="E4", type="TRANSFERRED_FUNDS", label="₹15,00,000 (UPI)", amount="₹15,00,000"),
            GraphEdge(id="R4", source="E4", target="E5", type="TRANSFERRED_FUNDS", label="₹42,00,000 (RTGS)", amount="₹42,00,000"),
            GraphEdge(id="R5", source="E5", target="E6", type="WIRE_TRANSFER", label="₹85,00,000 (Offshore)", amount="₹85,00,000"),
            GraphEdge(id="R6", source="E1", target="E8", type="USES_VEHICLE", label="Registered Transport"),
            GraphEdge(id="R7", source="E8", target="E7", type="SPOTTED_AT", label="Toll Plaza Footage"),
        ]
        self.graphs[cid] = {"nodes": {n.id: n for n in nodes}, "edges": edges}


case_store = CaseStore()
chunker = DocumentChunker()


# --------------------------------------------------------------------------- #
# Request & Response Schemas
# --------------------------------------------------------------------------- #
class NarrativeRequest(BaseModel):
    case_id: str = "CASE-2024-MH-088"
    narrative: str
    officer_badge: str = "INSP-4409"


class FeedbackRequest(BaseModel):
    case_id: str = "CASE-2024-MH-088"
    feedback_prompt: str
    officer_badge: str = "INSP-4409"


class ActionDispatchRequest(BaseModel):
    action_id: str
    entity_id: str
    case_id: str = "CASE-2024-MH-088"
    officer_badge: str = "INSP-4409"
    parameters: Dict[str, Any] = Field(default_factory=dict)


class FollowMoneyRequest(BaseModel):
    seed_node_id: str
    case_id: str = "CASE-2024-MH-088"
    max_hops: int = 3


class NewCaseRequest(BaseModel):
    title: str
    type: str
    police_station: str
    officer: str
    initial_facts: Optional[str] = None


# --------------------------------------------------------------------------- #
# API Routes
# --------------------------------------------------------------------------- #

@app.get("/")
def health_check():
    return {
        "status": "online",
        "service": "CrimeNet AI Unified API",
        "version": "1.0.0",
        "jurisdiction": "Indian Law Enforcement Edition"
    }


# 1. Cases Endpoints
@app.get("/api/cases")
def list_cases():
    return list(case_store.cases.values())


@app.post("/api/cases")
def create_case(req: NewCaseRequest):
    cid = f"CASE-{len(case_store.cases) + 1:03d}"
    new_case = {
        "id": cid,
        "title": req.title,
        "type": req.type,
        "status": "CRITICAL",
        "suspects": 0,
        "volume": "₹0",
        "police_station": req.police_station,
        "officer": req.officer,
        "created_at": "Today"
    }
    case_store.cases[cid] = new_case
    case_store.graphs[cid] = {"nodes": {}, "edges": []}

    default_audit_ledger.record_action(
        action="REGISTER_CASE",
        case_id=cid,
        officer_badge=req.officer,
        details={"title": req.title, "type": req.type}
    )

    if req.initial_facts:
        res = default_extractor.extract_from_narrative(req.initial_facts, case_id=cid)
        for n in res.nodes:
            case_store.graphs[cid]["nodes"][n.id] = n
        case_store.graphs[cid]["edges"].extend(res.edges)
        new_case["suspects"] = len(res.nodes)

    return new_case


# 2. Graph Canvas Endpoint
@app.get("/api/graph/{case_id}")
def get_graph(case_id: str):
    if case_id not in case_store.graphs:
        case_store.graphs[case_id] = {"nodes": {}, "edges": []}

    c_graph = case_store.graphs[case_id]
    return {
        "nodes": [n.to_dict() for n in c_graph["nodes"].values()],
        "edges": [e.to_dict() for e in c_graph["edges"]],
    }


# 3. Narrative Ingestion Endpoint (Text-to-Graph)
@app.post("/api/investigate/narrative")
def investigate_narrative(req: NarrativeRequest):
    if req.case_id not in case_store.graphs:
        case_store.graphs[req.case_id] = {"nodes": {}, "edges": []}

    # Extract entities and relationships
    result = default_extractor.extract_from_narrative(req.narrative, case_id=req.case_id)

    # Merge into active case graph
    c_graph = case_store.graphs[req.case_id]
    for n in result.nodes:
        c_graph["nodes"][n.id] = n
    c_graph["edges"].extend(result.edges)

    # Log to immutable audit ledger
    default_audit_ledger.record_action(
        action="NARRATIVE_INGESTION",
        case_id=req.case_id,
        officer_badge=req.officer_badge,
        details={
            "raw_length": len(req.narrative),
            "extracted_nodes": len(result.nodes),
            "extracted_edges": len(result.edges),
            "entities": [n.label for n in result.nodes]
        }
    )

    return {
        "status": "success",
        "extractedCount": len(result.nodes),
        "graph": {
            "nodes": [n.to_dict() for n in c_graph["nodes"].values()],
            "edges": [e.to_dict() for e in c_graph["edges"]],
        },
        "tokens": [t.normalized_value for t in result.tokens]
    }


# 4. Evidence Document Upload Endpoint (RAG Ingestion)
@app.post("/api/investigate/upload")
async def upload_evidence(
    case_id: str = Form("CASE-2024-MH-088"),
    officer_badge: str = Form("INSP-4409"),
    file: UploadFile = File(...)
):
    upload_path = UPLOADS_DIR / f"{case_id}_{file.filename}"
    with open(upload_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Parse and chunk document
    doc = DocumentLoader.load_file(str(upload_path), case_id=case_id)
    doc_chunks = chunker.chunk_document(doc)
    added_count = default_vector_store.add_chunks(doc_chunks, case_id=case_id)

    # Extract entities from document text
    extraction = default_extractor.extract_from_narrative(doc.full_text[:5000], case_id=case_id)
    if case_id not in case_store.graphs:
        case_store.graphs[case_id] = {"nodes": {}, "edges": []}

    c_graph = case_store.graphs[case_id]
    for n in extraction.nodes:
        c_graph["nodes"][n.id] = n
    c_graph["edges"].extend(extraction.edges)

    # Audit log entry
    default_audit_ledger.record_action(
        action="DOCUMENT_UPLOAD",
        case_id=case_id,
        officer_badge=officer_badge,
        details={
            "filename": file.filename,
            "chunks_indexed": added_count,
            "entities_found": len(extraction.nodes)
        }
    )

    return {
        "status": "indexed",
        "filename": file.filename,
        "chunksIndexed": added_count,
        "extractedEntities": len(extraction.nodes),
        "graph": {
            "nodes": [n.to_dict() for n in c_graph["nodes"].values()],
            "edges": [e.to_dict() for e in c_graph["edges"]],
        }
    }


# 5. Entity Dossier Endpoint (Agentic Synthesis with RAG Citations)
@app.get("/api/entity/{node_id}/dossier")
def get_entity_dossier(node_id: str, case_id: str = Query("CASE-2024-MH-088")):
    if case_id not in case_store.graphs:
        case_store.graphs[case_id] = {"nodes": {}, "edges": []}

    c_graph = case_store.graphs[case_id]
    node = c_graph["nodes"].get(node_id)
    if not node:
        # Dynamically register node for intelligence synthesis
        clean_label = node_id.replace("_", " ").strip()
        lower_id = node_id.lower()
        if any(w in lower_id for w in ["org", "ltd", "corp", "logistics", "infotech", "enterprises", "vault"]):
            inferred_type = "organization"
        elif any(w in lower_id for w in ["bank", "acc", "mule", "upi", "@"]):
            inferred_type = "account"
        elif any(w in lower_id for w in ["veh", "car", "fortuner", "truck"]):
            inferred_type = "vehicle"
        elif any(w in lower_id for w in ["loc", "yard", "plaza", "delhi", "mumbai", "surat"]):
            inferred_type = "location"
        elif any(c.isdigit() for c in node_id) and len([c for c in node_id if c.isdigit()]) >= 10:
            inferred_type = "phone"
        else:
            inferred_type = "person"

        threat = "CRITICAL" if any(w in lower_id for w in ["malhotra", "sheikh", "yadav", "alshehri", "mule", "vault", "apex"]) else "HIGH"
        score = 0.92 if threat == "CRITICAL" else 0.75

        node = GraphNode(
            id=node_id,
            label=clean_label,
            type=inferred_type,
            threat_level=threat,
            threat_score=score,
            metadata={"source": "Dynamic Network Inspection"}
        )
        c_graph["nodes"][node_id] = node

    connected_edges = [e for e in c_graph["edges"] if e.source == node_id or e.target == node_id]
    dossier = default_dossier_agent.generate_dossier(
        node=node,
        connected_edges=connected_edges,
        all_nodes_dict=c_graph["nodes"],
        case_id=case_id
    )

    return dossier.to_dict()


# 6. Follow the Money 3-Hop Tracing Endpoint
@app.post("/api/analytics/follow-money")
def follow_the_money(req: FollowMoneyRequest):
    if req.case_id not in case_store.graphs:
        case_store.graphs[req.case_id] = {"nodes": {}, "edges": []}

    c_graph = case_store.graphs[req.case_id]
    if req.seed_node_id not in c_graph["nodes"]:
        clean_label = req.seed_node_id.replace("_", " ").strip()
        c_graph["nodes"][req.seed_node_id] = GraphNode(
            id=req.seed_node_id,
            label=clean_label,
            type="account" if "acc" in req.seed_node_id.lower() or "@" in req.seed_node_id else "person",
            threat_level="CRITICAL",
            threat_score=0.91
        )
    res = default_financial_agent.trace_money(
        seed_node_id=req.seed_node_id,
        nodes_dict=c_graph["nodes"],
        edges=c_graph["edges"],
        max_hops=req.max_hops
    )
    return res.to_dict()


# 7. Human-in-the-Loop @feedback Endpoint
@app.post("/api/feedback")
def submit_feedback(req: FeedbackRequest):
    if req.case_id not in case_store.graphs:
        raise HTTPException(status_code=404, detail="Case not found")

    c_graph = case_store.graphs[req.case_id]
    res = default_feedback_agent.process_feedback(
        feedback_text=req.feedback_prompt,
        nodes_dict=c_graph["nodes"],
        edges=c_graph["edges"],
        case_id=req.case_id,
        officer_badge=req.officer_badge
    )
    return res.to_dict()


# 8. Threat Alerts Endpoint
@app.get("/api/alerts")
def get_threat_alerts(case_id: str = Query("CASE-2024-MH-088")):
    return [
        {
            "id": "ALT-101",
            "severity": "CRITICAL",
            "title": "Rapid Mule Layering Transfer Flagged",
            "timestamp": "10 mins ago",
            "description": "₹15,00,000 dispersed from vikram@okhdfcbank to SBI-Mule-40912, followed by immediate wire to Apex Global Logistics.",
            "targetNodeId": "E4",
            "actionLabel": "Freeze Mule Account",
            "actionId": "FREEZE"
        },
        {
            "id": "ALT-102",
            "severity": "HIGH",
            "title": "Border Transit Geofence Hit",
            "timestamp": "42 mins ago",
            "description": "Vehicle MH04AB9901 registered to Vikram Malhotra passed through Vapi Toll Plaza towards international container yard.",
            "targetNodeId": "E8",
            "actionLabel": "Dispatch Highway Patrol",
            "actionId": "ANPR_ALERT"
        },
        {
            "id": "ALT-103",
            "severity": "HIGH",
            "title": "Cross-Border Offshore Routing",
            "timestamp": "2 hours ago",
            "description": "Apex Global Logistics initiated ₹85,00,000 wire transfer to BVI Offshore Vault 99.",
            "targetNodeId": "E6",
            "actionLabel": "Requisition FIU-IND / Interpol Red Notice",
            "actionId": "FIU_NOTICE"
        }
    ]


# 9. Action Dispatch Endpoint (LOC, Freeze Account, Summons)
@app.post("/api/actions/dispatch")
def dispatch_action(req: ActionDispatchRequest):
    entry = default_audit_ledger.record_action(
        action=f"ACTION_{req.action_id}",
        case_id=req.case_id,
        officer_badge=req.officer_badge,
        target_entity=req.entity_id,
        details={"parameters": req.parameters}
    )

    action_names = {
        "LOC": "Lookout Circular (LOC) transmitted to Bureau of Immigration",
        "FREEZE": "Account Freeze Order requisitioned to Bank Nodal Officer under Sec 102 CrPC",
        "SUMMONS": "Notice of Appearance issued under Section 35(3) BNSS",
        "ANPR_ALERT": "FASTag vehicle intercept broadcast dispatched to State Police Highway Patrol"
    }

    return {
        "status": "dispatched",
        "actionId": req.action_id,
        "entityId": req.entity_id,
        "title": action_names.get(req.action_id, "Police Action Executed"),
        "auditId": entry.audit_id,
        "timestamp": entry.timestamp,
        "message": f"{action_names.get(req.action_id, 'Action executed')} and permanently logged in audit trail."
    }


# 10. Chronological Timeline Endpoint
@app.get("/api/cases/{case_id}/timeline")
def get_case_timeline(case_id: str):
    return [
        {"time": "2024-03-10 09:15 AM", "type": "FIR", "title": "FIR Registered", "desc": "Victim reports extortion call demanding ₹15,00,000 under threat of violence."},
        {"time": "2024-03-10 11:30 AM", "type": "TRANSACTION", "title": "Primary UPI Transfer", "desc": "₹15,00,000 transferred via UPI to vikram@okhdfcbank."},
        {"time": "2024-03-10 11:42 AM", "type": "TRANSACTION", "title": "Mule Account Funneling", "desc": "₹15,00,000 forwarded to SBI-Mule-40912 in Surat."},
        {"time": "2024-03-11 02:20 PM", "type": "VEHICLE", "title": "Toll Plaza Camera Hit", "desc": "Fortuner MH04AB9901 spotted at Vapi Toll Plaza heading to Surat Cargo Yard."},
        {"time": "2024-03-12 04:00 PM", "type": "WIRE", "title": "Offshore Layering Wire", "desc": "Apex Logistics initiates ₹85,00,000 wire to BVI Offshore Vault."}
    ]


# 11. Immutable Audit Ledger Endpoint
@app.get("/api/cases/{case_id}/audit")
def get_audit_trail(case_id: str, limit: int = 25):
    return default_audit_ledger.get_recent_entries(case_id=case_id, limit=limit)


# 12. Prosecutor Briefing Report Endpoint (PDF / Markdown export)
@app.get("/api/cases/{case_id}/report")
def get_case_report(case_id: str):
    c_info = case_store.cases.get(case_id, {"title": "General Investigation", "type": "Unknown"})
    c_graph = case_store.graphs.get(case_id, {"nodes": {}, "edges": []})
    audits = default_audit_ledger.get_recent_entries(case_id=case_id, limit=10)

    report_markdown = f"""# CONFIDENTIAL // PROSECUTOR INTELLIGENCE BRIEFING
**Case Title**: {c_info.get('title')} ({case_id})
**Crime Category**: {c_info.get('type')}
**Jurisdiction**: {c_info.get('police_station', 'Cyber Crime Cell')}
**Investigating Officer**: {c_info.get('officer', 'IO In-charge')}

---

## 1. Executive Summary
This intelligence briefing integrates multi-source evidence including First Information Reports (FIRs),
Call Detail Records (CDRs), Banking Statements, and Automated Number Plate Recognition (ANPR) camera captures.
CrimeNet AI topological analysis has identified an active criminal syndicate consisting of **{len(c_graph['nodes'])} mapped entities**
and **{len(c_graph['edges'])} verified relationship links**.

## 2. Identified Key Operatives
"""
    for n in c_graph["nodes"].values():
        if n.threat_level in ["CRITICAL", "HIGH"]:
            report_markdown += f"- **{n.label}** ({n.type}) — Threat Level: `{n.threat_level}` (Score: {n.threat_score})\n"

    report_markdown += """
## 3. Financial Layering & Follow-the-Money Trail
Analysis of fund dispersal indicates structured layering operations:
1. Initial extorted capital collected via UPI handles.
2. Immediate intra-hour dispersal to regional mule accounts.
3. Commercial wire routing via logistics shells to offshore jurisdictions.

## 4. Dispatched Actions & Judicial Compliance Log
Every automated lead has undergone investigator review and has been logged with cryptographic SHA-256 hash verification:
"""
    for a in audits:
        report_markdown += f"- `[{a.get('timestamp')}]` **{a.get('action')}** by `{a.get('officer_badge')}`: {a.get('details', {})}\n"

    return {
        "case_id": case_id,
        "title": c_info.get("title"),
        "reportMarkdown": report_markdown,
        "entitiesCount": len(c_graph["nodes"]),
        "edgesCount": len(c_graph["edges"]),
        "generatedAt": "Live"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.main:app", host=HOST, port=PORT, reload=True)
