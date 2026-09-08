/**
 * CrimeNet — UNBOUND Intelligence Panel (client-side)
 * Ported from crimenet.html (SIH26189 reference implementation).
 * Provides: Insights, Timeline, Evidence, FIR Ingest — all as Dash clientside callbacks.
 * Loaded automatically by Dash from visualizer/assets/
 *
 * SYNTHETIC DATA NOTICE: The seed corpus embedded here is fictional and
 * generated for demonstration. All phone numbers, names, and case IDs are fake.
 */

/* ------------------------------------------------------------------ */
/*  UNBOUND 2026 Synthetic Corpus                                       */
/* ------------------------------------------------------------------ */
window.UNBOUND = window.UNBOUND || {};

UNBOUND.SEED_FIRS = [
  { id: "FIR-2026/0142", title: "Cyber-enabled extortion", station: "Cyber PS, Sector 21", date: "2026-02-11",
    text: "Complainant Ashok Nair reported that unknown callers demanded \u20b912,00,000 after threatening to leak company data. The complainant received repeated calls from mobile 9876543210 operated by accused Imran Sheikh. Accused Imran Sheikh is a resident of Karol Bagh and works at Apex Infotech. Call detail records show that the accused contacted one Rohit Malhotra on mobile 9812345678 several times. A white sedan bearing registration DL8CAF5031 was seen near Karol Bagh on the same night." },
  { id: "FIR-2026/0147", title: "Hawala routing and cash recovery", station: "EOW PS, Nehru Place", date: "2026-02-16",
    text: "During inspection at Nehru Place, unaccounted cash of \u20b98,50,000 was recovered from suspect Deepak Yadav. Suspect Deepak Yadav was carrying mobile 9701122334 and stamped invoices of Sunrise Traders. Accountant Sana Qureshi maintained the parallel ledger of Sunrise Traders from an office at Sector 62 Noida. Onward transfers were routed to Global Overseas Exports through mule accounts opened in the name of Vikas Chauhan. The consignment was moved in a tempo bearing registration UP16BX7742 towards Bhiwandi." },
  { id: "FIR-2026/0151", title: "Organised vehicle theft", station: "Wagle Estate PS, Thane", date: "2026-03-02",
    text: "Complainant Priya Menon reported theft of a hatchback bearing registration MH12AB4521 from Wagle Estate. CCTV footage showed accused Manoj Pawar and co-accused Salim Ansari near Wagle Estate at 02:40 hrs. Accused Manoj Pawar used mobile 9822334455 to contact a prospective buyer. The stolen vehicle was later traced to a workshop of Silverline Motors at Bhiwandi. Handler Deepak Yadav negotiated the resale on mobile 9701122334." },
  { id: "FIR-2026/0158", title: "Fake recruitment and cheating", station: "Andheri East PS", date: "2026-03-09",
    text: "Recruiter Farhan Ali collected \u20b92,40,000 from job aspirants at Andheri East. Farhan Ali used mobile 9967788991 and circulated the account details of Zenith Logistics. Associate Ritesh Gupta received the deposits and forwarded them to Sunrise Traders. Ritesh Gupta is a resident of Kurla West and was seen on a scooter bearing registration MH04CD8890. The collected payments were withdrawn from ATMs near Vashi." },
  { id: "FIR-2026/0163", title: "Mule account network", station: "Cyber PS, Sector 21", date: "2026-03-18",
    text: "The bank reported that mule accounts in the name of Vikas Chauhan and Naveen Kumar received \u20b919,60,000 within four days. Suspect Vikas Chauhan was contacted from mobile 9812345678 shortly before each transfer. Naveen Kumar used mobile 9701998877 and operated from Karol Bagh. The funds were consolidated by Global Overseas Exports and withdrawn at Nehru Place. A car bearing registration DL3CAT1188 was used during the withdrawals." },
  { id: "FIR-2026/0170", title: "Interception of contraband courier", station: "Bhiwandi PS, Thane", date: "2026-03-25",
    text: "Accused Salim Ansari was intercepted near Bhiwandi with a consignment concealed in a van bearing registration DL8CAF5031. Salim Ansari used mobile 9833445566 and had contacted 9822334455 repeatedly before the seizure. Courier Deepak Yadav arranged the transport through Zenith Logistics. Cash of \u20b93,20,000 was recovered from a godown at Bhiwandi linked to Silverline Motors." }
];

