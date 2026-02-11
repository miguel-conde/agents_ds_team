---
description: 'Testing standards and best practices for data science projects'
applyTo: 'tests/**/*.py, src/**/*.py, **/*test*.py'
---

# Testing Standards for Data Science Projects

## Testing Philosophy

Data science testing requires a different approach than traditional software testing, focusing on:
- **Data quality and consistency** rather than just code correctness
- **Model behavior and performance** under various conditions
- **Reproducibility** across different environments and data samples
- **Statistical validity** of results and conclusions

## Test Categories

### **1. Unit Tests** (Fast, Isolated)
Test individual functions and components in isolation.

```python
# tests/test_preprocessing.py
import pytest
import pandas as pd
import numpy as np
from src.data.preprocessing import clean_data, remove_outliers

class TestDataCleaning:
    """Unit tests for data cleaning functions."""
    
    def test_clean_data_removes_null_rows(self):
        """Test that clean_data removes rows with null target values."""
        # Arrange
        df = pd.DataFrame({
            'feature1': [1, 2, 3, 4],
            'target': [0, 1, None, 1]
        })
        
        # Act
        result = clean_data(df, target_col='target')
        
        # Assert
        assert len(result) == 3
        assert result['target'].isnull().sum() == 0
    
    def test_remove_outliers_iqr_method(self):
        """Test outlier removal using IQR method."""
        # Arrange
        data = np.array([1, 2, 3, 4, 5, 100])  # 100 is outlier
        
        # Act
        result = remove_outliers(data, method='iqr')
        
        # Assert
        assert 100 not in result
        assert len(result) == 5
        
    @pytest.mark.parametrize("method,expected_length", [
        ('iqr', 5),
        ('zscore', 5), 
        ('isolation_forest', 5)
    ])
    def test_remove_outliers_methods(self, method, expected_length):
        """Test different outlier removal methods."""
        data = np.array([1, 2, 3, 4, 5, 100])
        result = remove_outliers(data, method=method)
        assert len(result) == expected_length
```

### **2. Integration Tests** (Medium Speed, Multiple Components)
Test how components work together, especially data pipelines.

```python
# tests/test_pipeline.py
import pytest
import pandas as pd
from src.data.ingestion import load_raw_data
from src.data.preprocessing import clean_data
from src.features.engineering import create_features

class TestDataPipeline:
    """Integration tests for data pipeline."""
    
    @pytest.fixture
    def sample_raw_data(self):
        """Sample raw data for testing."""
        return pd.DataFrame({
            'customer_id': [1, 2, 3, 4],
            'date': ['2023-01-01', '2023-01-02', '2023-01-01', '2023-01-03'],
            'amount': [100, 200, 150, 300],
            'target': [0, 1, 0, 1]
        })
    
    def test_full_preprocessing_pipeline(self, sample_raw_data):
        """Test complete preprocessing pipeline."""
        # Act
        cleaned = clean_data(sample_raw_data)
        featured = create_features(cleaned)
        
        # Assert
        assert featured is not None
        assert len(featured) > 0
        assert 'feature_engineered_col' in featured.columns
        
    def test_pipeline_preserves_customer_ids(self, sample_raw_data):
        """Ensure customer IDs are preserved through pipeline."""
        original_customers = set(sample_raw_data['customer_id'])
        
        # Act
        result = (sample_raw_data
                  .pipe(clean_data)
                  .pipe(create_features))
        
        # Assert
        final_customers = set(result['customer_id'])
        assert original_customers == final_customers
```

### **3. Data Quality Tests** (Validate Data Assumptions)
Test data quality and business rule compliance.

