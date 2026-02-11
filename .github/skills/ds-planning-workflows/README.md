# DS Planning Workflows Skill

A comprehensive skill for creating and managing structured JSON planning files specifically designed for data science workflows. This skill extends the general planning-workflows with DS-specific features like data contracts, leakage prevention, and MLOps requirements.

## Overview

This skill helps you:
- **Plan DS projects** with appropriate complexity assessment
- **Define data contracts** between DE, DS, and MLE agents  
- **Prevent data leakage** with automated risk detection
- **Ensure reproducibility** with MLOps best practices
- **Validate DS workflows** with specialized quality gates

## Quick Start

### 1. Create a DS Plan
```bash
# Create moderate complexity DS project plan
python scripts/create_ds_plan.py --complexity moderate --task "Customer churn prediction"

# Interactive mode for customization
python scripts/create_ds_plan.py --complexity complex --task "Marketing mix modeling" --interactive
```

### 2. Validate DS Requirements
```bash
# Check for data leakage risks
python scripts/check_leakage_risks.py --plan plan-ds-churn-prediction.json

# Full validation report
python scripts/check_leakage_risks.py --plan plan-ds-churn-prediction.json --verbose --output validation-report.json
```

## File Structure

```
ds-planning-workflows/
├── SKILL.md                       # Skill definition and usage
├── README.md                      # This file  
├── examples/                      # Real DS project examples
│   ├── plan-template-ds.json      # Enhanced DS template
│   ├── plan-churn-prediction.json # Customer churn example
│   └── plan-mmm-pharma.json       # Marketing mix modeling example
├── templates/                     # Templates by complexity
│   ├── simple-ds-project.json     # 2-4 weeks, single model
│   ├── moderate-ds-project.json   # 4-12 weeks, DE+DS+MLE
│   ├── complex-ds-project.json    # 12-24 weeks, full MLOps
│   └── enterprise-ds-project.json # 24+ weeks, governance
├── reference/                     # Guidelines and documentation
│   ├── ds-complexity-guidelines.md # How to assess DS project complexity
│   └── ds-examples.md             # Usage patterns and examples
└── scripts/                       # Automation tools
    ├── create_ds_plan.py          # Generate DS planning files
    ├── check_leakage_risks.py     # Automated leakage detection
    ├── validate_ds_plan.py        # DS-specific validation
    └── ds_progress_tracker.py     # Progress tracking with DS gates
```

## Key Features

### 📊 Data Contracts
Every DS project includes structured data contracts with:
- Schema definitions with constraints
- Data quality SLAs (>95% pass rate)
- Lineage and refresh requirements  
- Interface specifications DE→DS→MLE

### 🔒 Leakage Prevention
Automated detection and prevention of:
- Future information in historical predictions
- Temporal validation issues
- Feature engineering risks
- Evaluation protocol problems

### 🔄 MLOps Requirements
Built-in MLOps best practices:
- Reproducibility standards (<1% variance)
- Model registry and versioning
- Monitoring and drift detection
- Deployment and rollback strategies

### ✅ DS Validation Gates
Specialized validation checkpoints:
- Data pipeline validation (@ds-validator)
- Model validation with leakage checks
- Production readiness verification
- End-to-end workflow validation

## Complexity Levels

### Simple DS (2-4 weeks)
- Single model, basic evaluation
- 1-2 agents (DS + Validator)
- Notebook-based development
- **Use case**: Customer segmentation, simple recommendations

### Moderate DS (4-12 weeks)  
- Data pipeline + model + basic deployment
- 3-4 agents (DE + DS + MLE + Validator)
- Automated training and serving
- **Use case**: [Churn prediction](examples/plan-churn-prediction.json)

### Complex DS (12-24 weeks)
- Production ML system + comprehensive monitoring
- Full DS team with specialized roles
- Advanced ML techniques, real-time serving
- **Use case**: [Marketing mix modeling](examples/plan-mmm-pharma.json)

### Enterprise DS (24+ weeks)
- Enterprise ML platform + governance
- Regulatory compliance, audit trails
- Multi-model systems, AutoML
- **Use case**: Bank-wide risk modeling, clinical trials

## Usage Examples

### Customer Churn Prediction
```bash
# Generate plan from template
python scripts/create_ds_plan.py --complexity moderate --task "customer-churn-prediction"

# Check for temporal validation issues
python scripts/check_leakage_risks.py --plan plan-ds-customer-churn-prediction.json

# Expected output: Medium risk due to temporal nature, recommendations for 30-day gap
```

### Marketing Mix Modeling
```bash
# Generate complex DS plan
python scripts/create_ds_plan.py --complexity complex --task "pharma-mmm-attribution" --interactive

# Validate advanced modeling approach
python scripts/check_leakage_risks.py --plan plan-ds-pharma-mmm-attribution.json --verbose
```

## Integration with DS Agents

### Agent Workflow
1. **@head-of-ds-router** creates DS plan using this skill
2. **@data-engineer** implements data contracts from plan
3. **@data-scientist** follows evaluation protocol from plan  
4. **@ml-engineer** implements MLOps requirements from plan
5. **@ds-validator** validates against plan criteria at each step

### Handoff Pattern
```markdown
@head-of-ds-router → Creates plan with ds-planning-workflows skill
@ds-validator → Validates plan structure and requirements
@data-engineer → Implements deliverables per data contracts
@ds-validator → Validates data pipeline against contracts
@data-scientist → Develops model per evaluation protocol  
@ds-validator → Validates model for leakage and evaluation rigor
@ml-engineer → Implements production deployment per MLOps requirements
@ds-validator → Validates production readiness and monitoring
```

## Best Practices

### Planning Phase
- **Start with complexity assessment** using [guidelines](reference/ds-complexity-guidelines.md)
- **Define clear business objectives** with quantifiable success metrics
- **Include all stakeholders** from business, technical, and data domains
- **Plan for validation gates** at each major deliverable

### Execution Phase
- **Use automated leakage detection** before model deployment
- **Enforce data contracts** between agent handoffs
- **Validate reproducibility** with <1% variance tolerance
- **Monitor DS-specific metrics** (drift, leakage, performance)

### Common Anti-Patterns to Avoid
- Skipping temporal validation for time-series problems
- Using cross-validation for time-dependent data
- Missing baseline establishment and comparison
- Inadequate documentation of feature engineering logic
- Deploying without proper monitoring and rollback plans

## Support and Troubleshooting

### Common Issues
1. **High leakage risk score**: Review feature engineering and temporal validation
2. **Complexity mismatch**: Use complexity guidelines to reassess project scope
3. **Agent coordination problems**: Ensure clear data contracts and handoff protocols

### Getting Help
- Review [examples](examples/) for similar use cases
- Check [complexity guidelines](reference/ds-complexity-guidelines.md) for scoping
- Use verbose mode in scripts for detailed analysis
- Consult DS team agents for domain-specific guidance

## Contributing

To extend this skill:
1. Add new templates in `templates/` for specific DS domains
2. Enhance scripts with additional validation checks
3. Create new examples for emerging DS use cases
4. Update complexity guidelines based on experience