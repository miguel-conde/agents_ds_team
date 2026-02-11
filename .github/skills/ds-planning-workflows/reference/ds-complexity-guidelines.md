# DS Complexity Guidelines

## DS Complexity Assessment

When planning a data science project, use this framework to determine the appropriate complexity level and planning template.

### DS Complexity Dimensions

#### Data Complexity
- **Simple**: Single data source, structured data, <1M records
- **Moderate**: 2-3 data sources, some joins required, 1-100M records
- **Complex**: Multiple sources, real-time + batch, >100M records, unstructured data
- **Enterprise**: Multi-domain data, regulatory constraints, PII/PHI, cross-system integration

#### Model Complexity
- **Simple**: Single model, standard algorithms (logistic regression, random forest)
- **Moderate**: Multiple models, feature engineering pipeline, A/B testing
- **Complex**: Advanced ML (deep learning, time series), model ensembles, real-time inference
- **Enterprise**: Multi-model systems, AutoML, continuous learning, regulatory validation

#### Production Requirements
- **Simple**: Batch predictions, manual deployment, basic monitoring
- **Moderate**: Automated deployment, basic drift monitoring, rollback capability
- **Complex**: Real-time serving, comprehensive monitoring, A/B testing, canary deployment
- **Enterprise**: Full MLOps, governance, audit trails, multi-environment deployment

#### Business Impact
- **Simple**: Departmental use, <$100K impact, proof of concept
- **Moderate**: Cross-functional impact, $100K-$1M impact, operational improvements
- **Complex**: Strategic initiative, $1M-$10M impact, revenue-driving
- **Enterprise**: Mission-critical, >$10M impact, regulatory compliance required

## DS Complexity Assessment Questionnaire

### Data Assessment
1. **How many data sources need integration?**
   - 1 source → Simple
   - 2-3 sources → Moderate  
   - 4-10 sources → Complex
   - >10 sources → Enterprise

2. **What is the data volume and velocity?**
   - Batch, <1M records → Simple
   - Batch, <100M records → Moderate
   - Streaming + batch, >100M records → Complex
   - Real-time, multi-modal, >1B records → Enterprise

3. **Are there data quality concerns?**
   - Clean, structured data → Simple
   - Some quality issues, mostly structured → Moderate
   - Significant quality challenges, mixed data types → Complex
   - Legacy systems, complex transformations required → Enterprise

### Model Assessment
4. **How many models are required?**
   - Single model, single use case → Simple
   - 2-3 models, related use cases → Moderate
   - Model pipeline, multiple use cases → Complex
   - Model ecosystem, platform approach → Enterprise

5. **What are the performance requirements?**
   - Offline analysis, no strict SLAs → Simple
   - Batch predictions, weekly updates → Moderate
   - Real-time inference, <100ms latency → Complex
   - High-frequency, <10ms latency, 99.99% uptime → Enterprise

6. **Is temporal validation critical?**
   - No temporal dependencies → Simple
   - Some seasonal patterns → Moderate
   - Critical temporal validation, leakage risks → Complex
   - Complex temporal dynamics, regulatory requirements → Enterprise

### Production Assessment
7. **What deployment patterns are needed?**
   - Manual deployment, development environment only → Simple
   - Automated deployment, single environment → Moderate
   - Multi-environment CI/CD, staging + production → Complex
   - Global deployment, multiple regions, governance → Enterprise

8. **What monitoring is required?**
   - Basic performance tracking → Simple
   - Data drift monitoring, alerting → Moderate
   - Comprehensive observability, automated responses → Complex
   - Enterprise monitoring, audit trails, compliance → Enterprise

### Business Assessment
9. **Who are the stakeholders?**
   - Single team, technical users → Simple
   - Cross-functional team, mixed technical background → Moderate
   - Multiple departments, executive visibility → Complex
   - Board-level visibility, regulatory oversight → Enterprise

