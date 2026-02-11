---
description: 'Python coding standards and best practices for data science projects'
applyTo: '**/*.py'
---

# Python Coding Standards for Data Science

## Code Quality Standards

### **1. Code Formatting & Style**
- Use **Black** for automatic code formatting (`black --line-length 88`)
- Follow **PEP 8** conventions with exceptions for data science contexts
- Use **isort** for import organization (`isort --profile black`)
- Maximum line length: **88 characters** (Black default)

### **2. Import Organization**
```python
# Standard library imports
import os
import sys
from datetime import datetime, timedelta
from pathlib import Path

# Third-party imports  
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report

# Local application imports
from src.data.preprocessing import clean_data
from src.features.engineering import create_features
from src.models.training import train_model
```

### **3. Naming Conventions**
```python
# Variables and functions: snake_case
customer_data = pd.read_csv("customers.csv")
def calculate_churn_probability(features):
    pass

# Classes: PascalCase
class CustomerChurnModel:
    pass

# Constants: UPPER_SNAKE_CASE
MAX_FEATURES = 100
DEFAULT_MODEL_PATH = "models/production/"

# Private methods: leading underscore
def _validate_input_data(data):
    pass
```

## Data Science Specific Guidelines

### **1. Pandas Best Practices**
```python
# ✅ Efficient data operations
# Use vectorized operations instead of loops
df["new_col"] = df["col1"] * df["col2"]  # Good
df["new_col"] = "default"  # Initialize
df.loc[df["condition"], "new_col"] = df["col1"] * 2  # Conditional assignment

# ✅ Memory efficient data types
df["category_col"] = df["category_col"].astype("category")
df["int_col"] = pd.to_numeric(df["int_col"], downcast="integer")

# ✅ Explicit column selection
features = ["feature1", "feature2", "feature3"]
X = df[features].copy()  # Explicit and reproducible

# ❌ Avoid chained operations that can be ambiguous
# df[df["col"] > 0]["new_col"] = "value"  # Bad
df.loc[df["col"] > 0, "new_col"] = "value"  # Good
```

### **2. NumPy Best Practices**
```python
# ✅ Use appropriate data types
X = np.array(data, dtype=np.float32)  # Explicit dtype
mask = np.array(conditions, dtype=np.bool_)

# ✅ Vectorized operations
result = np.where(condition, value_if_true, value_if_false)
normalized = (X - X.mean()) / X.std()

# ✅ Random seed management
np.random.seed(42)  # Set seed for reproducibility
rng = np.random.RandomState(42)  # Local random state
```

### **3. Scikit-learn Patterns**
```python
# ✅ Consistent transformer patterns
from sklearn.base import BaseEstimator, TransformerMixin

class CustomTransformer(BaseEstimator, TransformerMixin):
    def __init__(self, feature_name):
        self.feature_name = feature_name
        
    def fit(self, X, y=None):
        # Store parameters during fit
        self.mean_ = X[self.feature_name].mean()
        return self
    
    def transform(self, X):
        # Apply transformation
        X_transformed = X.copy()
        X_transformed[f"{self.feature_name}_normalized"] = (
            X[self.feature_name] - self.mean_
        )
        return X_transformed

# ✅ Pipeline usage
from sklearn.pipeline import Pipeline

pipeline = Pipeline([
    ('imputer', SimpleImputer(strategy='mean')),
    ('scaler', StandardScaler()),
    ('model', LogisticRegression(random_state=42))
])
```

## Error Handling & Logging

### **1. Exception Handling**
```python
import logging
from typing import Optional, Union

logger = logging.getLogger(__name__)

def load_and_clean_data(file_path: str) -> pd.DataFrame:
    """Load and clean data with proper error handling."""
    try:
        df = pd.read_csv(file_path)
        logger.info(f"Loaded {len(df)} rows from {file_path}")
        
        # Data validation
        if df.empty:
            raise ValueError("Dataset is empty")
        
        required_columns = ["customer_id", "target"]
        missing_columns = [col for col in required_columns if col not in df.columns]
        if missing_columns:
            raise ValueError(f"Missing required columns: {missing_columns}")
            
        return df
        
    except FileNotFoundError:
        logger.error(f"File not found: {file_path}")
        raise
    except pd.errors.EmptyDataError:
        logger.error(f"Empty data file: {file_path}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error loading data: {e}")
        raise
```

