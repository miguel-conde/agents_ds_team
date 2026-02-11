# Planning Workflows Agent Skill

A comprehensive Agent Skill for VSCode Copilot that provides intelligent planning workflows for multi-agent collaboration projects of varying complexity levels.

## Overview

This skill automatically activates when users describe complex projects requiring multi-agent collaboration. It provides templates, validation tools, and guidelines for creating structured planning workflows that ensure effective coordination between specialist agents.

## Skill Components

### 📋 Templates (`templates/`)
- `simple-project.json` - 1-2 weeks, single domain focus
- `moderate-project.json` - 2-6 weeks, cross-domain collaboration  
- `complex-project.json` - 8-16 weeks, multi-platform integration
- `enterprise-project.json` - 12-24 months, organizational transformation

### 🛠️ Scripts (`scripts/`)
- `validate_plan.py` - Comprehensive planning file validation
- `create_plan.py` - Interactive and programmatic plan creation
- `check_dependencies.py` - Dependency analysis and timeline optimization

### 📚 Reference (`reference/`)
- `complexity-guidelines.md` - Detailed complexity assessment criteria
- `examples.md` - Real-world examples and common patterns

## Auto-Activation Triggers

This skill automatically activates when users mention:
- "Multi-agent collaboration project"
- "Complex workflow planning"
- "Project spanning multiple domains"
- "Enterprise-level planning"  
- "Coordinated agent development"
- "Cross-functional project planning"

## Quick Start

### For Users

1. **Describe your project**: "I need to plan a complex e-commerce integration project involving multiple APIs and user experience updates"

2. **Skill auto-activates**: The planning workflows skill will automatically provide relevant templates and guidance

3. **Follow recommendations**: Use provided templates and validation tools to structure your multi-agent collaboration

### For Agents

When this skill activates, you gain access to:

- **Complexity Assessment**: Guidelines to determine appropriate planning depth
- **Template Selection**: Pre-built JSON templates for different project scales
- **Validation Tools**: Scripts to verify plan structure and dependencies
- **Best Practices**: Examples and patterns for effective agent collaboration

## Template Selection Guide

| Complexity | Duration | Use When | Template File |
|------------|----------|----------|---------------|
| **Simple** | 1-2 weeks | Single domain, clear requirements | `simple-project.json` |
| **Moderate** | 2-6 weeks | Multi-domain, some unknowns | `moderate-project.json` |
| **Complex** | 8-16 weeks | Platform integration, high stakes | `complex-project.json` |
| **Enterprise** | 12-24 months | Organizational transformation | `enterprise-project.json` |

## Planning Workflow Structure

Each planning file includes:

```json
{
  "task_name": "Project identifier",
  "description": "Comprehensive project description", 
  "complexity_level": "simple|moderate|complex|enterprise",
  "estimated_duration": "Time estimate",
  "steps": [
    {
      "id": 1,
      "agent": "@specialist-name",
      "task": "Specific task description",
      "deliverable": "output-file.md",
      "dependencies": [],
      "estimated_time": "time estimate",
      "success_criteria": ["criterion1", "criterion2"]
    }
  ],
  "validation_criteria": ["overall success criteria"],
  "risk_factors": [{"category": "type", "mitigation": "strategy"}]
}
```

## Agent Collaboration Patterns

### Progressive Validation Pattern
```
specialist → validator → specialist → validator → final
```
**Use for**: High-risk or uncertain projects

### Parallel Development Pattern  
```
business-specialist
data-specialist    } → integration-validation → final
tech-specialist
```
**Use for**: Well-defined requirements with independent work streams

### Iterative Refinement Pattern
```
specialist → cross-consultation → validator → refinement → repeat
```
**Use for**: Complex projects with evolving requirements

## Validation and Quality Assurance

### Automatic Validation
Run validation on any planning file:
```bash
python scripts/validate_plan.py your-plan.json
```

### Dependency Analysis
Optimize workflow dependencies:
```bash
python scripts/check_dependencies.py your-plan.json
```

### Quality Checklist
- ✅ All steps have clear success criteria
- ✅ Dependencies form valid execution order
- ✅ Agent workload is balanced
- ✅ Risk factors are identified and mitigated
- ✅ Validation checkpoints are strategically placed

## Common Use Cases

### Software Development
- Feature development across frontend, backend, and data layers
- API integration projects requiring business validation
- User experience improvements with technical constraints

### Business Process Improvement
- Workflow automation with user experience considerations
- Data pipeline development with business validation
- Compliance implementations across multiple systems

### Digital Transformation
- Platform migrations with user training requirements
- Multi-channel experience development
- Legacy system modernization with business continuity

## Integration Tips

### With VSCode Copilot Agents
- Reference planning files in agent conversations
- Use step deliverables as conversation context
- Leverage validation checkpoints for quality gates

### With Development Tools
- Map planning steps to project management tickets
- Align deliverables with documentation structure
- Use validation criteria for definition-of-done

### With Team Workflows
- Share planning files for team alignment
- Use dependency analysis for resource planning
- Leverage templates for consistent project structure

## Troubleshooting

### Common Issues

**"Complexity level seems wrong"**
- Review `complexity-guidelines.md` assessment criteria
- Consider scope, stakeholders, and integration requirements
- Use complexity assessment questionnaire 

**"Dependencies are circular"**
- Run `check_dependencies.py` for analysis
- Review step order and prerequisites
- Consider splitting complex steps

**"Agent workload unbalanced"**
- Review agent distribution in dependency analysis
- Consider redistributing tasks across agents
- Add parallel execution opportunities

**"Validation steps unclear"**
- Review `examples.md` for validation patterns
- Add specific success criteria to each step
- Include measurable outcomes in criteria

## Best Practices

### Planning Phase
- Start with complexity assessment
- Use templates as starting point, customize as needed
- Include all stakeholders in scope definition

### Execution Phase  
- Follow dependency order strictly
- Use validation checkpoints to course-correct
- Update planning file as scope evolves

### Review Phase
- Validate against original success criteria
- Capture lessons learned for future projects
- Update templates based on experience

## Advanced Features

### Custom Template Creation
Extend existing templates by:
1. Copying similar complexity template
2. Modifying steps for specific domain needs
3. Adjusting validation patterns
4. Testing with validation scripts

### Workflow Optimization
Use dependency analysis to:
- Identify critical path and bottlenecks
- Optimize for parallel execution
- Balance agent workload
- Minimize project duration

### Risk Management Integration
- Map risk factors to mitigation steps
- Include risk validation in checkpoints
- Escalate based on risk thresholds
- Update risk assessment at phase gates

## Contributing

To improve this skill:
1. Add new templates for specific project types
2. Enhance validation scripts with additional checks
3. Contribute examples and patterns to reference docs
4. Suggest improvements to auto-activation triggers

## Version History

- **v1.0** - Initial implementation with core templates and validation
- **Future** - Enhanced risk management, integration with external project tools

---

*This skill follows the [VSCode Agent Skills specification](https://code.visualstudio.com/docs/copilot/customization/agent-skills) and is designed for progressive disclosure and auto-activation based on project complexity requirements.*