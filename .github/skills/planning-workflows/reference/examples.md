# Planning Workflows Examples

This document provides real-world examples of how to apply the planning workflows skill across different project types and complexity levels.

## Table of Contents

1. [Simple Project Examples](#simple-project-examples)
2. [Moderate Project Examples](#moderate-project-examples)
3. [Complex Project Examples](#complex-project-examples)
4. [Enterprise Project Examples](#enterprise-project-examples)
5. [Common Patterns](#common-patterns)
6. [Anti-Patterns to Avoid](#anti-patterns-to-avoid)

## Simple Project Examples

### Example 1: API Endpoint Implementation

**Scenario**: Add a new REST API endpoint to existing service

**Planning File**: Based on simple-project.json
```json
{
  "task_name": "User Profile API Endpoint",
  "description": "Implement GET /api/users/{id}/profile endpoint with authentication",
  "complexity_level": "simple",
  "estimated_duration": "1 week",
  "steps": [
    {
      "id": 1,
      "agent": "@tech-specialist",
      "task": "Design API schema and implement endpoint",
      "estimated_time": "3 days"
    },
    {
      "id": 2,
      "agent": "@validator",
      "task": "Review implementation and test cases",
      "dependencies": [1],
      "estimated_time": "1 day"
    }
  ]
}
```

**Why Simple**: Single domain (technical), clear requirements, no complex integrations.

### Example 2: Bug Fix with Documentation

**Scenario**: Fix authentication bug and update documentation

**Key Characteristics**:
- Clear problem definition
- Single domain expertise required
- Low risk impact
- Well-understood solution approach

**Agent Flow**: tech-specialist → validator → done

### Example 3: UI Component Creation

**Scenario**: Create reusable button component for design system

**Key Characteristics**:
- Creative domain focus
- Clear requirements
- Minimal dependencies
- Low integration complexity

**Agent Flow**: creative-specialist → validator → done

## Moderate Project Examples

### Example 1: Customer Dashboard Enhancement

**Scenario**: Add analytics dashboard to customer portal with data integration

**Planning File**: Based on moderate-project.json
```json
{
  "task_name": "Customer Analytics Dashboard",
  "description": "Integrate analytics data and create interactive dashboard in customer portal",
  "complexity_level": "moderate",
  "estimated_duration": "4-5 weeks",
  "steps": [
    {
      "id": 1,
      "agent": "@business-specialist",
      "task": "Define dashboard requirements and user stories"
    },
    {
      "id": 2,
      "agent": "@data-specialist", 
      "task": "Design analytics data pipeline and API",
      "dependencies": [1]
    },
    {
      "id": 3,
      "agent": "@creative-specialist",
      "task": "Design dashboard UX and components",
      "dependencies": [1]
    },
    {
      "id": 4,
      "agent": "@tech-specialist",
      "task": "Implement frontend and backend integration",
      "dependencies": [2, 3]
    },
    {
      "id": 5,
      "agent": "@validator",
      "task": "End-to-end validation and performance testing",
      "dependencies": [4]
    }
  ]
}
```

**Why Moderate**: Multiple domains, some integration complexity, clear but detailed requirements.

### Example 2: Payment Gateway Integration

**Scenario**: Integrate new payment provider with existing e-commerce system

**Key Characteristics**:
- Technical and business domain collaboration
- External system integration
- Security considerations
- Multi-step validation process

**Agent Flow**: business-specialist → tech-specialist → validator → tech-specialist → validator

**Success Pattern**: Early business validation, incremental technical implementation, multiple validation points.

### Example 3: Mobile App Feature Addition

**Scenario**: Add social sharing feature to mobile application

**Key Characteristics**:
- Creative and technical domains
- Platform-specific considerations
- User experience testing
- App store compliance

**Agent Flow**: business-specialist → creative-specialist → tech-specialist → validator → creative-specialist → validator

## Complex Project Examples

### Example 1: Multi-Platform Recommendation Engine

**Scenario**: Build personalized recommendation system across web and mobile platforms

**Planning File**: Based on complex-project.json (abbreviated)
```json
{
  "task_name": "Personalized Recommendation Engine",
  "description": "Develop ML-powered recommendation system with real-time personalization",
  "complexity_level": "complex", 
  "estimated_duration": "12-14 weeks",
  "phases": [
    {
      "phase": "Research & Strategy",
      "steps": [1, 2, 3, 4]
    },
    {
      "phase": "Architecture & Design", 
      "steps": [5, 6, 7, 8]
    },
    {
      "phase": "Implementation Planning",
      "steps": [9, 10]
    }
  ]
}
```

**Why Complex**: 
- Multiple domains (data science, technology, business, UX)
- Machine learning implementation complexity
- Multi-platform deployment
- Performance and scalability requirements

### Example 2: Legacy System Modernization

**Scenario**: Modernize legacy customer management system while maintaining business continuity

**Key Characteristics**:
- High business risk
- Data migration complexity
- User training requirements  
- Phased rollout strategy
- Compliance considerations

**Agent Collaboration Pattern**:
- Deep business analysis (business-specialist)
- Data architecture assessment (data-specialist)
- Modern platform design (tech-specialist)
- Change management UX (creative-specialist)
- Continuous integration validation (validator)

### Example 3: International Market Expansion Platform

**Scenario**: Adapt existing product for international markets with localization

**Key Characteristics**:
- Multi-cultural UX considerations
- International compliance requirements
- Currency and payment processing
- Multi-language data handling
- Cultural sensitivity in design

**Success Factors**:
- Early cultural research (business-specialist + creative-specialist)
- Flexible data architecture (data-specialist)
- Internationalization framework (tech-specialist)
- Continuous cultural validation (validator)

## Enterprise Project Examples

### Example 1: Digital Transformation Initiative

**Scenario**: Transform traditional retail company into omnichannel digital experience

**Planning File**: Based on enterprise-project.json (high-level)
```json
{
  "task_name": "Omnichannel Digital Transformation",
  "description": "Complete digital transformation enabling seamless online-offline customer experience",
  "complexity_level": "enterprise",
  "estimated_duration": "18-24 months",
  "governance": {
    "steering_committee": ["CEO", "CTO", "CMO"],
    "project_governance": "Stage-gate with board reviews"
  },
  "phases": [
    {
      "phase": "Strategy & Discovery",
      "duration": "12 weeks",
      "critical_milestone": "Board approval for architecture"
    },
    {
      "phase": "Architecture & Platform Design", 
      "duration": "16 weeks",
      "critical_milestone": "Platform vendor selection"
    },
    {
      "phase": "Implementation & Change Management",
      "duration": "52+ weeks" 
    }
  ]
}
```

**Why Enterprise**:
- Strategic corporate initiative
- Multi-year timeline
- Multiple business units
- Regulatory considerations
- Change management across organization

### Example 2: Compliance Platform Implementation

**Scenario**: Implement GDPR compliance platform across global organization

**Key Characteristics**:
- Regulatory requirements
- Legal team collaboration
- Multi-region data considerations
- Audit trail requirements
- Training and certification programs

**Critical Success Factors**:
- Legal compliance validation at each phase
- Data governance framework
- Multi-region technical architecture
- Comprehensive staff training
- Audit and monitoring systems

## Common Patterns

### The Progressive Validation Pattern

**When to Use**: Projects with high risk or uncertainty
**Structure**:
1. Specialist analysis
2. Validator review and feedback
3. Specialist refinement  
4. Validator final approval

**Example Flow**:
```
business-specialist → validator → business-specialist → data-specialist → validator → tech-specialist → validator
```

### The Parallel Development Pattern

**When to Use**: When domains can work independently initially
**Structure**:
1. Requirements gathering (business-specialist)
2. Parallel development (tech + creative + data specialists)
3. Integration validation (validator)
4. Final integration (tech-specialist)

### The Iterative Refinement Pattern

**When to Use**: Complex projects with unclear requirements
**Structure**:
1. Initial analysis (domain specialist)
2. Cross-domain consultation (multiple agents)
3. Validator synthesis and feedback
4. Refined analysis (original specialist)
5. Repeat until convergence

### The Risk-First Pattern

**When to Use**: High-risk or novel technology projects
**Structure**:
1. Risk analysis (validator)
2. Specialist investigation of highest risks
3. Risk mitigation planning (router coordination)
4. Iterative risk reduction implementation

## Anti-Patterns to Avoid

### ❌ The Waterfall Anti-Pattern

**Problem**: Sequential handoffs without feedback loops
```
business-specialist → data-specialist → tech-specialist → creative-specialist → validator
```

**Why Bad**: No opportunity for course correction, late discovery of issues

**Better Approach**: Include validation checkpoints and feedback loops

### ❌ The Validation Bottleneck Anti-Pattern

**Problem**: All validation concentrated at the end
```
specialist → specialist → specialist → validator (everything)
```

**Why Bad**: Late discovery of integration issues, overwhelming validation scope

**Better Approach**: Distributed validation throughout workflow

### ❌ The Missing Router Anti-Pattern

**Problem**: Complex projects without central coordination
- Agents directly coordinating complex handoffs
- No centralized decision making
- Unclear escalation paths

**Better Approach**: Use router for complex multi-agent coordination

### ❌ The Over-Engineering Anti-Pattern

**Problem**: Using complex project templates for simple tasks
- Enterprise-level governance for simple features
- Multiple validation phases for straightforward implementations
- Over-complicated agent orchestration

**Better Approach**: Match complexity level to actual project needs

### ❌ The Scope Creep Anti-Pattern

**Problem**: Starting simple but growing without re-planning
- Simple project becomes complex without updating methodology
- Agent assignments remain static as scope grows
- Validation approach doesn't scale with complexity

**Better Approach**: Regular complexity reassessment and plan updating

## Template Customization Examples

### Removing Unnecessary Agents

**Scenario**: Technical project with no UX component
```json
{
  "exclude_agents": ["@creative-specialist"],
  "adjusted_dependencies": "recalculated automatically"
}
```

### Adding Domain Focus

**Scenario**: Data-heavy project requiring extra validation
```json
{
  "focus_areas": ["data", "validation"],
  "enhanced_steps": [
    "Additional data quality checkpoints",
    "Extended validation procedures"
  ]
}
```

### Timeline Compression

**Scenario**: Urgent project requiring parallel execution
```json
{
  "optimization": "parallel",
  "adjusted_dependencies": "minimized for parallelization",
  "risk_mitigation": "increased validation frequency"
}
```

## Success Metrics Examples

### Simple Project Success Metrics
- Completion within 1 week
- Single revision cycle
- Zero post-deployment issues

### Moderate Project Success Metrics  
- 90% milestone completion on time
- <3 major requirement changes
- User acceptance >85%

### Complex Project Success Metrics
- Phase gate approvals within timeline
- Risk mitigation success rate >90%
- Stakeholder satisfaction >80%

### Enterprise Project Success Metrics
- Board-level milestone achievement
- ROI positive within 12 months
- Organization-wide adoption >75%

## Tools Integration Examples

### Development Tools Integration
```json
{
  "tools_integration": {
    "project_tracking": "Jira tickets creation for each step",
    "code_repository": "Branch creation following step dependencies", 
    "documentation": "Confluence page structure matching deliverables"
  }
}
```

### Communication Integration
```json
{
  "communication_tools": {
    "slack_channels": "Auto-creation per phase",
    "meeting_scheduling": "Validation checkpoints auto-scheduled",
    "reporting": "Weekly progress reports to stakeholders"
  }
}
```

This completes the examples documentation, providing concrete patterns and real-world scenarios for effective use of the planning workflows skill.