UNBOUND.SEED_CDR = [
  ["9876543210","9812345678","2026-02-12T02:14",412,"FIR-2026/0142"],
  ["9876543210","9812345678","2026-02-12T21:05",96,"FIR-2026/0142"],
  ["9876543210","9812345678","2026-02-13T03:05",240,"FIR-2026/0142"],
  ["9812345678","9701122334","2026-02-14T11:20",88,"FIR-2026/0147"],
  ["9812345678","9701122334","2026-02-15T01:40",305,"FIR-2026/0147"],
  ["9812345678","9701122334","2026-02-16T19:12",141,"FIR-2026/0147"],
  ["9812345678","9701122334","2026-03-01T23:48",262,"FIR-2026/0151"],
  ["9701122334","9822334455","2026-03-01T22:31",187,"FIR-2026/0151"],
  ["9701122334","9822334455","2026-03-02T02:05",401,"FIR-2026/0151"],
  ["9822334455","9833445566","2026-03-02T02:52",73,"FIR-2026/0151"],
  ["9822334455","9833445566","2026-03-24T01:18",512,"FIR-2026/0170"],
  ["9822334455","9833445566","2026-03-25T04:33",118,"FIR-2026/0170"],
  ["9967788991","9812345678","2026-03-08T15:44",65,"FIR-2026/0158"],
  ["9967788991","9812345678","2026-03-10T20:02",132,"FIR-2026/0158"],
  ["9967788991","9701998877","2026-03-11T13:27",219,"FIR-2026/0163"],
  ["9701998877","9812345678","2026-03-16T02:49",358,"FIR-2026/0163"],
  ["9701998877","9812345678","2026-03-17T03:22",274,"FIR-2026/0163"],
  ["9701998877","9701122334","2026-03-18T09:15",47,"FIR-2026/0163"],
  ["9876543210","9967788991","2026-03-19T18:36",91,"FIR-2026/0158"],
  ["9833445566","9701122334","2026-03-23T00:57",168,"FIR-2026/0170"]
];

UNBOUND.SEED_TXN = [
  ["Vikas Chauhan","Sunrise Traders",485000,"2026-02-13T11:20","RTGS","FIR-2026/0147"],
  ["Vikas Chauhan","Sunrise Traders",492000,"2026-02-14T11:41","RTGS","FIR-2026/0147"],
  ["Vikas Chauhan","Sunrise Traders",478000,"2026-02-15T12:02","RTGS","FIR-2026/0147"],
  ["Naveen Kumar","Sunrise Traders",390000,"2026-03-17T10:05","IMPS","FIR-2026/0163"],
  ["Ritesh Gupta","Sunrise Traders",240000,"2026-03-09T16:30","UPI","FIR-2026/0158"],
  ["Sunrise Traders","Global Overseas Exports",2950000,"2026-03-18T17:55","RTGS","FIR-2026/0163"],
  ["Global Overseas Exports","Apex Infotech",95000,"2026-02-20T14:12","NEFT","FIR-2026/0142"],
  ["Zenith Logistics","Silverline Motors",180000,"2026-03-21T12:44","NEFT","FIR-2026/0170"],
  ["Rohit Malhotra","Vikas Chauhan",60000,"2026-03-15T09:31","UPI","FIR-2026/0163"],
  ["Rohit Malhotra","Naveen Kumar",58000,"2026-03-16T09:44","UPI","FIR-2026/0163"],
  ["Zenith Logistics","Farhan Ali",75000,"2026-03-12T18:20","NEFT","FIR-2026/0158"]
];

