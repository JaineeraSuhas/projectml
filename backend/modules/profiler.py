"""
IDCFSS - Data Profiler Module
Generates comprehensive dataset quality statistics and profile.
"""
import pandas as pd
import numpy as np
import json
import math

def safe_float(val, default=0.0):
    try:
        v = float(val)
        if math.isnan(v) or math.isinf(v):
            return default
        return v
    except (ValueError, TypeError):
        return default

class DataProfiler:
    def __init__(self, df: pd.DataFrame):
        self.df = df.copy()

    def get_profile(self) -> dict:
        df = self.df
        total_cells = df.shape[0] * df.shape[1]
        missing_cells = df.isnull().sum().sum()
        duplicate_rows = int(df.duplicated().sum())

        col_profiles = {}
        for col in df.columns:
            col_profiles[col] = self._profile_column(col)

        quality_score = self._compute_quality_score(df, missing_cells, total_cells, duplicate_rows)

        return {
            "shape": {"rows": int(df.shape[0]), "cols": int(df.shape[1])},
            "total_cells": int(total_cells),
            "missing_cells": int(missing_cells),
            "missing_pct": round(100 * missing_cells / total_cells, 2) if total_cells > 0 else 0,
            "duplicate_rows": duplicate_rows,
            "quality_score": quality_score,
            "columns": col_profiles,
        }

    def _profile_column(self, col: str) -> dict:
        series = self.df[col]
        missing = int(series.isnull().sum())
        missing_pct = round(100 * missing / len(series), 2) if len(series) > 0 else 0
        dtype = str(series.dtype)

        result = {
            "dtype": dtype,
            "inferred_type": self._infer_type(series),
            "missing": missing,
            "missing_pct": missing_pct,
            "unique": int(series.nunique()),
            "unique_pct": round(100 * series.nunique() / len(series), 2) if len(series) > 0 else 0,
        }

        inferred = self._infer_type(series)
        if inferred == "numeric":
            # Ensure we are working with float for statistical operations to avoid numpy boolean issues
            num_series = series.dropna().astype(float)
            desc = num_series.describe()
            result["stats"] = {
                "mean": round(safe_float(desc.get("mean", 0)), 4),
                "std": round(safe_float(desc.get("std", 0)), 4),
                "min": round(safe_float(desc.get("min", 0)), 4),
                "q25": round(safe_float(desc.get("25%", 0)), 4),
                "median": round(safe_float(desc.get("50%", 0)), 4),
                "q75": round(safe_float(desc.get("75%", 0)), 4),
                "max": round(safe_float(desc.get("max", 0)), 4),
            }
            q1 = num_series.quantile(0.25)
            q3 = num_series.quantile(0.75)
            iqr = q3 - q1
            outliers = num_series[(num_series < q1 - 1.5 * iqr) | (num_series > q3 + 1.5 * iqr)]
            result["outlier_count"] = int(outliers.count())
        else:
            top5 = series.value_counts().head(5)
            result["top_values"] = {str(k): int(v) for k, v in top5.items()}

        return result

    def _infer_type(self, series: pd.Series) -> str:
        if pd.api.types.is_bool_dtype(series):
            return "categorical"  # Treat booleans as categorical to avoid confusion in stats
        if pd.api.types.is_numeric_dtype(series):
            return "numeric"
        if pd.api.types.is_datetime64_any_dtype(series):
            return "datetime"
        return "categorical"

    def _compute_quality_score(self, df, missing_cells, total_cells, duplicate_rows) -> float:
        score = 100.0
        if total_cells > 0:
            score -= 40 * (missing_cells / total_cells)
        if df.shape[0] > 0:
            score -= 20 * (duplicate_rows / df.shape[0])
        num_cols = df.select_dtypes(include=np.number).columns
        if len(num_cols) > 0:
            low_var = sum(1 for c in num_cols if df[c].std() < 0.01)
            score -= 10 * (low_var / len(num_cols))
        return max(0.0, round(score, 1))
