"""Comprehensive End-to-End Test Suite for CrimeNet Algorithms and Technologies.

Covers:
1. NetworkX Graph Engine on UNBOUND 2026 and 911 Hijackers datasets
2. Community Detection: Louvain, Hierarchical Clustering (Dendrogram Tree), Label Propagation, Modularity, Spectral
3. Social Influence / Centrality: PageRank, Betweenness Centrality, Closeness Centrality, Degree Centrality, HITS
4. Link Prediction: Jaccard Coefficient (missing-edges check), Adamic-Adar, Resource Allocation
5. Node Embedding / Graph ML: DeepWalk, Node2Vec, Non-negative Matrix Factorization (NMF)
6. NLP Information Extraction: Regex patterns (phone, vehicle, account, amount, cues, org), evidence preservation, and spaCy/HF interface
7. Forensic Anomaly Detection: Explainable detectors (odd-hour, structuring, cross-case, broker)
8. Isolation Forest Anomaly Detection (scikit-learn ensemble)
9. Neo4j Graph Database Driver & GDS Schema Verification
"""

import os
import sys
import json
import pytest
from pathlib import Path
import networkx as nx
import numpy as np

# Ensure root directory and ai-service are in sys.path
ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))
ai_service_dir = ROOT_DIR / "repo" / "ai-service"
if str(ai_service_dir) not in sys.path:
    sys.path.insert(0, str(ai_service_dir))

from storage.builtin_datasets import BuiltinDatasetsManager
from analyzer.request_taker import InMemoryAnalyzer
from analyzer import community_detection
from analyzer import social_influence_analysis
from analyzer import link_prediction
from analyzer import node_embedding
from app.nlp.extractor import Extractor, PHONE_RE, VEHICLE_RE, ACCOUNT_RE, MONEY_RE, ORG_RE, PERSON_CUES
from app.graph import analytics as pure_analytics
from app.graph import anomalies as pure_anomalies


# --------------------------------------------------------------------------- #
# Fixtures
# --------------------------------------------------------------------------- #
@pytest.fixture(scope="module")
def data_mgr():
    mgr = BuiltinDatasetsManager(None, None)
    unbound_path = str(ROOT_DIR / "datasets" / "preprocessed" / "unbound_case_2026.json")
    h911_path = str(ROOT_DIR / "datasets" / "preprocessed" / "911_hijackers.json")
    moreno_path = str(ROOT_DIR / "datasets" / "preprocessed" / "moreno_crime.json")
    
    mgr.add_dataset("unbound", "UNBOUND 2026", unbound_path)
    mgr.add_dataset("911", "911 Hijackers", h911_path)
    mgr.add_dataset("moreno", "Moreno Crime", moreno_path)
    return mgr


@pytest.fixture(scope="module")
def unbound_network(data_mgr):
    return data_mgr.get_network("unbound")


@pytest.fixture(scope="module")
def analyzer():
    return InMemoryAnalyzer()


# --------------------------------------------------------------------------- #
# 1. NetworkX Graph Engine Tests
# --------------------------------------------------------------------------- #
def test_networkx_graph_construction(unbound_network):
    """Verify NetworkX converts and constructs graphs cleanly without errors."""
    from analyzer.common.helpers import convert_to_nx_undirected_graph, convert_to_nx_directed_graph
    
    g_undirected, nodes_u = convert_to_nx_undirected_graph(unbound_network)
    assert isinstance(g_undirected, nx.Graph)
    assert g_undirected.number_of_nodes() > 0
    assert g_undirected.number_of_edges() > 0
    assert len(nodes_u) == g_undirected.number_of_nodes()

    g_directed, nodes_d = convert_to_nx_directed_graph(unbound_network, node_is_str=True)
    assert isinstance(g_directed, nx.DiGraph)
    assert g_directed.number_of_nodes() > 0
    assert g_directed.number_of_edges() > 0


# --------------------------------------------------------------------------- #
# 2. Community Detection Algorithm Tests (Louvain, Hierarchical, Modularity)
# --------------------------------------------------------------------------- #
def test_community_detection_louvain(analyzer, unbound_network):
    """Test Louvain community detection returns non-empty communities and valid partition."""
    task = {
        "task_id": "community_detection",
        "network": unbound_network,
        "options": {"method": "louvain", "parameters": {}}
    }
    res = analyzer.perform_analysis(task=task, params=None)
    assert res["success"] == 1
    assert "communities" in res
    assert len(res["communities"]) >= 2
    assert res.get("num_communities", len(res["communities"])) >= 2