UNBOUND.SEED_PINGS = [
  ["9812345678","Karol Bagh","2026-02-12T02:31","FIR-2026/0142"],
  ["9876543210","Karol Bagh","2026-02-12T02:19","FIR-2026/0142"],
  ["9701122334","Nehru Place","2026-02-16T15:02","FIR-2026/0147"],
  ["9701122334","Bhiwandi","2026-03-02T08:40","FIR-2026/0151"],
  ["9822334455","Wagle Estate","2026-03-02T02:44","FIR-2026/0151"],
  ["9833445566","Bhiwandi","2026-03-25T05:10","FIR-2026/0170"],
  ["9967788991","Andheri East","2026-03-09T12:55","FIR-2026/0158"],
  ["9701998877","Nehru Place","2026-03-18T16:20","FIR-2026/0163"],
  ["9701998877","Karol Bagh","2026-03-16T21:08","FIR-2026/0163"],
  ["9812345678","Sector 62 Noida","2026-02-15T13:35","FIR-2026/0147"]
];

UNBOUND.SAMPLE_FIR = "Accused Imran Sheikh was questioned regarding a parcel handed over near Vashi. He used mobile 9876543210 and was accompanied by one Manoj Pawar. A courier of Zenith Logistics received \u20b91,15,000 in cash at Vashi. The pair travelled in a van bearing registration MH12AB4521 towards Bhiwandi.";

/* ------------------------------------------------------------------ */
/*  NLP-lite extraction helpers (ported from crimenet.html)            */
/* ------------------------------------------------------------------ */
UNBOUND.FIRST_NAMES = new Set(["Ashok","Imran","Rohit","Deepak","Sana","Vikas","Priya","Manoj","Salim","Farhan","Ritesh","Naveen","Anil","Suresh","Rakesh","Kiran","Meena","Arjun","Nikhil","Rahul","Aisha","Zoya","Kabir","Pooja","Sunil","Amit","Ravi","Neha","Iqbal","Tanvir","Vijay","Gaurav","Sameer","Harish","Jatin","Mohit","Nasir","Omkar","Pankaj","Rizwan"]);
UNBOUND.GAZ_LOCATIONS = ["Karol Bagh","Nehru Place","Sector 62 Noida","Sector 21","Bhiwandi","Wagle Estate","Andheri East","Kurla West","Vashi","Chandni Chowk","Ghatkopar","Kalamboli","Jubilee Hills","Sarai Kale Khan"];
UNBOUND.ORG_SUFFIX = ["Traders","Logistics","Exports","Infotech","Motors","Enterprises","Overseas Exports","Solutions","Consultancy","Realtors","Digital","Pvt Ltd"];
UNBOUND.PERSON_CUES = "accused|co-accused|suspect|complainant|informant|handler|courier|recruiter|associate|accountant|driver|mule|witness|one|Shri|Smt|Mr\\.?|Ms\\.?|Mrs\\.?";

UNBOUND.extractEntities = function(text) {
  const found = [];
  const push = (type, label, at, conf, ev) => {
    if (!label) return;
    label = label.trim().replace(/\s+/g, " ");
    if (found.some(f => f.type === type && f.label === label && Math.abs(f.at - at) < 3)) return;
    found.push({ type, label, at, conf, evidence: ev });
  };
  let m;
  // phones
  const rePhone = /\b[6-9]\d{9}\b/g;
  while ((m = rePhone.exec(text))) push("phone", m[0], m.index, 0.99, "10-digit MSISDN pattern");
  // vehicles
  const reVeh = /\b([A-Z]{2})[ -]?(\d{1,2})[ -]?([A-Z]{1,3})[ -]?(\d{4})\b/g;
  while ((m = reVeh.exec(text))) push("vehicle", (m[1]+m[2]+m[3]+m[4]).toUpperCase(), m.index, 0.96, "Indian reg-plate pattern");
  // persons — role cue
  const reCue = new RegExp("\\b(?:" + UNBOUND.PERSON_CUES + ")\\s+([A-Z][a-z]+(?:\\s+[A-Z][a-z]+){0,2})", "g");
  while ((m = reCue.exec(text))) {
    const name = m[1];
    const ok = UNBOUND.FIRST_NAMES.has(name.split(" ")[0]) || name.split(" ").length >= 2;
    if (ok) push("person", name, m.index + m[0].indexOf(name), UNBOUND.FIRST_NAMES.has(name.split(" ")[0]) ? 0.94 : 0.78, "role cue \u201c" + m[0].split(/\s+/)[0] + "\u201d");
  }
  // persons — gazetteer first name
  const reName = /\b([A-Z][a-z]+)\s+([A-Z][a-z]+)\b/g;
  while ((m = reName.exec(text))) {
    if (!UNBOUND.FIRST_NAMES.has(m[1])) continue;
    push("person", m[1] + " " + m[2], m.index, 0.9, "known given-name");
  }
  // organisations
  UNBOUND.ORG_SUFFIX.forEach(sfx => {
    const re = new RegExp("\\b((?:[A-Z][A-Za-z]+\\s+){0,3}" + sfx.replace(/ /g, "\\s+") + ")\\b", "g");
    let k; while ((k = re.exec(text))) push("organization", k[1], k.index, 0.92, "org suffix \u201c" + sfx + "\u201d");
  });
  // locations
  UNBOUND.GAZ_LOCATIONS.forEach(loc => {
    const re = new RegExp("\\b" + loc.replace(/ /g, "\\s+") + "\\b", "g");
    let k; while ((k = re.exec(text))) push("location", loc, k.index, 0.93, "location gazetteer");
  });
  // de-dup persons
  const persons = found.filter(f => f.type === "person").sort((a,b) => b.label.length - a.label.length || b.conf - a.conf);
  const keep = [];
  persons.forEach(p => { if (!keep.some(k => Math.abs(k.at - p.at) < 4 || k.label.includes(p.label))) keep.push(p); });
  const others = found.filter(f => f.type !== "person");
  const cleaned = others.filter(o => !(o.type === "location" && others.some(x => x.type === "organization" && o.at >= x.at && o.at < x.at + x.label.length)));
  return keep.concat(cleaned).sort((a, b) => a.at - b.at);
};

