#!/usr/bin/env python3
"""
Planning Workflow Creation Script

This script helps create new planning files for agent collaboration
based on project complexity and requirements.

Usage: python create_plan.py [options]
"""

import json
import sys
import os
import argparse
from datetime import datetime
from typing import Dict, List, Any
import shutil

class PlanCreator:
    def __init__(self):
        self.script_dir = os.path.dirname(os.path.abspath(__file__))
        self.skill_dir = os.path.dirname(self.script_dir)
        self.templates_dir = os.path.join(self.skill_dir, 'templates')
        
        self.complexity_templates = {
            'simple': 'simple-project.json',
            'moderate': 'moderate-project.json', 
            'complex': 'complex-project.json',
            'enterprise': 'enterprise-project.json'
        }
    
    def get_available_templates(self) -> List[str]:
        """Get list of available complexity templates."""
        available = []
        for complexity, filename in self.complexity_templates.items():
            template_path = os.path.join(self.templates_dir, filename)
            if os.path.exists(template_path):
                available.append(complexity)
        return available
    
    def load_template(self, complexity: str) -> Dict[str, Any]:
        """Load a template based on complexity level."""
        if complexity not in self.complexity_templates:
            raise ValueError(f"Unknown complexity: {complexity}")
        
        template_file = self.complexity_templates[complexity]
        template_path = os.path.join(self.templates_dir, template_file)
        
        if not os.path.exists(template_path):
            raise FileNotFoundError(f"Template not found: {template_path}")
        
        with open(template_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def customize_template(self, template: Dict[str, Any], customizations: Dict[str, Any]) -> Dict[str, Any]:
        """Apply customizations to the template."""
        customized = template.copy()
        
        # Basic customizations
        if 'task_name' in customizations:
            customized['task_name'] = customizations['task_name']
        
        if 'description' in customizations:
            customized['description'] = customizations['description']
        
        if 'duration' in customizations:
            customized['estimated_duration'] = customizations['duration']
        
        # Advanced customizations
        if 'exclude_agents' in customizations:
            excluded = set(customizations['exclude_agents'])
            steps = customized.get('steps', [])
            customized['steps'] = [
                step for step in steps 
                if step.get('agent') not in excluded
            ]
            self._recalculate_dependencies(customized['steps'])
        
        if 'focus_areas' in customizations:
            self._prioritize_focus_areas(customized, customizations['focus_areas'])
        
        # Add metadata
        customized['_metadata'] = {
            'created_date': datetime.now().isoformat(),
            'template_source': template.get('complexity_level'),
            'customizations_applied': list(customizations.keys())
        }
        
        return customized
    
    def _recalculate_dependencies(self, steps: List[Dict[str, Any]]):
        """Recalculate dependencies after removing steps."""
        step_ids = {step['id'] for step in steps}
        
        for step in steps:
            original_deps = step.get('dependencies', [])
            valid_deps = [dep for dep in original_deps if dep in step_ids]
            step['dependencies'] = valid_deps
    
    def _prioritize_focus_areas(self, plan: Dict[str, Any], focus_areas: List[str]):
        """Adjust plan based on focus areas."""
        # This could be expanded to reorder steps, add emphasis, etc.
        plan['focus_areas'] = focus_areas
        
        # Example: If data is a focus, add more data validation steps
        if 'data' in focus_areas:
            steps = plan.get('steps', [])
            for step in steps:
                if '@data-specialist' in step.get('agent', ''):
                    # Add extra validation to data-focused steps
                    criteria = step.get('success_criteria', [])
                    if 'Data quality validated' not in criteria:
                        criteria.append('Data quality validated')
                        step['success_criteria'] = criteria
    
    def interactive_creation(self) -> Dict[str, Any]:
        """Create plan interactively by asking user questions."""
        print("🤖 Agent Collaboration Plan Creator")
        print("=" * 40)
        
        # Get basic information
        task_name = input("\n📝 Project/Task name: ").strip()
        if not task_name:
            task_name = "Untitled Project"
        
        description = input("📄 Brief description: ").strip()
        if not description:
            description = "Project description to be defined"
        
        # Choose complexity
        available_complexities = self.get_available_templates()
        print(f"\n🎯 Available complexity levels: {', '.join(available_complexities)}")
        
        complexity = None
        while not complexity:
            user_input = input("Select complexity level: ").strip().lower()
            if user_input in available_complexities:
                complexity = user_input
            else:
                print(f"Please choose from: {', '.join(available_complexities)}")
        
        # Optional customizations
        print(f"\n⚙️ Optional customizations (press Enter to skip):")
        
        duration = input("Custom duration estimate: ").strip()
        
        exclude_input = input("Exclude agents (comma-separated, e.g., @creative-specialist): ").strip()
        exclude_agents = [agent.strip() for agent in exclude_input.split(',') if agent.strip()] if exclude_input else []
        
        focus_input = input("Focus areas (comma-separated, e.g., data,security): ").strip()
        focus_areas = [area.strip() for area in focus_input.split(',') if area.strip()] if focus_input else []
        
        # Build customizations
        customizations = {
            'task_name': task_name,
            'description': description
        }
        
        if duration:
            customizations['duration'] = duration
        
        if exclude_agents:
            customizations['exclude_agents'] = exclude_agents
        
        if focus_areas:
            customizations['focus_areas'] = focus_areas
        
        return self.create_plan(complexity, customizations)
    
    def create_plan(self, complexity: str, customizations: Dict[str, Any] = None) -> Dict[str, Any]:
        """Create a new plan based on complexity and customizations."""
        template = self.load_template(complexity)
        
        if customizations:
            plan = self.customize_template(template, customizations)
        else:
            plan = template
        
        return plan
    
    def save_plan(self, plan: Dict[str, Any], output_file: str = None) -> str:
        """Save the plan to a file."""
        if not output_file:
            task_name = plan.get('task_name', 'untitled').lower()
            # Sanitize filename
            filename = ''.join(c if c.isalnum() or c in '-_' else '_' for c in task_name)
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            output_file = f"plan_{filename}_{timestamp}.json"
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(plan, f, indent=2, ensure_ascii=False)
        
        return output_file
    
    def preview_plan(self, plan: Dict[str, Any]) -> str:
        """Generate a preview summary of the plan."""
        lines = []
        lines.append(f"📋 Plan Preview: {plan.get('task_name', 'Untitled')}")
        lines.append(f"📄 Description: {plan.get('description', 'No description')}")
        lines.append(f"⏱️  Duration: {plan.get('estimated_duration', 'Unknown')}")
        lines.append(f"🎯 Complexity: {plan.get('complexity_level', 'Unknown')}")
        
        steps = plan.get('steps', [])
        lines.append(f"\n📝 Steps ({len(steps)}):")
        
        for step in steps:
            step_id = step.get('id', '?')
            agent = step.get('agent', '?')
            task = step.get('task', 'No task description')
            duration = step.get('estimated_time', '?')
            lines.append(f"  {step_id}. {agent}: {task} ({duration})")
        
        # Show agent distribution
        agent_counts = {}
        for step in steps:
            agent = step.get('agent', 'unknown')
            agent_counts[agent] = agent_counts.get(agent, 0) + 1
        
        lines.append(f"\n👥 Agent Distribution:")
        for agent, count in sorted(agent_counts.items()):
            lines.append(f"  {agent}: {count} step(s)")
        
        return "\n".join(lines)

def main():
    parser = argparse.ArgumentParser(description='Create agent collaboration planning files')
    parser.add_argument('--complexity', choices=['simple', 'moderate', 'complex', 'enterprise'],
                       help='Complexity level for the project')
    parser.add_argument('--task-name', help='Name of the task/project')
    parser.add_argument('--description', help='Project description')
    parser.add_argument('--duration', help='Estimated duration')
    parser.add_argument('--output', help='Output file path')
    parser.add_argument('--interactive', action='store_true', help='Interactive mode')
    parser.add_argument('--preview-only', action='store_true', help='Preview only, do not save')
    parser.add_argument('--exclude-agents', nargs='+', help='Agents to exclude from the plan')
    parser.add_argument('--focus-areas', nargs='+', help='Areas to focus on')
    
    args = parser.parse_args()
    
    creator = PlanCreator()
    
    try:
        if args.interactive:
            # Interactive mode
            plan = creator.interactive_creation()
        else:
            # Command line mode
            if not args.complexity:
                print("Error: --complexity is required in non-interactive mode")
                available = creator.get_available_templates()
                print(f"Available complexity levels: {', '.join(available)}")
                sys.exit(1)
            
            # Build customizations
            customizations = {}
            if args.task_name:
                customizations['task_name'] = args.task_name
            if args.description:
                customizations['description'] = args.description
            if args.duration:
                customizations['duration'] = args.duration
            if args.exclude_agents:
                customizations['exclude_agents'] = args.exclude_agents
            if args.focus_areas:
                customizations['focus_areas'] = args.focus_areas
            
            plan = creator.create_plan(args.complexity, customizations)
        
        # Show preview
        print("\n" + creator.preview_plan(plan))
        
        if not args.preview_only:
            output_file = creator.save_plan(plan, args.output)
            print(f"\n✅ Plan saved to: {output_file}")
            
            # Suggest validation
            script_dir = os.path.dirname(os.path.abspath(__file__))
            validate_script = os.path.join(script_dir, 'validate_plan.py')
            if os.path.exists(validate_script):
                print(f"💡 To validate: python {validate_script} {output_file}")
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()