10. **What is the business impact?**
    - Department efficiency, <$100K impact → Simple
    - Cross-functional efficiency, $100K-$1M impact → Moderate
    - Revenue impact, $1M-$10M impact → Complex
    - Strategic initiative, >$10M impact, mission-critical → Enterprise

## Scoring and Recommendation

### Scoring Method
- Count responses in each category (Simple=1, Moderate=2, Complex=3, Enterprise=4)
- Calculate average score across all 10 questions
- Use weighted average if business impact is particularly high/low

### Complexity Mapping
- **Score 1.0-1.5** → Simple DS Project
- **Score 1.6-2.5** → Moderate DS Project  
- **Score 2.6-3.5** → Complex DS Project
- **Score 3.6-4.0** → Enterprise DS Project

## DS Project Templates by Complexity

### Simple DS (2-4 weeks)
- **Template**: [simple-ds-project.json](../templates/simple-ds-project.json)
- **Agents**: @data-scientist + @ds-validator
- **Deliverables**: Model + basic evaluation + documentation
- **Validation Gates**: 1 validation checkpoint
- **Example**: Customer segmentation, simple recommendation system

### Moderate DS (4-12 weeks)  
- **Template**: [moderate-ds-project.json](../templates/moderate-ds-project.json)
- **Agents**: @data-engineer + @data-scientist + @ds-validator
- **Deliverables**: Data pipeline + model + basic deployment
- **Validation Gates**: 3 validation checkpoints (data, model, deployment)
- **Example**: [Churn prediction](../examples/plan-churn-prediction.json)

### Complex DS (12-24 weeks)
- **Template**: [complex-ds-project.json](../templates/complex-ds-project.json) 
- **Agents**: @data-engineer + @data-scientist + @ml-engineer + @ds-validator
- **Deliverables**: Production ML system + comprehensive monitoring
- **Validation Gates**: 5+ validation checkpoints with rigorous testing
- **Example**: [Pharma MMM](../examples/plan-mmm-pharma.json)

### Enterprise DS (24+ weeks)
- **Template**: [enterprise-ds-project.json](../templates/enterprise-ds-project.json)
- **Agents**: Full DS team + governance + compliance specialists
- **Deliverables**: Enterprise ML platform + full MLOps + audit capabilities
- **Validation Gates**: Continuous validation with regulatory compliance
- **Example**: Bank-wide risk modeling, clinical trial optimization

## Common Upgrade Scenarios

### When Projects Grow in Complexity
Projects often start simple but grow in complexity. Watch for these signals:

#### Simple → Moderate
- Stakeholder scope expands beyond original team
- Data quality issues discovered requiring pipeline work
- Business requests regular model updates

#### Moderate → Complex  
- Real-time inference requirements emerge
- Model performance critical to business operations
- Multiple models needed for full solution

#### Complex → Enterprise
- Regulatory compliance requirements identified
- Multi-region or global deployment needed
- Audit and governance requirements imposed

### Complexity Management Strategies

#### For Underestimated Complexity
1. **Phase the project**: Break into smaller deliverables
2. **Upgrade templates**: Move to higher complexity template
3. **Add specialists**: Include additional agents (DE, MLE)
4. **Increase validation**: Add more validation checkpoints

#### For Overestimated Complexity
1. **Simplify scope**: Reduce deliverables to core requirements
2. **Use simpler tools**: Choose less complex technology stack
3. **Reduce agents**: Remove unnecessary specialist involvement
4. **Streamline validation**: Focus on critical quality gates only

## Red Flags and Warnings

### High-Risk Combinations
- **High business impact + Simple approach**: Likely underestimated
- **Enterprise data + Moderate timeline**: Technical complexity underestimated
- **Regulatory constraints + Complex timeline**: Compliance overhead underestimated
- **Real-time requirements + Moderate complexity**: Infrastructure needs underestimated

### Success Predictors
- **Complexity assessment alignment**: Template matches actual project needs
- **Stakeholder buy-in**: All agents and reviewers identified and committed
- **Realistic timelines**: Duration estimates include validation and iteration
- **Clear success criteria**: Quantifiable business impact and technical metrics