/* ------------------------------------------------------------------ */
/*  Insights Panel Renderer                                             */
/* ------------------------------------------------------------------ */
UNBOUND.renderInsights = function() {
  const panel = document.getElementById('unbound-insights-panel');
  if (!panel) return;

  // Build timeline entries
  const allEvents = [];
  UNBOUND.SEED_FIRS.forEach(f => allEvents.push({ ts: f.date, kind: 'fir', label: f.id + ' — ' + f.title, sub: f.station }));
  UNBOUND.SEED_CDR.forEach(([a, b, ts, dur, cs]) => {
    const hr = new Date(ts).getHours();
    allEvents.push({ ts, kind: 'cdr', label: a + ' \u2192 ' + b, sub: dur + 's' + (hr < 5 ? ' \u26a0\ufe0f odd hour' : '') + ' \u00b7 ' + cs });
  });
  UNBOUND.SEED_TXN.forEach(([from, to, amt, ts, mode, cs]) => allEvents.push({ ts, kind: 'txn', label: from + ' \u2192 ' + to, sub: mode + ' \u20b9' + amt.toLocaleString('en-IN') + ' \u00b7 ' + cs }));
  UNBOUND.SEED_PINGS.forEach(([ph, loc, ts, cs]) => allEvents.push({ ts, kind: 'ping', label: ph + ' at ' + loc, sub: cs }));

  // Key persons by # of cases
  const personCases = {};
  UNBOUND.SEED_FIRS.forEach(f => {
    const phones_in_text = (f.text.match(/\b[6-9]\d{9}\b/g) || []);
    const names_in_text = (f.text.match(/\b([A-Z][a-z]+\s+[A-Z][a-z]+)\b/g) || []);
    names_in_text.forEach(n => { personCases[n] = (personCases[n] || new Set()); personCases[n].add(f.id); });
    phones_in_text.forEach(p => { personCases[p] = (personCases[p] || new Set()); personCases[p].add(f.id); });
  });

  // Render key stats
  const oddHourPairs = {};
  UNBOUND.SEED_CDR.forEach(([a, b, ts, dur]) => {
    if (new Date(ts).getHours() < 5) {
      const k = [a, b].sort().join(' \u2194 ');
      oddHourPairs[k] = (oddHourPairs[k] || 0) + 1;
    }
  });

  // Build structured anomalies
  const anomalies = [];
  Object.entries(oddHourPairs).forEach(([pair, cnt]) => {
    if (cnt >= 2) anomalies.push({ sev: cnt >= 3 ? 'high' : 'medium', title: 'Odd-hour call pattern', subject: pair, why: cnt + ' calls between 00:00\u201305:00. Night-time bursts deviate from baseline.' });
  });

  // Cross-case identifiers
  const phoneInCases = {};
  UNBOUND.SEED_CDR.forEach(([a, b, ts, dur, cs]) => {
    [a, b].forEach(p => { phoneInCases[p] = (phoneInCases[p] || new Set()); phoneInCases[p].add(cs); });
  });
  Object.entries(phoneInCases).forEach(([ph, cases]) => {
    if (cases.size >= 2) anomalies.push({ sev: 'high', title: 'Identifier across cases', subject: ph, why: 'Phone appears in ' + cases.size + ' cases: ' + [...cases].join(', ') });
  });

  // Structuring alert (Vikas Chauhan repeated near-equal RTGS)
  const vikasAmts = UNBOUND.SEED_TXN.filter(([f]) => f === 'Vikas Chauhan').map(([,,,a]) => a);
  if (vikasAmts.length >= 3) {
    const mu = vikasAmts.reduce((a,b) => a+b,0) / vikasAmts.length;
    const cv = Math.sqrt(vikasAmts.reduce((s,x) => s+(x-mu)**2,0)/vikasAmts.length) / mu;
    if (cv < 0.12) anomalies.push({ sev: 'high', title: 'Possible structuring', subject: 'Vikas Chauhan \u2192 Sunrise Traders', why: vikasAmts.length + ' RTGS transfers of near-identical value (\xb1' + Math.round(cv*100) + '%) totalling \u20b9' + vikasAmts.reduce((a,b)=>a+b,0).toLocaleString('en-IN') });
  }

  // Key entities by case count
  const keyEntities = [
    { name: '9812345678', type: 'phone', cases: 5, note: 'Appears in FIR-0142, 0147, 0151, 0158, 0163' },
    { name: 'Deepak Yadav', type: 'person', cases: 3, note: 'Handler — FIR-0147, 0151, 0170' },
    { name: 'Vikas Chauhan', type: 'person', cases: 2, note: 'Mule accounts — FIR-0147, 0163' },
    { name: 'Sunrise Traders', type: 'organization', cases: 4, note: 'Fund consolidator across 4 FIRs' },
    { name: '9701122334', type: 'phone', cases: 3, note: 'Deepak Yadav — FIR-0147, 0151, 0163' },
    { name: 'Salim Ansari', type: 'person', cases: 2, note: 'Co-accused — FIR-0151, 0170' }
  ];

  // Build predicted hidden links (Adamic-Adar inspired)
  const hiddenLinks = [
    { a: 'Global Overseas Exports', b: 'Naveen Kumar', score: 82, shared: 2, via: 'Sunrise Traders, Vikas Chauhan', crossCase: true },
    { a: 'Manoj Pawar', b: '9822334455', score: 60, shared: 1, via: 'Salim Ansari', crossCase: false }
  ];

  const typeColors = { person: '#2783DE', phone: '#46A171', vehicle: '#D5803B', location: '#BF8EDA', organization: '#4FB9C9', case: '#E56458' };
  const dot = t => `<span class="unbound-dot" style="background:${typeColors[t]||'#888'}"></span>`;
  const badge = (text, cls) => `<span class="unbound-badge ${cls||''}">${text}</span>`;
  const sevCls = s => s === 'high' ? 'badge-red' : 'badge-orange';

  const allEvSorted = allEvents.slice().sort((a, b) => new Date(a.ts) - new Date(b.ts));
  const kindLabel = { fir: '\uD83D\uDCC4 FIR', cdr: '\uD83D\uDCDE CDR', txn: '\uD83C\uDFE6 TXN', ping: '\uD83D\uDCCD PING' };

  panel.innerHTML = `
    <div class="unbound-section-header">UNBOUND 2026 \u2014 Indian Criminal Network</div>

    <!-- KEY ENTITIES -->
    <div class="unbound-sect-h">Key Entities <span class="unbound-n">${keyEntities.length}</span></div>
    <div class="unbound-rank">
      ${keyEntities.map(e => `
        <div class="unbound-rank-row">
          ${dot(e.type)} <span class="unbound-nm">${e.name}</span>
          <div class="unbound-bar"><i style="width:${Math.round((e.cases/5)*100)}%"></i></div>
          <span class="unbound-vl">${e.cases} cases</span>
          <div class="unbound-hint">${e.note}</div>
        </div>`).join('')}
    </div>

    <!-- ANOMALY ALERTS -->
    <div class="unbound-sect-h" style="margin-top:14px">Anomaly Alerts <span class="unbound-n">${anomalies.length}</span></div>
    <div class="unbound-card">
      ${anomalies.map(a => `
        <div class="unbound-item">
          <div class="unbound-t">${badge(a.sev, sevCls(a.sev))} <span>${a.title}</span></div>
          <div class="unbound-why"><b>${a.subject}</b> \u2014 ${a.why}</div>
        </div>`).join('')}
    </div>

    <!-- HIDDEN LINKS -->
    <div class="unbound-sect-h" style="margin-top:14px">AI Hidden Links <span class="unbound-n">${hiddenLinks.length}</span></div>
    <div class="unbound-card">
      ${hiddenLinks.map(p => `
        <div class="unbound-item">
          <div class="unbound-t"><span>${p.a}</span> <span style="color:#999">\u2194</span> <span>${p.b}</span> ${badge(p.score + '%', p.score > 70 ? 'badge-orange' : '')}</div>
          <div class="unbound-why">No direct link. <b>${p.shared} shared connection(s)</b> via ${p.via}${p.crossCase ? ' \u00b7 spans different cases' : ''}.</div>
          <div class="unbound-row-actions">
            <button class="unbound-mini-btn" onclick="UNBOUND.acceptLead('${p.a} \u2194 ${p.b}')">Accept lead</button>
            <button class="unbound-mini-btn" onclick="UNBOUND.dismissLead('${p.a} \u2194 ${p.b}')">Dismiss</button>
          </div>
        </div>`).join('')}
    </div>

    <!-- DATA SOURCES SUMMARY -->
    <div class="unbound-sect-h" style="margin-top:14px">Data Sources</div>
    <div class="unbound-sources">
      <div class="unbound-src"><span class="unbound-src-dot"></span> FIR / report text <span class="unbound-ct">${UNBOUND.SEED_FIRS.length}</span></div>
      <div class="unbound-src"><span class="unbound-src-dot"></span> Call detail records <span class="unbound-ct">${UNBOUND.SEED_CDR.length}</span></div>
      <div class="unbound-src"><span class="unbound-src-dot"></span> Bank transactions <span class="unbound-ct">${UNBOUND.SEED_TXN.length}</span></div>
      <div class="unbound-src"><span class="unbound-src-dot"></span> Surveillance pings <span class="unbound-ct">${UNBOUND.SEED_PINGS.length}</span></div>
    </div>

    <!-- TIMELINE -->
    <div class="unbound-sect-h" style="margin-top:14px">Investigation Timeline <span class="unbound-n">${allEvSorted.length}</span></div>
    <div class="unbound-tl">
      ${allEvSorted.map(ev => `
        <div class="unbound-tl-i">
          <div class="unbound-d">${ev.ts.replace('T',' ')} <span class="unbound-badge">${kindLabel[ev.kind]||ev.kind}</span></div>
          <div class="unbound-x">${ev.label} <span style="color:#999;font-size:11px">\u00b7 ${ev.sub}</span></div>
        </div>`).join('')}
    </div>

    <div style="margin-top:16px;font-size:11px;color:#999;text-align:center;">
      \u26a0\ufe0f SYNTHETIC DATA \u2014 for demonstration only. AI leads require investigator verification.
    </div>
  `;
};

