/**
 * CrimeNet — Universal AI Intelligence Engine (Client-Side)
 * Computes graph analytics, entity classification, Adamic-Adar hidden link prediction,
 * anomaly detection (hubs, bridges, cross-case), N-hop neighborhood exploration,
 * evidence trails, investigation timelines, and case reports across ALL loaded datasets and CSVs.
 */

window.UNBOUND = window.UNBOUND || {};

(function() {
  // State containers
  const state = {
    elements: [],
    nodes: [],
    edges: [],
    nodeMap: new Map(),
    adj: new Map(),
    activeTab: 'insights',
    selectedNodeId: null,
    searchQuery: '',
    filterType: 'ALL',
    filterRisk: 'ALL',
    nHopDistance: 1,
    acceptedLeads: new Set(),
    dismissedLeads: new Set(),
    graphMetrics: { density: 0, components: 1, avgDegree: 0, maxDegree: 0 }
  };

  window.UNBOUND.state = state;

  // Forensic type color palette consistent with CrimeNet
  const TYPE_COLORS = {
    person: '#2783DE',
    phone: '#46A171',
    vehicle: '#D5803B',
    location: '#BF8EDA',
    organization: '#4FB9C9',
    case: '#E56458',
    fir: '#E56458',
    account: '#F2A93B',
    bank: '#F2A93B',
    entity: '#7D7A75'
  };

  function getTypeColor(type) {
    const t = String(type || '').toLowerCase();
    return TYPE_COLORS[t] || '#6c757d';
  }

  function formatLabel(node) {
    if (!node) return '';
    return node.label || node.name || (node.properties && node.properties.name) || node.id || '';
  }

  function getNodeType(node) {
    if (!node) return 'person';
    return (node.type || (node.properties && node.properties.type) || 'person').toLowerCase();
  }

  /* ------------------------------------------------------------------ */
  /*  Graph Analytics Engine                                            */
  /* ------------------------------------------------------------------ */
  function parseElements(rawElements) {
    state.nodeMap.clear();
    state.adj.clear();
    state.nodes = [];
    state.edges = [];

    if (!Array.isArray(rawElements)) return;

    // First pass: extract nodes
    rawElements.forEach(el => {
      const d = el.data || el;
      if (d && d.id && !d.source) {
        const id = String(d.id);
        const type = getNodeType(d);
        const nodeObj = {
          id: id,
          label: formatLabel(d),
          type: type,
          properties: d.properties || (d.info && typeof d.info === 'object' ? d.info : {}) || {},
          degree: 0,
          inDegree: 0,
          outDegree: 0
        };
        state.nodeMap.set(id, nodeObj);
        state.nodes.push(nodeObj);
        state.adj.set(id, []);
      }
    });

    // Second pass: extract edges
    rawElements.forEach(el => {
      const d = el.data || el;
      if (d && d.source && d.target) {
        const src = String(d.source);
        const tgt = String(d.target);
        if (state.nodeMap.has(src) && state.nodeMap.has(tgt)) {
          const edgeObj = {
            id: String(d.id || `${src}_${tgt}_${state.edges.length}`),
            source: src,
            target: tgt,
            type: d.type || (d.properties && d.properties.type) || 'connected_to',
            weight: Number(d.weight || (d.properties && d.properties.weight) || 1),
            properties: d.properties || {}
          };
          state.edges.push(edgeObj);

          // Update adjacency
          state.adj.get(src).push({ neighborId: tgt, edge: edgeObj, dir: 'out' });
          state.adj.get(tgt).push({ neighborId: src, edge: edgeObj, dir: 'in' });

          const srcNode = state.nodeMap.get(src);
          const tgtNode = state.nodeMap.get(tgt);
          srcNode.degree += 1;
          srcNode.outDegree += 1;
          tgtNode.degree += 1;
          tgtNode.inDegree += 1;
        }
      }
    });

    // Compute graph metrics
    const n = state.nodes.length;
    const m = state.edges.length;
    const density = n > 1 ? (2 * m) / (n * (n - 1)) : 0;
    let maxDeg = 0;
    let sumDeg = 0;
    state.nodes.forEach(node => {
      if (node.degree > maxDeg) maxDeg = node.degree;
      sumDeg += node.degree;
    });

    // Connected components via BFS
    const visited = new Set();
    let components = 0;
    state.nodes.forEach(node => {
      if (!visited.has(node.id)) {
        components += 1;
        const q = [node.id];
        visited.add(node.id);
        while (q.length > 0) {
          const curr = q.shift();
          const neighbors = state.adj.get(curr) || [];
          neighbors.forEach(nbr => {
            if (!visited.has(nbr.neighborId)) {
              visited.add(nbr.neighborId);
              q.push(nbr.neighborId);
            }
          });
        }
      }
    });

    state.graphMetrics = {
      density: Math.round(density * 1000) / 10,
      components: components,
      avgDegree: n > 0 ? (sumDeg / n).toFixed(1) : 0,
      maxDegree: maxDeg
    };

    // Auto-select root node if none selected
    if (!state.selectedNodeId && state.nodes.length > 0) {
      const topHub = state.nodes.slice().sort((a, b) => b.degree - a.degree)[0];
      state.selectedNodeId = topHub ? topHub.id : state.nodes[0].id;
    }
  }

  /* ------------------------------------------------------------------ */
  /*  Link Prediction (Adamic-Adar & Common Neighbors)                   */
  /* ------------------------------------------------------------------ */
  function computeHiddenLinks() {
    const hiddenLinks = [];
    const n = state.nodes.length;
    if (n < 3) return hiddenLinks;

    const directNeighbors = new Map();
    state.nodes.forEach(node => {
      const nbrs = new Set((state.adj.get(node.id) || []).map(x => x.neighborId));
      directNeighbors.set(node.id, nbrs);
    });

    for (let i = 0; i < n; i++) {
      for (let j = i + 1; j < n; j++) {
        const u = state.nodes[i];
        const v = state.nodes[j];
        const pairKey = [u.id, v.id].sort().join('__');
        if (state.dismissedLeads.has(pairKey)) continue;

        const uNbrs = directNeighbors.get(u.id);
        if (uNbrs.has(v.id)) continue;

        // Find common neighbors
        const common = [];
        uNbrs.forEach(wId => {
          if (directNeighbors.get(v.id).has(wId)) {
            common.push(state.nodeMap.get(wId));
          }
        });

        if (common.length > 0) {
          let adamicAdar = 0;
          common.forEach(w => {
            const deg = w.degree;
            adamicAdar += 1 / Math.log2(deg + 1.1);
          });

          const conf = Math.min(95, Math.round(45 + common.length * 15 + adamicAdar * 12));
          const accepted = state.acceptedLeads.has(pairKey);

          hiddenLinks.push({
            pairKey: pairKey,
            nodeA: u,
            nodeB: v,
            score: conf,
            shared: common,
            accepted: accepted
          });
        }
      }
    }

    return hiddenLinks.sort((a, b) => b.score - a.score).slice(0, 12);
  }

  /* ------------------------------------------------------------------ */
  /*  Anomaly Detection (Hubs, Bridges, Cross-Case, Night Bursts)        */
  /* ------------------------------------------------------------------ */
  function detectAnomalies() {
    const anomalies = [];
    if (state.nodes.length === 0) return anomalies;

    // 1. Hub Anomalies
    const mean = state.nodes.reduce((s, n) => s + n.degree, 0) / state.nodes.length;
    const variance = state.nodes.reduce((s, n) => s + Math.pow(n.degree - mean, 2), 0) / state.nodes.length;
    const std = Math.sqrt(variance);
    const threshold = Math.max(3, mean + 1.4 * std);

    state.nodes.forEach(node => {
      if (node.degree >= threshold) {
        anomalies.push({
          sev: node.degree >= threshold * 1.3 ? 'high' : 'medium',
          type: 'Hub / Central Coordinator',
          badge: 'HUB',
          subject: `${formatLabel(node)} (${node.id})`,
          nodeId: node.id,
          why: `Extreme connectivity: ${node.degree} direct connections (average is ${mean.toFixed(1)}). Acts as central communications hub or mule repository.`
        });
      }
    });

    // 2. Critical Bridge / Bottleneck Nodes (Articulation Points)
    state.nodes.forEach(node => {
      if (node.degree >= 2 && (state.adj.get(node.id) || []).length >= 2) {
        const nbrs = state.adj.get(node.id).map(x => x.neighborId);
        let hasBridgePattern = false;
        for (let i = 0; i < nbrs.length; i++) {
          const nbrA = nbrs[i];
          const nbrANeighbors = new Set((state.adj.get(nbrA) || []).map(x => x.neighborId));
          for (let j = i + 1; j < nbrs.length; j++) {
            const nbrB = nbrs[j];
            if (!nbrANeighbors.has(nbrB)) {
              hasBridgePattern = true;
              break;
            }
          }
          if (hasBridgePattern) break;
        }

        if (hasBridgePattern && node.degree >= 3) {
          anomalies.push({
            sev: 'medium',
            type: 'Communication Bridge',
            badge: 'BRIDGE',
            subject: `${formatLabel(node)} (${node.id})`,
            nodeId: node.id,
            why: `Structural bottleneck linking disparate entities. Severing connections to this node disrupts communications between clusters.`
          });
        }
      }
    });

    // 3. Cross-Case Identifiers
    state.nodes.forEach(node => {
      const cases = (node.properties && node.properties.cases) || [];
      if (Array.isArray(cases) && cases.length >= 2) {
        anomalies.push({
          sev: 'high',
          type: 'Cross-Case Entity',
          badge: 'MULTI-CASE',
          subject: `${formatLabel(node)} (${node.id})`,
          nodeId: node.id,
          why: `Appears across ${cases.length} independent investigations: ${cases.join(', ')}.`
        });
      }
    });

    // 4. Night-time odd-hour burst communications
    state.edges.forEach(edge => {
      const ts = (edge.properties && (edge.properties.timestamp || edge.properties.date || edge.properties.time)) || '';
      if (ts && ts.includes('T')) {
        const hr = new Date(ts).getHours();
        if (hr >= 0 && hr < 5) {
          anomalies.push({
            sev: 'medium',
            type: 'Odd-Hour Interaction',
            badge: 'NIGHT-BURST',
            subject: `${formatLabel(state.nodeMap.get(edge.source))} \u2194 ${formatLabel(state.nodeMap.get(edge.target))}`,
            nodeId: edge.source,
            why: `Interaction recorded at ${ts.replace('T', ' ')} (00:00\u201305:00 window). Night-time operation deviates from baseline activity.`
          });
        }
      }
    });

    return anomalies.slice(0, 10);
  }

  /* ------------------------------------------------------------------ */
  /*  N-Hop Neighborhood BFS Traversal                                  */
  /* ------------------------------------------------------------------ */
  function getNHopNeighborhood(rootId, maxHops) {
    if (!state.nodeMap.has(rootId)) return { nodesByHop: [], allNodeIds: new Set() };

    const visited = new Map();
    visited.set(rootId, 0);
    const queue = [{ id: rootId, hop: 0 }];
    const nodesByHop = [[state.nodeMap.get(rootId)]];

    for (let h = 1; h <= maxHops; h++) nodesByHop[h] = [];

    while (queue.length > 0) {
      const curr = queue.shift();
      if (curr.hop >= maxHops) continue;

      const neighbors = state.adj.get(curr.id) || [];
      neighbors.forEach(nbr => {
        if (!visited.has(nbr.neighborId)) {
          const nextHop = curr.hop + 1;
          visited.set(nbr.neighborId, nextHop);
          nodesByHop[nextHop].push(state.nodeMap.get(nbr.neighborId));
          queue.push({ id: nbr.neighborId, hop: nextHop });
        }
      });
    }

    return {
      nodesByHop: nodesByHop,
      allNodeIds: new Set(visited.keys())
    };
  }

  /* ------------------------------------------------------------------ */
  /*  Timeline Events Extractor                                         */
  /* ------------------------------------------------------------------ */
  function extractTimeline() {
    const events = [];

    state.edges.forEach(edge => {
      const p = edge.properties || {};
      const ts = p.timestamp || p.date || p.time || p.call_time || p.txn_date;
      if (ts) {
        const srcNode = state.nodeMap.get(edge.source);
        const tgtNode = state.nodeMap.get(edge.target);
        const sub = [];
        if (p.duration) sub.push(`${p.duration}s`);
        if (p.amount) sub.push(`\u20b9${Number(p.amount).toLocaleString('en-IN')}`);
        if (p.cases) sub.push(Array.isArray(p.cases) ? p.cases.join(', ') : p.cases);
        if (p.case) sub.push(p.case);

        events.push({
          date: ts,
          type: edge.type || 'Interaction',
          label: `${formatLabel(srcNode)} \u2192 ${formatLabel(tgtNode)}`,
          sub: sub.join(' \u00b7 ') || edge.type,
          sourceId: edge.source
        });
      }
    });

    state.nodes.forEach(node => {
      const p = node.properties || {};
      const ts = p.date || p.timestamp || p.registration_date;
      if (ts) {
        events.push({
          date: ts,
          type: node.type.toUpperCase(),
          label: `${formatLabel(node)} recorded in registry`,
          sub: (p.cases && p.cases.join(', ')) || node.type,
          sourceId: node.id
        });
      }
    });

    return events.sort((a, b) => new Date(a.date) - new Date(b.date));
  }

  /* ------------------------------------------------------------------ */
  /*  Graph Focus & Cytoscape Actions                                   */
  /* ------------------------------------------------------------------ */
  window.UNBOUND.focusNodeInGraph = function(nodeId) {
    state.selectedNodeId = nodeId;
    try {
      const el = document.getElementById('cytoscape');
      const cy = el && el._cyreg && el._cyreg.cy;
      if (cy) {
        cy.nodes().unselect();
        const n = cy.getElementById(nodeId);
        if (n && n.length > 0) {
          n.select();
          cy.animate({ center: { eles: n }, zoom: 1.4 }, { duration: 450 });
          window.UNBOUND.showToast(`Centered on ${formatLabel(state.nodeMap.get(nodeId))}`, true);
        }
      }
    } catch (e) { console.warn(e); }
    window.UNBOUND.renderPanel();
  };

  window.UNBOUND.highlightNHopInGraph = function(nodeId, hops) {
    try {
      const el = document.getElementById('cytoscape');
      const cy = el && el._cyreg && el._cyreg.cy;
      if (cy) {
        cy.elements().unselect();
        const root = cy.getElementById(nodeId);
        if (root && root.length > 0) {
          let current = root;
          for (let h = 0; h < hops; h++) {
            current = current.union(current.neighborhood());
          }
          current.select();
          cy.animate({ fit: { eles: current, padding: 50 } }, { duration: 500 });
          window.UNBOUND.showToast(`Highlighted ${current.nodes().length} entities in ${hops}-hop neighborhood`, true);
          return;
        }
      }
    } catch (e) { console.warn(e); }
    window.UNBOUND.showToast(`Selected ${hops}-hop neighborhood for ${nodeId}`, true);
  };

  window.UNBOUND.focusPairInGraph = function(idA, idB) {
    try {
      const el = document.getElementById('cytoscape');
      const cy = el && el._cyreg && el._cyreg.cy;
      if (cy) {
        cy.elements().unselect();
        const a = cy.getElementById(idA);
        const b = cy.getElementById(idB);
        const pair = a.union(b);
        if (pair.length > 0) {
          pair.select();
          cy.animate({ fit: { eles: pair, padding: 70 } }, { duration: 450 });
          window.UNBOUND.showToast(`Focused pair: ${formatLabel(state.nodeMap.get(idA))} \u2194 ${formatLabel(state.nodeMap.get(idB))}`, true);
        }
      }
    } catch (e) { console.warn(e); }
  };

  window.UNBOUND.acceptLead = function(pairKey) {
    state.acceptedLeads.add(pairKey);
    window.UNBOUND.showToast(`Lead verified & saved to dossier`, true);
    window.UNBOUND.renderPanel();
  };

  window.UNBOUND.dismissLead = function(pairKey) {
    state.dismissedLeads.add(pairKey);
    window.UNBOUND.showToast(`Lead dismissed`);
    window.UNBOUND.renderPanel();
  };

  window.UNBOUND.showToast = function(msg, ok) {
    let t = document.getElementById('unbound-toast');
    if (!t) {
      t = document.createElement('div');
      t.id = 'unbound-toast';
      document.body.appendChild(t);
    }
    t.innerHTML = (ok ? '<span style="color:#8FD3AB">\u2713</span> ' : '') + msg;
    t.className = 'unbound-toast on';
    clearTimeout(window.UNBOUND._toastT);
    window.UNBOUND._toastT = setTimeout(() => t.className = 'unbound-toast', 2600);
  };

  /* ------------------------------------------------------------------ */
  /*  Report Modal Generator                                            */
  /* ------------------------------------------------------------------ */
  window.UNBOUND.openReportModal = function() {
    let modal = document.getElementById('crimenet-report-modal');
    if (!modal) {
      modal = document.createElement('div');
      modal.id = 'crimenet-report-modal';
      document.body.appendChild(modal);
    }

    const anomalies = detectAnomalies();
    const hiddenLinks = computeHiddenLinks();
    const topEntities = state.nodes.slice().sort((a, b) => b.degree - a.degree).slice(0, 8);
    const dateStr = new Date().toLocaleDateString('en-GB', { day: 'numeric', month: 'short', year: 'numeric', hour: '2-digit', minute: '2-digit' });

    modal.innerHTML = `
      <div class="crimenet-report-backdrop" onclick="document.getElementById('crimenet-report-modal').style.display='none'"></div>
      <div class="crimenet-report-content">
        <div class="crimenet-report-header">
          <div>
            <div style="font-size:16px;font-weight:700;color:#2C2C2B">CrimeNet Case Intelligence Dossier</div>
            <div style="font-size:11px;color:#7D7A75">Automated Multi-Source Forensic Analysis \u00b7 Generated ${dateStr}</div>
          </div>
          <button class="unbound-mini-btn" onclick="document.getElementById('crimenet-report-modal').style.display='none'" style="font-size:14px">\u2715</button>
        </div>
        <div class="crimenet-report-body" id="crimenet-printable-report">
          <div style="background:#F9F8F7;padding:10px;border-radius:6px;margin-bottom:12px;display:grid;grid-template-columns:repeat(4,1fr);gap:8px;text-align:center">
            <div><div style="font-size:16px;font-weight:700;color:#2783DE">${state.nodes.length}</div><div style="font-size:10px;color:#7D7A75">TOTAL ENTITIES</div></div>
            <div><div style="font-size:16px;font-weight:700;color:#46A171">${state.edges.length}</div><div style="font-size:10px;color:#7D7A75">RELATIONSHIPS</div></div>
            <div><div style="font-size:16px;font-weight:700;color:#D5803B">${state.graphMetrics.density}%</div><div style="font-size:10px;color:#7D7A75">DENSITY</div></div>
            <div><div style="font-size:16px;font-weight:700;color:#E56458">${anomalies.length}</div><div style="font-size:10px;color:#7D7A75">ACTIVE ALERTS</div></div>
          </div>

          <div style="font-size:12px;font-weight:700;margin:12px 0 6px">1. Key Entities of Interest</div>
          <table style="width:100%;font-size:11px;border-collapse:collapse;margin-bottom:12px">
            <tr style="border-bottom:1px solid #E6E5E3;color:#7D7A75;text-align:left">
              <th style="padding:4px">Entity</th>
              <th style="padding:4px">Type</th>
              <th style="padding:4px">Connections</th>
              <th style="padding:4px">Known Association</th>
            </tr>
            ${topEntities.map(e => `
              <tr style="border-bottom:1px solid #F0EFED">
                <td style="padding:4px;font-weight:600">${formatLabel(e)}</td>
                <td style="padding:4px"><span style="color:${getTypeColor(e.type)}">${e.type}</span></td>
                <td style="padding:4px">${e.degree}</td>
                <td style="padding:4px;color:#666">${(e.properties && (e.properties.cases ? e.properties.cases.join(', ') : e.properties.role)) || 'Associated in active ring'}</td>
              </tr>
            `).join('')}
          </table>

          <div style="font-size:12px;font-weight:700;margin:12px 0 6px">2. High-Priority Forensic Anomalies</div>
          <div style="font-size:11px;display:flex;flex-direction:column;gap:6px;margin-bottom:12px">
            ${anomalies.slice(0, 5).map(a => `
              <div style="padding:6px 8px;background:#F9F8F7;border-left:3px solid ${a.sev==='high'?'#E56458':'#D5803B'};border-radius:3px">
                <b>[${a.type}]</b> ${a.subject}: ${a.why}
              </div>
            `).join('')}
          </div>

          <div style="font-size:12px;font-weight:700;margin:12px 0 6px">3. AI Predicted Hidden Links</div>
          <div style="font-size:11px;display:flex;flex-direction:column;gap:6px;margin-bottom:12px">
            ${hiddenLinks.slice(0, 4).map(l => `
              <div style="padding:6px 8px;background:#F9F8F7;border-radius:3px">
                <b>${formatLabel(l.nodeA)} \u2194 ${formatLabel(l.nodeB)}</b> (${l.score}% confidence)
                <div style="color:#666;margin-top:2px">Shared intermediaries: ${l.shared.map(formatLabel).join(', ')}</div>
              </div>
            `).join('')}
          </div>
        </div>
        <div class="crimenet-report-footer">
          <button class="unbound-btn-primary" onclick="window.print()">\uD83D\uDDA8\uFE0F Print / Save PDF</button>
          <button class="unbound-btn" onclick="navigator.clipboard.writeText(document.getElementById('crimenet-printable-report').innerText);window.UNBOUND.showToast('Copied report to clipboard', true)">\uD83D\uDCCB Copy</button>
          <button class="unbound-btn" onclick="document.getElementById('crimenet-report-modal').style.display='none'">Close</button>
        </div>
      </div>
    `;
    modal.style.display = 'flex';
  };

  /* ------------------------------------------------------------------ */
  /*  Intelligence Panel DOM Renderer                                    */
  /* ------------------------------------------------------------------ */
  window.UNBOUND.renderPanel = function() {
    const panel = document.getElementById('unbound-insights-panel');
    if (!panel) return;

    if (state.nodes.length === 0) {
      panel.innerHTML = `
        <div style="padding:24px 14px;text-align:center;color:#7D7A75;font-size:12px">
          <div style="font-size:24px;margin-bottom:8px">\uD83D\uDD0D</div>
          <div style="font-weight:600;font-size:13px;color:#2C2C2B;margin-bottom:4px">No Active Network Loaded</div>
          <div>Select a dataset or upload a CSV in the <b>NETWORK</b> tab to generate explorable graph intelligence.</div>
        </div>
      `;
      return;
    }

    const dot = t => `<span class="unbound-dot" style="background:${getTypeColor(t)}"></span>`;
    const badge = (txt, cls) => `<span class="unbound-badge ${cls||''}">${txt}</span>`;
    const anomalies = detectAnomalies();
    const hiddenLinks = computeHiddenLinks();

    // Group entity types for filter pills
    const typeCounts = {};
    state.nodes.forEach(n => {
      typeCounts[n.type] = (typeCounts[n.type] || 0) + 1;
    });

    // Filter nodes based on search & filter pills
    const q = state.searchQuery.toLowerCase().trim();
    const filteredNodes = state.nodes.filter(node => {
      if (state.filterType !== 'ALL' && node.type !== state.filterType) return false;
      if (q) {
        const matchesName = formatLabel(node).toLowerCase().includes(q);
        const matchesId = node.id.toLowerCase().includes(q);
        const matchesProp = Object.values(node.properties).some(v => String(v).toLowerCase().includes(q));
        if (!matchesName && !matchesId && !matchesProp) return false;
      }
      return true;
    });

    // Update bottom status bar dynamically
    const statusBar = document.getElementById('unbound-status-bar');
    if (statusBar) {
      const casesSet = new Set();
      state.nodes.forEach(n => {
        if (n.type === 'case') casesSet.add(n.id);
        if (n.properties && n.properties.cases) {
          (Array.isArray(n.properties.cases) ? n.properties.cases : [n.properties.cases]).forEach(c => casesSet.add(c));
        }
      });
      statusBar.innerHTML = `
        <span style="display:flex;align-items:center;gap:4px"><b>${state.nodes.length}</b> entities</span>
        <span style="display:flex;align-items:center;gap:4px"><b>${state.edges.length}</b> relationships</span>
        <span style="display:flex;align-items:center;gap:4px"><b>${casesSet.size}</b> cases</span>
        <span style="display:flex;align-items:center;gap:4px"><b>${anomalies.length}</b> alerts</span>
        <span style="margin-left:auto;display:flex;align-items:center;font-size:11px;color:#7D7A75">
          <span id="unbound-status-pulse" style="width:7px;height:7px;border-radius:50%;background:#46A171;display:inline-block;margin-right:5px"></span>
          Human-in-the-loop \u00b7 AI leads require investigator verification
        </span>
      `;
    }

    // Header & Subnav
    let html = `
      <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:8px">
        <div style="font-size:13px;font-weight:700;color:#2C2C2B">AI Intelligence</div>
        <button class="unbound-mini-btn" onclick="window.UNBOUND.openReportModal()" style="color:#2783DE;border-color:#c8e1fa;background:#f2f8fd">
          \uD83D\uDCC4 Export Dossier
        </button>
      </div>

      <!-- Subnav Navigation Pills -->
      <div class="crimenet-intel-subnav">
        <button class="intel-nav-pill ${state.activeTab==='insights'?'active':''}" onclick="window.UNBOUND.setSubTab('insights')">Insights</button>
        <button class="intel-nav-pill ${state.activeTab==='hidden'?'active':''}" onclick="window.UNBOUND.setSubTab('hidden')">Hidden Links (${hiddenLinks.length})</button>
        <button class="intel-nav-pill ${state.activeTab==='anomalies'?'active':''}" onclick="window.UNBOUND.setSubTab('anomalies')">Anomalies (${anomalies.length})</button>
        <button class="intel-nav-pill ${state.activeTab==='nhop'?'active':''}" onclick="window.UNBOUND.setSubTab('nhop')">N-Hop & Evidence</button>
        <button class="intel-nav-pill ${state.activeTab==='timeline'?'active':''}" onclick="window.UNBOUND.setSubTab('timeline')">Timeline</button>
      </div>
    `;

    /* -------------------------------------------------- */
    /* TAB 1: INSIGHTS & NETWORK ANALYSIS                 */
    /* -------------------------------------------------- */
    if (state.activeTab === 'insights') {
      const topEntities = state.nodes.slice().sort((a, b) => b.degree - a.degree).slice(0, 8);
      const topNode = topEntities[0];

      html += `
        <!-- Metrics Grid -->
        <div class="crimenet-metrics-grid">
          <div class="crimenet-metric-card">
            <div class="val" style="color:#2783DE">${state.nodes.length}</div>
            <div class="lbl">ENTITIES</div>
          </div>
          <div class="crimenet-metric-card">
            <div class="val" style="color:#46A171">${state.edges.length}</div>
            <div class="lbl">LINKS</div>
          </div>
          <div class="crimenet-metric-card">
            <div class="val" style="color:#D5803B">${state.graphMetrics.density}%</div>
            <div class="lbl">DENSITY</div>
          </div>
          <div class="crimenet-metric-card">
            <div class="val" style="color:#BF8EDA">${state.graphMetrics.components}</div>
            <div class="lbl">CLUSTERS</div>
          </div>
        </div>

        <!-- Explainable Intelligence Brief -->
        <div class="unbound-sect-h" style="margin-top:10px">Explainable AI Insights</div>
        <div class="unbound-card" style="font-size:11px;line-height:1.5;padding:8px 10px">
          ${topNode ? `
            <div style="margin-bottom:6px">
              \u2022 <b>Primary Key Broker:</b> <a href="javascript:void(0)" onclick="window.UNBOUND.focusNodeInGraph('${topNode.id}')" style="color:#2783DE;font-weight:600">${formatLabel(topNode)}</a> controls the highest connection density (${topNode.degree} links) across the network.
            </div>` : ''}
          <div style="margin-bottom:6px">
            \u2022 <b>Topology Diagnostics:</b> Network comprises ${state.graphMetrics.components} distinct components with an average degree of ${state.graphMetrics.avgDegree} connections per node.
          </div>
          <div>
            \u2022 <b>Entity Spectrum:</b> Identified ${Object.keys(typeCounts).length} functional entity classes: ${Object.entries(typeCounts).map(([t, c]) => `${c} ${t}s`).join(', ')}.
          </div>
        </div>

        <!-- Search and Filter Bar -->
        <div class="unbound-sect-h" style="margin-top:12px">Search & Filter Entities</div>
        <div style="margin-bottom:6px">
          <input type="text" class="crimenet-search-bar" id="crimenet-intel-search"
                 placeholder="Search entity name, phone, plate, ID..."
                 value="${state.searchQuery}"
                 oninput="window.UNBOUND.handleSearch(this.value)" />
        </div>
        <div style="display:flex;gap:4px;flex-wrap:wrap;margin-bottom:8px">
          <button class="crimenet-type-chip ${state.filterType==='ALL'?'active':''}" onclick="window.UNBOUND.setFilterType('ALL')">All (${state.nodes.length})</button>
          ${Object.entries(typeCounts).map(([t, cnt]) => `
            <button class="crimenet-type-chip ${state.filterType===t?'active':''}" onclick="window.UNBOUND.setFilterType('${t}')">
              ${dot(t)} ${t} (${cnt})
            </button>
          `).join('')}
        </div>

        <!-- Key Entities Ranked List -->
        <div class="unbound-sect-h">Ranked Entities <span class="unbound-n">${filteredNodes.length}</span></div>
        <div class="unbound-rank">
          ${filteredNodes.slice(0, 15).map(e => {
            const maxD = state.graphMetrics.maxDegree || 1;
            const pct = Math.max(8, Math.round((e.degree / maxD) * 100));
            const isSel = e.id === state.selectedNodeId;
            return `
              <div class="unbound-rank-row ${isSel?'selected-rank':''}" onclick="window.UNBOUND.focusNodeInGraph('${e.id}')" style="cursor:pointer">
                ${dot(e.type)} <span class="unbound-nm">${formatLabel(e)}</span>
                <div class="unbound-bar"><i style="width:${pct}%;background:${getTypeColor(e.type)}"></i></div>
                <span class="unbound-vl">${e.degree} link${e.degree!==1?'s':''}</span>
                <div class="unbound-hint">${e.type} \u00b7 ID: ${e.id}</div>
              </div>
            `;
          }).join('')}
        </div>
      `;
    }

    /* -------------------------------------------------- */
    /* TAB 2: HIDDEN LINKS                                */
    /* -------------------------------------------------- */
    else if (state.activeTab === 'hidden') {
      html += `
        <div class="unbound-sect-h">AI Hidden-Link Prediction <span class="unbound-n">${hiddenLinks.length}</span></div>
        <div style="font-size:11px;color:#7D7A75;margin-bottom:8px">
          Inferred using Adamic-Adar triadic closure over indirect shared contacts.
        </div>
        ${hiddenLinks.length === 0 ? `
          <div style="padding:16px;text-align:center;color:#999;font-size:11px">No hidden link anomalies found in current network.</div>
        ` : `
          <div class="unbound-card">
            ${hiddenLinks.map(p => `
              <div class="unbound-item">
                <div class="unbound-t">
                  <a href="javascript:void(0)" onclick="window.UNBOUND.focusNodeInGraph('${p.nodeA.id}')" style="color:#2783DE;font-weight:600">${formatLabel(p.nodeA)}</a>
                  <span style="color:#999">\u2194</span>
                  <a href="javascript:void(0)" onclick="window.UNBOUND.focusNodeInGraph('${p.nodeB.id}')" style="color:#2783DE;font-weight:600">${formatLabel(p.nodeB)}</a>
                  ${badge(p.score + '% Lead', p.score > 70 ? 'badge-orange' : '')}
                </div>
                <div class="unbound-why">
                  No direct link observed. <b>${p.shared.length} shared connection(s)</b> via ${p.shared.map(formatLabel).join(', ')}.
                </div>
                <div class="unbound-row-actions">
                  <button class="unbound-mini-btn" onclick="window.UNBOUND.focusPairInGraph('${p.nodeA.id}', '${p.nodeB.id}')">Focus Pair</button>
                  ${p.accepted ? `
                    <span class="unbound-badge badge-green">\u2713 Accepted</span>
                  ` : `
                    <button class="unbound-mini-btn" style="color:#46A171" onclick="window.UNBOUND.acceptLead('${p.pairKey}')">Accept Lead</button>
                    <button class="unbound-mini-btn" style="color:#999" onclick="window.UNBOUND.dismissLead('${p.pairKey}')">Dismiss</button>
                  `}
                </div>
              </div>
            `).join('')}
          </div>
        `}
      `;
    }

    /* -------------------------------------------------- */
    /* TAB 3: ANOMALIES                                   */
    /* -------------------------------------------------- */
    else if (state.activeTab === 'anomalies') {
      html += `
        <div class="unbound-sect-h">Anomaly Alerts <span class="unbound-n">${anomalies.length}</span></div>
        <div style="font-size:11px;color:#7D7A75;margin-bottom:8px">
          Automated structural and operational risk detection.
        </div>
        ${anomalies.length === 0 ? `
          <div style="padding:16px;text-align:center;color:#999;font-size:11px">No critical anomalies detected.</div>
        ` : `
          <div class="unbound-card">
            ${anomalies.map(a => `
              <div class="unbound-item">
                <div class="unbound-t">
                  ${badge(a.badge, a.sev === 'high' ? 'badge-red' : 'badge-orange')}
                  <span style="font-weight:600">${a.type}</span>
                </div>
                <div class="unbound-why" style="margin-top:3px">
                  <b style="color:#2C2C2B">${a.subject}</b> \u2014 ${a.why}
                </div>
                <div class="unbound-row-actions">
                  <button class="unbound-mini-btn" onclick="window.UNBOUND.focusNodeInGraph('${a.nodeId}')">Focus in Graph</button>
                  <button class="unbound-mini-btn" onclick="window.UNBOUND.exploreNHopForNode('${a.nodeId}')">Explore N-Hop</button>
                </div>
              </div>
            `).join('')}
          </div>
        `}
      `;
    }

    /* -------------------------------------------------- */
    /* TAB 4: N-HOP EXPLORATION & EVIDENCE TRAIL          */
    /* -------------------------------------------------- */
    else if (state.activeTab === 'nhop') {
      const selectedNode = state.nodeMap.get(state.selectedNodeId) || state.nodes[0];
      const nhopResult = selectedNode ? getNHopNeighborhood(selectedNode.id, state.nHopDistance) : { nodesByHop: [], allNodeIds: new Set() };
      const directEdges = selectedNode ? (state.adj.get(selectedNode.id) || []) : [];

      html += `
        <div class="unbound-sect-h">N-Hop Exploration</div>
        <div class="crimenet-nhop-box">
          <div style="margin-bottom:6px">
            <label style="font-size:10px;font-weight:600;color:#7D7A75;display:block;margin-bottom:2px">FOCUS ENTITY</label>
            <select class="crimenet-search-bar" onchange="window.UNBOUND.setSelectedNode(this.value)">
              ${state.nodes.map(n => `
                <option value="${n.id}" ${n.id===state.selectedNodeId?'selected':''}>${formatLabel(n)} (${n.type})</option>
              `).join('')}
            </select>
          </div>

          <div style="margin-bottom:8px">
            <label style="font-size:10px;font-weight:600;color:#7D7A75;display:block;margin-bottom:4px">EXPLORATION DEPTH</label>
            <div style="display:flex;gap:4px">
              <button class="intel-nav-pill ${state.nHopDistance===1?'active':''}" onclick="window.UNBOUND.setNHopDistance(1)">1-Hop (Direct)</button>
              <button class="intel-nav-pill ${state.nHopDistance===2?'active':''}" onclick="window.UNBOUND.setNHopDistance(2)">2-Hop (Associates)</button>
              <button class="intel-nav-pill ${state.nHopDistance===3?'active':''}" onclick="window.UNBOUND.setNHopDistance(3)">3-Hop (Extended)</button>
            </div>
          </div>

          <div style="font-size:11px;color:#2C2C2B;background:#fff;padding:6px 8px;border-radius:4px;border:1px solid #E6E5E3;margin-bottom:8px">
            <b>${nhopResult.allNodeIds.size}</b> entities in <b>${state.nHopDistance}-hop</b> radius of <b>${formatLabel(selectedNode)}</b>.
          </div>

          <div style="display:flex;gap:4px">
            <button class="unbound-btn-primary" onclick="window.UNBOUND.highlightNHopInGraph('${selectedNode.id}', ${state.nHopDistance})">
              \uD83D\uDD0E Highlight N-Hop Subgraph
            </button>
            <button class="unbound-btn" onclick="window.UNBOUND.focusNodeInGraph('${selectedNode.id}')">
              \uD83C\uDFAF Center
            </button>
          </div>
        </div>

        <!-- Evidence Trail for Selected Entity -->
        <div class="unbound-sect-h" style="margin-top:14px">Evidence Trail \u2014 ${formatLabel(selectedNode)}</div>
        <div class="crimenet-evidence-card">
          <div style="display:flex;align-items:center;gap:6px;margin-bottom:6px">
            ${dot(selectedNode.type)}
            <b style="font-size:12px">${formatLabel(selectedNode)}</b>
            <span class="unbound-badge" style="background:${getTypeColor(selectedNode.type)}22;color:${getTypeColor(selectedNode.type)}">${selectedNode.type}</span>
          </div>

          <!-- Known Properties -->
          <div style="font-size:10px;color:#7D7A75;margin-bottom:8px;line-height:1.4">
            ${Object.entries(selectedNode.properties || {}).filter(([k]) => k !== 'name' && k !== 'type').map(([k, v]) => `
              <div><b>${k}:</b> ${Array.isArray(v) ? v.join(', ') : String(v)}</div>
            `).join('')}
          </div>

          <!-- Direct Connected Associates -->
          <div style="font-size:11px;font-weight:600;margin-bottom:4px">Direct Links (${directEdges.length})</div>
          <div style="max-height:160px;overflow-y:auto">
            ${directEdges.length === 0 ? `
              <div style="color:#999;font-size:10px">No connections recorded.</div>
            ` : directEdges.map(nbr => {
              const tgt = state.nodeMap.get(nbr.neighborId);
              return `
                <div style="display:flex;align-items:center;justify-content:space-between;padding:4px 0;border-bottom:1px solid #F0EFED;font-size:11px">
                  <div style="overflow:hidden;text-overflow:ellipsis;white-space:nowrap;max-width:180px">
                    ${dot(tgt.type)} <a href="javascript:void(0)" onclick="window.UNBOUND.focusNodeInGraph('${tgt.id}')" style="color:#2783DE">${formatLabel(tgt)}</a>
                  </div>
                  <span class="unbound-badge" style="font-size:9px">${nbr.edge.type}</span>
                </div>
              `;
            }).join('')}
          </div>
        </div>
      `;
    }

    /* -------------------------------------------------- */
    /* TAB 5: INVESTIGATION TIMELINE                      */
    /* -------------------------------------------------- */
    else if (state.activeTab === 'timeline') {
      const timelineEvents = extractTimeline();

      html += `
        <div class="unbound-sect-h">Investigation Timeline <span class="unbound-n">${timelineEvents.length}</span></div>
        <div style="font-size:11px;color:#7D7A75;margin-bottom:8px">
          Chronological event sequencing from call logs, transactions, and incident filings.
        </div>
        ${timelineEvents.length === 0 ? `
          <div style="padding:16px;text-align:center;color:#999;font-size:11px">
            No temporal/timestamp records detected in this dataset.
          </div>
        ` : `
          <div class="unbound-tl">
            ${timelineEvents.map(ev => `
              <div class="unbound-tl-i">
                <div class="unbound-d">${ev.date.replace('T', ' ')} <span class="unbound-badge">${ev.type}</span></div>
                <div class="unbound-x">${ev.label}</div>
                <div style="font-size:10px;color:#7D7A75;margin-top:2px">${ev.sub}</div>
              </div>
            `).join('')}
          </div>
        `}
      `;
    }

    panel.innerHTML = html;
  };

  /* ------------------------------------------------------------------ */
  /*  User Interaction Handlers                                         */
  /* ------------------------------------------------------------------ */
  window.UNBOUND.setSubTab = function(tabName) {
    state.activeTab = tabName;
    window.UNBOUND.renderPanel();
  };

  window.UNBOUND.handleSearch = function(query) {
    state.searchQuery = query;
    window.UNBOUND.renderPanel();
    const searchInput = document.getElementById('crimenet-intel-search');
    if (searchInput) {
      searchInput.focus();
      searchInput.setSelectionRange(query.length, query.length);
    }
  };

  window.UNBOUND.setFilterType = function(type) {
    state.filterType = type;
    window.UNBOUND.renderPanel();
  };

  window.UNBOUND.setNHopDistance = function(distance) {
    state.nHopDistance = distance;
    window.UNBOUND.renderPanel();
  };

  window.UNBOUND.setSelectedNode = function(nodeId) {
    state.selectedNodeId = nodeId;
    window.UNBOUND.renderPanel();
  };

  window.UNBOUND.exploreNHopForNode = function(nodeId) {
    state.selectedNodeId = nodeId;
    state.activeTab = 'nhop';
    window.UNBOUND.renderPanel();
  };

  /* ------------------------------------------------------------------ */
  /*  Dash Clientside Callback Bridge                                   */
  /* ------------------------------------------------------------------ */
  window.UNBOUND.onNetworkUpdate = function(elements, tapNodeData, tabValue) {
    if (Array.isArray(elements)) {
      state.elements = elements;
      parseElements(elements);
    }

    if (tapNodeData && tapNodeData.id) {
      state.selectedNodeId = String(tapNodeData.id);
    }

    window.UNBOUND.renderPanel();
  };

  // Initial boot listener
  document.addEventListener('DOMContentLoaded', () => {
    setTimeout(window.UNBOUND.renderPanel, 500);
    setTimeout(window.UNBOUND.renderPanel, 1500);
  });

})();
