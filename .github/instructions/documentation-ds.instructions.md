---
description: 'Documentation standards and best practices for data science projects'
applyTo: '**/*.{md,qmd,rst}, docs/**, notebooks/**/*.ipynb'
---

# Documentation Standards for Data Science Projects

## Documentation Philosophy

Data science documentation serves multiple audiences and purposes:
- **Technical stakeholders** need implementation details and reproducibility instructions
- **Business stakeholders** need insights, methodology, and business impact
- **Future team members** need context, decisions made, and lessons learned
- **Regulatory/compliance** needs audit trails and validation evidence

## Documentation Structure

### **1. Project-Level Documentation**

#### **README.md** (Project Overview)
```markdown
# Customer Churn Prediction

## Business Problem
Predict customer churn with 90%+ precision to enable proactive retention campaigns.

## Solution Approach
- **Model**: Random Forest classifier with customer behavioral features
- **Performance**: 85% AUC, 92% precision at 10% recall 
- **Impact**: Reduces churn by 15%, saving $2.1M annually

## Quick Start
```bash
# Setup environment
pip install -r requirements.txt

# Train model
python src/models/train.py

# Generate predictions  
python src/models/predict.py --input data/new_customers.csv
```

## Project Structure
```
├── data/
│   ├── raw/           # Original, immutable data
│   ├── processed/     # Cleaned and transformed data
│   └── features/      # Feature store outputs
├── models/            # Trained model artifacts
├── notebooks/         # Exploratory analysis
├── src/              # Source code
└── docs/             # Detailed documentation
```

## Key Results
- **Baseline Performance**: 65% AUC (logistic regression)
- **Final Performance**: 85% AUC (random forest)
- **Business Metrics**: 92% precision, 15% churn reduction
- **Production Status**: Deployed, monitoring active

## Team & Contact
- **Data Scientist**: [Name] - Model development and validation
- **ML Engineer**: [Name] - Production deployment and monitoring
- **Business Owner**: [Name] - Requirements and impact measurement
```

#### **METADATA.md** (Technical Specifications)
```markdown
# Project Metadata

## Data Sources
| Source | Description | Update Frequency | Owner |
|--------|-------------|------------------|-------|
| CRM Database | Customer profiles | Daily | Marketing |
| Transaction DB | Purchase history | Real-time | Finance |
| Support Tickets | Customer service interactions | Daily | Support |

## Model Specifications
- **Algorithm**: Random Forest Classifier
- **Features**: 47 engineered features (demographic, behavioral, temporal)
- **Training Data**: 2020-01-01 to 2023-06-30 (856K customers)
- **Validation Strategy**: Time-based split with 6-month holdout
- **Performance Metrics**: AUC=0.85, Precision@10%=0.92

## Infrastructure
- **Training**: AWS EC2 (4x xlarge instances)
- **Serving**: AWS SageMaker Endpoint (2x medium instances)  
- **Monitoring**: CloudWatch + Custom Dashboards
- **Data Storage**: S3 (raw), Redshift (processed), RDS (metadata)

## Compliance & Governance
- **Data Privacy**: GDPR compliant, PII anonymized
- **Model Validation**: Independent validation by DS team
- **Audit Trail**: MLflow experiment tracking
- **Access Control**: Role-based permissions (IAM)
```

### **2. Code Documentation**

#### **Docstrings** (NumPy Style)
```python
def calculate_customer_lifetime_value(
    transaction_data: pd.DataFrame,
    customer_id: str,
    prediction_horizon_days: int = 365
) -> float:
    """
    Calculate predicted customer lifetime value.
    
    Computes CLV using historical transaction patterns and churn probability.
    Uses RFM features and applies time-decay weighting for recent behavior.
    
    Parameters
    ----------
    transaction_data : pd.DataFrame
        Customer transaction history with columns:
        - customer_id: str, unique customer identifier
        - transaction_date: datetime, transaction timestamp  
        - amount: float, transaction amount in USD
        - product_category: str, purchased product category
    customer_id : str
        Target customer identifier for CLV calculation
    prediction_horizon_days : int, default 365
        Number of days to predict CLV over
        
    Returns
    -------
    float
        Predicted customer lifetime value in USD
        
    Examples
    --------
    >>> transactions = pd.DataFrame({
    ...     'customer_id': ['C001', 'C001', 'C002'],
    ...     'transaction_date': pd.to_datetime(['2023-01-01', '2023-02-01', '2023-01-15']),
    ...     'amount': [100.0, 250.0, 75.0],
    ...     'product_category': ['Electronics', 'Clothing', 'Books']
    ... })
    >>> clv = calculate_customer_lifetime_value(transactions, 'C001')
    >>> isinstance(clv, float) and clv > 0
    True
    
    Notes
    -----
    CLV calculation methodology:
    1. Extract RFM features from transaction history
    2. Apply churn probability model to estimate retention
    3. Project future transaction value using trend analysis
    4. Apply time-decay discount rate of 10% annually
    
    Assumptions:
    - Transaction patterns are indicative of future behavior
    - Churn model accuracy of 85% AUC applies to prediction horizon
    - Economic conditions remain stable during prediction period
    
    References
    ----------
    [1] Kumar, V., & Reinartz, W. (2016). Creating Enduring Customer Value.
    [2] Fader, P. S., & Hardie, B. G. (2020). Customer lifetime value modeling.
    """
```

