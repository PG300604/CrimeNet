/**
 * CrimeNet - Hierarchical Clustering Tree View
 * Interactive Tree Structure / Dendrogram visualization for network hierarchy
 */

(function () {
  'use strict';

  let currentTreeData = null;
  let selectedClusterNodeIds = null;
  let selectedClusterId = null;
  let selectedClusterLabel = null;
  let lastRawData = '';

  function getCytoscape() {
    const el = document.getElementById('cytoscape');
    if (el && el._cyreg && el._cyreg.cy) return el._cyreg.cy;
    if (window.cy && typeof window.cy.elements === 'function') return window.cy;
    return null;
  }

  function initObserver() {
    const dataContainer = document.getElementById('hierarchical-tree-data');
    if (!dataContainer) {
      setTimeout(initObserver, 300);
      return;
    }

    const checkData = () => {
      const raw = (dataContainer.textContent || '').trim();
      if (raw !== lastRawData) {
        lastRawData = raw;
        if (raw) {
          try {
            const data = JSON.parse(raw);
            currentTreeData = data;
            renderTree(data);
          } catch (e) {
            console.error('CrimeNet: Failed to parse hierarchical tree data', e);
          }
        } else {
          clearTree();
        }
      }
    };

    const observer = new MutationObserver(checkData);
    observer.observe(dataContainer, { childList: true, characterData: true, subtree: true });
    // Also periodic poll in case textContent was updated without childList trigger
    setInterval(checkData, 400);
  }

  function clearTree() {
    currentTreeData = null;
    selectedClusterNodeIds = null;
    selectedClusterId = null;
    selectedClusterLabel = null;

    const wrapper = document.getElementById('hierarchical-tree-view-wrapper');
    if (wrapper) wrapper.innerHTML = '';

    resetGraphHighlights();
  }

  function resetGraphHighlights() {
    const cy = getCytoscape();
    if (!cy) return;

    cy.batch(() => {
      cy.elements().removeClass('crimenet-cluster-node crimenet-cluster-edge crimenet-dimmed');
    });

    const activeHeaders = document.querySelectorAll('.hclust-node-header.active-tree-cluster, .hclust-leaf-row.active-tree-leaf');
    activeHeaders.forEach(el => el.classList.remove('active-tree-cluster', 'active-tree-leaf'));

    const inspectCard = document.getElementById('hclust-inspect-card');
    if (inspectCard) inspectCard.style.display = 'none';

    selectedClusterNodeIds = null;
    selectedClusterId = null;
    selectedClusterLabel = null;
  }

  function renderTree(treeData) {
    const wrapper = document.getElementById('hierarchical-tree-view-wrapper');
    if (!wrapper) return;

    wrapper.innerHTML = '';

    const rootContainer = document.createElement('div');
    rootContainer.className = 'hclust-view-container';

    // 1. Toolbar Controls
    const toolbar = document.createElement('div');
    toolbar.className = 'hclust-toolbar';

    const btnExpand = document.createElement('button');
    btnExpand.type = 'button';
    btnExpand.className = 'hclust-btn';
    btnExpand.textContent = 'Expand All';
    btnExpand.addEventListener('click', expandAll);

    const btnCollapse = document.createElement('button');
    btnCollapse.type = 'button';
    btnCollapse.className = 'hclust-btn';
    btnCollapse.textContent = 'Collapse All';
    btnCollapse.addEventListener('click', collapseAll);

    const btnFocus = document.createElement('button');
    btnFocus.type = 'button';
    btnFocus.className = 'hclust-btn';
    btnFocus.textContent = 'Focus Cluster';
    btnFocus.addEventListener('click', focusActiveCluster);

    const btnReset = document.createElement('button');
    btnReset.type = 'button';
    btnReset.className = 'hclust-btn hclust-btn-reset';
    btnReset.textContent = 'Reset';
    btnReset.addEventListener('click', () => {
      resetGraphHighlights();
      const cy = getCytoscape();
      if (cy) {
        cy.animate({ fit: { eles: cy.elements(), padding: 30 } }, { duration: 300 });
      }
    });

    toolbar.appendChild(btnExpand);
    toolbar.appendChild(btnCollapse);
    toolbar.appendChild(btnFocus);
    toolbar.appendChild(btnReset);
    rootContainer.appendChild(toolbar);

    // 2. Cluster Inspection Card (initially hidden)
    const inspectCard = document.createElement('div');
    inspectCard.id = 'hclust-inspect-card';
    inspectCard.className = 'hclust-inspect-card';
    inspectCard.style.display = 'none';
    rootContainer.appendChild(inspectCard);

    // 3. Tree Scroll Container
    const treeScroll = document.createElement('div');
    treeScroll.className = 'hclust-tree-scroll';

    const treeRoot = buildDOMTreeNode(treeData, 0);
    treeScroll.appendChild(treeRoot);
    rootContainer.appendChild(treeScroll);

    wrapper.appendChild(rootContainer);
  }

  function buildDOMTreeNode(nodeData, depth) {
    if (nodeData.is_leaf) {
      // Leaf Entity Item
      const leafRow = document.createElement('div');
      leafRow.className = 'hclust-leaf-row';
      leafRow.dataset.nodeId = String(nodeData.id);
      leafRow.style.paddingLeft = (depth * 16 + 18) + 'px';

      const leafDot = document.createElement('span');
      leafDot.className = 'hclust-leaf-dot';

      const leafLabel = document.createElement('span');
      leafLabel.className = 'hclust-leaf-label';
      leafLabel.textContent = nodeData.label || nodeData.id;
      leafLabel.title = `ID: ${nodeData.id}`;

      leafRow.appendChild(leafDot);
      leafRow.appendChild(leafLabel);

      leafRow.addEventListener('click', (e) => {
        e.stopPropagation();
        onLeafClick(nodeData, leafRow);
      });

      return leafRow;
    }

    // Cluster Branch Item
    const branchContainer = document.createElement('div');
    branchContainer.className = 'hclust-branch-container';

    const header = document.createElement('div');
    header.className = 'hclust-node-header';
    header.dataset.clusterId = nodeData.id;
    header.style.paddingLeft = (depth * 16 + 4) + 'px';

    const toggleIcon = document.createElement('span');
    toggleIcon.className = 'hclust-toggle-icon';
    toggleIcon.textContent = depth >= 2 ? '▶' : '▼';

    const labelSpan = document.createElement('span');
    labelSpan.className = 'hclust-cluster-label';
    labelSpan.textContent = nodeData.label;

    const countBadge = document.createElement('span');
    countBadge.className = 'hclust-count-badge';
    countBadge.textContent = String(nodeData.size || (nodeData.nodes ? nodeData.nodes.length : 0));
    countBadge.title = `${countBadge.textContent} entities`;

    header.appendChild(toggleIcon);
    header.appendChild(labelSpan);
    header.appendChild(countBadge);

    const childrenContainer = document.createElement('div');
    childrenContainer.className = 'hclust-children-container';
    if (depth >= 2) {
      childrenContainer.classList.add('collapsed');
    }

    // Toggle expand/collapse when clicking arrow
    toggleIcon.addEventListener('click', (e) => {
      e.stopPropagation();
      const isCollapsed = childrenContainer.classList.toggle('collapsed');
      toggleIcon.textContent = isCollapsed ? '▶' : '▼';
    });

    // Selecting cluster when clicking header
    header.addEventListener('click', (e) => {
      e.stopPropagation();
      onClusterClick(nodeData, header);
    });

    branchContainer.appendChild(header);

    if (nodeData.children && nodeData.children.length > 0) {
      nodeData.children.forEach(child => {
        childrenContainer.appendChild(buildDOMTreeNode(child, depth + 1));
      });
    }

    branchContainer.appendChild(childrenContainer);
    return branchContainer;
  }

  function onClusterClick(clusterData, headerElement) {
    // 1. Highlight in Tree UI
    document.querySelectorAll('.hclust-node-header.active-tree-cluster, .hclust-leaf-row.active-tree-leaf')
      .forEach(el => el.classList.remove('active-tree-cluster', 'active-tree-leaf'));
    headerElement.classList.add('active-tree-cluster');

    selectedClusterId = clusterData.id;
    selectedClusterLabel = clusterData.label;
    selectedClusterNodeIds = clusterData.nodes || [];

    // 2. Highlight Cluster in Cytoscape & Dim non-cluster nodes
    const cy = getCytoscape();
    if (cy && selectedClusterNodeIds.length > 0) {
      cy.batch(() => {
        // Reset classes
        cy.elements().removeClass('crimenet-cluster-node crimenet-cluster-edge crimenet-dimmed');

        // Dim everything
        cy.elements().addClass('crimenet-dimmed');

        // Un-dim & highlight cluster nodes
        const clusterNodeSet = new Set(selectedClusterNodeIds.map(String));
        const clusterNodes = cy.nodes().filter(node => clusterNodeSet.has(String(node.id())));
        clusterNodes.removeClass('crimenet-dimmed').addClass('crimenet-cluster-node');

        // Highlight edges where both source and target are in cluster
        const clusterEdges = clusterNodes.connectedEdges().filter(edge => {
          return clusterNodeSet.has(String(edge.source().id())) && clusterNodeSet.has(String(edge.target().id()));
        });
        clusterEdges.removeClass('crimenet-dimmed').addClass('crimenet-cluster-edge');
      });
    }

    // 3. Update Cluster Inspection Card
    updateInspectionCard(clusterData);
  }

  function updateInspectionCard(clusterData) {
    const inspectCard = document.getElementById('hclust-inspect-card');
    if (!inspectCard) return;

    inspectCard.style.display = 'block';
    inspectCard.innerHTML = '';

    // Card Header
    const cardHeader = document.createElement('div');
    cardHeader.className = 'hclust-card-header';

    const titleBox = document.createElement('div');
    titleBox.className = 'hclust-card-title-box';

    const title = document.createElement('span');
    title.className = 'hclust-card-title';
    title.textContent = clusterData.label;

    const sizeBadge = document.createElement('span');
    sizeBadge.className = 'hclust-card-size';
    sizeBadge.textContent = `${clusterData.size || clusterData.nodes.length} entities`;

    titleBox.appendChild(title);
    titleBox.appendChild(sizeBadge);

    const closeBtn = document.createElement('button');
    closeBtn.type = 'button';
    closeBtn.className = 'hclust-card-close';
    closeBtn.textContent = '✕';
    closeBtn.title = 'Close inspection';
    closeBtn.addEventListener('click', (e) => {
      e.stopPropagation();
      resetGraphHighlights();
    });

    cardHeader.appendChild(titleBox);
    cardHeader.appendChild(closeBtn);
    inspectCard.appendChild(cardHeader);

    // Action buttons in Card
    const actionsRow = document.createElement('div');
    actionsRow.className = 'hclust-card-actions';

    const btnFocus = document.createElement('button');
    btnFocus.type = 'button';
    btnFocus.className = 'hclust-card-btn';
    btnFocus.textContent = 'Focus in Graph';
    btnFocus.addEventListener('click', focusActiveCluster);

    actionsRow.appendChild(btnFocus);
    inspectCard.appendChild(actionsRow);

    // Entity Badges List
    const entityListWrapper = document.createElement('div');
    entityListWrapper.className = 'hclust-card-entities-wrapper';

    const entityListLabel = document.createElement('div');
    entityListLabel.className = 'hclust-card-entities-label';
    entityListLabel.textContent = 'Cluster Entities:';
    entityListWrapper.appendChild(entityListLabel);

    const chipsContainer = document.createElement('div');
    chipsContainer.className = 'hclust-card-chips';

    const cy = getCytoscape();
    const nodeIds = clusterData.nodes || [];

    nodeIds.forEach(id => {
      const chip = document.createElement('span');
      chip.className = 'hclust-entity-chip';
      let displayLabel = String(id);
      if (cy) {
        const cyNode = cy.getElementById(String(id));
        if (cyNode.length && cyNode.data('label')) {
          displayLabel = cyNode.data('label');
        }
      }
      chip.textContent = displayLabel;
      chip.title = `Click to select ${displayLabel}`;

      chip.addEventListener('click', (e) => {
        e.stopPropagation();
        focusSingleNode(id);
      });

      chipsContainer.appendChild(chip);
    });

    entityListWrapper.appendChild(chipsContainer);
    inspectCard.appendChild(entityListWrapper);
  }

  function onLeafClick(leafData, leafElement) {
    document.querySelectorAll('.hclust-node-header.active-tree-cluster, .hclust-leaf-row.active-tree-leaf')
      .forEach(el => el.classList.remove('active-tree-cluster', 'active-tree-leaf'));
    leafElement.classList.add('active-tree-leaf');

    focusSingleNode(leafData.id);
  }

  function focusSingleNode(nodeId) {
    const cy = getCytoscape();
    if (!cy) return;

    const cyNode = cy.getElementById(String(nodeId));
    if (!cyNode.length) return;

    cy.batch(() => {
      cy.$(':selected').unselect();
      cyNode.select();
    });

    try {
      cyNode.emit('tap');
    } catch (e) {
      console.debug('CrimeNet: tap event emitted', e);
    }

    const currentZoom = cy.zoom();
    const targetZoom = Math.max(currentZoom, 1.35);

    cy.animate({
      center: { eles: cyNode },
      zoom: targetZoom
    }, {
      duration: 350
    });
  }

  function focusActiveCluster() {
    const cy = getCytoscape();
    if (!cy) return;

    if (!selectedClusterNodeIds || selectedClusterNodeIds.length === 0) {
      const firstHeader = document.querySelector('.hclust-node-header');
      if (firstHeader) {
        firstHeader.click();
        return;
      }
      return;
    }

    const clusterNodeSet = new Set(selectedClusterNodeIds.map(String));
    const clusterNodes = cy.nodes().filter(node => clusterNodeSet.has(String(node.id())));

    if (clusterNodes.length > 0) {
      cy.animate({
        fit: { eles: clusterNodes, padding: 60 }
      }, {
        duration: 350
      });
    }
  }

  function expandAll() {
    const childrenList = document.querySelectorAll('.hclust-children-container');
    childrenList.forEach(el => el.classList.remove('collapsed'));
    const toggleIcons = document.querySelectorAll('.hclust-toggle-icon');
    toggleIcons.forEach(icon => icon.textContent = '▼');
  }

  function collapseAll() {
    // Keep root (depth 0) and top clusters (depth 1) open, collapse sub-clusters
    const containers = document.querySelectorAll('.hclust-branch-container');
    containers.forEach(container => {
      const header = container.querySelector(':scope > .hclust-node-header');
      const children = container.querySelector(':scope > .hclust-children-container');
      const toggle = header ? header.querySelector('.hclust-toggle-icon') : null;

      if (header && children) {
        const clusterId = header.dataset.clusterId;
        // Keep root open
        if (clusterId === 'root') {
          children.classList.remove('collapsed');
          if (toggle) toggle.textContent = '▼';
        } else {
          children.classList.add('collapsed');
          if (toggle) toggle.textContent = '▶';
        }
      }
    });
  }

  // Initialize once DOM is ready
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initObserver);
  } else {
    initObserver();
  }
})();
