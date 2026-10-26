/* ==========================================================================
   Vi (Vodafone Idea) Intelligent NOC — Frontend Application Engine
   Synchronizes:
   - 1,000 Historical Resolved Tickets (25/page pagination + multi-select filters)
   - 6 Systemic Failure Clusters & Golden Correlation (VLAN 402 = 1420B)
   - Conversational Executive Insights Console ("Ask Gemini")
   - 100 Open Active Tickets synchronized across Tab 2 (Cross-Domain RCA) & Tab 3 (CLI + RCA Export)
   ========================================================================== */

const APP_STATE = {
  activeTab: 1,
  selectedOpenTicketId: "INC-Telco-OPEN-001",
  clusters: [],
  queryTemplates: [],
  openTickets: [],
  openTicketsMap: {},
  historicalTickets: [],
  filteredHistorical: [],
  currentPage: 1,
  pageSize: 25,
  filters: {
    domain: new Set(),
    severity: new Set(),
    circle: new Set(),
    clusterId: null,
    goldenOnly: false,
    search: "",
  },
  darkMode: false,
  simTimer: null,
};

function escapeHtml(str) {
  if (str === null || str === undefined) return "";
  return String(str)
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;");
}

function formatRichMarkdownInline(text) {
  if (!text) return "";
  let s = escapeHtml(text);
  s = s.replace(/\*\*(.+?)\*\*/g, "<strong>$1</strong>");
  s = s.replace(/`([^`]+)`/g, '<code class="mono-code" style="background:rgba(238,39,55,0.1);padding:1px 6px;border-radius:5px;color:var(--vi-red);">$1</code>');
  s = s.replace(/\n/g, "<br/>");
  return s;
}

function severityBadgeClass(sev) {
  if (!sev) return "badge-p3";
  if (sev.startsWith("P1")) return "badge-p1";
  if (sev.startsWith("P2")) return "badge-p2";
  return "badge-p3";
}

function updateClock() {
  const el = document.getElementById("live-ist-clock");
  if (!el) return;
  const now = new Date();
  const istTime = now.toLocaleTimeString("en-IN", {
    timeZone: "Asia/Kolkata",
    hour12: false,
  });
  el.textContent = `IST ${istTime}`;
}

setInterval(updateClock, 1000);
updateClock();

/* --------------------------------------------------------------------------
   Bootstrap Dataset on Startup
   -------------------------------------------------------------------------- */
async function initApp() {
  try {
    const res = await fetch("/api/bootstrap");
    const data = await res.json();

    APP_STATE.clusters = data.clusters || [];
    APP_STATE.queryTemplates = data.query_templates || [];
    APP_STATE.openTickets = data.open_tickets || [];
    APP_STATE.openTicketsMap = {};
    APP_STATE.openTickets.forEach((t) => {
      APP_STATE.openTicketsMap[t.ticket_id] = t;
    });
    APP_STATE.historicalTickets = data.historical_tickets || [];
    APP_STATE.selectedOpenTicketId = data.default_open_ticket_id || "INC-Telco-OPEN-001";

    renderClusters();
    populateExecutiveQueryDropdown();
    populateOpenTicketsDropdowns();
    applyHistoricalFilters();
    selectOpenTicket(APP_STATE.selectedOpenTicketId);
  } catch (err) {
    console.error("Failed to bootstrap Vi NOC demo:", err);
  }
}

/* --------------------------------------------------------------------------
   Navigation & Theme Toggle
   -------------------------------------------------------------------------- */
function switchTab(tabNum) {
  APP_STATE.activeTab = tabNum;
  [1, 2, 3].forEach((n) => {
    const btn = document.getElementById(`nav-tab-${n}`);
    const panel = document.getElementById(`tab-panel-${n}`);
    if (btn) btn.classList.toggle("active", n === tabNum);
    if (panel) panel.classList.toggle("active", n === tabNum);
  });
  window.scrollTo({ top: 0, behavior: "smooth" });
}

function toggleTheme() {
  APP_STATE.darkMode = !APP_STATE.darkMode;
  document.body.classList.toggle("noc-dark", APP_STATE.darkMode);
  const btn = document.getElementById("theme-toggle-button");
  if (btn) {
    btn.innerHTML = APP_STATE.darkMode ? "☀️ myvi.in Theme" : "🌙 NOC Wall Dark";
  }
}

/* --------------------------------------------------------------------------
   Tab 1: 6 Systemic Failure Clusters
   -------------------------------------------------------------------------- */
function renderClusters() {
  const container = document.getElementById("clusters-container");
  if (!container) return;

  container.innerHTML = APP_STATE.clusters
    .map((c) => {
      const isGolden = c.cluster_id === "CLU-01";
      const isSelected = APP_STATE.filters.clusterId === c.cluster_id;
      return `
        <div class="cluster-card ${isGolden ? "golden-cluster" : ""} ${isSelected ? "selected-cluster" : ""}"
             onclick="filterByCluster('${c.cluster_id}')">
          <div>
            <div class="cluster-top-row">
              <span class="cluster-num-badge">Cluster ${c.number} • ${escapeHtml(c.primary_domain)}</span>
              <span class="cluster-vol-badge">${c.ticket_count} Tickets (${escapeHtml(c.pct_of_total)})</span>
            </div>
            <h4 style="margin-top:10px;">${escapeHtml(c.title)}</h4>
            ${
              isGolden
                ? `<div style="margin-top:6px;"><span class="badge badge-p1">★ Golden Correlation: 46 Coordinated VLAN 402 Tickets</span></div>`
                : ""
            }
            <p class="cluster-desc" style="margin-top:8px;">${escapeHtml(c.root_cause_pattern)}</p>
          </div>
          <div class="cluster-meta-footer">
            <span class="mono-code">${escapeHtml(c.rfo_reference)}</span>
            <span style="color:var(--status-resolved);">MTTR: ${c.avg_mttr_before_min}m ➔ ${c.avg_mttr_after_min}m (-${escapeHtml(c.mttr_reduction_pct)})</span>
          </div>
        </div>
      `;
    })
    .join("");
}

function runClusterDiscoveryAnimation() {
  const statusEl = document.getElementById("cluster-analysis-status");
  const btn = document.getElementById("btn-analyze-clusters");
  if (!statusEl || !btn) return;

  btn.disabled = true;
  btn.textContent = "⏳ Scanning 1,000 Tickets...";
  statusEl.style.display = "block";
  statusEl.innerHTML =
    "🔍 <strong>Step 1/2:</strong> Embedding 1,000 tickets &amp; correlating cross-domain alarms...";

  setTimeout(() => {
    statusEl.innerHTML =
      "✓ <strong>6 Systemic Clusters Verified:</strong> Spotlighting <strong>46 Golden Correlation tickets (VLAN 402 MTU=1420B, RFO-Telco-2026-0811)</strong> • <strong>-42% MTTR</strong>.";
    btn.disabled = false;
    btn.textContent = "✓ 6 Systemic Clusters Verified";
  }, 750);
}

function filterByCluster(clusterId) {
  if (APP_STATE.filters.clusterId === clusterId) {
    APP_STATE.filters.clusterId = null;
  } else {
    APP_STATE.filters.clusterId = clusterId;
  }
  const clearBtn = document.getElementById("btn-clear-cluster-filter");
  if (clearBtn) {
    clearBtn.style.display = APP_STATE.filters.clusterId ? "inline-flex" : "none";
  }
  APP_STATE.currentPage = 1;
  renderClusters();
  applyHistoricalFilters();
}

/* --------------------------------------------------------------------------
   Tab 1: Conversational Executive Insights Console ("Ask Gemini")
   -------------------------------------------------------------------------- */
function populateExecutiveQueryDropdown() {
  const select = document.getElementById("exec-query-select");
  const input = document.getElementById("exec-query-input");
  if (!select || !input) return;

  const optsHtml = APP_STATE.queryTemplates
    .map(
      (q, i) =>
        `<option value="${escapeHtml(q.id)}">${i + 1}. ${escapeHtml(q.question)}</option>`
    )
    .concat([`<option value="custom">-- Type your own custom question below --</option>`])
    .join("");

  select.innerHTML = optsHtml;

  if (APP_STATE.queryTemplates.length > 0) {
    select.value = APP_STATE.queryTemplates[0].id;
    input.value = APP_STATE.queryTemplates[0].question;
    renderExecutiveInsightCard(APP_STATE.queryTemplates[0], "gemini-3.8-flash • Vertex AI (Global)", 135);
  }
}

function onSelectExecutiveTemplate() {
  const select = document.getElementById("exec-query-select");
  const input = document.getElementById("exec-query-input");
  if (!select || !input) return;

  const val = select.value;
  if (val === "custom") {
    input.value = "";
    input.focus();
    return;
  }
  const found = APP_STATE.queryTemplates.find((q) => q.id === val);
  if (found) {
    input.value = found.question;
    submitExecutiveQuery(false);
  }
}

async function submitExecutiveQuery(forceLive) {
  const select = document.getElementById("exec-query-select");
  const input = document.getElementById("exec-query-input");
  const out = document.getElementById("gemini-insights-output");
  const pill = document.getElementById("ask-gemini-model-pill");
  if (!input || !out) return;

  const question = input.value.trim();
  if (!question) return;

  const templateId = select && select.value !== "custom" ? select.value : null;

  out.innerHTML = `
    <div style="padding:18px;display:flex;align-items:center;gap:12px;font-weight:700;color:var(--vi-red);">
      <span>⚡ Gemini 3.8 Flash analyzing 1,000 historical resolved tickets &amp; RFO citations...</span>
    </div>
  `;

  try {
    const res = await fetch("/api/ai/ask", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        question,
        template_id: templateId,
        force_live: Boolean(forceLive),
      }),
    });
    const data = await res.json();
    if (pill && data.model_used) {
      pill.textContent = `${data.model_used} (${data.latency_ms || 140} ms)`;
    }
    renderExecutiveInsightCard(data, data.model_used || "gemini-3.8-flash", data.latency_ms || 140);
  } catch (err) {
    out.innerHTML = `<div style="color:var(--status-p1);font-weight:700;">Error querying Gemini Insights: ${escapeHtml(err.message)}</div>`;
  }
}

function renderExecutiveInsightCard(data, modelUsed, latencyMs) {
  const out = document.getElementById("gemini-insights-output");
  if (!out || !data) return;

  const metricsHtml = (data.summary_metrics || [])
    .map(
      (m) => `
      <div class="response-kpi-item">
        <div class="rk-lbl">${escapeHtml(m.label)}</div>
        <div class="rk-val">${escapeHtml(m.value)}</div>
        <div class="rk-sub">${escapeHtml(m.delta)}</div>
      </div>
    `
    )
    .join("");

  const citationsHtml = (data.evidence_citations || [])
    .map((c) => `<li>${formatRichMarkdownInline(c)}</li>`)
    .join("");

  out.innerHTML = `
    <div class="gemini-response-header">
      <h4>🎯 ${escapeHtml(data.headline || data.question)}</h4>
      <span class="gemini-model-tag">✓ ${escapeHtml(modelUsed)} • ${latencyMs} ms</span>
    </div>

    <div class="response-kpi-strip">
      ${metricsHtml}
    </div>

    <div class="response-sections-grid">
      <div class="response-box">
        <h5>📊 Direct Executive Summary &amp; Cross-Domain Metrics</h5>
        <p>${formatRichMarkdownInline(data.executive_summary)}</p>
      </div>

      <div class="response-box">
        <h5>📑 Evidence &amp; Historical Ticket Citations</h5>
        <ul>${citationsHtml}</ul>
        <div class="rec-callout">
          <strong>🛠️ Actionable Operational Recommendation:</strong><br/>
          ${formatRichMarkdownInline(data.operational_recommendation)}
        </div>
      </div>
    </div>
  `;
}

/* --------------------------------------------------------------------------
   Tab 1: Searchable & Multi-Select Filtered Data Table (1,000 Tickets, 25/page)
   -------------------------------------------------------------------------- */
function toggleMultiFilter(filterType, value) {
  const set = APP_STATE.filters[filterType];
  if (!set) return;
  if (set.has(value)) {
    set.delete(value);
  } else {
    set.add(value);
  }
  APP_STATE.currentPage = 1;
  syncFilterChipsUI();
  applyHistoricalFilters();
}

function toggleGoldenFilter() {
  APP_STATE.filters.goldenOnly = !APP_STATE.filters.goldenOnly;
  const btn = document.getElementById("btn-filter-golden");
  if (btn) {
    btn.style.background = APP_STATE.filters.goldenOnly ? "var(--vi-red)" : "";
    btn.style.color = APP_STATE.filters.goldenOnly ? "#ffffff" : "";
    btn.style.borderColor = APP_STATE.filters.goldenOnly ? "var(--vi-red)" : "";
  }
  APP_STATE.currentPage = 1;
  applyHistoricalFilters();
}

function resetTableFilters() {
  APP_STATE.filters.domain.clear();
  APP_STATE.filters.severity.clear();
  APP_STATE.filters.circle.clear();
  APP_STATE.filters.clusterId = null;
  APP_STATE.filters.goldenOnly = false;
  APP_STATE.filters.search = "";

  const searchInput = document.getElementById("historical-search-input");
  if (searchInput) searchInput.value = "";

  const goldenBtn = document.getElementById("btn-filter-golden");
  if (goldenBtn) {
    goldenBtn.style.background = "";
    goldenBtn.style.color = "";
    goldenBtn.style.borderColor = "";
  }

  const clearClusterBtn = document.getElementById("btn-clear-cluster-filter");
  if (clearClusterBtn) clearClusterBtn.style.display = "none";

  APP_STATE.currentPage = 1;
  syncFilterChipsUI();
  renderClusters();
  applyHistoricalFilters();
}

function syncFilterChipsUI() {
  document.querySelectorAll(".filter-chip").forEach((chip) => {
    const ftype = chip.getAttribute("data-filter-type");
    const val = chip.getAttribute("data-val");
    const active = APP_STATE.filters[ftype] && APP_STATE.filters[ftype].has(val);
    chip.classList.toggle("active", Boolean(active));
  });
}

function onHistoricalSearchInput() {
  const el = document.getElementById("historical-search-input");
  APP_STATE.filters.search = el ? el.value.trim().toLowerCase() : "";
  APP_STATE.currentPage = 1;
  applyHistoricalFilters();
}

function applyHistoricalFilters() {
  const { domain, severity, circle, clusterId, goldenOnly, search } = APP_STATE.filters;

  APP_STATE.filteredHistorical = APP_STATE.historicalTickets.filter((t) => {
    if (domain.size > 0 && !domain.has(t.domain)) return false;
    if (severity.size > 0 && !severity.has(t.severity)) return false;
    if (circle.size > 0 && !circle.has(t.circle)) return false;
    if (clusterId && t.cluster_id !== clusterId) return false;
    if (goldenOnly && !t.is_golden_correlation) return false;
    if (search) {
      const hay = `${t.ticket_id} ${t.affected_nodes} ${t.alarm_summary} ${t.root_cause} ${t.rfo_id} ${t.circle}`.toLowerCase();
      if (!hay.includes(search)) return false;
    }
    return true;
  });

  renderHistoricalTablePage();
}

function renderHistoricalTablePage() {
  const tbody = document.getElementById("historical-table-body");
  const summaryEl = document.getElementById("table-showing-summary");
  const pageInfoEl = document.getElementById("pagination-info");
  const pageBadgeEl = document.getElementById("page-number-badge");
  if (!tbody) return;

  const total = APP_STATE.filteredHistorical.length;
  const totalPages = Math.max(1, Math.ceil(total / APP_STATE.pageSize));
  if (APP_STATE.currentPage > totalPages) APP_STATE.currentPage = totalPages;
  if (APP_STATE.currentPage < 1) APP_STATE.currentPage = 1;

  const startIdx = (APP_STATE.currentPage - 1) * APP_STATE.pageSize;
  const endIdx = Math.min(startIdx + APP_STATE.pageSize, total);
  const slice = APP_STATE.filteredHistorical.slice(startIdx, endIdx);

  if (summaryEl) {
    summaryEl.textContent =
      total === 0
        ? "0 matching tickets"
        : `Showing ${startIdx + 1}–${endIdx} of ${total.toLocaleString()} resolved tickets`;
  }
  if (pageInfoEl) {
    pageInfoEl.textContent = `Page ${APP_STATE.currentPage} of ${totalPages} (25 records per page)`;
  }
  if (pageBadgeEl) {
    pageBadgeEl.textContent = `Page ${APP_STATE.currentPage} / ${totalPages}`;
  }

  if (slice.length === 0) {
    tbody.innerHTML = `
      <tr>
        <td colspan="9" style="text-align:center;padding:28px;font-weight:700;color:var(--text-secondary);">
          No historical tickets match the current filter combination. Click "Reset All Filters" to restore all 1,000 records.
        </td>
      </tr>
    `;
    return;
  }

  tbody.innerHTML = slice
    .map((t) => {
      const sevClass = severityBadgeClass(t.severity);
      return `
        <tr class="${t.is_golden_correlation ? "golden-row" : ""}" onclick="openHistoricalTicketModal('${t.ticket_id}')">
          <td class="mono-code" style="font-weight:800;color:var(--vi-red);">
            ${escapeHtml(t.ticket_id)}
            ${t.is_golden_correlation ? `<div style="font-size:10px;color:#d97706;">★ Golden VLAN 402</div>` : ""}
          </td>
          <td><span class="badge ${sevClass}">${escapeHtml(t.severity)}</span></td>
          <td><span class="badge badge-domain">${escapeHtml(t.domain)}</span></td>
          <td style="font-weight:700;">${escapeHtml(t.circle)}</td>
          <td class="mono-code" style="max-width:220px;">${escapeHtml(t.affected_nodes)}</td>
          <td style="max-width:340px;">
            <div style="font-weight:700;">${escapeHtml(t.alarm_summary)}</div>
            <div style="font-size:11.5px;color:var(--text-secondary);margin-top:2px;"><strong>RCA:</strong> ${escapeHtml(t.root_cause)}</div>
          </td>
          <td class="mono-code" style="font-weight:700;">${t.mttr_minutes}m</td>
          <td class="mono-code"><span class="badge badge-domain">${escapeHtml(t.rfo_id)}</span></td>
          <td><span class="badge badge-resolved">✓ ${escapeHtml(t.status)}</span></td>
        </tr>
      `;
    })
    .join("");
}

function changePage(delta) {
  APP_STATE.currentPage += delta;
  renderHistoricalTablePage();
}

function goToPage(p) {
  const totalPages = Math.max(1, Math.ceil(APP_STATE.filteredHistorical.length / APP_STATE.pageSize));
  APP_STATE.currentPage = Math.min(Math.max(1, p), totalPages);
  renderHistoricalTablePage();
}

function openHistoricalTicketModal(ticketId) {
  const t = APP_STATE.historicalTickets.find((x) => x.ticket_id === ticketId);
  if (!t) return;
  const titleEl = document.getElementById("modal-title");
  const bodyEl = document.getElementById("modal-body-content");
  const backdrop = document.getElementById("vi-modal-backdrop");
  if (!titleEl || !bodyEl || !backdrop) return;

  titleEl.innerHTML = `🗂️ Historical Ticket Record: <span class="mono-code" style="color:var(--vi-red);">${escapeHtml(t.ticket_id)}</span>`;
  bodyEl.innerHTML = `
    <div style="display:flex;gap:8px;flex-wrap:wrap;margin-bottom:14px;">
      <span class="badge ${severityBadgeClass(t.severity)}">${escapeHtml(t.severity)}</span>
      <span class="badge badge-domain">${escapeHtml(t.domain)}</span>
      <span class="badge badge-domain">${escapeHtml(t.circle)}</span>
      <span class="badge badge-resolved">✓ ${escapeHtml(t.status)} (MTTR: ${t.mttr_minutes} mins)</span>
      <span class="badge badge-domain mono-code">${escapeHtml(t.rfo_id)}</span>
    </div>
    <div class="metadata-kv-list">
      <div class="metadata-kv-row"><span class="kv-k">Affected Network Elements</span><span class="kv-v mono-code">${escapeHtml(t.affected_nodes)}</span></div>
      <div class="metadata-kv-row"><span class="kv-k">Detected / Resolved</span><span class="kv-v mono-code">${escapeHtml(t.timestamp)} ➔ ${escapeHtml(t.resolved_at)}</span></div>
      <div class="metadata-kv-row"><span class="kv-k">Systemic Cluster ID</span><span class="kv-v mono-code">${escapeHtml(t.cluster_id)} ${t.is_golden_correlation ? "(Golden Correlation Cluster)" : ""}</span></div>
    </div>
    <div style="margin-top:14px;padding:14px;border-radius:12px;background:var(--bg-surface-alt);border:1px solid var(--border-warm);">
      <div style="font-weight:800;color:var(--vi-red);margin-bottom:4px;">Alarm Summary</div>
      <div>${escapeHtml(t.alarm_summary)}</div>
      <div style="font-weight:800;color:var(--vi-red);margin-top:12px;margin-bottom:4px;">Verified Root Cause</div>
      <div>${escapeHtml(t.root_cause)}</div>
      <div style="font-weight:800;color:var(--status-resolved);margin-top:12px;margin-bottom:4px;">Executed Resolution Steps</div>
      <div class="mono-code">${escapeHtml(t.resolution_steps)}</div>
    </div>
  `;
  backdrop.classList.add("open");
}

/* --------------------------------------------------------------------------
   Tab 2 & Tab 3: Synchronized 100 Open Active Tickets
   -------------------------------------------------------------------------- */
function populateOpenTicketsDropdowns() {
  const s2 = document.getElementById("tab2-ticket-select");
  const s3 = document.getElementById("tab3-ticket-select");
  if (!s2 || !s3) return;

  const optionsHtml = APP_STATE.openTickets
    .map((t) => {
      const snip = t.alarm_summary.length > 72 ? t.alarm_summary.slice(0, 72) + "..." : t.alarm_summary;
      return `<option value="${escapeHtml(t.ticket_id)}">[${escapeHtml(t.severity)}] ${escapeHtml(t.ticket_id)} - ${escapeHtml(t.domain_label)} (${escapeHtml(t.circle)}) - ${escapeHtml(snip)}</option>`;
    })
    .join("");

  s2.innerHTML = optionsHtml;
  s3.innerHTML = optionsHtml;
}

function selectOpenTicket(ticketId) {
  const ticket = APP_STATE.openTicketsMap[ticketId];
  if (!ticket) return;

  APP_STATE.selectedOpenTicketId = ticketId;

  // Synchronize both dropdowns
  const s2 = document.getElementById("tab2-ticket-select");
  const s3 = document.getElementById("tab3-ticket-select");
  if (s2 && s2.value !== ticketId) s2.value = ticketId;
  if (s3 && s3.value !== ticketId) s3.value = ticketId;

  // Synchronize header badge
  const headerBadge = document.getElementById("header-active-ticket-badge");
  if (headerBadge) {
    headerBadge.textContent = `${ticket.ticket_id} (${ticket.severity.split("-")[0]})`;
    headerBadge.className = `badge ${severityBadgeClass(ticket.severity)} mono-code`;
  }

  // Synchronize quick anchor pills on Tab 2 & Tab 3
  ["001", "002", "003"].forEach((suffix) => {
    const id = `INC-Telco-OPEN-${suffix}`;
    const p2 = document.getElementById(`pill-open-${suffix}`);
    const p3 = document.getElementById(`t3-pill-open-${suffix}`);
    if (p2) p2.classList.toggle("active", ticketId === id);
    if (p3) p3.classList.toggle("active", ticketId === id);
  });

  renderTab2TicketSummary(ticket);
  renderTab2CopilotOutput(ticket, null, "gemini-3.8-flash • Vertex AI Cross-Domain Engine", 165);
  renderTab3RemediationAndRca(ticket);
}

function renderTab2TicketSummary(ticket) {
  const sevBadge = document.getElementById("t2-severity-badge");
  const metaList = document.getElementById("t2-ticket-metadata");
  const alarmEl = document.getElementById("t2-alarm-summary");
  const topoEl = document.getElementById("t2-topology-container");

  if (sevBadge) {
    sevBadge.className = `badge ${severityBadgeClass(ticket.severity)}`;
    sevBadge.textContent = ticket.severity;
  }

  if (metaList) {
    metaList.innerHTML = `
      <div class="metadata-kv-row"><span class="kv-k">Ticket ID</span><span class="kv-v mono-code" style="color:var(--vi-red);">${escapeHtml(ticket.ticket_id)}</span></div>
      <div class="metadata-kv-row"><span class="kv-k">Queue Status</span><span class="kv-v"><span class="badge badge-open">${escapeHtml(ticket.status)}</span></span></div>
      <div class="metadata-kv-row"><span class="kv-k">Vi Telecom Circle</span><span class="kv-v">${escapeHtml(ticket.circle)}</span></div>
      <div class="metadata-kv-row"><span class="kv-k">Primary Domain</span><span class="kv-v"><span class="badge badge-domain">${escapeHtml(ticket.domain_label)}</span></span></div>
      <div class="metadata-kv-row"><span class="kv-k">Affected Nodes</span><span class="kv-v mono-code">${escapeHtml(ticket.affected_nodes)}</span></div>
      <div class="metadata-kv-row"><span class="kv-k">Detection Time</span><span class="kv-v mono-code">${escapeHtml(ticket.timestamp)}</span></div>
      <div class="metadata-kv-row"><span class="kv-k">Initial RCA State</span><span class="kv-v" style="color:#d97706;">${escapeHtml(ticket.root_cause)}</span></div>
    `;
  }

  if (alarmEl) {
    alarmEl.textContent = ticket.alarm_summary;
  }

  if (topoEl && ticket.triage && ticket.triage.cross_domain_correlation) {
    const path = ticket.triage.cross_domain_correlation.topology_path || [];
    topoEl.innerHTML = path
      .map(
        (node) => `
        <div class="topo-node-card state-${escapeHtml(node.state)}">
          <div>
            <div style="font-size:11px;font-weight:800;text-transform:uppercase;color:var(--text-secondary);">${escapeHtml(node.layer)}</div>
            <div class="mono-code" style="font-weight:800;font-size:13px;color:var(--text-primary);">${escapeHtml(node.node)}</div>
            <div style="font-size:12px;color:var(--text-secondary);margin-top:2px;">${escapeHtml(node.symptom)}</div>
          </div>
          <span class="badge ${node.state === "critical" ? "badge-p1" : node.state === "warn" ? "badge-p2" : "badge-resolved"}">
            ${node.state === "critical" ? "CRITICAL" : node.state === "warn" ? "CORRELATED" : "NORMAL"}
          </span>
        </div>
      `
      )
      .join("");
  }
}

async function runCopilotTriage(forceLive) {
  const ticket = APP_STATE.openTicketsMap[APP_STATE.selectedOpenTicketId];
  if (!ticket) return;

  const out = document.getElementById("t2-copilot-output");
  if (out) {
    out.innerHTML = `
      <div style="padding:22px;border-radius:14px;background:var(--bg-surface-alt);font-weight:700;color:var(--vi-red);">
        ⚡ Gemini 3.8 Flash correlating RAN, IP Transport, and 5G Core telemetry for <span class="mono-code">${escapeHtml(ticket.ticket_id)}</span> against 1,000 historical tickets...
      </div>
    `;
  }

  try {
    const res = await fetch("/api/ai/triage", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        ticket_id: ticket.ticket_id,
        force_live: Boolean(forceLive),
      }),
    });
    const data = await res.json();
    renderTab2CopilotOutput(ticket, data.live_insight, data.model_used, data.latency_ms);
  } catch (err) {
    renderTab2CopilotOutput(ticket, null, "gemini-3.8-flash (Grounded)", 150);
  }
}

function renderTab2CopilotOutput(ticket, liveInsight, modelUsed, latencyMs) {
  const out = document.getElementById("t2-copilot-output");
  if (!out || !ticket || !ticket.triage) return;

  const tr = ticket.triage;
  const imp = tr.operational_impact;
  const corr = tr.cross_domain_correlation;
  const rca = tr.hypothesized_root_cause;
  const hist = tr.historical_knowledge_match;

  const metricsHtml = (imp.metrics || [])
    .map(
      (m) => `
      <div class="response-kpi-item">
        <div class="rk-lbl">${escapeHtml(m.label)}</div>
        <div class="rk-val">${escapeHtml(m.value)}</div>
        <div class="rk-sub">${escapeHtml(m.sub)}</div>
      </div>
    `
    )
    .join("");

  out.innerHTML = `
    <div style="display:flex;align-items:center;justify-content:space-between;gap:10px;margin-bottom:14px;flex-wrap:wrap;">
      <span class="badge badge-resolved">✓ AI Triage Confidence: ${escapeHtml(tr.confidence_score)} • ${escapeHtml(tr.matched_cluster)}</span>
      <span class="gemini-model-tag">${escapeHtml(modelUsed)} • ${latencyMs} ms</span>
    </div>

    ${
      liveInsight
        ? `
      <div style="margin-bottom:14px;padding:13px 16px;border-radius:12px;background:var(--vi-yellow-soft);color:#1e1f2e;border-left:5px solid var(--vi-red);font-size:13px;">
        <strong>✨ Live Gemini 3.8 Flash Deep Protocol Synthesis:</strong><br/>
        ${formatRichMarkdownInline(liveInsight)}
      </div>
    `
        : ""
    }

    <!-- 1. Operational Impact Assessment -->
    <div class="response-box" style="margin-bottom:12px;">
      <h5>1. Operational Impact Assessment — ${escapeHtml(imp.headline)}</h5>
      <div class="response-kpi-strip" style="margin-top:8px;margin-bottom:10px;">
        ${metricsHtml}
      </div>
      <p>${formatRichMarkdownInline(imp.narrative)}</p>
    </div>

    <!-- 2. Cross-Domain Correlation Engine -->
    <div class="response-box" style="margin-bottom:12px;">
      <h5>2. Cross-Domain Correlation Engine — ${escapeHtml(corr.headline)}</h5>
      <p>${formatRichMarkdownInline(corr.narrative)}</p>
    </div>

    <!-- 3. Hypothesized Root Cause -->
    <div class="response-box" style="margin-bottom:12px;">
      <h5>3. Hypothesized Root Cause (${escapeHtml(rca.protocol_reference)})</h5>
      <p>${formatRichMarkdownInline(rca.diagnosis)}</p>
    </div>

    <!-- 4. Historical Knowledge Match -->
    <div class="response-box" style="margin-bottom:14px;">
      <h5>4. Historical Knowledge Match (${escapeHtml(hist.similarity_pct)} Vector Similarity)</h5>
      <div style="display:flex;gap:8px;flex-wrap:wrap;margin-bottom:8px;">
        <span class="badge badge-p1 mono-code">Citations: ${escapeHtml(hist.matched_tickets)}</span>
        <span class="badge badge-domain mono-code">Post-Mortem: ${escapeHtml(hist.rfo_id)}</span>
        <span class="badge badge-resolved">Verified Benchmark MTTR: ${escapeHtml(hist.historical_mttr)}</span>
      </div>
      <p>${formatRichMarkdownInline(hist.summary)}</p>
    </div>

    <!-- 5. Next Step Prompt -->
    <div style="display:flex;align-items:center;justify-content:space-between;gap:14px;padding:14px 18px;border-radius:14px;background:var(--bg-promo);border:1.5px solid var(--vi-red);flex-wrap:wrap;">
      <div>
        <div style="font-size:11.5px;font-weight:800;text-transform:uppercase;color:var(--vi-red);">5. Recommended Next Step</div>
        <div style="font-size:13.5px;font-weight:700;color:var(--text-primary);">
          Execute the validated CLI remediation playbook &amp; generate the Executive Post-Mortem RCA Report in Tab 3.
        </div>
      </div>
      <button class="vi-btn-primary" onclick="switchTab(3)">
        Proceed to Tab 3: Guided CLI Remediation &amp; RCA Export →
      </button>
    </div>
  `;
}

/* --------------------------------------------------------------------------
   Tab 3: Guided CLI Remediation Playbook, Simulator & Executive RCA Export
   -------------------------------------------------------------------------- */
function renderTab3RemediationAndRca(ticket) {
  if (!ticket || !ticket.playbook) return;
  const pb = ticket.playbook;

  const subEl = document.getElementById("t3-playbook-subtitle");
  if (subEl) {
    subEl.textContent = `${pb.title} • Est. Recovery: ${pb.estimated_recovery_time} • Risk: ${pb.risk_level}`;
  }

  const stepsContainer = document.getElementById("t3-playbook-steps");
  if (stepsContainer) {
    stepsContainer.innerHTML = (pb.steps || [])
      .map(
        (s, idx) => `
        <div class="playbook-step-card">
          <div style="display:flex;align-items:center;justify-content:space-between;gap:8px;flex-wrap:wrap;">
            <span style="font-weight:800;font-size:13.5px;color:var(--text-primary);">
              Step ${s.step}: ${escapeHtml(s.title)}
            </span>
            <span class="badge badge-domain mono-code">${escapeHtml(s.target_node)}</span>
          </div>
          <div style="font-size:12.5px;color:var(--text-secondary);margin-top:4px;">
            ${escapeHtml(s.description)}
          </div>
          <div class="cli-command-box">
            <code id="cli-cmd-${idx}">${escapeHtml(s.command)}</code>
            <button class="copy-cli-btn" onclick="copySingleCli(${idx}, this)">Copy CLI</button>
          </div>
        </div>
      `
      )
      .join("");
  }

  // Reset terminal simulator to ready state
  const badgesEl = document.getElementById("t3-verification-badges");
  if (badgesEl) badgesEl.innerHTML = "";

  const termEl = document.getElementById("t3-terminal-output");
  if (termEl) {
    termEl.innerHTML = `
      <div class="term-line" style="color:#8b949e;"># Vi SuperNOC Automated Remediation Sandbox — Target Ticket: ${escapeHtml(ticket.ticket_id)} (${escapeHtml(ticket.affected_nodes)})</div>
      <div class="term-line" style="color:#8b949e;"># Click "▶ Simulate Pre-Check & Validation" above to execute the ${pb.steps.length}-step CLI sequence...</div>
    `;
  }

  // Populate Executive RCA Report preview
  const rcaLabel = document.getElementById("rca-ticket-label");
  if (rcaLabel) rcaLabel.textContent = ticket.ticket_id;

  const rcaBox = document.getElementById("t3-rca-markdown-box");
  if (rcaBox) {
    rcaBox.textContent = ticket.rca_markdown || "";
  }
}

function copySingleCli(idx, btnEl) {
  const codeEl = document.getElementById(`cli-cmd-${idx}`);
  if (!codeEl) return;
  navigator.clipboard.writeText(codeEl.textContent);
  if (btnEl) {
    const orig = btnEl.textContent;
    btnEl.textContent = "✓ Copied";
    setTimeout(() => {
      btnEl.textContent = orig;
    }, 1400);
  }
}

function copyAllPlaybookCommands() {
  const ticket = APP_STATE.openTicketsMap[APP_STATE.selectedOpenTicketId];
  if (!ticket || !ticket.playbook) return;
  const allCmds = ticket.playbook.steps.map((s) => `# Step ${s.step}: ${s.title}\n${s.command}`).join("\n\n");
  navigator.clipboard.writeText(allCmds);
}

