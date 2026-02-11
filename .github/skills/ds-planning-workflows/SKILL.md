---
name: ds-planning-workflows
description: Create and manage structured JSON planning files for data science workflows. Use when user requests DS projects requiring data contracts, evaluation protocols, and MLOps requirements.
---

# DS Planning Workflows

## When to use this skill
Use this skill when the user requests data science projects that require:
- Data engineering pipelines with quality contracts
- Model development with evaluation protocols  
- Production ML deployment with monitoring
- End-to-end DS workflows (DE → DS → MLE)
- Projects with leakage risks or temporal validation needs

## Quick start

```bash
# Create DS plan
python scripts/create_ds_plan.py --complexity moderate --task "description"

# Validate DS-specific requirements
python scripts/validate_ds_plan.py plan-ds-[name].json
python scripts/check_leakage_risks.py --plan plan-ds-[name].json
```

**Need DS complexity help?** → [ds-complexity-guidelines.md](reference/ds-complexity-guidelines.md)  
**Want to see DS examples?** → [examples/](examples/) (real DS project files)

## DS Planning templates by complexity

| Level | Duration | Template | Usage |
|-------|----------|----------|-------|
| Simple DS | 2-4 weeks | [simple-ds-project.json](templates/simple-ds-project.json) | Single model, basic validation |
| Moderate DS | 4-12 weeks | [moderate-ds-project.json](templates/moderate-ds-project.json) | Data contracts + deployment |
| Complex DS | 12-24 weeks | [complex-ds-project.json](templates/complex-ds-project.json) | Multi-model, production ML |
| Enterprise DS | 24+ weeks | [enterprise-ds-project.json](templates/enterprise-ds-project.json) | Full MLOps + governance |

**Unsure which level?** → Use [DS complexity assessment](reference/ds-complexity-guidelines.md#ds-complexity-assessment) 

## Core DS workflow

1. **Analyze DS complexity** → Select DS template
2. **Generate DS plan** → Include data contracts + evaluation protocols
3. **Validate DS structure** → Check leakage risks + reproducibility  
4. **Execute with DS tracking** → Follow DE→DS→MLE order
5. **Monitor DS progress** → Use DS-specific validation gates

**Need DS JSON structure details?** → [ds-examples.md](reference/ds-examples.md#ds-planning-workflows-examples)  
**Want DS collaboration patterns?** → [ds-examples.md](reference/ds-examples.md#ds-agent-patterns)

## DS Agent roles

- **@head-of-ds-router**: Orchestration with decision rights
- **@data-engineer**: Data contracts, pipelines, DQ
- **@data-scientist**: Features, baselines, evaluation  
- **@ml-engineer**: Production, monitoring, deployment
- **@ds-validator**: Leakage detection, reproducibility

**Planning DS agent handoffs?** → [ds-examples.md](reference/ds-examples.md#ds-collaboration-patterns)

## Resources by DS use case

**🤔 "How complex is my DS project?"** → [ds-complexity-guidelines.md](reference/ds-complexity-guidelines.md)  
**📋 "Show me real DS examples"** → [examples/](examples/) (churn, MMM, recommendation projects)  
**🔧 "How do DS agent handoffs work?"** → [ds-examples.md](reference/ds-examples.md#ds-collaboration-patterns)  
**🏗️ "What's the DS JSON structure?"** → [ds-examples.md](reference/ds-examples.md#ds-planning-structure)  
**⚠️ "DS project went wrong, what to avoid?"** → [ds-examples.md](reference/ds-examples.md#ds-anti-patterns)

## DS Progress tracking

**⚠️ Note**: Use `ds_progress_tracker.py` for DS-specific validation gates

```bash
# Track DS completion with validation
python scripts/ds_progress_tracker.py --plan [file].json --complete-step N --validate

# Check leakage risks
python scripts/check_leakage_risks.py --plan [file].json --step N
```

Creates `[plan-name].ds-progress.json` alongside your planning file to track DS validation status.

## DS-Specific Features

### Data Contracts
- Schema definitions with constraints
- Data quality SLAs (>95% pass rate)
- Lineage and refresh requirements
- Interface specifications DE→DS→MLE

### Evaluation Protocols  
- Baseline establishment requirements
- Leakage prevention validation
- Temporal validation strategies
- Statistical significance testing

### MLOps Requirements
- Reproducibility standards (<1% variance)
- Model registry and versioning
- Monitoring and drift detection
- Deployment and rollback strategies

### Risk Assessment
- Data leakage risks
- Reproducibility challenges  
- Production scaling constraints
- Business impact validation