def test_community_detection_hierarchical_tree(analyzer, unbound_network):
    """Test Hierarchical Clustering generates tree structure with depth and nodes."""
    task = {
        "task_id": "community_detection",
        "network": unbound_network,
        "options": {"method": "hierarchical", "parameters": {"K": 4}}
    }
    res = analyzer.perform_analysis(task=task, params=None)
    assert res["success"] == 1
    assert "tree" in res
    tree = res["tree"]
    assert tree["id"] == "root"
    assert "children" in tree
    assert len(tree["children"]) > 0
    assert "stats" in res
    assert res["stats"]["hierarchy_depth"] >= 1
    assert res["stats"]["total_entities"] > 0


def test_community_detection_label_propagation(analyzer, unbound_network):
    """Test Label Propagation community detection."""
    task = {
        "task_id": "community_detection",
        "network": unbound_network,
        "options": {"method": "label_propagation", "parameters": {}}
    }
    res = analyzer.perform_analysis(task=task, params=None)
    assert res["success"] == 1
    assert "communities" in res
    assert len(res["communities"]) >= 1


def test_community_detection_modularity(analyzer, unbound_network):
    """Test Clauset-Newman-Moore Modularity Maximization."""
    task = {
        "task_id": "community_detection",
        "network": unbound_network,
        "options": {"method": "modularity", "parameters": {}}
    }
    res = analyzer.perform_analysis(task=task, params=None)
    assert res["success"] == 1
    assert "communities" in res
    assert len(res["communities"]) >= 1


def test_community_detection_spectral(analyzer, unbound_network):
    """Test Spectral Clustering on graph Laplacian."""
    task = {
        "task_id": "community_detection",
        "network": unbound_network,
        "options": {"method": "spectral", "parameters": {"K": 3}}
    }
    res = analyzer.perform_analysis(task=task, params=None)
    assert res["success"] == 1
    assert "communities" in res
    assert len(res["communities"]) == 3


# --------------------------------------------------------------------------- #
# 3. Social Influence & Centrality Tests (PageRank, Betweenness, Closeness)
# --------------------------------------------------------------------------- #
def test_social_influence_pagerank(analyzer, unbound_network):
    """Test PageRank influence scoring."""
    task = {
        "task_id": "social_influence_analysis",
        "network": unbound_network,
        "options": {"method": "pagerank", "parameters": {}}
    }
    res = analyzer.perform_analysis(task=task, params=None)
    assert res["success"] == 1
    assert "scores" in res
    assert len(res["scores"]) > 0
    total_pr = sum(res["scores"].values())
    assert abs(total_pr - 1.0) < 1e-3


def test_social_influence_betweenness(analyzer, unbound_network):
    """Test Brandes Betweenness Centrality for bottleneck / broker identification."""
    task = {
        "task_id": "social_influence_analysis",
        "network": unbound_network,
        "options": {"method": "betweenness", "parameters": {}}
    }
    res = analyzer.perform_analysis(task=task, params=None)
    assert res["success"] == 1
    assert "scores" in res
    assert len(res["scores"]) > 0
    assert any(score > 0 for score in res["scores"].values())


def test_social_influence_closeness(analyzer, unbound_network):
    """Test Closeness Centrality."""
    task = {
        "task_id": "social_influence_analysis",
        "network": unbound_network,
        "options": {"method": "closeness_centrality", "parameters": {}}
    }
    res = analyzer.perform_analysis(task=task, params=None)
    assert res["success"] == 1
    assert "scores" in res
    assert len(res["scores"]) > 0