#### **Module Documentation**
```python
"""
Customer segmentation and lifetime value analysis.

This module provides functions for:
- RFM (Recency, Frequency, Monetary) analysis
- Customer segmentation using clustering algorithms
- Lifetime value prediction and ranking
- Cohort analysis and retention metrics

Key Classes
-----------
CustomerSegmenter : sklearn-compatible transformer
    Segments customers using RFM features and K-means clustering
    
CLVPredictor : sklearn-compatible estimator
    Predicts customer lifetime value using ensemble methods
    
Functions
---------
calculate_rfm_features : Extract RFM features from transaction data
plot_segments : Visualize customer segments and characteristics
validate_clv_predictions : Validate CLV predictions against business metrics

Examples
--------
Basic usage for customer segmentation:

>>> from src.analysis.segmentation import CustomerSegmenter
>>> segmenter = CustomerSegmenter(n_segments=5)
>>> segments = segmenter.fit_transform(customer_features)
>>> segments['segment_name'].value_counts()
Champions      1250
Loyal          980
At Risk        654
New            423
Lost           193

Dependencies
------------
- pandas >= 1.3.0
- scikit-learn >= 1.0.0  
- numpy >= 1.21.0
- matplotlib >= 3.3.0

See Also
--------
src.features.rfm : RFM feature engineering utilities
src.models.clv : CLV prediction model implementations
"""
```

### **3. Analysis Documentation**

#### **Jupyter Notebooks** (Structured Analysis)
```markdown
# Customer Churn Analysis - Exploratory Data Analysis

## Executive Summary
- **Dataset**: 856K customers, 2020-2023 transaction history
- **Key Finding**: Churn rate increases 3x after 6+ months without purchase
- **Recommendation**: Implement 4-month re-engagement campaign
- **Next Steps**: Feature engineering based on temporal patterns

## 1. Business Context

### Problem Definition
Current customer retention strategy lacks predictive targeting, resulting in:
- 23% annual churn rate (industry benchmark: 18%)
- $3.2M revenue loss from preventable churn
- Inefficient marketing spend on low-risk customers

### Success Criteria
- Predict churn with 90%+ precision at 10% recall
- Identify top 20% at-risk customers for intervention
- Reduce overall churn rate by 15% within 6 months
```

#### **Analysis Structure Template**
```markdown
# Analysis Template

## 1. Objective & Hypotheses
**Primary Objective**: [Clear statement of what you're analyzing]

**Hypotheses**: 
- H1: [Testable hypothesis with expected direction]
- H2: [Alternative hypothesis]
- H0: [Null hypothesis]

## 2. Data Description
**Source**: [Data origin and collection method]
**Time Period**: [Date range of analysis]
**Sample Size**: [Number of observations]
**Key Variables**: [Main variables of interest]

## 3. Methodology
**Statistical Methods**: [Tests and techniques used]
**Validation Approach**: [How results will be validated]
**Assumptions**: [Key assumptions and their validation]
**Limitations**: [Known constraints and biases]

## 4. Results

### 4.1 Descriptive Statistics
[Tables and charts showing data distributions]

### 4.2 Statistical Tests
[Hypothesis test results with p-values and effect sizes]

### 4.3 Model Performance
[Validation metrics and comparison to baselines]

## 5. Interpretation

### 5.1 Business Implications
[What the results mean for business decisions]

### 5.2 Statistical Significance
[Confidence in results and practical significance]

### 5.3 Limitations & Caveats
[Important limitations and uncertainty]

## 6. Recommendations

### 6.1 Immediate Actions
[High-confidence recommendations for implementation]

### 6.2 Further Investigation
[Areas needing additional analysis]

### 6.3 Monitoring Plan
[How to track success and detect issues]

## 7. Appendix
- **Code**: [Analysis code and reproducibility instructions]
- **Detailed Results**: [Full statistical output]
- **Data Quality**: [Data validation and cleaning notes]
```