function runTerminalSimulation() {
  const ticket = APP_STATE.openTicketsMap[APP_STATE.selectedOpenTicketId];
  if (!ticket || !ticket.playbook) return;

  const logs = ticket.playbook.simulation_logs || [];
  const badges = ticket.playbook.verification_badges || [];
  const termEl = document.getElementById("t3-terminal-output");
  const badgesEl = document.getElementById("t3-verification-badges");
  const btn = document.getElementById("btn-simulate-cli");
  if (!termEl || !badgesEl) return;

  if (APP_STATE.simTimer) {
    clearInterval(APP_STATE.simTimer);
    APP_STATE.simTimer = null;
  }

  termEl.innerHTML = `<div class="term-line" style="color:#58a6ff;">[Vi-SuperNOC-SSH] Connecting to ${escapeHtml(ticket.affected_nodes)}... Connected.</div>`;
  badgesEl.innerHTML = "";
  if (btn) {
    btn.disabled = true;
    btn.textContent = "⏳ Executing Pre-Check & Validation...";
  }

  let i = 0;
  APP_STATE.simTimer = setInterval(() => {
    if (i < logs.length) {
      const entry = logs[i];
      const div = document.createElement("div");
      div.className = `term-line ${entry.type || ""}`;
      div.textContent = `[${entry.time}] ${entry.text}`;
      termEl.appendChild(div);
      termEl.scrollTop = termEl.scrollHeight;
      i++;
    } else {
      clearInterval(APP_STATE.simTimer);
      APP_STATE.simTimer = null;
      badgesEl.innerHTML = badges
        .map((b) => `<span class="badge badge-resolved" style="font-size:12.5px;padding:6px 13px;">${escapeHtml(b)}</span>`)
        .join("");
      if (btn) {
        btn.disabled = false;
        btn.textContent = "✓ Validation Passed — Re-Run Simulation";
      }
    }
  }, 180);
}