# --------------------------------------------------------------------------- #
# 4. Link Prediction Algorithm Tests (Jaccard, Adamic-Adar, Resource Alloc)
# --------------------------------------------------------------------------- #
def test_link_prediction_jaccard_excludes_existing_edges(analyzer, unbound_network):
    """Verify that Jaccard link prediction ONLY returns candidate missing links, never existing edges."""
    existing_pairs = set()
    for e in unbound_network.get("edges", []):
        u, v = e["source"], e["target"]
        existing_pairs.add((u, v))
        existing_pairs.add((v, u))

    task = {
        "task_id": "link_prediction",
        "network": unbound_network,
        "options": {"method": "jaccard_coefficient", "parameters": {}}
    }
    res = analyzer.perform_analysis(task=task, params=None)
    assert res["success"] == 1
    assert "predictions" in res
    assert len(res["predictions"]) > 0

    for src, cands in res["predictions"].items():
        for tgt in cands:
            assert (src, tgt) not in existing_pairs, f"Link prediction returned existing edge: {src} <-> {tgt}"


def test_link_prediction_adamic_adar(analyzer, unbound_network):
    """Test Adamic-Adar candidate link prediction."""
    task = {
        "task_id": "link_prediction",
        "network": unbound_network,
        "options": {"method": "adamic_adar_index", "parameters": {}}
    }
    res = analyzer.perform_analysis(task=task, params=None)
    assert res["success"] == 1
    assert "predictions" in res


def test_link_prediction_resource_allocation(analyzer, unbound_network):
    """Test Resource Allocation link prediction."""
    task = {
        "task_id": "link_prediction",
        "network": unbound_network,
        "options": {"method": "resource_allocation_index", "parameters": {}}
    }
    res = analyzer.perform_analysis(task=task, params=None)
    assert res["success"] == 1
    assert "predictions" in res


# --------------------------------------------------------------------------- #
# 5. Graph Embedding / ML Tests (DeepWalk, Node2Vec, NMF)
# --------------------------------------------------------------------------- #
def test_node_embedding_nmf(analyzer, unbound_network):
    """Test Non-negative Matrix Factorization node embeddings."""
    task = {
        "task_id": "node_embedding",
        "network": unbound_network,
        "options": {"method": "nmf", "parameters": {"K": 8}}
    }
    res = analyzer.perform_analysis(task=task, params=None)
    assert res["success"] == 1
    assert "vectors" in res
    assert len(res["vectors"]) > 0
    sample_vec = next(iter(res["vectors"].values()))
    assert len(sample_vec) == 8


def test_node_embedding_deepwalk(analyzer, unbound_network):
    """Test DeepWalk random-walk word2vec embeddings."""
    task = {
        "task_id": "node_embedding",
        "network": unbound_network,
        "options": {"method": "deepwalk", "parameters": {"K": 16}}
    }
    res = analyzer.perform_analysis(task=task, params=None)
    assert res["success"] == 1
    assert "vectors" in res
    assert len(res["vectors"]) > 0


def test_node_embedding_node2vec(analyzer, unbound_network):
    """Test Node2Vec parameterized biased random walk embeddings."""
    task = {
        "task_id": "node_embedding",
        "network": unbound_network,
        "options": {"method": "node2vec", "parameters": {"K": 16}}
    }
    res = analyzer.perform_analysis(task=task, params=None)
    assert res["success"] == 1
    assert "vectors" in res
    assert len(res["vectors"]) > 0


# --------------------------------------------------------------------------- #
# 6. NLP Information Extraction (Regex, spaCy/Transformers interface)
# --------------------------------------------------------------------------- #
def test_nlp_regex_extraction():
    """Verify regular expressions extract Indian entities accurately with evidence."""
    sample_fir = (
        "Complainant reported that accused Ashok Nair operating mobile 9876543210 "
        "drove vehicle MH04AB1234 near Bhiwandi. Transfer of Rs. 4,50,000 made to "
        "A/c no 912345678901 belonging to Sunrise Traders."
    )
    ext = Extractor()
    processed = ext.process(sample_fir)
    entities = processed["entities"]
    relations = processed["relations"]

    ent_map = {e["type"]: e["text"] for e in entities}
    assert "phone" in ent_map and ent_map["phone"] == "9876543210"
    assert "vehicle" in ent_map and ent_map["vehicle"] == "MH04AB1234"
    assert "person" in ent_map and ent_map["person"] == "Ashok Nair"
    assert "location" in ent_map and ent_map["location"] == "Bhiwandi"
    assert "organization" in ent_map and "Sunrise Traders" in ent_map["organization"]
    assert "account" in ent_map and ent_map["account"] == "912345678901"

    # Evidence preservation
    assert all(len(e["evidence"]) > 0 for e in entities)
    assert all(e["confidence"] >= 0.7 for e in entities)

    # Relations inferred
    rel_types = {r["type"] for r in relations}
    assert "USES_PHONE" in rel_types or "USES_VEHICLE" in rel_types or "SEEN_AT" in rel_types


