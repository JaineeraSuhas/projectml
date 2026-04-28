"""
IDCFSS - Outlier Detector Module
Detects and handles outliers using IQR, Z-score, and Isolation Forest.
"""
import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest
from typing import List


class OutlierDetector:
    def detect_iqr(self, df: pd.DataFrame, col: str, factor: float = 1.5) -> List[int]:
        if not pd.api.types.is_numeric_dtype(df[col]):
            return []
        q1 = df[col].quantile(0.25)
        q3 = df[col].quantile(0.75)
        iqr = q3 - q1
        mask = (df[col] < q1 - factor * iqr) | (df[col] > q3 + factor * iqr)
        return df.index[mask & df[col].notna()].tolist()

    def detect_zscore(self, df: pd.DataFrame, col: str, threshold: float = 3.0) -> List[int]:
        if not pd.api.types.is_numeric_dtype(df[col]):
            return []
        mean = df[col].mean()
        std = df[col].std()
        if std == 0:
            return []
        z = (df[col] - mean) / std
        mask = z.abs() > threshold
        return df.index[mask & df[col].notna()].tolist()

    def detect_isolation_forest(self, df: pd.DataFrame, cols: List[str], contamination: float = 0.05) -> List[int]:
        num_cols = [c for c in cols if pd.api.types.is_numeric_dtype(df[c])]
        if not num_cols:
            return []
        sub = df[num_cols].dropna()
        if len(sub) < 10:
            return []
        clf = IsolationForest(contamination=contamination, random_state=42)
        preds = clf.fit_predict(sub)
        return sub.index[preds == -1].tolist()

    def cap_outliers(self, df: pd.DataFrame, col: str, method: str = "iqr") -> pd.DataFrame:
        df = df.copy()
        if not pd.api.types.is_numeric_dtype(df[col]):
            return df
        if method == "iqr":
            q1 = df[col].quantile(0.25)
            q3 = df[col].quantile(0.75)
            iqr = q3 - q1
            lower = q1 - 1.5 * iqr
            upper = q3 + 1.5 * iqr
        else:
            mean = df[col].mean()
            std = df[col].std()
            lower = mean - 3 * std
            upper = mean + 3 * std
        df[col] = df[col].clip(lower=lower, upper=upper)
        return df

    def remove_outliers(self, df: pd.DataFrame, indices: List[int]) -> pd.DataFrame:
        return df.drop(index=[i for i in indices if i in df.index])

    def impute_outliers(self, df: pd.DataFrame, col: str, indices: List[int], method: str = "median") -> pd.DataFrame:
        df = df.copy()
        valid_indices = [i for i in indices if i in df.index]
        if not valid_indices:
            return df
        if method == "median":
            fill_val = df[col].median()
        elif method == "mean":
            fill_val = df[col].mean()
        else:
            fill_val = df[col].median()
        df.loc[valid_indices, col] = fill_val
        return df

    def apply_strategy(self, df: pd.DataFrame, col: str, detect_method: str = "iqr",
                       action: str = "cap", contamination: float = 0.05) -> pd.DataFrame:
        if detect_method == "iqr":
            indices = self.detect_iqr(df, col)
        elif detect_method == "zscore":
            indices = self.detect_zscore(df, col)
        elif detect_method == "isolation_forest":
            indices = self.detect_isolation_forest(df, [col], contamination)
        else:
            indices = self.detect_iqr(df, col)

        if not indices:
            return df

        if action == "remove":
            return self.remove_outliers(df, indices)
        elif action == "cap":
            return self.cap_outliers(df, col, method=detect_method if detect_method != "isolation_forest" else "iqr")
        elif action == "impute":
            return self.impute_outliers(df, col, indices)
        return df
