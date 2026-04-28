"""
IDCFSS - Unit Tests
Tests for all backend modules.
"""
import pytest
import pandas as pd
import numpy as np
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

from modules.profiler import DataProfiler
from modules.missing_handler import MissingValueHandler
from modules.outlier_detector import OutlierDetector
from modules.encoder import CategoricalEncoder
from modules.scaler import FeatureScaler
from modules.feature_selector import FeatureSelector
from modules.pipeline_exporter import PipelineExporter


@pytest.fixture
def sample_df():
    np.random.seed(42)
    return pd.DataFrame({
        'age': [25, 30, np.nan, 45, 50, 22, np.nan, 35, 40, 28],
        'salary': [50000, 60000, 55000, 70000, 200000, 45000, 52000, 65000, 72000, 48000],
        'city': ['NYC', 'LA', 'NYC', 'CHI', 'LA', 'NYC', 'CHI', 'LA', 'NYC', 'CHI'],
        'gender': ['M', 'F', 'M', 'F', 'M', 'F', 'M', 'F', 'M', 'F'],
        'target': [1, 0, 1, 0, 1, 0, 1, 0, 1, 0],
    })


class TestDataProfiler:
    def test_profile_shape(self, sample_df):
        profiler = DataProfiler(sample_df)
        profile = profiler.get_profile()
        assert profile['shape']['rows'] == 10
        assert profile['shape']['cols'] == 5

    def test_missing_detection(self, sample_df):
        profiler = DataProfiler(sample_df)
        profile = profiler.get_profile()
        assert profile['columns']['age']['missing'] == 2
        assert profile['columns']['salary']['missing'] == 0

    def test_quality_score_range(self, sample_df):
        profiler = DataProfiler(sample_df)
        profile = profiler.get_profile()
        assert 0 <= profile['quality_score'] <= 100

    def test_inferred_types(self, sample_df):
        profiler = DataProfiler(sample_df)
        profile = profiler.get_profile()
        assert profile['columns']['age']['inferred_type'] == 'numeric'
        assert profile['columns']['city']['inferred_type'] == 'categorical'

    def test_outlier_count(self, sample_df):
        profiler = DataProfiler(sample_df)
        profile = profiler.get_profile()
        assert profile['columns']['salary']['outlier_count'] >= 0

    def test_empty_dataframe(self):
        df = pd.DataFrame({'a': [], 'b': []})
        profiler = DataProfiler(df)
        profile = profiler.get_profile()
        assert profile['shape']['rows'] == 0


class TestMissingValueHandler:
    def test_impute_mean(self, sample_df):
        handler = MissingValueHandler()
        result = handler.impute_mean(sample_df, 'age')
        assert result['age'].isnull().sum() == 0

    def test_impute_median(self, sample_df):
        handler = MissingValueHandler()
        result = handler.impute_median(sample_df, 'age')
        assert result['age'].isnull().sum() == 0

    def test_impute_mode(self, sample_df):
        handler = MissingValueHandler()
        result = handler.impute_mode(sample_df, 'city')
        assert result['city'].isnull().sum() == 0

    def test_forward_fill(self, sample_df):
        handler = MissingValueHandler()
        result = handler.fill_forward(sample_df, 'age')
        assert result['age'].iloc[2] == 30.0  # filled from previous

    def test_apply_strategy(self, sample_df):
        handler = MissingValueHandler()
        result = handler.apply_strategy(sample_df, 'age', 'median')
        assert result['age'].isnull().sum() == 0

    def test_detect(self, sample_df):
        handler = MissingValueHandler()
        missing = handler.detect(sample_df)
        assert 'age' in missing
        assert missing['age'] == 2


