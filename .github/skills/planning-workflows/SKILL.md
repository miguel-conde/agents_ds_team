---
name: planning-workflows
description: Create and manage structured JSON planning files for complex multi-agent workflows. Use when user requests projects requiring 3+ agents, multiple phases with dependencies, or enterprise-level coordination.
---

# Planning Workflows

## When to use this skill
Use this skill when the user requests complex projects that require:
- 3+ specialist agents working together
- Multiple phases with dependencies and validation checkpoints
- Structured execution tracking with progress management
- Enterprise-level coordination across domains
- Projects estimated at 8+ weeks or 100+ lines of deliverables

## Quick start

```bash
# Create plan
python scripts/create_plan.py --complexity moderate --task "description"

# Validate and track
python scripts/validate_plan.py plan-[name].json
python scripts/progress_tracker.py --plan plan-[name].json --status
```

**Need complexity help?** → [complexity-guidelines.md](reference/complexity-guidelines.md)  
**Want to see examples?** → [examples/](examples/) (real project files)

## Planning templates by complexity

| Level | Duration | Template | Usage |
|-------|----------|----------|-------|
| Simple | 1-3 weeks | Direct delegation | No planning file needed |
| Moderate | 4-8 weeks | [moderate-project.json](templates/moderate-project.json) | 5-8 steps, basic validation |
| Complex | 8-16 weeks | [complex-project.json](templates/complex-project.json) | 8-12 steps, cross-domain |
| Enterprise | 16+ weeks | [enterprise-project.json](templates/enterprise-project.json) | 12+ steps, governance |

**Unsure which level?** → Use [complexity assessment questionnaire](reference/complexity-guidelines.md#complexity-assessment-questionnaire) 

## Core workflow

1. **Analyze complexity** → Select template
2. **Generate plan** → Customize template 
3. **Validate structure** → Check dependencies
4. **Execute with tracking** → Follow step order
5. **Monitor progress** → Use persistent tracking

**Need JSON structure details?** → [examples.md](reference/examples.md#planning-workflows-examples)  
**Want collaboration patterns?** → [examples.md](reference/examples.md#common-patterns)

## Agent roles

- **@business-specialist**: Strategy, ROI, stakeholders
- **@tech-specialist**: Architecture, implementation
- **@creative-specialist**: UX/UI, branding
- **@data-specialist**: Analytics, ML/AI
- **@validator**: QA, cross-domain validation

**Planning agent handoffs?** → [examples.md](reference/examples.md#common-patterns)

## Resources by use case

**🤔 "How complex is my project?"** → [complexity-guidelines.md](reference/complexity-guidelines.md)  
**📋 "Show me real examples"** → [examples/](examples/) (fintech, marketplace projects)  
**🔧 "How do agent handoffs work?"** → [examples.md](reference/examples.md#common-patterns)  
**🏗️ "What's the JSON structure?"** → [examples.md](reference/examples.md#planning-workflows-examples)  
**⚠️ "Project went wrong, what patterns to avoid?"** → [examples.md](reference/examples.md#anti-patterns-to-avoid)

## Progress tracking

**⚠️ Note**: Use `progress_tracker.py` for persistent tracking (not #todos)

```bash
# Track completion
python scripts/progress_tracker.py --plan [file].json --complete-step N

# View status
python scripts/progress_tracker.py --plan [file].json --status
```

Creates `[plan-name].progress.json` alongside your planning file to track completed steps.