### **4. Model Documentation**

#### **Model Cards** (Model Documentation Standard)
```markdown
# Model Card: Customer Churn Prediction

## Model Details
- **Model Name**: CustomerChurnClassifier_v2.1
- **Model Type**: Random Forest Classifier  
- **Version**: 2.1 (Production)
- **Date**: 2023-12-15
- **Owner**: Data Science Team
- **License**: Internal Use Only

## Intended Use
- **Primary Use**: Predict customer churn probability for retention campaigns
- **Intended Users**: Marketing team, customer success managers
- **Out-of-Scope Uses**: Not for credit decisions, legal determinations, or individual-level automated decisions

## Training Data
- **Dataset**: Customer behavioral data, 2020-2023
- **Size**: 856,432 customers, 47 features
- **Sampling**: All active customers as of training date
- **Preprocessing**: Missing value imputation, categorical encoding, feature scaling

## Performance Metrics

### Overall Performance
- **AUC-ROC**: 0.847 (95% CI: 0.841-0.853)
- **Precision@10%**: 0.916 (targeting top 10% risk scores)
- **Recall@10%**: 0.087 (captures 8.7% of actual churners)
- **Baseline Comparison**: +18 percentage points over logistic regression

### Performance by Subgroup
| Segment | AUC | Precision@10% | Count |
|---------|-----|---------------|-------|
| New Customers (< 6 months) | 0.823 | 0.892 | 156K |
| Established (6-24 months) | 0.856 | 0.924 | 445K |
| Long-term (> 24 months) | 0.871 | 0.931 | 255K |
| High Value (top 20%) | 0.879 | 0.945 | 171K |
| Geographic - Urban | 0.851 | 0.919 | 623K |
| Geographic - Rural | 0.834 | 0.903 | 233K |

## Ethical Considerations

### Fairness Assessment
- **Demographic Parity**: Model predictions show no significant bias across age groups (p>0.05)
- **Equalized Odds**: Similar true positive rates across geographic regions (max difference: 0.03)
- **Individual Fairness**: Similar customers receive similar prediction scores (Lipschitz constant: 0.15)

### Bias Mitigation
- Features exclude protected attributes (age, gender, race)
- Regular bias testing with fairness metrics
- Human review required for edge cases (scores > 95%)

## Limitations & Risks

### Known Limitations
- **Concept Drift**: Model performance degrades with changing economic conditions
- **Data Gaps**: Limited data for customers with <3 months history
- **Seasonal Effects**: Lower accuracy during holiday periods
- **Cold Start**: New customer segments may not be well represented

### Risk Mitigation
- **Monitoring**: Weekly model performance checks
- **Fallbacks**: Revert to rule-based system if performance drops >5%
- **Regular Retraining**: Monthly model updates with new data
- **Human Oversight**: Marketing team reviews all high-risk predictions

### Potential Negative Impacts
- **False Positives**: Unnecessary retention spending on loyal customers
- **False Negatives**: Missing at-risk customers who actually churn
- **Fairness**: Potential for indirect discrimination through correlated features

## Maintenance & Monitoring

### Performance Monitoring
- **Real-time**: Prediction distribution monitoring
- **Daily**: Data drift detection on input features
- **Weekly**: Model performance on labeled outcomes
- **Monthly**: Bias metrics and fairness assessment

### Retraining Schedule
- **Regular**: Monthly retraining with rolling 2-year window
- **Triggered**: Emergency retraining if performance drops >10%
- **Validation**: A/B test new model versions before deployment

### Contact Information
- **Model Owner**: data-science-team@company.com
- **Technical Contact**: ml-engineering@company.com
- **Business Owner**: marketing@company.com
```

### **5. Process Documentation**

#### **Experiment Tracking** (MLflow/Weights & Biases)
```python
# Experiment documentation template
experiment_config = {
    "experiment_name": "churn_prediction_v2_1",
    "hypothesis": "Adding temporal features will improve precision@10% by 5pp",
    "baseline_model": "random_forest_v2_0",
    "changes": [
        "Added 7-day and 30-day rolling transaction features",
        "Increased max_depth from 10 to 15", 
        "Added early stopping with validation monitoring"
    ],
    "success_criteria": {
        "primary": "precision_at_10_percent > 0.90",
        "secondary": "auc_roc > 0.84",
        "business": "incremental_revenue > $50K per quarter"
    },
    "risks": [
        "Overfitting due to increased model complexity",
        "Longer training time may impact CI/CD pipeline",
        "New features may introduce data quality issues"
    ]
}
```