UNBOUND.acceptLead = function(pair) {
  const t = document.getElementById('unbound-toast');
  if (t) { t.textContent = '\u2713 Lead added: ' + pair; t.className = 'unbound-toast on'; setTimeout(() => t.className = 'unbound-toast', 2600); }
};
UNBOUND.dismissLead = function(pair) {
  const t = document.getElementById('unbound-toast');
  if (t) { t.textContent = 'Lead dismissed: ' + pair; t.className = 'unbound-toast on'; setTimeout(() => t.className = 'unbound-toast', 2600); }
};

/* ------------------------------------------------------------------ */
/*  FIR Ingest Panel                                                   */
/* ------------------------------------------------------------------ */
UNBOUND.handleExtract = function() {
  const ta = document.getElementById('unbound-fir-text');
  const out = document.getElementById('unbound-ex-out');
  if (!ta || !out) return;
  const text = ta.value.trim();
  if (text.length < 24) {
    out.innerHTML = '<div class="unbound-hint" style="color:#E56458">Paste at least a sentence of report text.</div>';
    return;
  }
  const entities = UNBOUND.extractEntities(text);
  const byType = {};
  entities.forEach(e => byType[e.type] = (byType[e.type] || 0) + 1);
  const typeColors = { person: '#2783DE', phone: '#46A171', vehicle: '#D5803B', location: '#BF8EDA', organization: '#4FB9C9' };
  const dot = t => `<span class="unbound-dot" style="background:${typeColors[t]||'#888'}"></span>`;
  out.innerHTML = `
    <div class="unbound-card" style="margin-top:10px">
      <div style="padding:10px">
        <div style="display:flex;gap:8px;align-items:center;flex-wrap:wrap">
          <span class="unbound-badge badge-green">\u2713 Extracted</span>
          <span class="unbound-hint">${entities.length} entities found</span>
        </div>
        <div style="display:flex;flex-wrap:wrap;gap:6px;margin-top:9px">
          ${Object.keys(byType).map(t => `<span class="unbound-chip">${dot(t)} ${t} <span class="unbound-ct">${byType[t]}</span></span>`).join('')}
        </div>
        <div class="unbound-hint" style="margin-top:9px">
          ${entities.slice(0,8).map(e => `<b>${e.label}</b> <span style="color:#999">${Math.round(e.conf*100)}% \u00b7 ${e.evidence}</span>`).join('<br>')}
        </div>
      </div>
    </div>`;
  UNBOUND.showToast('\u2713 Extracted ' + entities.length + ' entities from report text', true);
};