function generateExecutiveRcaReport() {
  const ticket = APP_STATE.openTicketsMap[APP_STATE.selectedOpenTicketId];
  if (!ticket) return;

  const rcaBox = document.getElementById("t3-rca-markdown-box");
  const statusEl = document.getElementById("rca-report-status");
  if (!rcaBox) return;

  rcaBox.textContent = ticket.rca_markdown;
  if (statusEl) {
    statusEl.innerHTML = `✓ Generated Executive RCA Post-Mortem for <span class="mono-code">${escapeHtml(ticket.ticket_id)}</span> (${escapeHtml(ticket.triage.historical_knowledge_match.rfo_id)})`;
  }
}

function copyRcaMarkdown() {
  const rcaBox = document.getElementById("t3-rca-markdown-box");
  const btn = document.getElementById("btn-copy-rca");
  if (!rcaBox) return;
  navigator.clipboard.writeText(rcaBox.textContent);
  if (btn) {
    const orig = btn.textContent;
    btn.textContent = "✓ Copied Markdown!";
    setTimeout(() => {
      btn.textContent = orig;
    }, 1500);
  }
}

function downloadRcaMarkdown() {
  const ticket = APP_STATE.openTicketsMap[APP_STATE.selectedOpenTicketId];
  const rcaBox = document.getElementById("t3-rca-markdown-box");
  if (!ticket || !rcaBox) return;

  const blob = new Blob([rcaBox.textContent], { type: "text/markdown;charset=utf-8" });
  const url = URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url;
  a.download = `Vi_SuperNOC_RCA_${ticket.ticket_id}.md`;
  document.body.appendChild(a);
  a.click();
  document.body.removeChild(a);
  URL.revokeObjectURL(url);
}

