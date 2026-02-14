# DS Agent Team Testing Guide

## Quick Start: 3 Testing Options

### ✅ **Option 1: Built-in Real Data (RECOMMENDED)**
Uses sklearn's California Housing dataset - no downloads required.

```bash
source .venv/bin/activate
python tests/integration/test_ds_with_real_data.py
```

**What it tests:**
- Router decomposition with real regression problem
- Data engineer pipeline + data contracts
- Data scientist baseline vs. model validation
- ML engineer production specifications

**Dataset:** 20,640 California properties, 8 features, predict median house value

---

### 🔧 **Option 2: Synthetic Data (Current Integration Test)**
Uses generated churn data with controlled error scenarios.

```bash
source .venv/bin/activate
python tests/integration/test_ds_workflow.py
```

**What it tests:**
- Full agent collaboration workflow
- DS-validator error detection (leakage, drift, etc.)
- Planning file execution tracking
- Error injection and recovery

**Dataset:** Synthetic customer churn (configurable size)

---

### 📊 **Option 3: Kaggle Datasets (Most Realistic)**
Real business datasets for production-like testing.

```bash
# One-time setup
pip install kaggle
# Get API key from kaggle.com/account
mkdir -p ~/.kaggle
echo '{"username":"YOUR_USERNAME","key":"YOUR_KEY"}' > ~/.kaggle/kaggle.json
chmod 600 ~/.kaggle/kaggle.json

# Download dataset
kaggle datasets download -d blastchar/telco-customer-churn
unzip telco-customer-churn.zip -d tests/integration/kaggle_data/

# Test with custom script (you'll need to adapt test_ds_with_real_data.py)
```

**Popular datasets for DS team testing:**
- `blastchar/telco-customer-churn` - Classification (churn)
- `shivam2503/diamonds` - Regression (price prediction)
- `uciml/breast-cancer-wisconsin-data` - Binary classification (medical)
- `mlg-ulb/creditcardfraud` - Anomaly detection

---

## Test Coverage Matrix

| Test Scenario | Router | Data Engineer | Data Scientist | ML Engineer | Validator |
|---------------|--------|---------------|----------------|-------------|-----------|
| **Real Data Test** | ✅ Planning | ✅ Contract + DQ | ✅ Baseline + Model | ✅ Serving Spec | ⚠️ Basic |
| **Synthetic Test** | ✅ Planning | ✅ Pipeline | ✅ Full Workflow | ✅ Production | ✅ Error Detection |
| **Kaggle Test** | ✅ Planning | ✅ Real Issues | ✅ Business Metrics | ✅ Scale Testing | ✅ Production |

---

## Expected Test Outputs

### Artifacts Generated:
```
tests/integration/artifacts/
├── real_data_project_plan.json          # Router deliverable
├── housing_data_contract.json           # Data Engineer
├── housing_dq_results.json              # Data quality validation
├── housing_model_evaluation.json        # Data Scientist
└── housing_model_serving_spec.json      # ML Engineer
```

### Success Criteria:
- ✅ Router creates valid planning file with data contracts
- ✅ Data Engineer delivers 100% DQ pass rate
- ✅ Data Scientist beats baseline by >10%
- ✅ ML Engineer provides production-ready deployment spec
- ✅ All deliverables follow Definition of Done standards

---

## Interactive Testing (Manual Agent Invocation)

Want to test agents interactively? Try these prompts:

### Test Router:
```
Create a DS project plan for predicting employee attrition using 
HR data (tenure, salary, performance ratings). Focus on retention 
strategies for high-value employees.
```

### Test Data Engineer:
```
@data-engineer Create a data contract and quality validation pipeline 
for the California Housing dataset. Ensure geographic constraints are validated.
```

### Test Data Scientist:
```
@data-scientist Build a house price prediction model using the California 
Housing dataset. Include baseline comparison and feature importance analysis.
```

### Test ML Engineer:
```
@ml-engineer Design production serving infrastructure for a house price 
prediction model. Include monitoring for data drift and performance degradation.
```

### Test Validator:
```
@ds-validator Validate this churn model feature engineering for potential 
data leakage. Features include: last_purchase_date, days_to_churn, 
total_purchases, churn (target).
```

---

## Performance Benchmarks

Based on synthetic data testing (5,000 samples):

| Agent | Avg Execution Time | Key Deliverables |
|-------|-------------------|------------------|
| Router | 1-2 seconds | Planning file |
| Data Engineer | 5-10 seconds | Contract + DQ validation |
| Data Scientist | 15-30 seconds | Baseline + model + evaluation |
| ML Engineer | 3-5 seconds | Serving spec + runbook |
| Validator | 2-5 seconds | Error detection report |

**Total workflow**: ~30-60 seconds for complete DS project decomposition

---

## Troubleshooting

**Error: Virtual environment not activated**
```bash
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# .venv\Scripts\activate   # Windows
pip install -r requirements.txt
```

**Error: sklearn dataset download fails**
```python
# Try with different scikit-learn dataset
from sklearn.datasets import load_diabetes, load_wine, fetch_california_housing
```

**Error: Missing dependencies**
```bash
pip install scikit-learn pandas numpy
```

---

## Next Steps

1. **Run the built-in test first**: `python tests/integration/test_ds_with_real_data.py`
2. **Review artifacts**: Check `tests/integration/artifacts/` for generated files
3. **Test interactively**: Use the prompts above to test individual agents
4. **Scale up**: Try with Kaggle datasets for production-like scenarios

For questions or issues, check `AGENTS.md` for agent contracts and workflows.
