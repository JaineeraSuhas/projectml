"""
IDCFSS - Main FastAPI Server
Intelligent Data Cleaning & Feature Selection System
Atria Institute of Technology, VTU Bangalore
"""
import os
import io
import uuid
import json
import traceback
from pathlib import Path
from typing import Optional, Dict, Any

import pandas as pd
import numpy as np
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, StreamingResponse, JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles

from modules.profiler import DataProfiler
from modules.missing_handler import MissingValueHandler
from modules.outlier_detector import OutlierDetector
from modules.encoder import CategoricalEncoder
from modules.scaler import FeatureScaler
from modules.feature_selector import FeatureSelector
from modules.report_generator import generate_html_report
from modules.pipeline_exporter import PipelineExporter

app = FastAPI(
    title="IDCFSS API",
    description="Intelligent Data Cleaning & Feature Selection System",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve frontend static files
FRONTEND_DIR = Path(__file__).parent.parent / "frontend"
if FRONTEND_DIR.exists():
    app.mount("/static", StaticFiles(directory=str(FRONTEND_DIR)), name="static")

# In-memory session storage
sessions: Dict[str, Dict[str, Any]] = {}
MAX_FILE_SIZE = 100 * 1024 * 1024  # 100MB


def df_to_safe_dict(df: pd.DataFrame) -> list:
    """Convert dataframe to JSON-safe list of dicts."""
    return json.loads(df.head(50).to_json(orient="records", date_format="iso", default_handler=str))


def load_dataframe(content: bytes, filename: str) -> pd.DataFrame:
    if filename.endswith(".csv"):
        try:
            df = pd.read_csv(io.BytesIO(content))
        except UnicodeDecodeError:
            df = pd.read_csv(io.BytesIO(content), encoding='latin1')
    elif filename.endswith((".xlsx", ".xls")):
        df = pd.read_excel(io.BytesIO(content))
    else:
        raise ValueError(f"Unsupported file type: {filename}")
    return df


@app.get("/")
def root():
    """Serve the frontend index.html."""
    index_file = FRONTEND_DIR / "index.html"
    if index_file.exists():
        return FileResponse(str(index_file))
    return {"status": "ok", "service": "IDCFSS API v1.0"}


@app.post("/upload")
async def upload_dataset(file: UploadFile = File(...)):
    """Upload a CSV/XLSX file, generate data profile, and return session ID."""
    try:
        content = await file.read()
        if len(content) > MAX_FILE_SIZE:
            raise HTTPException(status_code=413, detail="File exceeds 100MB limit")

        filename = file.filename or "dataset.csv"
        df = load_dataframe(content, filename)

        if df.empty:
            raise HTTPException(status_code=400, detail="Uploaded file is empty")

        session_id = str(uuid.uuid4())
        profiler = DataProfiler(df)
        profile = profiler.get_profile()

        sessions[session_id] = {
            "df": df,
            "filename": filename,
            "profile": profile,
            "cleaned_df": None,
            "cleaned_profile": None,
            "cleaning_log": [],
            "feature_importance": {},
            "selected_features": [],
            "pipeline_steps": [],
            "encoding_map": {},
        }

        return {
            "session_id": session_id,
            "filename": filename,
            "profile": profile,
            "preview": df_to_safe_dict(df),
            "columns": df.columns.tolist(),
        }

    except HTTPException:
        raise
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/clean")
async def clean_dataset(body: dict):
    """Apply cleaning operations to the uploaded dataset."""
    try:
        session_id = body.get("session_id")
        if not session_id or session_id not in sessions:
            raise HTTPException(status_code=404, detail="Session not found")

        session = sessions[session_id]
        df = session["df"].copy()
        config = body.get("config", {})
        log = []

        # --- Missing Value Handling ---
        missing_cfg = config.get("missing", {})
        handler = MissingValueHandler()
        for col, strategy in missing_cfg.items():
            if col in df.columns and df[col].isnull().sum() > 0:
                before = int(df[col].isnull().sum())
                df = handler.apply_strategy(df, col, strategy)
                after = int(df[col].isnull().sum())
                log.append({"step": "Missing Value", "column": col, "strategy": strategy,
                             "detail": f"Filled {before - after} nulls"})

        # --- Outlier Handling ---
        outlier_cfg = config.get("outliers", {})
        detector = OutlierDetector()
        for col, opts in outlier_cfg.items():
            if col in df.columns and pd.api.types.is_numeric_dtype(df[col]):
                method = opts.get("method", "iqr")
                action = opts.get("action", "cap")
                rows_before = len(df)
                df = detector.apply_strategy(df, col, detect_method=method, action=action)
                rows_after = len(df)
                diff = rows_before - rows_after
                log.append({"step": "Outlier Handling", "column": col,
                             "strategy": f"{method} -> {action}",
                             "detail": f"{diff} rows affected" if action == "remove" else "Values adjusted"})

        # --- Categorical Encoding ---
        encoding_cfg = config.get("encoding", {})
        encoder = CategoricalEncoder()
        for col, strategy in encoding_cfg.items():
            if col in df.columns:
                target_col = config.get("target_column")
                df = encoder.apply_strategy(df, col, strategy, target_col=target_col)
                orig_unique = sessions[session_id]['df'][col].nunique() if col in sessions[session_id]['df'].columns else '?'
                log.append({"step": "Encoding", "column": col, "strategy": strategy,
                             "detail": f"Unique: {orig_unique}"})

        # --- Feature Scaling ---
        scaling_cfg = config.get("scaling", {})
        if scaling_cfg:
            method = scaling_cfg.get("method", "standard")
            cols_to_scale = scaling_cfg.get("columns", [])
            valid_cols = [c for c in cols_to_scale if c in df.columns and pd.api.types.is_numeric_dtype(df[c])]
            if valid_cols and method != "none":
                scaler = FeatureScaler()
                df = scaler.apply_strategy(df, valid_cols, method)
                display_cols = ", ".join(valid_cols[:3]) + ("..." if len(valid_cols) > 3 else "")
                log.append({"step": "Scaling", "column": display_cols,
                             "strategy": method, "detail": f"{len(valid_cols)} columns scaled"})

        # Drop duplicate rows if requested
        if config.get("drop_duplicates", False):
            before = len(df)
            df = df.drop_duplicates()
            log.append({"step": "Duplicates", "column": "all", "strategy": "drop",
                        "detail": f"Removed {before - len(df)} duplicates"})

        cleaned_profiler = DataProfiler(df)
        cleaned_profile = cleaned_profiler.get_profile()

        session["cleaned_df"] = df
        session["cleaned_profile"] = cleaned_profile
        session["cleaning_log"] = log
        session["encoding_map"] = encoder.get_encoding_map()

        return {
            "session_id": session_id,
            "cleaned_profile": cleaned_profile,
            "cleaning_log": log,
            "preview": df_to_safe_dict(df),
            "columns": df.columns.tolist(),
        }

    except HTTPException:
        raise
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/features")
async def select_features(body: dict):
    """Run feature selection on the cleaned dataset."""
    try:
        session_id = body.get("session_id")
        if not session_id or session_id not in sessions:
            raise HTTPException(status_code=404, detail="Session not found")

        session = sessions[session_id]
        df = session.get("cleaned_df") if session.get("cleaned_df") is not None else session["df"]
        config = body.get("config", {})

        target_col = config.get("target_column")
        method = config.get("method", "random_forest")
        n_features = config.get("n_features", 10)

        num_cols = df.select_dtypes(include=np.number).columns.tolist()
        X_cols = [c for c in num_cols if c != target_col]

        if not X_cols:
            raise HTTPException(status_code=400, detail="No numeric feature columns found after preprocessing")

        selector = FeatureSelector()

        if method == "random_forest":
            if target_col and target_col in df.columns:
                importance = selector.random_forest_importance(df, X_cols, target_col)
            else:
                importance = {c: float(df[c].var()) for c in X_cols}
        elif method == "xgboost":
            if target_col and target_col in df.columns:
                importance = selector.xgboost_importance(df, X_cols, target_col)
            else:
                importance = {c: float(df[c].var()) for c in X_cols}
        elif method == "lasso":
            if target_col and target_col in df.columns:
                selector.lasso_select(df, X_cols, target_col)
                importance = {c: selector.get_importance_scores().get(c, 0.0) for c in X_cols}
            else:
                importance = {c: float(df[c].var()) for c in X_cols}
        elif method == "anova":
            if target_col and target_col in df.columns:
                selector.anova_f_select(df, X_cols, target_col, k=n_features)
                importance = {c: selector.get_importance_scores().get(c, 0.0) for c in X_cols}
            else:
                importance = {c: float(df[c].var()) for c in X_cols}
        elif method == "mutual_info":
            if target_col and target_col in df.columns:
                selector.mutual_info_select(df, X_cols, target_col, k=n_features)
                importance = {c: selector.get_importance_scores().get(c, 0.0) for c in X_cols}
            else:
                importance = {c: float(df[c].var()) for c in X_cols}
        elif method == "correlation":
            kept = selector.correlation_filter(df)
            importance = {c: 1.0 if c in kept else 0.0 for c in X_cols}
        else:
            importance = {c: float(df[c].var()) for c in X_cols}

        sorted_features = sorted(importance.items(), key=lambda x: -x[1])
        selected_features = [f[0] for f in sorted_features[:n_features]]

        session["feature_importance"] = importance
        session["selected_features"] = selected_features

        return {
            "session_id": session_id,
            "feature_importance": importance,
            "selected_features": selected_features,
            "all_features": X_cols,
        }

    except HTTPException:
        raise
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/report/{session_id}", response_class=HTMLResponse)
async def get_report(session_id: str):
    """Return the HTML quality report for a session."""
    if session_id not in sessions:
        raise HTTPException(status_code=404, detail="Session not found")
    session = sessions[session_id]
    html = generate_html_report(
        session["profile"],
        session.get("cleaned_profile") or session["profile"],
        session.get("cleaning_log", []),
        session.get("feature_importance", {}),
        session.get("selected_features", []),
        session.get("encoding_map", {}),
    )
    return HTMLResponse(content=html)


@app.get("/download/{session_id}")
async def download_cleaned(session_id: str, format: str = "csv"):
    """Download the cleaned dataset as CSV or XLSX."""
    if session_id not in sessions:
        raise HTTPException(status_code=404, detail="Session not found")
    session = sessions[session_id]
    df = session.get("cleaned_df") if session.get("cleaned_df") is not None else session["df"]

    if format == "xlsx":
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine="openpyxl") as writer:
            df.to_excel(writer, index=False)
        output.seek(0)
        return StreamingResponse(
            output,
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            headers={"Content-Disposition": 'attachment; filename="idcfss_cleaned.xlsx"'}
        )
    else:
        output = io.StringIO()
        df.to_csv(output, index=False)
        output.seek(0)
        return StreamingResponse(
            io.BytesIO(output.getvalue().encode()),
            media_type="text/csv",
            headers={"Content-Disposition": 'attachment; filename="idcfss_cleaned.csv"'}
        )


