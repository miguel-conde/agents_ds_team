# Model Evaluation Standards

## Overview

This document defines the evaluation standards and protocols that all DS models must follow. These standards ensure consistent, fair, and business-relevant model assessment across our team.

## Evaluation Principles

### 1. **Business-First Metrics**
Primary evaluation must use business metrics, not just statistical metrics.

```python
# Example hierarchy for customer churn model
primary_metric = "incremental_revenue_per_customer"
secondary_metric = "precision_at_k"  # k = top 10% predictions  
diagnostic_metrics = ["auc_roc", "calibration_error", "fairness_parity"]
```

### 2. **Out-of-Time Validation**
All temporal data must use time-based splits to detect concept drift.

```python
# Required temporal validation
train_period = "2020-01-01 to 2022-12-31"
validation_period = "2023-01-01 to 2023-06-30" 
test_period = "2023-07-01 to 2023-12-31"

# No data leakage between periods
assert test_start_date > validation_end_date
```

### 3. **Baseline Comparison**
Every model must demonstrate improvement over multiple baselines.

## Required Baselines

### **Tier 1: Simple Baselines** (Always Required)
```python
baselines_required = {
    "random": "random_prediction_within_class_distribution",
    "majority_class": "predict_most_frequent_class", 
    "mean_target": "predict_historical_mean",
    "seasonal_naive": "predict_same_period_last_year"
}
```

### **Tier 2: Heuristic Baselines** (Business Logic)
- Domain-specific rules from business experts
- Current manual process or business rules
- Simple threshold-based decisions

### **Tier 3: Statistical Baselines** (Standard Models)  
- Linear/Logistic regression with basic features
- Decision tree with limited depth
- Moving average or exponential smoothing (time series)

## Validation Strategies

### **Cross-Validation Framework**
```python
# Time series data
cv_strategy = {
    "method": "expanding_window",
    "min_train_size": 180,  # days
    "forecast_horizon": 30,  # days
    "step_size": 7,  # weekly steps
    "purged_gap": 1,  # day gap to prevent leakage
    "embargo": 0  # no embargo unless trading strategy
}

# Cross-sectional data with groups
cv_strategy = {
    "method": "grouped_k_fold", 
    "group_col": "customer_id",
    "k": 5,
    "stratify": "target", 
    "shuffle": True,
    "random_state": 42
}
```

### **Holdout Test Set Requirements**
- Minimum 15% of total sample size
- Representative of prediction deployment conditions  
- Touched only once for final evaluation
- Results must be significant with confidence intervals

## Performance Metrics

### **Classification Problems**

#### **Binary Classification**
```python
required_metrics = {
    "business_metric": "custom_business_impact",
    "discrimination": "auc_roc",  
    "precision_recall": "average_precision",
    "calibration": "brier_score",
    "threshold_metrics": "precision_at_k, recall_at_k"
}

# Business metric example
def custom_business_impact(y_true, y_pred_proba, k=0.1):
    """Revenue impact of top k% predictions"""
    cutoff = np.percentile(y_pred_proba, (1-k)*100) 
    selected = y_pred_proba >= cutoff
    precision_at_k = y_true[selected].mean()
    return precision_at_k * revenue_per_conversion * np.sum(selected)
```

#### **Multiclass Classification**
```python
required_metrics = {
    "balanced_accuracy": "handles_class_imbalance",
    "macro_f1": "equal_weight_per_class",
    "weighted_f1": "sample_weight_per_class", 
    "confusion_matrix": "per_class_performance"
}
```

### **Regression Problems**
```python
required_metrics = {
    "business_metric": "custom_cost_function",
    "accuracy": "mean_absolute_percentage_error", 
    "bias": "mean_error",
    "variance": "std_error",
    "tail_performance": "quantile_loss_90th_percentile"
}
```

### **Time Series Forecasting**
```python
required_metrics = {
    "mape": "mean_absolute_percentage_error",
    "smape": "symmetric_mape", 
    "directional_accuracy": "correct_trend_direction",
    "coverage": "prediction_interval_coverage"
}
```

## Model Interpretation Requirements

### **Feature Importance**
```python
interpretation_methods = {
    "global": ["permutation_importance", "shap_values"],
    "local": ["lime", "shap_local"],
    "partial_dependence": "show_feature_relationships"
}
```

### **Business Validation**
- Feature importance aligns with business understanding
- Model decisions explainable to business stakeholders
- Edge cases and failure modes identified
- Fairness assessment across protected groups

## Fairness and Bias Evaluation

### **Protected Groups Analysis** 
```python
protected_attributes = ["age", "gender", "race", "geographic_region"]

fairness_metrics = {
    "demographic_parity": "equal_positive_rate_across_groups",
    "equalized_odds": "equal_tpr_and_fpr_across_groups", 
    "calibration": "equal_precision_across_groups",
    "individual_fairness": "similar_treatment_for_similar_individuals"
}
```

### **Bias Detection Protocol**
1. **Selection bias**: Compare model performance across subgroups
2. **Historical bias**: Assess training data representation
3. **Evaluation bias**: Ensure validation data reflects deployment
4. **Algorithmic bias**: Test for disparate impact

## Model Robustness Testing

### **Data Drift Testing**
```python
drift_tests = {
    "feature_drift": "kolmogorov_smirnov_test",
    "target_drift": "chi_square_test", 
    "concept_drift": "model_performance_degradation",
    "covariate_shift": "domain_adaptation_metrics"
}
```

### **Stress Testing** 
- Performance under missing data scenarios
- Behavior with edge case inputs
- Robustness to adversarial examples  
- Impact of feature correlation changes

### **Stability Analysis**
- Performance variance across multiple training runs
- Sensitivity to hyperparameter changes
- Bootstrap confidence intervals for all metrics
- Statistical significance testing for model comparisons

## Documentation Requirements

### **Evaluation Report Template**
```markdown
# Model Evaluation Report

## Business Context
- Problem statement and success criteria
- Business metric definition and targets

## Data and Methodology
- Dataset description and splits
- Cross-validation strategy  
- Baseline models and selection

## Results
- Performance comparison table
- Statistical significance tests
- Business impact projections

## Model Interpretation
- Feature importance analysis
- Business logic validation
- Edge cases and limitations

## Fairness and Bias
- Protected group analysis
- Bias mitigation strategies
- Ethical considerations

## Production Readiness
- Robustness testing results
- Monitoring and alerting plan
- Rollback criteria and procedures
```

### **Metrics Dashboard**
All models must include automated dashboard with:
- Real-time performance monitoring
- Data drift detection alerts
- Prediction distribution tracking  
- Business metric impact measurement

## Approval Gates

### **Gate 1: Validation Performance**
- [ ] Beats all required baselines with statistical significance
- [ ] Business metric improvement confirmed
- [ ] Cross-validation results stable and consistent
- [ ] Interpretation aligns with business logic

### **Gate 2: Fairness and Robustness**
- [ ] Fairness metrics within acceptable ranges
- [ ] Stress testing passed without critical failures
- [ ] Stability analysis shows <5% performance variance
- [ ] Edge cases identified and mitigation planned

### **Gate 3: Production Readiness**  
- [ ] Monitoring and alerting implemented
- [ ] Rollback procedures tested
- [ ] Documentation complete and reviewed
- [ ] Business stakeholder sign-off obtained

---

This evaluation framework ensures our models are not only statistically sound but also fair, robust, and aligned with business objectives for successful production deployment.