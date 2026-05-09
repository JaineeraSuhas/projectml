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
import logging
from pathlib import Path
from typing import Optional, Dict, Any
from datetime import datetime, timedelta
import sys

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

# ===== CONFIGURATION & LOGGING =====
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
ENVIRONMENT = os.getenv("ENVIRONMENT", "development")
SESSION_TIMEOUT = int(os.getenv("SESSION_TIMEOUT", "3600"))  # 1 hour

logging.basicConfig(
    level=LOG_LEVEL,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    stream=sys.stdout
)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="IDCFSS API",
    description="Intelligent Data Cleaning & Feature Selection System",
    version="1.0.0"
)

# ===== CORS CONFIGURATION =====
allowed_origins = os.getenv("ALLOWED_ORIGINS", "*").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "DELETE", "OPTIONS"],
    allow_headers=["Content-Type", "Authorization"],
    max_age=600,
)

# Serve frontend static files
FRONTEND_DIR = Path(__file__).parent.parent / "frontend"
if FRONTEND_DIR.exists():
    app.mount("/static", StaticFiles(directory=str(FRONTEND_DIR)), name="static")

# In-memory session storage with timestamps
sessions: Dict[str, Dict[str, Any]] = {}
MAX_FILE_SIZE = int(os.getenv("MAX_FILE_SIZE", 100)) * 1024 * 1024  # MB to bytes
MAX_SESSIONS = int(os.getenv("MAX_SESSIONS", 100))
MAX_ROWS = int(os.getenv("MAX_ROWS", 100000))

def cleanup_expired_sessions():
    """Remove sessions older than SESSION_TIMEOUT."""
    now = datetime.now()
    expired = []
    for session_id, session_data in sessions.items():
        created_at = session_data.get("created_at", now)
        if now - created_at > timedelta(seconds=SESSION_TIMEOUT):
            expired.append(session_id)
    
    for session_id in expired:
        del sessions[session_id]
        logger.info(f"Cleaned up expired session: {session_id}")
    
    return len(expired)


def check_session_limit():
    """Check if we've reached max sessions and cleanup old ones if needed."""
    if len(sessions) >= MAX_SESSIONS:
        cleanup_expired_sessions()
        if len(sessions) >= MAX_SESSIONS:
            # Force cleanup of oldest session
            oldest_id = min(sessions.keys(), key=lambda k: sessions[k].get("created_at", datetime.now()))
            del sessions[oldest_id]
            logger.warning(f"Force deleted oldest session: {oldest_id}")



def df_to_safe_dict(df: pd.DataFrame) -> list:
    """Convert dataframe to JSON-safe list of dicts."""
    return json.loads(df.head(50).to_json(orient="records", date_format="iso", default_handler=str))


def restore_original_dtypes(df: pd.DataFrame, original_df: pd.DataFrame) -> pd.DataFrame:
    """
    Restore column dtypes in df to match original_df as closely as possible.
    This is crucial after KNN/MICE imputation which converts ints to float64.
    Only touches columns that exist in both dataframes.
    """
    df = df.copy()
    for col in df.columns:
        if col not in original_df.columns:
            continue
        orig_dtype = original_df[col].dtype
        cur_dtype = df[col].dtype
        if cur_dtype == orig_dtype:
            continue
        try:
            # Restore integer columns: only if no NaNs remain (can't have NaN in int)
            if pd.api.types.is_integer_dtype(orig_dtype) and pd.api.types.is_float_dtype(cur_dtype):
                if df[col].isnull().sum() == 0:
                    df[col] = df[col].round().astype(orig_dtype)
                # else keep as float (NaN forces float)
            # Restore object/string columns that were not meant to be numeric
            elif pd.api.types.is_object_dtype(orig_dtype) and not pd.api.types.is_object_dtype(cur_dtype):
                df[col] = df[col].astype(str)
        except Exception:
            pass  # Best-effort — keep as-is if conversion fails
    return df


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
    
    if len(df) > MAX_ROWS:
        raise ValueError(f"Dataset exceeds maximum {MAX_ROWS} rows. Please upload a smaller dataset.")
    
    return df


