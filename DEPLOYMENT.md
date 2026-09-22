# CrimeNet — Complete Deployment Guide

> **WHO THIS IS FOR**: You are helping deploy the CrimeNet project to the internet via Render.com (free tier). A teammate has already prepared all deployment files in a GitHub PR. Your job is to merge that PR and deploy the app on Render.

---

## 1. PROJECT CONTEXT

**CrimeNet** is a Python Dash web application for criminal network analysis and visualization. It is a **single Python process** — no databases, no Java backend, no separate frontend build needed.

### Tech Stack (what actually runs)
- **Python 3.11** (recommended for deployment)
- **Dash 2.18.1** (Plotly's web framework, built on Flask)
- **Cytoscape.js** (graph visualization, served by Dash)
- **NetworkX 3.3** (graph algorithms — community detection, centrality, link prediction)
- **Flask** (WSGI server underneath Dash)
- **Gunicorn** (production WSGI server for deployment)

### How it works
- Entry point: `visualizer/index.py` (local dev) or `visualizer/wsgi.py` (production)
- Everything runs **in-memory** — no database connections needed
- Ships with **14 built-in criminal network datasets** as JSON files in `datasets/preprocessed/`
- Serves on a single port (default 8050 locally, `$PORT` on Render)

---

## 2. WHAT THE PR CONTAINS

A PR from branch `deploy/render-setup` has been created. It adds **4 new files** and modifies **1 file**. Here is exactly what each does:

### NEW: `requirements-deploy.txt`
Clean, modern Python dependencies for cloud deployment. The original `requirements.txt` has ancient pinned versions from 2019 (tensorflow, torch, etc.) that are NOT needed by the visualizer and will fail to install on modern Python. This file contains only what the app actually uses.

### NEW: `Procfile`
```
web: gunicorn --chdir . visualizer.wsgi:server --bind 0.0.0.0:$PORT --timeout 120 --workers 2
```
Tells Render (and any Heroku-compatible PaaS) how to start the app. Uses Gunicorn to serve the Flask server exposed by `wsgi.py`.

### NEW: `render.yaml`
```yaml
services:
  - type: web
    name: crimenet
    runtime: python
    buildCommand: pip install -r requirements-deploy.txt
    startCommand: gunicorn --chdir . visualizer.wsgi:server --bind 0.0.0.0:$PORT --timeout 120 --workers 2
    envVars:
      - key: PYTHON_VERSION
        value: "3.11"
```
Render blueprint for one-click deployment. Optional but makes setup faster.

### NEW: `visualizer/wsgi.py`
WSGI entry point for Gunicorn. It does exactly what `index.py` does (sets up layout, registers callbacks, creates the ActiveNetwork) but instead of calling `run_server()`, it exposes the Flask `server` object for Gunicorn to serve. Logs go to stderr (captured by Render automatically) instead of a file.

### MODIFIED: `visualizer/app.py` (line 38)
```python
# BEFORE (crashes when Gunicorn passes its own CLI arguments):
args = parser.parse_args()

# AFTER (ignores unknown arguments safely):
args, _ = parser.parse_known_args()
```
This is the **critical fix**. Without it, `argparse` throws `SystemExit` when Gunicorn invokes the module because Gunicorn passes its own CLI flags that `argparse` doesn't recognize.

---

## 3. STEP-BY-STEP DEPLOYMENT

### Step 3.1 — Merge the PR

1. Go to the GitHub repository
2. Find the PR from branch `deploy/render-setup`
3. Review the 5 changed files (described above)
4. **Merge the PR** into `main`

If the PR is on a fork, you may need to:
- Go to: `https://github.com/<YOUR-USERNAME>/CrimeNet/compare/main...PG300604:CrimeNet:deploy/render-setup`
- Create a PR from there and merge it

### Step 3.2 — Sign Up on Render

1. Go to **https://render.com**
2. Click **Get Started for Free**
3. **Sign in with GitHub** (use the GitHub account that owns/has access to the CrimeNet repo)
4. Authorize Render to access your repositories

### Step 3.3 — Create a New Web Service

1. From the Render dashboard, click **New +** → **Web Service**
2. Select **Build and deploy from a Git repository** → **Next**
3. Find and select the **CrimeNet** repository
4. If you don't see it, click **Configure account** to grant Render access to the repo

### Step 3.4 — Configure the Service

Fill in these settings **exactly**:

| Setting | Value |
|---------|-------|
| **Name** | `crimenet` (or any name you want — this becomes part of the URL) |
| **Region** | Singapore (closest to India) or any other |
| **Branch** | `main` |
| **Root Directory** | *(leave blank)* |
| **Runtime** | **Python** |
| **Build Command** | `pip install -r requirements-deploy.txt` |
| **Start Command** | `gunicorn --chdir . visualizer.wsgi:server --bind 0.0.0.0:$PORT --timeout 120 --workers 2` |
| **Instance Type** | **Free** |

### Step 3.5 — Set Environment Variables

Scroll down to the **Environment Variables** section and add:

| Key | Value |
|-----|-------|
| `PYTHON_VERSION` | `3.11` |

This is **critical** — without it Render may use Python 3.7 which will fail.

### Step 3.6 — Deploy

1. Click **Create Web Service**
2. Render will:
   - Clone the repo
   - Install dependencies from `requirements-deploy.txt` (~2-3 min)
   - Start Gunicorn with the start command
3. Watch the **Build Logs** for progress
4. When you see `Listening on http://0.0.0.0:XXXXX` or similar, the app is live
5. Render assigns a URL like: `https://crimenet-xxxx.onrender.com`

**Expected build time: 5-8 minutes on free tier.**

---

## 4. POST-DEPLOYMENT VERIFICATION

Once the URL is live, verify these features work:

### Test 1: Page Load
- Open `https://crimenet-xxxx.onrender.com` in a browser
- **Expected**: Dark-themed CrimeNet UI loads with sidebar and empty graph canvas
- If you get a blank page, wait 30-60 seconds (free tier cold start)

### Test 2: Load a Dataset
1. In the right sidebar, go to the **NETWORK** tab
2. Select **"Montreal Street Gangs"** from the dropdown
3. Click **Load Network**
- **Expected**: Graph renders with 35 nodes and edges in the canvas

### Test 3: Community Detection
1. Switch to the **ANALYSIS** tab
2. Select **Community Detection** → **Louvain**
3. Click **Analyze**
- **Expected**: Nodes get colored by community cluster

### Test 4: Social Influence
1. Select **Social Influence Analysis** → **PageRank**
2. Click **Analyze**
- **Expected**: Node sizes change based on PageRank scores

### Test 5: Link Prediction
1. Select **Link Prediction** → **Adamic-Adar**
2. Click **Analyze**
- **Expected**: Predicted edges (dashed lines) appear between nodes

### Test 6: Search
1. Click the **Search** (magnifying glass) button in the toolbar
2. Type a node name
- **Expected**: Matching node(s) highlighted with red border

---

## 5. TROUBLESHOOTING

### Build fails with "No module named X"
- Check that the **Build Command** is `pip install -r requirements-deploy.txt` (NOT `requirements.txt`)
- The old `requirements.txt` has incompatible pinned versions from 2019

### Build fails with "Python version not supported"
- Make sure `PYTHON_VERSION` = `3.11` is set in environment variables
- Do NOT use Python 3.7 or 3.8 (too old) or 3.13 (too new for some deps)

### App crashes on startup with "SystemExit" or argparse error
- Verify `visualizer/app.py` line 38 reads:
  ```python
  args, _ = parser.parse_known_args()
  ```
  NOT `args = parser.parse_args()`
- If the PR wasn't merged properly, this fix may be missing

### App loads but shows blank page
- Free tier cold-starts take 30-60 seconds. Refresh after waiting.
- Check Render logs for Python errors.

### "Service unavailable" after some time
- Free tier **spins down after 15 minutes of inactivity**
- The next visit triggers a cold-start (~30-60 sec)
- **Tip for hackathon demo**: Open the URL 1-2 minutes before presenting
- To keep it always-on: upgrade to Render's Starter plan ($7/month)

### Memory issues (OOM kill)
- Free tier has 512 MB RAM. The app with all 14 datasets loaded uses ~150-200 MB, well within limits.
- If loading very large custom datasets, you may hit the limit.

### Gunicorn timeout errors
- The `--timeout 120` flag gives workers 120 seconds before timeout
- If large graph algorithms take longer, increase to `--timeout 300`
- Edit the Start Command in Render dashboard (no code change needed)

---

## 6. QUICK REFERENCE — ALL COMMANDS

### Local development (unchanged)
```bash
cd CrimeNet
pip install -r requirements-deploy.txt
python visualizer/index.py
# Opens at http://127.0.0.1:8050
```

### Local production test (simulates Render)
```bash
cd CrimeNet
pip install -r requirements-deploy.txt
gunicorn --chdir . visualizer.wsgi:server --bind 0.0.0.0:8050 --timeout 120 --workers 2
# Opens at http://127.0.0.1:8050
```

### Render deployment
```
Build Command:  pip install -r requirements-deploy.txt
Start Command:  gunicorn --chdir . visualizer.wsgi:server --bind 0.0.0.0:$PORT --timeout 120 --workers 2
Env Var:        PYTHON_VERSION=3.11
```

---

## 7. FILE MAP — WHAT MATTERS FOR DEPLOYMENT

```
CrimeNet/
├── requirements-deploy.txt     ← [NEW] Cloud-compatible dependencies
├── Procfile                    ← [NEW] Gunicorn start command
├── render.yaml                 ← [NEW] Render one-click blueprint
│
├── visualizer/
│   ├── wsgi.py                 ← [NEW] Production WSGI entry point
│   ├── app.py                  ← [MODIFIED] argparse fix (line 38)
│   ├── index.py                ← Local dev entry point (unchanged)
│   ├── dash_layout.py          ← UI layout definitions
│   ├── dash_formatter.py       ← UI component formatters
│   ├── dash_style.py           ← Cytoscape stylesheet
│   ├── dash_io.py              ← Dash I/O declarations
│   ├── io_utils.py             ← Graph format converters
│   └── assets/                 ← CSS, JS, icons (served by Dash)
│
├── analyzer/                   ← Graph algorithms (all in-memory)
├── storage/                    ← In-memory graph storage + dataset loader
├── framework/                  ← Interface contracts
└── datasets/preprocessed/      ← 14 JSON benchmark datasets (bundled)
```

---

## 8. BACKUP PLAN — ALTERNATIVE PLATFORMS

If Render doesn't work for any reason:

### Railway.app
1. Go to https://railway.app → Sign in with GitHub
2. **New Project** → **Deploy from GitHub repo** → Select CrimeNet
3. Railway auto-detects the `Procfile`
4. Add env var: `PYTHON_VERSION=3.11`
5. Deploy. Get a URL.
- Free trial: $5 credit (enough for days of usage)

### Hugging Face Spaces
1. Go to https://huggingface.co/spaces → Create new Space
2. Select **Docker** SDK
3. Create a `Dockerfile`:
   ```dockerfile
   FROM python:3.11-slim
   WORKDIR /app
   COPY . .
   RUN pip install -r requirements-deploy.txt
   EXPOSE 7860
   CMD ["gunicorn", "--chdir", ".", "visualizer.wsgi:server", "--bind", "0.0.0.0:7860", "--timeout", "120", "--workers", "2"]
   ```
4. Push code to the Space repo
5. Builds and deploys automatically. Always-on on free tier.

---

## 9. TEST RESULTS (PRE-VALIDATED)

All deployment code was tested before the PR was created:

| Test | Status |
|------|--------|
| Syntax compilation (all modules) | ✅ PASS |
| WSGI import chain (`visualizer.wsgi.server` → Flask object) | ✅ PASS |
| HTTP GET `/` → 200 (6118 bytes) | ✅ PASS |
| HTTP GET `/_dash-layout` → 200 | ✅ PASS |
| Community Detection algorithms | ✅ PASS |
| Link Prediction algorithms | ✅ PASS |
| Node Embedding algorithms | ✅ PASS |
| Social Influence algorithms | ✅ PASS |