class TestOutlierDetector:
    def test_detect_iqr(self, sample_df):
        detector = OutlierDetector()
        outliers = detector.detect_iqr(sample_df, 'salary')
        assert isinstance(outliers, list)

    def test_detect_zscore(self, sample_df):
        detector = OutlierDetector()
        outliers = detector.detect_zscore(sample_df, 'salary')
        assert isinstance(outliers, list)

    def test_cap_outliers(self, sample_df):
        detector = OutlierDetector()
        result = detector.cap_outliers(sample_df, 'salary')
        assert result['salary'].max() <= sample_df['salary'].max()

    def test_remove_outliers(self, sample_df):
        detector = OutlierDetector()
        outliers = detector.detect_iqr(sample_df, 'salary')
        if outliers:
            result = detector.remove_outliers(sample_df, outliers)
            assert len(result) < len(sample_df)

    def test_apply_strategy_cap(self, sample_df):
        detector = OutlierDetector()
        result = detector.apply_strategy(sample_df, 'salary', detect_method='iqr', action='cap')
        assert len(result) == len(sample_df)


class TestCategoricalEncoder:
    def test_label_encode(self, sample_df):
        encoder = CategoricalEncoder()
        result = encoder.label_encode(sample_df, 'city')
        assert pd.api.types.is_numeric_dtype(result['city']) or result['city'].apply(lambda x: isinstance(x, (int, float, np.integer, np.floating)) or pd.isna(x)).all()

    def test_onehot_encode(self, sample_df):
        encoder = CategoricalEncoder()
        result = encoder.onehot_encode(sample_df, ['gender'])
        assert 'gender' not in result.columns
        assert any('gender_' in c for c in result.columns)

    def test_binary_encode(self, sample_df):
        encoder = CategoricalEncoder()
        result = encoder.binary_encode(sample_df, 'city')
        assert 'city' not in result.columns
        assert any('city_bin_' in c for c in result.columns)

    def test_encoding_map(self, sample_df):
        encoder = CategoricalEncoder()
        encoder.label_encode(sample_df, 'city')
        assert 'city' in encoder.get_encoding_map()


class TestFeatureScaler:
    def test_standard_scale(self, sample_df):
        scaler = FeatureScaler()
        result = scaler.standard_scale(sample_df, ['age', 'salary'])
        assert abs(result['salary'].mean()) < 0.5

    def test_minmax_scale(self, sample_df):
        scaler = FeatureScaler()
        df = sample_df.fillna(0)
        result = scaler.minmax_scale(df, ['salary'])
        assert result['salary'].min() >= -0.01
        assert result['salary'].max() <= 1.01

    def test_robust_scale(self, sample_df):
        scaler = FeatureScaler()
        result = scaler.robust_scale(sample_df, ['salary'])
        assert 'salary' in result.columns


class TestFeatureSelector:
    def test_random_forest_importance(self, sample_df):
        df = sample_df.dropna()
        selector = FeatureSelector()
        importance = selector.random_forest_importance(df, ['age', 'salary'], 'target')
        assert isinstance(importance, dict)
        assert len(importance) == 2

    def test_correlation_filter(self, sample_df):
        selector = FeatureSelector()
        kept = selector.correlation_filter(sample_df.dropna())
        assert isinstance(kept, list)

    def test_variance_threshold(self, sample_df):
        selector = FeatureSelector()
        kept = selector.variance_threshold(sample_df.dropna())
        assert isinstance(kept, list)


class TestPipelineExporter:
    def test_add_step(self):
        exporter = PipelineExporter()
        exporter.add_step("missing", "median", ["age"])
        assert len(exporter.steps) == 1

    def test_to_json(self):
        exporter = PipelineExporter()
        exporter.add_step("missing", "median", ["age"])
        json_str = exporter.to_json()
        assert '"pipeline"' in json_str

    def test_to_python_code(self):
        exporter = PipelineExporter()
        exporter.add_step("missing", "median", ["age"])
        exporter.add_step("scaling", "standard", ["age", "salary"])
        code = exporter.to_python_code()
        assert "def preprocess" in code
        assert "fillna" in code


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
