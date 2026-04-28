"""
IDCFSS - Categorical Encoder Module
Handles encoding of categorical columns using multiple strategies.
"""
import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder
from typing import Dict, Optional


class CategoricalEncoder:
    def __init__(self):
        self._encoding_maps: Dict[str, dict] = {}
        self._label_encoders: Dict[str, LabelEncoder] = {}

    def label_encode(self, df: pd.DataFrame, col: str) -> pd.DataFrame:
        df = df.copy()
        le = LabelEncoder()
        non_null = df[col].dropna()
        le.fit(non_null.astype(str))
        df[col] = df[col].apply(lambda x: le.transform([str(x)])[0] if pd.notna(x) else np.nan)
        self._label_encoders[col] = le
        self._encoding_maps[col] = {str(cls): int(i) for i, cls in enumerate(le.classes_)}
        return df

    def onehot_encode(self, df: pd.DataFrame, cols: list) -> pd.DataFrame:
        df = df.copy()
        for col in cols:
            if col in df.columns:
                dummies = pd.get_dummies(df[col], prefix=col, drop_first=False).astype(int)
                df = pd.concat([df.drop(columns=[col]), dummies], axis=1)
                self._encoding_maps[col] = {"method": "onehot", "columns": dummies.columns.tolist()}
        return df

    def binary_encode(self, df: pd.DataFrame, col: str) -> pd.DataFrame:
        df = df.copy()
        unique_vals = df[col].dropna().unique()
        val_map = {v: i for i, v in enumerate(sorted([str(v) for v in unique_vals]))}
        max_bits = max(len(bin(len(val_map))) - 2, 1)
        df[col + "_int"] = df[col].apply(lambda x: val_map.get(str(x), -1) if pd.notna(x) else -1)
        for bit in range(max_bits):
            df[f"{col}_bin_{bit}"] = df[col + "_int"].apply(lambda x: (x >> bit) & 1 if x >= 0 else 0)
        df = df.drop(columns=[col, col + "_int"])
        self._encoding_maps[col] = {"method": "binary", "map": val_map, "bits": max_bits}
        return df

    def target_encode(self, df: pd.DataFrame, col: str, target: str) -> pd.DataFrame:
        df = df.copy()
        if target not in df.columns or not pd.api.types.is_numeric_dtype(df[target]):
            return self.label_encode(df, col)
        target_mean = df.groupby(col)[target].mean().to_dict()
        global_mean = df[target].mean()
        df[col] = df[col].map(target_mean).fillna(global_mean)
        self._encoding_maps[col] = {"method": "target", "map": {str(k): float(v) for k, v in target_mean.items()}}
        return df

    def get_encoding_map(self) -> dict:
        return self._encoding_maps

    def apply_strategy(self, df: pd.DataFrame, col: str, strategy: str, target_col: Optional[str] = None) -> pd.DataFrame:
        strategy = strategy.lower()
        if strategy == "label":
            return self.label_encode(df, col)
        elif strategy == "onehot":
            return self.onehot_encode(df, [col])
        elif strategy == "binary":
            return self.binary_encode(df, col)
        elif strategy == "target" and target_col:
            return self.target_encode(df, col, target_col)
        else:
            n_unique = df[col].nunique()
            if n_unique > 50:
                return self.binary_encode(df, col)
            elif n_unique <= 10:
                return self.onehot_encode(df, [col])
            else:
                return self.label_encode(df, col)