/* --------------------------------------------------------------------------
   Demo Script Walkthrough Modal
   -------------------------------------------------------------------------- */
function toggleScriptModal(open) {
  const backdrop = document.getElementById("vi-modal-backdrop");
  const titleEl = document.getElementById("modal-title");
  const bodyEl = document.getElementById("modal-body-content");
  if (!backdrop || !titleEl || !bodyEl) return;

  if (!open) {
    backdrop.classList.remove("open");
    return;
  }

  titleEl.innerHTML = `🎯 Vi (Vodafone Idea) NOC RCA &amp; Trouble Ticket Demo — Presenter Walkthrough`;
  bodyEl.innerHTML = `
    <div style="display:flex;flex-direction:column;gap:14px;">
      <div style="padding:14px;border-radius:12px;background:var(--bg-promo);border-left:4px solid var(--vi-red);">
        <strong>1. Tab 1 — Institutional Knowledge Base &amp; Ticket Clusters (1,000 Resolved Tickets)</strong>
        <ul style="margin-top:6px;padding-left:18px;">
          <li>Highlight the 5 KPI cards: <strong>1,000 Resolved</strong>, <strong>100 Open Incidents</strong>, <strong>450 RAN | 300 Transport | 250 Core</strong>, <strong>6 Systemic Clusters</strong>, and <strong>42% MTTR Improvement</strong>.</li>
          <li>Click <strong>"Analyze 1,000 Historical Tickets with Gemini"</strong> to show unsupervised discovery of the 6 failure clusters—especially <strong>Cluster 1 (46 Golden Correlation tickets: INC-Telco-78500 to INC-Telco-78545, RFO-Telco-2026-0811)</strong> where Transport <code>VLAN 402 MTU=1420B</code> truncated N4 PFCP packets and caused Pune VoNR call drops.</li>
          <li>Use the <strong>"Ask Gemini"</strong> console to select any of the 5 executive questions (or ask a custom question via live Vertex AI <code>gemini-3.8-flash</code>).</li>
          <li>Filter the 1,000-ticket table by Domain, Severity, Circle, or click <strong>"Highlight Golden Correlation"</strong>.</li>
        </ul>
      </div>

      <div style="padding:14px;border-radius:12px;background:var(--bg-surface-alt);border-left:4px solid var(--vi-yellow);">
        <strong>2. Tab 2 — Live Incident Triage &amp; Cross-Domain RCA (100 Open Active Tickets)</strong>
        <ul style="margin-top:6px;padding-left:18px;">
          <li>Starts on Featured Anchor #1: <code>INC-Telco-OPEN-001 (P1-Critical | 5G Core | VoNR Drops)</code> on <code>UPF-MH-PUN-EDGE-01</code> &amp; <code>SMF-MH-PUN-02</code>.</li>
          <li>Click <strong>"Run AI Cross-Domain Triage &amp; RCA"</strong> to demonstrate how Gemini correlates the 5G Core N4 timeouts to Transport <code>VLAN 402 (MTU 1420B)</code> and 22 Pune RAN cell alarms with <strong>98.4% similarity</strong> to <code>RFO-Telco-2026-0811</code>.</li>
          <li>Switch between Showcase Anchors <code>INC-Telco-OPEN-002</code> (Mumbai Transport Fiber Attenuation) and <code>INC-Telco-OPEN-003</code> (Delhi-NCR RAN Massive MIMO Sleep Lockup) or any of the 100 open tickets.</li>
        </ul>
      </div>

      <div style="padding:14px;border-radius:12px;background:var(--bg-surface-alt);border-left:4px solid var(--status-resolved);">
        <strong>3. Tab 3 — Guided CLI Remediation &amp; One-Click Executive RCA Report</strong>
        <ul style="margin-top:6px;padding-left:18px;">
          <li>Notice the ticket selector is 100% synchronized with Tab 2.</li>
          <li>Inspect the copy-pasteable CLI commands (<code>show interface vlan402 | include MTU</code>, <code>mtu 1500; commit</code>, <code>smf-cli --action reset-pfcp-peer</code>).</li>
          <li>Click <strong>"▶ Simulate Pre-Check &amp; Validation"</strong> to watch the terminal verify <code>✓ MTU Verified: 1500</code>, <code>✓ PFCP Heartbeat: OK</code>, and <code>✓ Call Drop Rate: Restored &lt;0.02%</code>.</li>
          <li>Click <strong>"Generate Executive RCA Report"</strong> and export via <strong>Copy to Clipboard</strong> or <strong>Download Markdown (.md)</strong>.</li>
        </ul>
      </div>
    </div>
  `;
  backdrop.classList.add("open");
}