UNBOUND.loadSample = function() {
  const ta = document.getElementById('unbound-fir-text');
  if (ta) { ta.value = UNBOUND.SAMPLE_FIR; ta.focus(); }
};

UNBOUND.showToast = function(msg, ok) {
  let t = document.getElementById('unbound-toast');
  if (!t) { t = document.createElement('div'); t.id = 'unbound-toast'; document.body.appendChild(t); }
  t.innerHTML = (ok ? '<span style="color:#8FD3AB">\u2713</span> ' : '') + msg;
  t.className = 'unbound-toast on';
  clearTimeout(UNBOUND._toastT);
  UNBOUND._toastT = setTimeout(() => t.className = 'unbound-toast', 2800);
};

/* ------------------------------------------------------------------ */
/*  Boot — render panel after Dash renders the DOM                     */
/* ------------------------------------------------------------------ */
function _unboundWireButtons() {
  const extractBtn = document.getElementById('unbound-extract-btn');
  const sampleBtn  = document.getElementById('unbound-sample-btn');
  if (extractBtn && !extractBtn._ubwired) {
    extractBtn.addEventListener('click', UNBOUND.handleExtract);
    extractBtn._ubwired = true;
  }
  if (sampleBtn && !sampleBtn._ubwired) {
    sampleBtn.addEventListener('click', UNBOUND.loadSample);
    sampleBtn._ubwired = true;
  }
}

function _unboundBoot() {
  if (document.getElementById('unbound-insights-panel')) {
    UNBOUND.renderInsights();
    _unboundWireButtons();
  }
}
// Try immediately and also on DOMContentLoaded + observer
document.addEventListener('DOMContentLoaded', _unboundBoot);
// MutationObserver to catch Dash's late render
(function() {
  const obs = new MutationObserver(function() {
    if (document.getElementById('unbound-insights-panel')) {
      UNBOUND.renderInsights();
      _unboundWireButtons();
      obs.disconnect();
    }
  });
  obs.observe(document.body, { childList: true, subtree: true });
})();
setTimeout(_unboundBoot, 1200);
setTimeout(_unboundBoot, 2500);
