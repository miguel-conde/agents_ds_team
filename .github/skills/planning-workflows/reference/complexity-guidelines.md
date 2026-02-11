# Project Complexity Guidelines

This document provides detailed guidelines for determining project complexity levels in agent collaboration workflows. Use this to select appropriate templates and planning approaches.

## Complexity Levels Overview

| Level | Duration | Team Size | Domains | Risk Level | Example Projects |
|-------|----------|-----------|---------|------------|------------------|
| **Simple** | 1-2 weeks | 1-2 agents | 1-2 | Low | Feature implementation, bug fixes |
| **Moderate** | 2-6 weeks | 2-4 agents | 2-3 | Medium | Small product features, integrations |
| **Complex** | 8-16 weeks | 3-5 agents | 3-4 | High | New product modules, platform updates |
| **Enterprise** | 12-24 months | 4-6 agents | 4+ | Very High | Digital transformation, platform rebuilds |

## Detailed Complexity Criteria

### Simple Projects (1-2 weeks)

**Characteristics:**
- Single domain focus (tech, business, or creative)
- Clear, well-defined requirements
- Minimal dependencies on external systems
- Low risk tolerance requirements
- Straightforward implementation path

**Typical Scenarios:**
- Bug fixes with clear reproduction steps
- Small feature additions to existing systems
- Documentation updates or creation
- Simple automation tasks
- Basic UI/UX improvements

**Agent Involvement:**
- Usually 1-2 specialists
- Router for coordination if needed
- Validator for final review

**Decision Criteria:**
- Can be completed by a single domain expert?
- Requirements are completely clear?
- No major integration challenges?
- Low business impact if delayed?

**Example Planning Pattern:**
1. Specialist analysis and implementation
2. Validator review and approval
3. Documentation and handoff

---

### Moderate Projects (2-6 weeks)

**Characteristics:**
- Cross-domain collaboration required
- Some unknowns in requirements or implementation
- Integration with 1-2 existing systems
- Moderate stakeholder involvement
- Manageable risk profile

**Typical Scenarios:**
- New feature development with API integrations
- Data pipeline creation or modification
- User experience improvements across multiple touchpoints
- Security enhancements with compliance requirements
- Performance optimization initiatives

**Agent Involvement:**
- 2-4 specialists working collaboratively
- Router for workflow coordination
- Validator for integration verification
- Multiple validation checkpoints

**Decision Criteria:**
- Requires expertise from 2-3 domains?
- Some research or discovery needed?
- Integration complexity but manageable?
- Multiple stakeholders but clear ownership?

**Example Planning Pattern:**
1. Business analysis and requirements
2. Technical and data architecture design
3. Creative/UX design if applicable
4. Cross-domain integration validation
5. Implementation planning
6. Final validation and approval

---

### Complex Projects (8-16 weeks)

**Characteristics:**
- Multi-domain expertise essential
- Significant unknowns requiring research and discovery
- Integration with multiple systems and platforms
- High stakeholder complexity
- Substantial business impact and risk

**Typical Scenarios:**
- New product line development
- Platform migration or modernization
- Advanced analytics and ML implementation
- Multi-channel user experience redesign
- Enterprise system integrations

**Agent Involvement:**
- 3-5 specialists with deep collaboration
- Router for complex workflow orchestration
- Multiple validation phases with escalation paths
- Cross-agent consultation patterns

**Decision Criteria:**
- Requires deep expertise from 3+ domains?
- Significant research and experimentation needed?
- Complex integration requirements?
- High business stakes with risk management needs?

**Example Planning Pattern:**
1. Comprehensive business strategy and requirements
2. Data landscape analysis and architecture
3. Technical architecture with scalability considerations
4. User experience strategy and design systems
5. Multiple integration validation phases
6. Risk assessment and mitigation planning
7. Implementation roadmap with phased approach
8. Comprehensive final validation

---

### Enterprise Projects (12-24 months)

**Characteristics:**
- Organization-wide transformation
- Board-level strategic importance
- Regulatory and compliance requirements
- Vendor ecosystem coordination
- Change management across multiple business units

**Typical Scenarios:**
- Digital transformation initiatives
- Enterprise platform replacements
- Regulatory compliance implementations (GDPR, SOX, etc.)
- Merger and acquisition technology integration
- Corporate rebranding with technology implications

**Agent Involvement:**
- All 5+ agents with specialized responsibilities
- Router managing complex multi-phase workflows
- Extensive validation with governance checkpoints
- External stakeholder coordination

**Decision Criteria:**
- Strategic corporate initiative?
- Multiple business units affected?
- Regulatory or compliance requirements?
- Board or C-level oversight required?
- Budget exceeding departmental limits?

**Example Planning Pattern:**
- **Phase 1: Strategy & Discovery (8-12 weeks)**
  - Enterprise strategic assessment
  - Technology and data landscape analysis
  - Governance framework establishment
  - Cross-domain strategy validation
  
