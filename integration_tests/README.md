# Integration Test: Complete Churn Prediction Workflow

## Objective

Validate the end-to-end DS agent framework with a realistic churn prediction project that tests:
- **Router decomposition**: How head-of-ds-router analyzes and delegates tasks
- **Agent collaboration**: Specialists working without overlap or confusion
- **DS-specific validation**: ds-validator catching common data science errors
- **Planning execution**: Using ds-planning-workflows skill for project management

## Test Scenario: E-commerce Customer Churn Prediction

### Business Context
**Company**: RetailCorp (fictional e-commerce company)
**Problem**: High customer churn rate (25%) affecting revenue growth
**Goal**: Build predictive model to identify at-risk customers for retention campaigns
**Success Criteria**: 90%+ precision at 10% recall, reducing churn by 15%

### Test Data Description
```json
{
  "dataset_size": "500K customers, 2-year history",
  "features_available": [
    "customer_demographics: age, location, signup_date",
    "transaction_history: purchase_amount, frequency, recency", 
    "engagement_metrics: website_visits, email_opens, support_tickets",
    "product_preferences: categories, brands, price_sensitivity"
  ],
  "target_variable": "churned_within_90_days",
  "data_quality_issues": [
    "Missing values in 15% of engagement metrics",
    "Inconsistent date formats across systems",
    "Duplicate customer records (2% of dataset)"
  ]
}
```

### Test Phases

## Phase 1: Initial Router Analysis
**Input Query**: 
> "We need to build a customer churn prediction model for our e-commerce platform. We have high churn rates (25%) and want to identify customers likely to churn in the next 90 days so we can run targeted retention campaigns. We need 90%+ precision to keep campaign costs manageable. We have customer demographics, transaction history, and engagement data available."

**Expected Router Behavior**:
1. Analyze complexity (moderate-to-high due to multiple data sources)
2. Use ds-planning-workflows skill to create structured plan
3. Define success metrics and validation requirements
4. Route initial data assessment to data-engineer
5. Create planning file with agent assignments and dependencies

## Phase 2: Agent Collaboration Testing

### 2.1 Data Engineer Tasks
**Assignment**: "Assess data quality, create data contracts, and design ingestion pipeline"
**Expected Deliverables**:
- Data quality assessment report
- Schema specifications for clean data
- ETL pipeline design with data contracts
- Data validation tests

**Common DS Errors to Test**:
- ❌ **Target leakage**: Using features computed after churn event
- ❌ **Temporal misalignment**: Training on future data
- ❌ **Data drift**: Training/serving data distributions differ

### 2.2 Data Scientist Tasks  
**Assignment**: "Develop churn prediction model with proper evaluation protocol"
**Expected Deliverables**:
- Exploratory data analysis
- Feature engineering specifications
- Model development with baseline comparison
- Evaluation protocol with temporal validation

**Common DS Errors to Test**:
- ❌ **No baseline**: Skipping simple heuristic comparison
- ❌ **Data snooping**: Using test data for feature selection
- ❌ **Survivorship bias**: Excluding churned customers from training

### 2.3 ML Engineer Tasks
**Assignment**: "Productionize model with monitoring and serving infrastructure"  
**Expected Deliverables**:
- Model training pipeline with reproducibility
- Serving infrastructure design
- Monitoring and alerting specifications
- Deployment strategy with rollback procedures

**Common DS Errors to Test**:
- ❌ **Training-serving skew**: Different feature computation in production
- ❌ **Model drift**: No monitoring for concept drift
- ❌ **No rollback**: Missing automated fallback procedures

## Phase 3: Validation Testing

### 3.1 Planning Validation
**DS-Validator Task**: Review planning structure and dependencies
**Test Scenarios**:
- ✅ **Valid Plan**: Proper task sequencing, clear DoD, risk assessment
- ❌ **Invalid Plan**: Missing dependencies, unclear success metrics
- ❌ **Incomplete Plan**: Missing MLops requirements, no evaluation protocol

### 3.2 Analysis Validation  
**DS-Validator Task**: Check statistical methodology and interpretation
**Test Scenarios**:
- ✅ **Valid Analysis**: Proper hypothesis testing, confidence intervals
- ❌ **Leakage Risk**: Features using future information detected
- ❌ **Statistical Error**: Multiple testing without correction

### 3.3 Production Validation
**DS-Validator Task**: Verify production readiness and monitoring
**Test Scenarios**:
- ✅ **Production Ready**: Monitoring, tests, documentation complete
- ❌ **Missing Tests**: No unit tests for feature transformations
- ❌ **No Monitoring**: Missing model performance tracking

## Phase 4: Workflow Integration

### 4.1 Planning File Execution
**Test**: Use ds-planning-workflows skill to manage project lifecycle
**Validation Criteria**:
- Planning file updates with task completion
- Dependencies properly tracked and enforced  
- Quality gates respected before downstream work
- Agent handoffs follow documented protocols

### 4.2 Error Detection and Recovery
**Test**: DS-validator catches errors and routes for corrections
**Validation Criteria**:
- Common DS errors detected in validation checkpoints
- Clear feedback provided for error correction
- Router coordinates error resolution between agents
- Project continues after error resolution

### 4.3 Success Criteria Validation
**Test**: Final deliverables meet business requirements
**Validation Criteria**:
- Model performance exceeds success criteria (90% precision@10%)
- All DS methodology standards followed
- Production deployment plan complete
- Business impact quantified and validated

## Expected Outcomes

### Successful Integration Test Results:
1. **Router Intelligence**: Correctly decomposes complex DS project
2. **Agent Specialization**: Each agent focuses on their domain expertise
3. **No Overlap**: Clear boundaries prevent duplicate work
4. **Error Detection**: DS-validator catches 95%+ of common DS errors
5. **Planning Execution**: Project progresses through quality gates systematically
6. **Business Alignment**: Final solution meets stated business requirements

### Key Performance Indicators:
- **Planning Accuracy**: Estimated effort vs actual < 20% variance
- **Error Detection Rate**: >95% of seeded errors caught by validation
- **Agent Coordination**: <5% duplicated work across agents
- **Quality Gates**: 100% gate requirements met before progression
- **Business Value**: Clear path from model to business impact quantified

## Files Created During Test

1. **`integration_tests/test_runner.py`** - Automated test execution script
2. **`integration_tests/test_scenarios.py`** - Individual test case definitions  
3. **`integration_tests/mock_data/`** - Sample datasets for testing
4. **`integration_tests/expected_outputs/`** - Reference deliverables for validation
5. **`integration_tests/error_scenarios.py`** - Common DS errors to inject and detect
6. **`integration_tests/results/`** - Test execution results and logs

This integration test validates that our DS agent team framework can handle realistic, complex data science projects with proper coordination, validation, and business alignment.