function closeModal() {
  const backdrop = document.getElementById("vi-modal-backdrop");
  if (backdrop) backdrop.classList.remove("open");
}

function toggleSideWalkthrough(open) {
  const drawer = document.getElementById("vi-side-drawer");
  const backdrop = document.getElementById("vi-side-drawer-backdrop");
  if (!drawer || !backdrop) return;
  drawer.classList.toggle("open", Boolean(open));
  backdrop.classList.toggle("open", Boolean(open));
}

function quickJumpDemoStep(step) {
  toggleSideWalkthrough(false);
  if (step === "tab1_clusters") {
    switchTab(1);
    runClusterDiscoveryAnimation();
  } else if (step === "tab1_golden") {
    switchTab(1);
    if (!APP_STATE.filters.goldenOnly) {
      toggleGoldenFilter();
    }
    const tbl = document.getElementById("historical-tickets-table");
    if (tbl) tbl.scrollIntoView({ behavior: "smooth" });
  } else if (step === "tab2_open001") {
    selectOpenTicket("INC-Telco-OPEN-001");
    switchTab(2);
    runCopilotTriage(false);
  } else if (step === "tab2_open002") {
    selectOpenTicket("INC-Telco-OPEN-002");
    switchTab(2);
    runCopilotTriage(false);
  } else if (step === "tab2_open003") {
    selectOpenTicket("INC-Telco-OPEN-003");
    switchTab(2);
    runCopilotTriage(false);
  } else if (step === "tab3_sim") {
    switchTab(3);
    runTerminalSimulation();
    generateExecutiveRcaReport();
  }
}

window.addEventListener("DOMContentLoaded", initApp);