- **Phase 2: Architecture & Design (12-16 weeks)**
  - Enterprise architecture design
  - Data and analytics platform architecture
  - User experience and design system creation
  - Operating model transformation planning
  - Comprehensive architecture validation
  
- **Phase 3: Implementation Planning (8-12 weeks)**
  - Implementation strategy and deployment planning
  - Change management and adoption strategy
  - Data migration and governance planning
  - Final readiness validation and certification

## Complexity Assessment Questionnaire

Use this questionnaire to help determine the appropriate complexity level:

### Business Impact Assessment

1. **Strategic Importance (0-4 points)**
   - 0: Operational task
   - 1: Department improvement
   - 2: Division impact
   - 3: Company-wide effect
   - 4: Strategic transformation

2. **Stakeholder Scope (0-4 points)**
   - 0: Single person
   - 1: Small team (2-5 people)
   - 2: Department (10-50 people)
   - 3: Multiple departments
   - 4: Enterprise-wide

3. **Budget Impact (0-4 points)**
   - 0: <$1K
   - 1: $1K-$10K
   - 2: $10K-$100K
   - 3: $100K-$1M
   - 4: >$1M

### Technical Complexity Assessment

4. **Domain Expertise Required (0-4 points)**
   - 0: Single domain
   - 1: Two domains
   - 2: Three domains
   - 3: Four domains
   - 4: All domains + external expertise

5. **Integration Complexity (0-4 points)**
   - 0: No integrations
   - 1: Single system integration
   - 2: 2-3 system integrations
   - 3: Complex multi-system integration
   - 4: Enterprise ecosystem integration

6. **Technical Risk (0-4 points)**
   - 0: Well-understood technology
   - 1: Some new technology
   - 2: Moderate technical risk
   - 3: High technical complexity
   - 4: Cutting-edge/experimental technology

### Timeline and Resource Assessment

7. **Estimated Duration (0-4 points)**
   - 0: <1 week
   - 1: 1-2 weeks
   - 2: 2-8 weeks
   - 3: 2-6 months
   - 4: >6 months

8. **Resource Requirements (0-4 points)**
   - 0: 1 person part-time
   - 1: 1-2 people
   - 2: Small team (3-5)
   - 3: Multiple teams
   - 4: Organization-wide resources

### Scoring Guide

**Total Score Ranges:**

- **0-8 points: Simple Project**
  - Use simple-project.json template
  - Focus on single-domain execution
  - Minimal validation requirements

- **9-16 points: Moderate Project**
  - Use moderate-project.json template
  - Cross-domain collaboration
  - Regular validation checkpoints

- **17-24 points: Complex Project**
  - Use complex-project.json template
  - Multi-phase approach
  - Extensive integration validation

- **25-32 points: Enterprise Project**
  - Use enterprise-project.json template
  - Governance and phase gates
  - Comprehensive risk management

## Red Flags for Complexity Escalation

Watch for these indicators that suggest moving to a higher complexity level:

### Technical Red Flags
- Unknown or experimental technology requirements
- Integration with legacy systems without APIs
- Performance requirements exceeding current capabilities
- Security requirements beyond standard frameworks
- Data migration involving multiple source systems

### Business Red Flags
- Unclear or changing requirements
- Multiple competing stakeholder priorities
- Regulatory or compliance implications
- Budget or timeline pressure from leadership
- Dependency on external vendor deliverables

### Organizational Red Flags
- Resistance to change from affected teams
- Skills gaps in required technology areas
- Competing priorities for shared resources
- Previous failed attempts at similar initiatives
- Lack of executive sponsorship for scope

## Planning Approach by Complexity

### Simple Projects
- **Planning Time**: 1-2 hours
- **Validation**: Single final review
- **Documentation**: Basic deliverables
- **Risk Management**: Informal

### Moderate Projects
- **Planning Time**: 1-2 days
- **Validation**: 2-3 checkpoints
- **Documentation**: Structured deliverables
- **Risk Management**: Identified and tracked

### Complex Projects
- **Planning Time**: 1-2 weeks
- **Validation**: Multiple phase gates
- **Documentation**: Comprehensive documentation
- **Risk Management**: Formal risk register

### Enterprise Projects
- **Planning Time**: 2-4 weeks
- **Validation**: Governance board reviews
- **Documentation**: Enterprise documentation standards
- **Risk Management**: Enterprise risk management integration

## Additional Considerations

### When to Simplify
Consider breaking down larger projects if:
- Initial complexity assessment exceeds team capabilities
- Timeline pressure requires faster delivery
- Budget constraints limit scope
- Stakeholder alignment is difficult to achieve

### When to Escalate
Consider moving to higher complexity if:
- Scope increases during initial analysis
- Technical challenges are more complex than anticipated
- Stakeholder requirements expand
- Integration requirements become more demanding

### Adaptive Planning
- Start with appropriate complexity level
- Be prepared to adjust based on discoveries
- Regular complexity reassessment at validation checkpoints
- Clear escalation paths defined upfront