@app.get("/pipeline/{session_id}")
async def download_pipeline(session_id: str, format: str = "json"):
    """Download the preprocessing pipeline as JSON or Python code."""
    if session_id not in sessions:
        raise HTTPException(status_code=404, detail="Session not found")
    session = sessions[session_id]

    exporter = PipelineExporter()
    log = session.get("cleaning_log", [])
    for entry in log:
        step = entry.get("step", "").lower()
        col = entry.get("column", "")
        strategy = entry.get("strategy", "")
        if "missing" in step:
            exporter.add_step("missing", strategy, [col])
        elif "outlier" in step:
            parts = strategy.split("->") if "->" in strategy else [strategy, "cap"]
            exporter.add_step("outlier", parts[-1].strip(), [col])
        elif "encoding" in step:
            exporter.add_step("encoding", strategy, [col])
        elif "scaling" in step:
            exporter.add_step("scaling", strategy, [col])

    selected = session.get("selected_features", [])
    if selected:
        exporter.add_step("feature_selection", "select", selected)

    if format == "python":
        code = exporter.to_python_code()
        return StreamingResponse(
            io.BytesIO(code.encode()),
            media_type="text/x-python",
            headers={"Content-Disposition": 'attachment; filename="idcfss_pipeline.py"'}
        )
    else:
        json_str = exporter.to_json()
        return StreamingResponse(
            io.BytesIO(json_str.encode()),
            media_type="application/json",
            headers={"Content-Disposition": 'attachment; filename="idcfss_pipeline.json"'}
        )


@app.delete("/session/{session_id}")
async def delete_session(session_id: str):
    """Clean up a session."""
    if session_id in sessions:
        del sessions[session_id]
    return {"status": "deleted"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
