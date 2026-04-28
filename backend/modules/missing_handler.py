"""
IDCFSS - Missing Value Handler Module
Handles detection and imputation of missing values using multiple strategies.
"""
import pandas as pd
import numpy as np
from sklearn.impute import KNNImputer
from sklearn.experimental import enable_iterative_imputer  # noqa: F401
from sklearn.impute import IterativeImputer
from typing import Optional


class MissingValueHandler:
    def detect(self, df: pd.DataFrame) -> dict:
        return {col: int(df[col].isnull().sum()) for col in df.columns if df[col].isnull().sum() > 0}

    def impute_mean(self, df: pd.DataFrame, col: str) -> pd.DataFrame:
        df = df.copy()
        if pd.api.types.is_numeric_dtype(df[col]):
            df[col] = df[col].fillna(df[col].mean())
        return df

    def impute_median(self, df: pd.DataFrame, col: str) -> pd.DataFrame:
        df = df.copy()
        if pd.api.types.is_numeric_dtype(df[col]):
            df[col] = df[col].fillna(df[col].median())
        return df

    def impute_mode(self, df: pd.DataFrame, col: str) -> pd.DataFrame:
        df = df.copy()
        mode_val = df[col].mode()
        if len(mode_val) > 0:
            df[col] = df[col].fillna(mode_val[0])
        return df

    def impute_constant(self, df: pd.DataFrame, col: str, value) -> pd.DataFrame:
        df = df.copy()
        df[col] = df[col].fillna(value)
        return df

    def impute_knn(self, df: pd.DataFrame, cols: list, k: int = 5) -> pd.DataFrame:
        df = df.copy()
        num_cols = [c for c in cols if pd.api.types.is_numeric_dtype(df[c])]
        if not num_cols:
            return df
        imputer = KNNImputer(n_neighbors=k)
        df[num_cols] = imputer.fit_transform(df[num_cols])
        return df

    def impute_mice(self, df: pd.DataFrame) -> pd.DataFrame:
        df = df.copy()
        num_cols = df.select_dtypes(include=np.number).columns.tolist()
        if not num_cols:
            return df
        imputer = IterativeImputer(random_state=42, max_iter=10)
        df[num_cols] = imputer.fit_transform(df[num_cols])
        return df

    def fill_forward(self, df: pd.DataFrame, col: str) -> pd.DataFrame:
        df = df.copy()
        df[col] = df[col].ffill()
        return df

    def fill_backward(self, df: pd.DataFrame, col: str) -> pd.DataFrame:
        df = df.copy()
        df[col] = df[col].bfill()
        return df

    def drop_rows(self, df: pd.DataFrame, threshold: float = 0.5) -> pd.DataFrame:
        df = df.copy()
        min_valid = int(df.shape[1] * (1 - threshold))
        return df.dropna(thresh=min_valid)

    def apply_strategy(self, df: pd.DataFrame, col: str, strategy: str, constant_value=None, k: int = 5) -> pd.DataFrame:
        strategy = strategy.lower()
        if strategy == "mean":
            return self.impute_mean(df, col)
        elif strategy == "median":
            return self.impute_median(df, col)
        elif strategy == "mode":
            return self.impute_mode(df, col)
        elif strategy == "knn":
            return self.impute_knn(df, [col], k=k)
        elif strategy == "mice":
            return self.impute_mice(df)
        elif strategy == "ffill":
            return self.fill_forward(df, col)
        elif strategy == "bfill":
            return self.fill_backward(df, col)
        elif strategy == "constant" and constant_value is not None:
            return self.impute_constant(df, col, constant_value)
        elif strategy == "drop":
            return self.drop_rows(df)
        else:
            if pd.api.types.is_numeric_dtype(df[col]):
                return self.impute_median(df, col)
            return self.impute_mode(df, col)
