# IDCFSS — Intelligent Data Cleaning & Feature Selection System
**Automated ML Pipeline Optimization Platform**
Atria Institute of Technology, VTU Bangalore · v1.0 · April 2026
Author: Jaineera

## Quick Start

### Step 1 — Install backend dependencies:
```bash
cd backend
pip install -r requirements.txt
```

### Step 2 — Start the API:
```bash
cd backend
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

### Step 3 — Open the frontend:
Open `frontend/index.html` in your browser.
The frontend connects to `http://localhost:8000` by default.

## Project Structure
```
porjectml/
├── backend/
│   ├── main.py                  # FastAPI server (10 endpoints)
│   ├── requirements.txt
│   └── modules/
│       ├── __init__.py
│       ├── profiler.py          # Quality scoring
│       ├── missing_handler.py   # 8 imputation strategies
│       ├── outlier_detector.py  # IQR, Z-score, Isolation Forest
│       ├── encoder.py           # Label, One-Hot, Binary, Target
│       ├── scaler.py            # MinMax, Standard, Robust
│       ├── feature_selector.py  # RF, XGBoost, Lasso, ANOVA, MI
│       ├── report_generator.py  # HTML before/after report
│       └── pipeline_exporter.py # JSON + Python code gen
├── frontend/
│   ├── index.html               # Main HTML shell
│   ├── style.css                # MD3 design system
│   ├── app-core.js              # State management & utilities
│   ├── app-steps-01.js          # Upload & Profile steps
│   ├── app-steps-2.js           # Clean step
│   └── app-steps-34.js          # Features & Export steps
├── tests/test_modules.py
└── README.md
```

## API Endpoints
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | /upload | Upload CSV/XLSX → session ID + profile |
| POST | /clean | Apply cleaning config → cleaned dataset |
| POST | /features | Run feature selection → importance scores |
| GET | /report/{session_id} | HTML quality report |
| GET | /download/{session_id}?format=csv | Download cleaned CSV |
| GET | /download/{session_id}?format=xlsx | Download cleaned XLSX |
| GET | /pipeline/{session_id}?format=python | Python pipeline code |
| GET | /pipeline/{session_id}?format=json | JSON pipeline config |
| DELETE | /session/{session_id} | Clean up session |

## Running Tests
```bash
cd backend
pip install pytest
pytest ../tests/test_modules.py -v
```