```python
# tests/test_data_quality.py
import pytest
import pandas as pd
from src.data.validation import DataQualityChecker

class TestDataQuality:
    """Data quality validation tests."""
    
    @pytest.fixture
    def quality_checker(self):
        return DataQualityChecker()
    
    def test_no_data_leakage_in_features(self, customer_features):
        """Ensure features don't contain future information."""
        feature_date = customer_features['feature_date'].max()
        target_date = customer_features['target_date'].min()
        
        # Features must be created before target event
        assert feature_date < target_date, "Data leakage detected!"
        
    def test_feature_coverage(self, feature_dataframe):
        """Test that required features have sufficient coverage."""
        required_features = ['age', 'income', 'tenure']
        
        for feature in required_features:
            coverage = 1 - feature_dataframe[feature].isnull().mean()
            assert coverage > 0.95, f"Feature {feature} has low coverage: {coverage}"
    
    def test_target_distribution(self, dataset_with_target):
        """Check target variable distribution."""
        target_ratio = dataset_with_target['target'].mean()
        
        # Business rule: churn rate should be between 5% and 30%
        assert 0.05 <= target_ratio <= 0.30, f"Unusual target distribution: {target_ratio}"
        
    def test_feature_stability(self, train_features, validation_features):
        """Test feature stability between train and validation sets."""
        from scipy.stats import ks_2samp
        
        for column in train_features.select_dtypes(include=[np.number]).columns:
            statistic, p_value = ks_2samp(
                train_features[column].dropna(),
                validation_features[column].dropna()
            )
            # Features should have similar distributions
            assert p_value > 0.05, f"Feature {column} shows distribution shift"
```

### **4. Model Tests** (Model Behavior and Performance)
Test model training, prediction, and performance.

```python
# tests/test_models.py
import pytest
import numpy as np
import pandas as pd
from sklearn.datasets import make_classification
from src.models.training import ChurnModel

class TestChurnModel:
    """Model behavior and performance tests."""
    
    @pytest.fixture
    def sample_training_data(self):
        """Generate sample classification data."""
        X, y = make_classification(
            n_samples=1000,
            n_features=10,
            n_informative=5,
            random_state=42
        )
        return pd.DataFrame(X), pd.Series(y)
    
    def test_model_trains_successfully(self, sample_training_data):
        """Test that model can be trained without errors."""
        X, y = sample_training_data
        model = ChurnModel()
        
        # Should not raise any exceptions
        model.fit(X, y)
        assert hasattr(model, 'is_fitted')
        assert model.is_fitted
        
    def test_model_predictions_are_valid_probabilities(self, sample_training_data):
        """Test prediction outputs are valid probabilities."""
        X, y = sample_training_data
        X_train, X_test = X[:800], X[800:]
        y_train = y[:800]
        
        model = ChurnModel()
        model.fit(X_train, y_train)
        predictions = model.predict_proba(X_test)
        
        # Check probability constraints
        assert np.all(predictions >= 0), "Negative probabilities found"
        assert np.all(predictions <= 1), "Probabilities > 1 found"
        assert np.allclose(predictions.sum(axis=1), 1), "Probabilities don't sum to 1"
        
    def test_model_performance_exceeds_baseline(self, sample_training_data):
        """Test model performance beats simple baseline."""
        from sklearn.model_selection import train_test_split
        from sklearn.metrics import roc_auc_score
        from sklearn.dummy import DummyClassifier
        
        X, y = sample_training_data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )
        
        # Train baseline
        baseline = DummyClassifier(strategy='stratified', random_state=42)
        baseline.fit(X_train, y_train)
        baseline_score = roc_auc_score(y_test, baseline.predict_proba(X_test)[:, 1])
        
        # Train actual model
        model = ChurnModel()
        model.fit(X_train, y_train)
        model_score = roc_auc_score(y_test, model.predict_proba(X_test)[:, 1])
        
        # Model should beat baseline
        assert model_score > baseline_score, f"Model ({model_score:.3f}) doesn't beat baseline ({baseline_score:.3f})"
        
    def test_model_reproducibility(self, sample_training_data):
        """Test that model training is reproducible."""
        X, y = sample_training_data
        
        # Train two identical models
        model1 = ChurnModel(random_state=42)
        model2 = ChurnModel(random_state=42)
        
        model1.fit(X, y)
        model2.fit(X, y)
        
        # Predictions should be identical
        pred1 = model1.predict_proba(X)
        pred2 = model2.predict_proba(X)
        
        np.testing.assert_array_almost_equal(pred1, pred2, decimal=10)
```

### **5. Statistical Tests** (Validate Assumptions)
Test statistical assumptions and hypothesis testing.