@app.get("/health")
def health_check():
    """Health check endpoint for monitoring and load balancers."""
    try:
        cleanup_expired_sessions()
        return {
            "status": "healthy",
            "environment": ENVIRONMENT,
            "version": "1.0.0",
            "sessions_active": len(sessions),
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        raise HTTPException(status_code=503, detail="Service unavailable")


@app.get("/")
def root():
    """Serve the frontend index.html."""
    index_file = FRONTEND_DIR / "index.html"
    if index_file.exists():
        return FileResponse(str(index_file))
    return {"status": "ok", "service": "IDCFSS API v1.0", "environment": ENVIRONMENT}


@app.post("/upload")
async def upload_dataset(file: UploadFile = File(...)):
    """Upload a CSV/XLSX file, generate data profile, and return session ID."""
    try:
        # Validate filename
        if not file.filename:
            raise HTTPException(status_code=400, detail="No filename provided")
        
        filename = file.filename
        if not filename.lower().endswith(('.csv', '.xlsx', '.xls')):
            raise HTTPException(status_code=400, detail="Only CSV and Excel files are supported")
        
        # Read and validate file size
        content = await file.read()
        if len(content) > MAX_FILE_SIZE:
            raise HTTPException(status_code=413, detail=f"File exceeds {MAX_FILE_SIZE / 1024 / 1024:.0f}MB limit")
        
        if len(content) == 0:
            raise HTTPException(status_code=400, detail="Uploaded file is empty")
        
        # Load and validate dataframe
        df = load_dataframe(content, filename)
        
        if df.empty:
            raise HTTPException(status_code=400, detail="Uploaded file contains no data")
        
        if df.shape[1] == 0:
            raise HTTPException(status_code=400, detail="Uploaded file has no columns")
        
        # Check session limit
        check_session_limit()
        
        # Create session
        session_id = str(uuid.uuid4())
        profiler = DataProfiler(df)
        profile = profiler.get_profile()
        
        sessions[session_id] = {
            "df": df,
            "filename": filename,
            "profile": profile,
            # export_df: human-readable cleaned data (no encoding/scaling) — used for download
            "export_df": None,
            # ml_df: fully processed data (encoded + scaled) — used for feature selection
            "ml_df": None,
            "cleaned_profile": None,
            "cleaning_log": [],
            "feature_importance": {},
            "selected_features": [],
            "pipeline_steps": [],
            "encoding_map": {},
            "created_at": datetime.now(),
        }
        
        logger.info(f"Session created: {session_id} | File: {filename} | Shape: {df.shape}")
        
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
        logger.error(f"Upload error: {str(e)}\n{traceback.format_exc()}")
        raise HTTPException(status_code=500, detail="Failed to process uploaded file")


@app.post("/clean")
async def clean_dataset(body: dict):
    """
    Apply cleaning operations to the uploaded dataset.

    Pipeline is split into two stages:
      1. export_df  — missing values + outliers + duplicates only.
                      Categorical columns are kept as original text.
                      This is what gets downloaded by the user.
      2. ml_df      — export_df further processed with encoding + scaling.
                      Used internally for feature selection / ML tasks.
    """
    try:
        session_id = body.get("session_id")
        if not session_id or session_id not in sessions:
            raise HTTPException(status_code=404, detail="Session not found or expired")

        session = sessions[session_id]
        if "df" not in session or session["df"] is None:
            raise HTTPException(status_code=400, detail="No dataset in session")
        
        df = session["df"].copy()
        config = body.get("config", {})
        log = []

        try:
            # ── STAGE 1: Human-readable cleaning (exported to CSV/XLSX) ──────────

            # --- Missing Value Handling ---
            missing_cfg = config.get("missing", {})
            handler = MissingValueHandler()
            for col, strategy in missing_cfg.items():
                if col in df.columns and df[col].isnull().sum() > 0:
                    before = int(df[col].isnull().sum())
                    df = handler.apply_strategy(df, col, strategy)
                    if col in df.columns:
                        after = int(df[col].isnull().sum())
                        detail = f"Filled {before - after} nulls"
                    else:
                        detail = f"Dropped column with {before} nulls"
                    log.append({"step": "Missing Value", "column": col, "strategy": strategy,
                                 "detail": detail})

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

            # --- Drop Duplicates ---
            if config.get("drop_duplicates", False):
                before = len(df)
                df = df.drop_duplicates()
                removed = before - len(df)
                if removed > 0:
                    log.append({"step": "Duplicates", "column": "all", "strategy": "drop",
                                "detail": f"Removed {removed} duplicates"})

            # Save human-readable version for download (original text values preserved).
            # Restore original column dtypes so KNN/MICE float conversion doesn't leak
            # into the CSV (e.g. int column 25 → 25.0 → back to 25).
            export_df = restore_original_dtypes(df, session["df"])

            # ── STAGE 2: ML preprocessing (encoding + scaling) for feature selection ─
            ml_df = df.copy()

            # --- Categorical Encoding (applied to ml_df only) ---
            encoding_cfg = config.get("encoding", {})
            encoder = CategoricalEncoder()
            for col, strategy in encoding_cfg.items():
                # Skip if user chose 'none'
                if strategy in ("none", "", None):
                    continue
                if col in ml_df.columns:
                    target_col = config.get("target_column")
                    ml_df = encoder.apply_strategy(ml_df, col, strategy, target_col=target_col)
                    orig_unique = session['df'][col].nunique() if col in session['df'].columns else '?'
                    log.append({"step": "Encoding", "column": col, "strategy": strategy,
                                 "detail": f"{orig_unique} unique values encoded (ML only)"})

            # --- Feature Scaling (applied to ml_df only) ---
            scaling_cfg = config.get("scaling", {})
            if scaling_cfg:
                scale_method = scaling_cfg.get("method", "standard")
                cols_to_scale = scaling_cfg.get("columns", [])
                valid_cols = [
                    c for c in cols_to_scale
                    if c in ml_df.columns and pd.api.types.is_numeric_dtype(ml_df[c])
                ]
                if valid_cols and scale_method not in ("none", "", None):
                    scaler = FeatureScaler()
                    ml_df = scaler.apply_strategy(ml_df, valid_cols, scale_method)
                    display_cols = ", ".join(valid_cols[:3]) + ("..." if len(valid_cols) > 3 else "")
                    log.append({"step": "Scaling", "column": display_cols,
                                 "strategy": scale_method,
                                 "detail": f"{len(valid_cols)} columns scaled (ML only)"})

            # ── Profile is based on export_df so column types stay readable ────────
            cleaned_profiler = DataProfiler(export_df)
            cleaned_profile = cleaned_profiler.get_profile()

            session["export_df"] = export_df          # human-readable → download
            session["ml_df"] = ml_df                  # encoded+scaled → feature selection
            # Keep cleaned_df as an alias pointing to export_df for backwards compat
            session["cleaned_df"] = export_df
            session["cleaned_profile"] = cleaned_profile
            session["cleaning_log"] = log
            session["encoding_map"] = encoder.get_encoding_map()

            logger.info(
                f"Dataset cleaned: {session_id} | Steps: {len(log)} "
                f"| Export shape: {export_df.shape} | ML shape: {ml_df.shape}"
            )

            return {
                "session_id": session_id,
                "cleaned_profile": cleaned_profile,
                "cleaning_log": log,
                "preview": df_to_safe_dict(export_df),
                "columns": export_df.columns.tolist(),
            }

        except Exception as e:
            logger.error(f"Cleaning pipeline error in session {session_id}: {str(e)}\n{traceback.format_exc()}")
            raise HTTPException(status_code=400, detail=f"Cleaning failed: {str(e)}")

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Clean endpoint error: {str(e)}\n{traceback.format_exc()}")
        raise HTTPException(status_code=500, detail="Internal server error during cleaning")


@app.post("/features")
async def select_features(body: dict):
    """Run feature selection on the ML-processed (encoded+scaled) dataset."""
    try:
        session_id = body.get("session_id")
        if not session_id or session_id not in sessions:
            raise HTTPException(status_code=404, detail="Session not found or expired")

        session = sessions[session_id]
        # Prefer ml_df (encoded+scaled) for feature selection; fall back to export_df or raw df
        df = session.get("ml_df")
        if df is None:
            df = session.get("export_df")
        if df is None:
            df = session.get("cleaned_df")
        if df is None:
            df = session.get("df")
        
        if df is None:
            raise HTTPException(status_code=400, detail="No dataset available in session")
        
        config = body.get("config", {})

        target_col = config.get("target_column")
        method = config.get("method", "random_forest")
        n_features = max(1, min(config.get("n_features", 10), len(df.columns) - 1))

        num_cols = df.select_dtypes(include=np.number).columns.tolist()
        X_cols = [c for c in num_cols if c != target_col]

        if not X_cols:
            raise HTTPException(status_code=400, detail="No numeric feature columns found after preprocessing")

        selector = FeatureSelector()

        try:
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
            
            logger.info(f"Features selected: {session_id} | Method: {method} | Count: {len(selected_features)}")

            return {
                "session_id": session_id,
                "feature_importance": importance,
                "selected_features": selected_features,
                "all_features": X_cols,
            }
        
        except Exception as e:
            logger.error(f"Feature selection error: {str(e)}")
            raise HTTPException(status_code=400, detail=f"Feature selection failed: {str(e)}")

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Features endpoint error: {str(e)}\n{traceback.format_exc()}")
        raise HTTPException(status_code=500, detail="Internal server error during feature selection")


@app.get("/report/{session_id}", response_class=HTMLResponse)
async def get_report(session_id: str):
    """Return the HTML quality report for a session."""
    try:
        if session_id not in sessions:
            raise HTTPException(status_code=404, detail="Session not found or expired")
        
        session = sessions[session_id]
        html = generate_html_report(
            session["profile"],
            session.get("cleaned_profile") or session["profile"],
            session.get("cleaning_log", []),
            session.get("feature_importance", {}),
            session.get("selected_features", []),
            session.get("encoding_map", {}),
        )
        logger.info(f"Report generated: {session_id}")
        return HTMLResponse(content=html)
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Report generation error: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to generate report")


@app.get("/download/{session_id}")
async def download_cleaned(session_id: str, format: str = "csv"):
    """Download the cleaned (human-readable) dataset as CSV or XLSX."""
    try:
        if session_id not in sessions:
            raise HTTPException(status_code=404, detail="Session not found or expired")
        
        if format not in ["csv", "xlsx"]:
            raise HTTPException(status_code=400, detail="Format must be 'csv' or 'xlsx'")
        
        session = sessions[session_id]
        # Always export the human-readable version (original categorical text preserved,
        # no encoding or scaling applied).  Fall back to raw df if cleaning hasn't run yet.
        df = session.get("export_df")
        if df is None:
            df = session.get("cleaned_df")
        if df is None:
            df = session.get("df")
        
        if df is None:
            raise HTTPException(status_code=400, detail="No dataset available in session")

        try:
            if format == "xlsx":
                output = io.BytesIO()
                with pd.ExcelWriter(output, engine="openpyxl") as writer:
                    df.to_excel(writer, index=False)
                output.seek(0)
                logger.info(f"Dataset exported: {session_id} | Format: xlsx | Size: {len(output.getvalue())} bytes")
                return StreamingResponse(
                    output,
                    media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    headers={"Content-Disposition": 'attachment; filename="idcfss_cleaned.xlsx"'}
                )
            else:
                output = io.StringIO()
                df.to_csv(output, index=False)
                output.seek(0)
                content = output.getvalue().encode()
                logger.info(f"Dataset exported: {session_id} | Format: csv | Size: {len(content)} bytes")
                return StreamingResponse(
                    io.BytesIO(content),
                    media_type="text/csv",
                    headers={"Content-Disposition": 'attachment; filename="idcfss_cleaned.csv"'}
                )
        except Exception as e:
            logger.error(f"Export error for {session_id}: {str(e)}")
            raise HTTPException(status_code=500, detail="Failed to export dataset")
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Download endpoint error: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")


@app.get("/pipeline/{session_id}")
async def download_pipeline(session_id: str, format: str = "json"):
    """Download the preprocessing pipeline as JSON or Python code."""
    try:
        if session_id not in sessions:
            raise HTTPException(status_code=404, detail="Session not found or expired")
        
        if format not in ["json", "python"]:
            raise HTTPException(status_code=400, detail="Format must be 'json' or 'python'")
        
        session = sessions[session_id]

        try:
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
                logger.info(f"Pipeline exported: {session_id} | Format: python")
                return StreamingResponse(
                    io.BytesIO(code.encode()),
                    media_type="text/x-python",
                    headers={"Content-Disposition": 'attachment; filename="idcfss_pipeline.py"'}
                )
            else:
                json_str = exporter.to_json()
                logger.info(f"Pipeline exported: {session_id} | Format: json")
                return StreamingResponse(
                    io.BytesIO(json_str.encode()),
                    media_type="application/json",
                    headers={"Content-Disposition": 'attachment; filename="idcfss_pipeline.json"'}
                )
        except Exception as e:
            logger.error(f"Pipeline export error: {str(e)}")
            raise HTTPException(status_code=500, detail="Failed to export pipeline")
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Pipeline endpoint error: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")


@app.delete("/session/{session_id}")
async def delete_session(session_id: str):
    """Clean up a session."""
    try:
        if session_id in sessions:
            del sessions[session_id]
            logger.info(f"Session deleted: {session_id}")
            return {"status": "deleted", "session_id": session_id}
        else:
            raise HTTPException(status_code=404, detail="Session not found")
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Session deletion error: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to delete session")


if __name__ == "__main__":
    import uvicorn
    
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", "8000"))
    reload = ENVIRONMENT == "development"
    
    logger.info(f"Starting IDCFSS API | Environment: {ENVIRONMENT} | Host: {host}:{port}")
    uvicorn.run("main:app", host=host, port=port, reload=reload)
