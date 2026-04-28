"""
IDCFSS - Feature Scaler Module
Handles normalization and standardization of numeric features.
"""
import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler, StandardScaler, RobustScaler
from typing import List, Dict, Any


class FeatureScaler:
    def __init__(self):
        self._scalers: Dict[str, Any] = {}

    def minmax_scale(self, df: pd.DataFrame, cols: List[str]) -> pd.DataFrame:
        df = df.copy()
        valid_cols = [c for c in cols if pd.api.types.is_numeric_dtype(df[c])]
        if not valid_cols:
            return df
        scaler = MinMaxScaler()
        df[valid_cols] = scaler.fit_transform(df[valid_cols])
        self._scalers["minmax"] = scaler
        return df

    def standard_scale(self, df: pd.DataFrame, cols: List[str]) -> pd.DataFrame:
        df = df.copy()
        valid_cols = [c for c in cols if pd.api.types.is_numeric_dtype(df[c])]
        if not valid_cols:
            return df
        scaler = StandardScaler()
        df[valid_cols] = scaler.fit_transform(df[valid_cols])
        self._scalers["standard"] = scaler
        return df

    def robust_scale(self, df: pd.DataFrame, cols: List[str]) -> pd.DataFrame:
        df = df.copy()
        valid_cols = [c for c in cols if pd.api.types.is_numeric_dtype(df[c])]
        if not valid_cols:
            return df
        scaler = RobustScaler()
        df[valid_cols] = scaler.fit_transform(df[valid_cols])
        self._scalers["robust"] = scaler
        return df

    def get_scaler_params(self) -> dict:
        result = {}
        for name, scaler in self._scalers.items():
            result[name] = {
                "type": type(scaler).__name__,
                "fitted": True
            }
            if hasattr(scaler, "scale_"):
                result[name]["scale"] = scaler.scale_.tolist()
            if hasattr(scaler, "mean_"):
                result[name]["mean"] = scaler.mean_.tolist()
        return result

    def apply_strategy(self, df: pd.DataFrame, cols: List[str], strategy: str) -> pd.DataFrame:
        strategy = strategy.lower()
        if strategy == "minmax":
            return self.minmax_scale(df, cols)
        elif strategy == "standard":
            return self.standard_scale(df, cols)
        elif strategy == "robust":
            return self.robust_scale(df, cols)
        else:
            return df