```python
# tests/test_statistics.py
import pytest
import numpy as np
from scipy import stats
from src.analysis.statistical_tests import perform_ab_test

class TestStatisticalValidation:
    """Statistical assumption and test validation."""
    
    def test_ab_test_power_analysis(self):
        """Test A/B test has sufficient power."""
        # Generate test data with known effect
        np.random.seed(42)
        control = np.random.normal(0.1, 0.02, 1000)  # 10% conversion
        treatment = np.random.normal(0.12, 0.02, 1000)  # 12% conversion
        
        result = perform_ab_test(control, treatment)
        
        # Should detect the 2 percentage point difference
        assert result['p_value'] < 0.05
        assert result['effect_size'] > 0
        assert result['power'] > 0.8
        
    def test_normality_assumption(self, continuous_feature_data):
        """Test normality assumption for statistical tests."""
        # Test for normality (may need transformation if fails)
        statistic, p_value = stats.normaltest(continuous_feature_data)
        
        if p_value < 0.05:
            # Data is not normal, suggest transformation
            log_transformed = np.log(continuous_feature_data + 1)
            log_stat, log_p = stats.normaltest(log_transformed)
            
            # Log transformation should improve normality
            assert log_p > p_value, "Log transformation didn't improve normality"
            
    def test_feature_correlation_assumptions(self, feature_matrix):
        """Test multicollinearity assumptions."""
        correlation_matrix = feature_matrix.corr().abs()
        
        # Check for high correlations (excluding diagonal)
        np.fill_diagonal(correlation_matrix.values, 0)
        max_correlation = correlation_matrix.max().max()
        
        assert max_correlation < 0.95, f"High correlation detected: {max_correlation}"
```

## Test Configuration

### **pytest Configuration** (pytest.ini)
```ini
[tool:pytest]
addopts = 
    --strict-markers
    --disable-warnings
    --tb=short
    --cov=src
    --cov-report=term-missing
    --cov-report=html
    --cov-fail-under=80

markers =
    slow: marks tests as slow (deselect with '-m "not slow"')
    integration: marks tests as integration tests
    unit: marks tests as unit tests
    data_quality: marks tests as data quality validation
    model: marks tests as model validation

testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
```

### **Test Fixtures** (conftest.py)
```python
# tests/conftest.py
import pytest
import pandas as pd
import numpy as np

@pytest.fixture(scope="session")
def sample_dataset():
    """Sample dataset for testing."""
    np.random.seed(42)
    return pd.DataFrame({
        'customer_id': range(1000),
        'age': np.random.randint(18, 80, 1000),
        'income': np.random.normal(50000, 15000, 1000),
        'tenure_months': np.random.randint(1, 60, 1000),
        'target': np.random.binomial(1, 0.2, 1000)
    })

@pytest.fixture
def trained_model():
    """Pre-trained model for testing."""
    from src.models.training import ChurnModel
    from sklearn.datasets import make_classification
    
    X, y = make_classification(n_samples=1000, random_state=42)
    model = ChurnModel()
    model.fit(pd.DataFrame(X), pd.Series(y))
    return model

@pytest.fixture
def mock_database_connection():
    """Mock database connection for testing."""
    class MockConnection:
        def execute(self, query):
            return pd.DataFrame({'result': [1, 2, 3]})
    
    return MockConnection()
```

## Test Data Management

### **Test Data Strategy**
```python
# tests/test_data/generate_test_data.py
"""Generate deterministic test datasets."""

def create_churn_dataset(n_samples=1000, random_state=42):
    """Create synthetic churn dataset for testing."""
    np.random.seed(random_state)
    
    # Create correlated features
    age = np.random.normal(40, 12, n_samples)
    income = 30000 + age * 1000 + np.random.normal(0, 5000, n_samples) 
    tenure = np.random.exponential(24, n_samples)
    
    # Create target with realistic relationships  
    churn_prob = 1 / (1 + np.exp(-(
        -2 + 
        0.05 * (age - 40) +
        -0.00003 * (income - 50000) + 
        -0.1 * tenure +
        np.random.normal(0, 0.5, n_samples)
    )))
    
    target = np.random.binomial(1, churn_prob, n_samples)
    
    return pd.DataFrame({
        'customer_id': range(n_samples),
        'age': age.clip(18, 80),
        'income': income.clip(20000, 200000),
        'tenure_months': tenure.clip(1, 120),
        'churn': target
    })
```