### **2. Logging Configuration**
```python
import logging
from pathlib import Path

def setup_logging(log_level: str = "INFO") -> None:
    """Configure logging for data science projects."""
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)
    
    logging.basicConfig(
        level=getattr(logging, log_level.upper()),
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[
            logging.FileHandler(log_dir / "experiment.log"),
            logging.StreamHandler()
        ]
    )

# Usage in scripts
logger = logging.getLogger(__name__)
logger.info("Starting model training")
logger.warning("Low data quality detected")
logger.error("Model training failed")
```

## Type Hints & Documentation

### **1. Type Annotations**
```python
from typing import Dict, List, Optional, Tuple, Union
import pandas as pd
import numpy as np

def calculate_feature_importance(
    model: Union["RandomForestClassifier", "GradientBoostingClassifier"],
    feature_names: List[str],
    top_k: Optional[int] = 10
) -> Dict[str, float]:
    """Calculate and return top k feature importances."""
    importances = dict(zip(feature_names, model.feature_importances_))
    sorted_features = dict(
        sorted(importances.items(), key=lambda x: x[1], reverse=True)
    )
    return dict(list(sorted_features.items())[:top_k]) if top_k else sorted_features

def create_train_test_split(
    data: pd.DataFrame,
    target_col: str,
    test_size: float = 0.2,
    random_state: int = 42
) -> Tuple[pd.DataFrame, pd.DataFrame, pd.Series, pd.Series]:
    """Create train/test split with proper typing."""
    X = data.drop(columns=[target_col])
    y = data[target_col]
    return train_test_split(X, y, test_size=test_size, random_state=random_state)
```

### **2. Docstring Standards**
```python
def engineer_features(
    df: pd.DataFrame,
    date_col: str = "date",
    customer_col: str = "customer_id"
) -> pd.DataFrame:
    """
    Engineer features for customer churn prediction.
    
    Creates time-based features including recency, frequency, and monetary
    features as well as temporal aggregations.
    
    Parameters
    ----------
    df : pd.DataFrame
        Raw customer transaction data with columns: customer_id, date, amount
    date_col : str, default 'date'
        Name of the date column for temporal features
    customer_col : str, default 'customer_id' 
        Name of the customer identifier column
        
    Returns
    -------
    pd.DataFrame
        Feature engineered dataset with additional columns:
        - days_since_last_purchase
        - total_purchases_30d
        - avg_purchase_amount
        
    Examples
    --------
    >>> transactions = pd.DataFrame({
    ...     'customer_id': [1, 1, 2],
    ...     'date': ['2023-01-01', '2023-01-15', '2023-01-10'],
    ...     'amount': [100, 50, 200]
    ... })
    >>> features = engineer_features(transactions)
    >>> 'days_since_last_purchase' in features.columns
    True
    
    Notes
    -----
    This function assumes the date column can be parsed by pd.to_datetime().
    Missing values in the amount column will be filled with 0.
    """
    # Implementation here
    pass
```

## Performance & Memory Optimization

### **1. Memory Efficient Operations**
```python
# ✅ Memory efficient data loading
def load_large_dataset(file_path: str, chunk_size: int = 10000) -> pd.DataFrame:
    """Load large dataset in chunks to manage memory."""
    chunks = []
    for chunk in pd.read_csv(file_path, chunksize=chunk_size):
        # Process chunk
        processed_chunk = process_chunk(chunk)
        chunks.append(processed_chunk)
    return pd.concat(chunks, ignore_index=True)

# ✅ Data type optimization
def optimize_dtypes(df: pd.DataFrame) -> pd.DataFrame:
    """Optimize DataFrame dtypes for memory efficiency."""
    df_optimized = df.copy()
    
    # Convert object columns to category if low cardinality
    for col in df_optimized.select_dtypes(include=['object']).columns:
        if df_optimized[col].nunique() / len(df_optimized) < 0.5:
            df_optimized[col] = df_optimized[col].astype('category')
    
    # Downcast integers
    for col in df_optimized.select_dtypes(include=['int64']).columns:
        df_optimized[col] = pd.to_numeric(df_optimized[col], downcast='integer')
    
    return df_optimized
```