#### **Deployment Documentation**
```markdown
# Production Deployment Guide

## Pre-deployment Checklist
- [ ] Model performance validated on holdout test set
- [ ] A/B test plan approved by business stakeholders  
- [ ] Monitoring and alerting configured
- [ ] Rollback procedure tested
- [ ] Model card completed and reviewed
- [ ] Security and compliance review passed

## Deployment Steps
1. **Model Registration**: Upload model artifact to MLflow registry
2. **Infrastructure Setup**: Provision SageMaker endpoint with auto-scaling
3. **Integration Testing**: Test API endpoints with sample data
4. **Staged Rollout**: Deploy to 10% of traffic initially
5. **Performance Validation**: Monitor for 48 hours before full rollout
6. **Full Deployment**: Route 100% of prediction traffic to new model

## Monitoring & Alerting
- **Data Drift**: Alert if feature distributions shift >2 standard deviations
- **Model Performance**: Alert if precision@10% drops below 0.85
- **System Performance**: Alert if prediction latency exceeds 500ms
- **Data Quality**: Alert if missing value rate exceeds 5%

## Rollback Procedure
1. **Automatic**: Revert to previous model if alerts trigger
2. **Manual**: Update traffic routing in AWS console
3. **Verification**: Confirm rollback with test predictions
4. **Communication**: Notify stakeholders of rollback and timeline for fix
```

## Documentation Tools & Automation

### **Automated Documentation Generation**
```python
# Auto-generate data documentation
def document_dataset(df: pd.DataFrame, output_path: str) -> None:
    """Generate automated data documentation."""
    from ydata_profiling import ProfileReport
    
    profile = ProfileReport(
        df, 
        title="Customer Dataset Profile",
        explorative=True,
        dark_mode=True
    )
    profile.to_file(f"{output_path}/data_profile.html")

# Auto-generate API documentation  
def document_model_api(model_class, output_path: str) -> None:
    """Generate API documentation for model class."""
    import pydoc
    
    # Generate HTML documentation
    doc = pydoc.HTMLDoc()
    documentation = doc.docclass(model_class)
    
    with open(f"{output_path}/model_api.html", "w") as f:
        f.write(documentation)
```

### **Documentation Templates**
```python
# templates/analysis_template.py
"""
Template for standardized analysis notebooks.

Usage:
    jupyter notebook --template=templates/analysis_template.ipynb
"""

STANDARD_IMPORTS = """
# Standard imports for all analysis notebooks
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
import warnings
warnings.filterwarnings('ignore')

# Set style for consistent plots
plt.style.use('seaborn-v0_8')
sns.set_palette("husl")

# Configure pandas display
pd.set_option('display.max_columns', 100)
pd.set_option('display.max_rows', 50)
"""

ANALYSIS_SECTIONS = [
    "# 1. Executive Summary",
    "# 2. Business Context", 
    "# 3. Data Overview",
    "# 4. Exploratory Analysis",
    "# 5. Statistical Testing",
    "# 6. Results & Interpretation", 
    "# 7. Recommendations",
    "# 8. Next Steps"
]
```

## Documentation Quality Standards

### **Review Checklist**
- [ ] **Clarity**: Can a new team member understand and reproduce the work?
- [ ] **Completeness**: Are all key decisions and assumptions documented?
- [ ] **Accuracy**: Are claims supported by evidence and properly qualified?
- [ ] **Currency**: Is documentation up-to-date with latest code changes?
- [ ] **Accessibility**: Are technical concepts explained for business audience?

### **Style Guidelines**
- **Headers**: Use descriptive, actionable headers
- **Numbers**: Always include units, confidence intervals, and context
- **Visualizations**: Include clear titles, axis labels, and captions
- **Code**: Comment complex logic and include usage examples
- **Links**: Reference external sources and related documentation

### **Maintenance Process**
- **Regular Review**: Quarterly documentation audit for accuracy
- **Version Control**: Track documentation changes with code changes
- **Automated Checks**: Lint documentation for broken links and formatting
- **Feedback Loop**: Collect user feedback and iterate on clarity

This documentation framework ensures our data science work is transparent, reproducible, and accessible to both technical and business stakeholders while maintaining high standards for production systems.