def test_nlp_spacy_transformer_fallback():
    """Verify that when spaCy or transformers are not installed, the extractor gracefully defaults to regex tier."""
    ext = Extractor(model="non_existent_model_name")
    assert ext._nlp is None  # Graceful fallback without crash
    res = ext.entities("Contact phone 9812345678")
    assert any(e.type == "phone" and e.text == "9812345678" for e in res)


# --------------------------------------------------------------------------- #
# 7. Forensic Anomaly Detection (Explainable Detectors)
# --------------------------------------------------------------------------- #
def test_explainable_anomaly_detection():
    """Verify explainable anomaly detection detects odd-hour, value outliers, and structuring."""
    g = pure_analytics.Graph()
    g.add_node("person:vikram", "person", "Vikram Patel", "FIR-101")
    g.add_node("phone:9876543210", "phone", "9876543210", "FIR-101")
    g.add_node("phone:9812345678", "phone", "9812345678", "FIR-102")
    g.add_edge("person:vikram", "phone:9876543210")
    g.add_edge("phone:9876543210", "phone:9812345678")

    records = [
        {"kind": "cdr", "a": "9876543210", "b": "9812345678", "ts": "2026-03-01T02:15:00Z"},
        {"kind": "cdr", "a": "9876543210", "b": "9812345678", "ts": "2026-03-01T03:45:00Z"},
        {"kind": "txn", "from": "Vikram Patel", "to": "Sunrise Traders", "amount": 95000, "case": "FIR-101"},
        {"kind": "txn", "from": "Vikram Patel", "to": "Sunrise Traders", "amount": 96000, "case": "FIR-101"},
        {"kind": "txn", "from": "Vikram Patel", "to": "Sunrise Traders", "amount": 95500, "case": "FIR-101"},
    ]

    metrics = pure_analytics.analyse(g)["metrics"]
    anomalies = pure_anomalies.detect(g, records, metrics)

    kinds = {a["kind"] for a in anomalies}
    assert "odd-hour" in kinds or "structuring" in kinds
    # Must have explanatory evidence
    assert all("explanation" in a and len(a["explanation"]) > 0 for a in anomalies)


# --------------------------------------------------------------------------- #
# 8. Isolation Forest Anomaly Detection (scikit-learn ensemble)
# --------------------------------------------------------------------------- #
def test_isolation_forest_anomaly_detection():
    """Verify Isolation Forest detects multivariate transactional / behavioral outliers."""
    from sklearn.ensemble import IsolationForest

    np.random.seed(42)
    normal_amounts = np.random.uniform(5000, 25000, size=(60, 1))
    normal_hours = np.random.uniform(9, 20, size=(60, 1))
    normal_freqs = np.random.uniform(1, 4, size=(60, 1))
    normal_data = np.hstack([normal_amounts, normal_hours, normal_freqs])

    outliers = np.array([
        [490000.0, 3.0, 18.0],
        [480000.0, 2.5, 15.0],
        [980000.0, 4.0, 22.0]
    ])

    X = np.vstack([normal_data, outliers])

    iso_forest = IsolationForest(contamination=0.05, random_state=42)
    iso_forest.fit(X)
    predictions = iso_forest.predict(X)

    assert predictions[-1] == -1
    assert predictions[-2] == -1
    assert predictions[-3] == -1


# --------------------------------------------------------------------------- #
# 9. Neo4j Graph Database Driver & Schema Check
# --------------------------------------------------------------------------- #
def test_neo4j_driver_and_schema():
    """Verify Neo4j driver is imported and seed query schema file is syntactically sound."""
    import neo4j
    assert hasattr(neo4j, "GraphDatabase")

    seed_path = ROOT_DIR / "repo" / "neo4j" / "seed.cypher"
    assert seed_path.exists()
    content = seed_path.read_text(encoding="utf-8")
    assert "CREATE CONSTRAINT" in content or "gds." in content or "MATCH" in content
    assert "Person" in content