### **2. Vectorized Operations**
```python
# ✅ Use vectorized operations instead of loops
def calculate_rfm_features(df: pd.DataFrame) -> pd.DataFrame:
    """Calculate RFM features using vectorized operations."""
    current_date = df['date'].max()
    
    # Recency: vectorized date operations
    df['days_since_last_purchase'] = (current_date - df['date']).dt.days
    
    # Frequency: vectorized groupby operations  
    frequency = df.groupby('customer_id')['transaction_id'].count()
    df['frequency'] = df['customer_id'].map(frequency)
    
    # Monetary: vectorized aggregations
    monetary = df.groupby('customer_id')['amount'].sum()
    df['monetary'] = df['customer_id'].map(monetary)
    
    return df
```

## Configuration Management

### **1. Configuration Files**
```python
# config.py
from dataclasses import dataclass
from pathlib import Path

@dataclass
class DataConfig:
    """Data processing configuration."""
    raw_data_path: Path = Path("data/raw")
    processed_data_path: Path = Path("data/processed")
    feature_store_path: Path = Path("data/features")
    
@dataclass  
class ModelConfig:
    """Model training configuration."""
    model_type: str = "random_forest"
    random_state: int = 42
    test_size: float = 0.2
    cv_folds: int = 5
    
@dataclass
class Config:
    """Main configuration class."""
    data: DataConfig = DataConfig()
    model: ModelConfig = ModelConfig()
    
# Usage
config = Config()
df = pd.read_csv(config.data.raw_data_path / "customers.csv")
```

### **2. Environment Variables**
```python
import os
from pathlib import Path

# Environment configuration
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///default.db")
MODEL_REGISTRY_PATH = Path(os.getenv("MODEL_REGISTRY_PATH", "models/"))
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

# Feature flags
ENABLE_FEATURE_X = os.getenv("ENABLE_FEATURE_X", "false").lower() == "true"
```

## Code Organization

### **1. Project Structure**
```
src/
├── __init__.py
├── data/
│   ├── __init__.py
│   ├── ingestion.py      # Data loading functions
│   └── preprocessing.py   # Cleaning and validation
├── features/
│   ├── __init__.py
│   ├── engineering.py    # Feature creation
│   └── selection.py      # Feature selection
├── models/
│   ├── __init__.py
│   ├── training.py       # Model training
│   ├── evaluation.py     # Model evaluation  
│   └── prediction.py     # Inference
└── utils/
    ├── __init__.py
    ├── logging.py        # Logging utilities
    └── validation.py     # Input validation
```

### **2. Module Organization**
```python
# features/engineering.py
"""Feature engineering utilities and transformers."""

__all__ = ["create_features", "FeatureEngineer", "validate_features"]

from .core import create_features
from .transformers import FeatureEngineer  
from .validation import validate_features
```

## Common Anti-Patterns to Avoid

### **❌ Don't Do This:**
```python
# Hardcoded values
df = pd.read_csv("/home/user/data/file.csv")  # Use config
model = RandomForestClassifier(n_estimators=100)  # Use parameters

# Unclear variable names
df1 = data.groupby("customer").sum()  # Use descriptive names
X = df[cols]  # What are 'cols'?

# No error handling
result = some_risky_operation()  # Can fail silently

# Mutable default arguments
def process_data(data, columns=[]):  # Creates bugs
    columns.append("new_col")
```

### **✅ Do This Instead:**
```python
# Configurable paths
config = load_config()
df = pd.read_csv(config.data.raw_data_path / "customer_data.csv")

# Clear variable names and parameters
customer_aggregates = customer_data.groupby("customer_id").sum()
feature_columns = ["age", "income", "tenure"]
X = df[feature_columns].copy()

# Proper error handling
try:
    result = some_risky_operation()
except SpecificError as e:
    logger.error(f"Operation failed: {e}")
    raise

# Immutable defaults
def process_data(data, columns: Optional[List[str]] = None) -> pd.DataFrame:
    if columns is None:
        columns = ["default_column"]
```

These Python standards ensure our data science code is maintainable, reproducible, and follows industry best practices for production deployment.