### **Property-Based Testing**
```python
# Use hypothesis for property-based testing
from hypothesis import given, strategies as st
import hypothesis.extra.pandas as pdst

@given(df=pdst.data_frames([
    pdst.column('amount', dtype=float),
    pdst.column('quantity', dtype=int, elements=st.integers(min_value=1, max_value=100))
]))
def test_total_calculation_properties(df):
    """Property-based test for total calculation."""
    df['total'] = df['amount'] * df['quantity']
    
    # Properties that should always hold
    assert (df['total'] >= 0).all(), "Total should never be negative"
    assert df['total'].notna().all(), "Total should never be NaN"
    
    # If amount or quantity is zero, total should be zero
    zero_mask = (df['amount'] == 0) | (df['quantity'] == 0)
    assert (df.loc[zero_mask, 'total'] == 0).all()
```

## Performance Testing

### **Memory and Speed Tests**
```python
# tests/test_performance.py
import pytest
import time
import psutil
import pandas as pd

def test_preprocessing_performance():
    """Test preprocessing completes within time limit."""
    large_dataset = pd.DataFrame({
        'feature': range(100000),
        'target': [0, 1] * 50000
    })
    
    start_time = time.time()
    result = preprocess_data(large_dataset)
    end_time = time.time()
    
    # Should complete within 30 seconds
    assert (end_time - start_time) < 30
    assert len(result) > 0

def test_memory_usage():
    """Test memory usage stays within limits."""
    process = psutil.Process()
    initial_memory = process.memory_info().rss / 1024 / 1024  # MB
    
    # Perform memory-intensive operation
    large_dataset = pd.DataFrame(np.random.randn(100000, 100))
    processed = some_memory_intensive_function(large_dataset)
    
    final_memory = process.memory_info().rss / 1024 / 1024  # MB
    memory_increase = final_memory - initial_memory
    
    # Should not use more than 500MB additional memory
    assert memory_increase < 500
```

## Continuous Testing

### **Pre-commit Hooks** (.pre-commit-config.yaml)
```yaml
repos:
  - repo: local
    hooks:
      - id: pytest-unit
        name: pytest-unit
        entry: pytest tests/ -m "not slow"
        language: system
        pass_filenames: false
        always_run: true
        
      - id: pytest-data-quality
        name: pytest-data-quality
        entry: pytest tests/ -m "data_quality"
        language: system
        pass_filenames: false
        always_run: true
```

### **GitHub Actions CI** (.github/workflows/test.yml)
```yaml
name: Test Suite
on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: [3.8, 3.9, "3.10"]
        
    steps:
    - uses: actions/checkout@v3
    - name: Set up Python
      uses: actions/setup-python@v3
      with:
        python-version: ${{ matrix.python-version }}
        
    - name: Install dependencies
      run: |
        pip install -r requirements.txt
        pip install -r requirements-dev.txt
        
    - name: Run unit tests
      run: pytest tests/ -m "unit" --cov=src
      
    - name: Run integration tests
      run: pytest tests/ -m "integration"
      
    - name: Run data quality tests
      run: pytest tests/ -m "data_quality"
```

## Best Practices Summary

### **Test Structure**
- **AAA Pattern**: Arrange, Act, Assert
- **Descriptive names**: `test_should_remove_outliers_when_iqr_method_used`
- **One assertion per test** when possible
- **Independent tests** that can run in any order

### **Data Science Specific**
- **Test data pipelines end-to-end** to catch integration issues
- **Validate statistical assumptions** before applying methods
- **Test model reproducibility** with fixed random seeds
- **Use property-based testing** for mathematical invariants
- **Mock external dependencies** (databases, APIs) for unit tests

### **Performance Considerations**
- **Fast unit tests** (< 1 second each)
- **Separate slow integration tests** with appropriate markers
- **Use test fixtures** to avoid repeated setup
- **Profile memory usage** for large dataset operations

This testing framework ensures our data science code is reliable, maintainable, and produces consistent results across different environments and data conditions.