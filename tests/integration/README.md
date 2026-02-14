# DS Agent Team Integration Testing

## Overview

Phase 4 of the DS Agent Team framework includes comprehensive integration testing to validate that all agents work together correctly in a realistic data science workflow.

## What's Being Tested

### 1. **Router Decomposition**
- head-of-ds-router correctly decomposes complex DS projects
- Creates comprehensive planning files using ds-planning-workflows skill
- Assigns appropriate tasks to specialist agents

### 2. **Agent Collaboration**
- data-engineer creates data contracts and quality validation
- data-scientist develops models with proper evaluation protocols
- ml-engineer designs production infrastructure and monitoring
- No task overlap or coordination issues between agents

### 3. **DS-Validator Error Detection**
- Catches data leakage (future information in training data)
- Detects target leakage (perfect predictors)
- Identifies multicollinearity issues
- Validates temporal consistency
- Flags excessive missing values

### 4. **Planning File Execution Tracking**
- Updates planning files with actual progress
- Tracks deliverable completion status
- Monitors execution time vs estimates

## Test Scenario: Customer Churn Prediction

The integration test simulates a complete churn prediction project:

1. **Business Problem**: Predict customer churn with 85%+ precision
2. **Dataset**: 5,000 synthetic customers with realistic behavioral patterns
3. **Workflow**: Full DE → DS → MLE workflow with validation
4. **Validation**: Problematic dataset to test error detection

## Running the Tests

### Prerequisites

1. **Virtual Environment** (MANDATORY for DS team):
```bash
python3 -m venv .venv
source .venv/bin/activate
```

2. **Install Dependencies**:
```bash
pip install pandas numpy scikit-learn pyyaml click tqdm
```

### Execute Integration Test

```bash
# Ensure virtual environment is active
source .venv/bin/activate

# Run the complete integration test
python tests/integration/test_ds_workflow.py
```

### Expected Output

The test will generate:
- ✅ Planning file with DS-specific structure
- ✅ Data contracts and quality validation
- ✅ Model evaluation reports with baseline comparison
- ✅ Production deployment specifications
- ✅ Error detection from ds-validator
- ✅ Planning file with execution progress

## Test Artifacts

All test artifacts are saved to `tests/integration/artifacts/`:
- `ds_project_plan.json` - Original project plan
- `ds_project_plan_with_progress.json` - Plan with completion status
- `data_contract.json` - Data engineer deliverable
- `processed_customer_data.csv` - Clean dataset
- `model_evaluation_report.json` - Data scientist deliverable
- `serving_specification.json` - ML engineer deliverable
- `deployment_runbook.md` - Production deployment guide

## Success Criteria

For the integration test to pass:

1. **Planning Phase**: Router creates valid DS planning file
2. **Execution Phase**: All 3 agents complete their tasks successfully
3. **Validation Phase**: DS-validator catches at least 3 DS-specific errors
4. **Tracking Phase**: Planning file correctly updated with progress

## Interpreting Results

### ✅ **PASSED** - Framework Ready for Production
- All agents collaborate effectively
- DS-validator catches critical errors
- Deliverables meet quality standards
- Planning workflow executes correctly

### ❌ **FAILED** - Issues Need Resolution
- Check individual agent failures in output
- Review error logs for specific issues
- Validate agent handoff configurations
- Ensure ds-validator rules are comprehensive

## Debugging Failed Tests

If tests fail, check:
1. **Virtual environment**: Ensure `.venv` is activated
2. **Dependencies**: Verify all packages installed correctly  
3. **Agent configurations**: Review agent YAML frontmatter
4. **File permissions**: Ensure scripts are executable
5. **Data quality**: Check if synthetic data generation is working

## Extending the Tests

To add new test scenarios:
1. Create additional problematic datasets in `ChurnDataGenerator`
2. Add new agent simulation methods in `DSAgentSimulator`
3. Extend error detection in `simulate_ds_validator`
4. Update success criteria and reporting

## Integration with CI/CD

This integration test can be included in automated testing:

```yaml
# .github/workflows/integration.yml
name: DS Agent Integration Tests
on: [push, pull_request]

jobs:
  integration-test:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    - name: Set up Python
      uses: actions/setup-python@v3
      with:
        python-version: 3.12
    - name: Create virtual environment
      run: python -m venv .venv
    - name: Install dependencies
      run: |
        source .venv/bin/activate
        pip install pandas numpy scikit-learn pyyaml click tqdm
    - name: Run integration tests
      run: |
        source .venv/bin/activate
        python tests/integration/test_ds_workflow.py
```

This ensures the DS agent team framework continues to work correctly as the codebase evolves.