#!/usr/bin/env python3
"""
Planning Workflow Validation Script

This script validates the structure, dependencies, and logical consistency 
of agent collaboration planning files used by the VSCode Copilot agent system.

Usage: python validate_plan.py <plan_file.json>
"""

import json
import sys
import os
from datetime import datetime
from typing import Dict, List, Set, Any, Tuple

class PlanValidator:
    def __init__(self, plan_file: str):
        self.plan_file = plan_file
        self.plan_data = None
        self.errors = []
        self.warnings = []
        
    def load_plan(self) -> bool:
        """Load and parse the planning file."""
        try:
            with open(self.plan_file, 'r', encoding='utf-8') as f:
                self.plan_data = json.load(f)
            return True
        except FileNotFoundError:
            self.errors.append(f"File not found: {self.plan_file}")
            return False
        except json.JSONDecodeError as e:
            self.errors.append(f"Invalid JSON format: {str(e)}")
            return False
        except Exception as e:
            self.errors.append(f"Error loading file: {str(e)}")
            return False
    
    def validate_structure(self) -> bool:
        """Validate the basic structure of the planning file."""
        required_fields = [
            'task_name', 'description', 'estimated_duration', 
            'complexity_level', 'steps', 'validation_criteria'
        ]
        
        for field in required_fields:
            if field not in self.plan_data:
                self.errors.append(f"Missing required field: {field}")
        
        # Validate complexity level
        valid_complexity = ['simple', 'moderate', 'complex', 'enterprise']
        complexity = self.plan_data.get('complexity_level')
        if complexity and complexity not in valid_complexity:
            self.errors.append(f"Invalid complexity level: {complexity}. Must be one of {valid_complexity}")
        
        # Validate steps structure
        steps = self.plan_data.get('steps', [])
        if not isinstance(steps, list) or len(steps) == 0:
            self.errors.append("Steps must be a non-empty list")
        
        return len(self.errors) == 0
    
    def validate_agents(self) -> bool:
        """Validate that all referenced agents exist in the system."""
        valid_agents = [
            '@router', '@tech-specialist', '@business-specialist',
            '@creative-specialist', '@data-specialist', '@validator'
        ]
        
        steps = self.plan_data.get('steps', [])
        for step in steps:
            agent = step.get('agent')
            if not agent:
                self.errors.append(f"Step {step.get('id', 'unknown')} missing agent assignment")
            elif agent not in valid_agents:
                self.warnings.append(f"Unknown agent '{agent}' in step {step.get('id')}. Valid agents: {valid_agents}")
        
        return True
    
    def validate_dependencies(self) -> bool:
        """Validate step dependencies for logical consistency."""
        steps = self.plan_data.get('steps', [])
        step_ids = {step.get('id') for step in steps}
        
        # Check for duplicate step IDs
        if len(step_ids) != len(steps):
            self.errors.append("Duplicate step IDs detected")
        
        # Validate dependency references
        for step in steps:
            step_id = step.get('id')
            dependencies = step.get('dependencies', [])
            
            for dep in dependencies:
                if dep not in step_ids:
                    self.errors.append(f"Step {step_id} references non-existent dependency: {dep}")
                elif dep >= step_id:
                    self.errors.append(f"Step {step_id} has forward or self dependency: {dep}")
        
        # Check for circular dependencies
        if self._has_circular_dependencies(steps):
            self.errors.append("Circular dependencies detected in step workflow")
        
        return len(self.errors) == 0
    
    def _has_circular_dependencies(self, steps: List[Dict]) -> bool:
        """Check for circular dependencies using DFS."""
        step_deps = {step['id']: step.get('dependencies', []) for step in steps}
        visited = set()
        rec_stack = set()
        
        def dfs(node):
            visited.add(node)
            rec_stack.add(node)
            
            for neighbor in step_deps.get(node, []):
                if neighbor not in visited:
                    if dfs(neighbor):
                        return True
                elif neighbor in rec_stack:
                    return True
            
            rec_stack.remove(node)
            return False
        
        for step_id in step_deps:
            if step_id not in visited:
                if dfs(step_id):
                    return True
        
        return False
    
    def validate_deliverables(self) -> bool:
        """Validate deliverable naming and consistency."""
        steps = self.plan_data.get('steps', [])
        deliverables = set()
        
        for step in steps:
            deliverable = step.get('deliverable')
            if not deliverable:
                self.warnings.append(f"Step {step.get('id')} missing deliverable specification")
            elif deliverable in deliverables:
                self.warnings.append(f"Duplicate deliverable name: {deliverable}")
            else:
                deliverables.add(deliverable)
                
                # Check naming convention
                if not deliverable.endswith('.md'):
                    self.warnings.append(f"Deliverable '{deliverable}' should end with .md for consistency")
        
        return True
    
    def validate_time_estimates(self) -> bool:
        """Validate time estimates for reasonableness."""
        steps = self.plan_data.get('steps', [])
        total_time_days = 0
        
        time_units = {
            'days': 1, 'day': 1,
            'weeks': 7, 'week': 7, 
            'months': 30, 'month': 30
        }
        
        for step in steps:
            time_est = step.get('estimated_time', '')
            if time_est:
                # Parse time estimate (e.g., "1-2 weeks", "3 days")
                try:
                    # Simple parsing - extract numbers and units
                    import re
                    matches = re.findall(r'(\d+)(?:-(\d+))?\s*(\w+)', time_est.lower())
                    if matches:
                        min_time, max_time, unit = matches[0]
                        multiplier = time_units.get(unit, 1)
                        days = int(max_time or min_time) * multiplier
                        total_time_days += days
                except:
                    self.warnings.append(f"Could not parse time estimate in step {step.get('id')}: '{time_est}'")
        
        # Compare with overall estimated duration
        overall_duration = self.plan_data.get('estimated_duration', '')
        if 'week' in overall_duration.lower():
            import re
            weeks_match = re.search(r'(\d+)(?:-(\d+))?\s*weeks?', overall_duration.lower())
            if weeks_match:
                max_weeks = int(weeks_match.group(2) or weeks_match.group(1))
                if total_time_days > max_weeks * 7 * 1.5:  # 50% buffer
                    self.warnings.append(f"Step time estimates ({total_time_days} days) seem high compared to overall duration")
        
        return True
    
    def validate_success_criteria(self) -> bool:
        """Validate success criteria completeness."""
        steps = self.plan_data.get('steps', [])
        
        for step in steps:
            criteria = step.get('success_criteria', [])
            if not criteria:
                self.warnings.append(f"Step {step.get('id')} missing success criteria")
            elif len(criteria) < 2:
                self.warnings.append(f"Step {step.get('id')} has minimal success criteria (consider adding more)")
        
        # Validate overall validation criteria
        overall_criteria = self.plan_data.get('validation_criteria', [])
        if len(overall_criteria) < 3:
            self.warnings.append("Consider adding more comprehensive validation criteria for the overall project")
        
        return True
    
    def generate_report(self) -> str:
        """Generate a validation report."""
        report = [f"Planning File Validation Report: {self.plan_file}"]
        report.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report.append("=" * 60)
        
        if not self.errors and not self.warnings:
            report.append("✅ VALIDATION PASSED - No issues found")
        else:
            if self.errors:
                report.append(f"❌ ERRORS ({len(self.errors)}):")
                for i, error in enumerate(self.errors, 1):
                    report.append(f"  {i}. {error}")
                report.append("")
            
            if self.warnings:
                report.append(f"⚠️  WARNINGS ({len(self.warnings)}):")
                for i, warning in enumerate(self.warnings, 1):
                    report.append(f"  {i}. {warning}")
                report.append("")
        
        # Add summary statistics
        if self.plan_data:
            steps = self.plan_data.get('steps', [])
            report.append("📊 PLAN SUMMARY:")
            report.append(f"  • Complexity: {self.plan_data.get('complexity_level', 'unknown')}")
            report.append(f"  • Steps: {len(steps)}")
            report.append(f"  • Duration: {self.plan_data.get('estimated_duration', 'unknown')}")
            
            # Count agents
            agents = [step.get('agent') for step in steps]
            agent_counts = {}
            for agent in agents:
                agent_counts[agent] = agent_counts.get(agent, 0) + 1
            report.append(f"  • Agent distribution: {dict(agent_counts)}")
        
        return "\n".join(report)
    
    def validate(self) -> bool:
        """Run complete validation."""
        if not self.load_plan():
            return False
        
        self.validate_structure()
        self.validate_agents() 
        self.validate_dependencies()
        self.validate_deliverables()
        self.validate_time_estimates()
        self.validate_success_criteria()
        
        return len(self.errors) == 0

def main():
    if len(sys.argv) != 2:
        print("Usage: python validate_plan.py <plan_file.json>")
        sys.exit(1)
    
    plan_file = sys.argv[1]
    if not os.path.exists(plan_file):
        print(f"Error: File not found: {plan_file}")
        sys.exit(1)
    
    validator = PlanValidator(plan_file)
    is_valid = validator.validate()
    
    print(validator.generate_report())
    
    sys.exit(0 if is_valid else 1)

if __name__ == "__main__":
    main()