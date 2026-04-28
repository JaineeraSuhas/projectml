"""
IDCFSS - Feature Selector Module
Implements Filter, Wrapper, and Embedded feature selection methods.
"""
import pandas as pd
import numpy as np
from sklearn.feature_selection import (
    VarianceThreshold, SelectKBest, chi2, f_classif, mutual_info_classif,
    RFE
)
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.linear_model import Lasso
from typing import List, Dict


class FeatureSelector:
    def __init__(self):
        self._importance_scores: Dict[str, float] = {}

    def variance_threshold(self, df: pd.DataFrame, threshold: float = 0.01) -> List[str]:
        num_cols = df.select_dtypes(include=np.number).columns.tolist()
        if not num_cols:
            return []
        selector = VarianceThreshold(threshold=threshold)
        selector.fit(df[num_cols].fillna(0))
        return [num_cols[i] for i, s in enumerate(selector.get_support()) if s]

    def correlation_filter(self, df: pd.DataFrame, threshold: float = 0.95) -> List[str]:
        num_cols = df.select_dtypes(include=np.number).columns.tolist()
        if not num_cols:
            return num_cols
        corr = df[num_cols].corr().abs()
        upper = corr.where(np.triu(np.ones(corr.shape), k=1).astype(bool))
        to_drop = [col for col in upper.columns if any(upper[col] > threshold)]
        return [c for c in num_cols if c not in to_drop]

    def anova_f_select(self, df: pd.DataFrame, X_cols: List[str], y_col: str, k: int = 10) -> List[str]:
        try:
            X = df[X_cols].fillna(0)
            y = df[y_col].fillna(df[y_col].mode()[0])
            k = min(k, len(X_cols))
            selector = SelectKBest(f_classif, k=k)
            selector.fit(X, y)
            selected = [X_cols[i] for i, s in enumerate(selector.get_support()) if s]
            scores = dict(zip(X_cols, selector.scores_))
            self._importance_scores.update({k: float(v) for k, v in scores.items()})
            return selected
        except Exception:
            return X_cols[:k]

    def mutual_info_select(self, df: pd.DataFrame, X_cols: List[str], y_col: str, k: int = 10) -> List[str]:
        try:
            X = df[X_cols].fillna(0)
            y = df[y_col].fillna(df[y_col].mode()[0])
            k = min(k, len(X_cols))
            selector = SelectKBest(mutual_info_classif, k=k)
            selector.fit(X, y)
            selected = [X_cols[i] for i, s in enumerate(selector.get_support()) if s]
            scores = dict(zip(X_cols, selector.scores_))
            self._importance_scores.update({k: float(v) for k, v in scores.items()})
            return selected
        except Exception:
            return X_cols[:k]

    def lasso_select(self, df: pd.DataFrame, X_cols: List[str], y_col: str, alpha: float = 0.01) -> List[str]:
        try:
            X = df[X_cols].fillna(0)
            y = df[y_col].fillna(0)
            lasso = Lasso(alpha=alpha, max_iter=5000)
            lasso.fit(X, y)
            selected = [X_cols[i] for i, c in enumerate(lasso.coef_) if abs(c) > 1e-6]
            self._importance_scores.update({X_cols[i]: abs(float(c)) for i, c in enumerate(lasso.coef_)})
            return selected if selected else X_cols[:5]
        except Exception:
            return X_cols

    def random_forest_importance(self, df: pd.DataFrame, X_cols: List[str], y_col: str) -> Dict[str, float]:
        try:
            X = df[X_cols].fillna(0)
            y = df[y_col].fillna(df[y_col].mode()[0])
            is_classification = df[y_col].nunique() < 20
            if is_classification:
                clf = RandomForestClassifier(n_estimators=100, random_state=42)
            else:
                clf = RandomForestRegressor(n_estimators=100, random_state=42)
            clf.fit(X, y)
            importance = dict(zip(X_cols, clf.feature_importances_))
            self._importance_scores.update({k: float(v) for k, v in importance.items()})
            return {k: float(v) for k, v in sorted(importance.items(), key=lambda x: -x[1])}
        except Exception:
            return {col: 0.0 for col in X_cols}

    def xgboost_importance(self, df: pd.DataFrame, X_cols: List[str], y_col: str) -> Dict[str, float]:
        try:
            from xgboost import XGBClassifier, XGBRegressor
            from sklearn.preprocessing import LabelEncoder
            X = df[X_cols].fillna(0)
            y = df[y_col].fillna(df[y_col].mode()[0])
            is_classification = df[y_col].nunique() < 20
            if is_classification:
                le = LabelEncoder()
                y = le.fit_transform(y.astype(str))
                clf = XGBClassifier(n_estimators=100, random_state=42, eval_metric='logloss', use_label_encoder=False)
            else:
                clf = XGBRegressor(n_estimators=100, random_state=42)
            clf.fit(X, y)
            importance = dict(zip(X_cols, clf.feature_importances_))
            self._importance_scores.update({k: float(v) for k, v in importance.items()})
            return {k: float(v) for k, v in sorted(importance.items(), key=lambda x: -x[1])}
        except Exception:
            return self.random_forest_importance(df, X_cols, y_col)

    def get_importance_scores(self) -> Dict[str, float]:
        return self._importance_scores
