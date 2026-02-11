#!/usr/bin/env python3
"""
Create DS Planning Files

This script helps generate data science planning files based on complexity assessment
and business requirements.
"""

import argparse
import json
import os
from datetime import datetime
from pathlib import Path

def load_template(complexity_level):
    """Load the appropriate DS planning template."""
    template_map = {
        'simple': 'simple-ds-project.json',
        'moderate': 'moderate-ds-project.json', 
        'complex': 'complex-ds-project.json',
        'enterprise': 'enterprise-ds-project.json'
    }
    
    template_file = template_map.get(complexity_level)
    if not template_file:
        raise ValueError(f"Unknown complexity level: {complexity_level}")
    
    template_path = Path(__file__).parent.parent / 'templates' / template_file
    
    if not template_path.exists():
        # Fall back to moderate template if specific template doesn't exist
        template_path = Path(__file__).parent.parent / 'templates' / 'moderate-ds-project.json'
    
    with open(template_path, 'r') as f:
        return json.load(f)

def customize_template(template, task_name, description):
    """Customize template with user inputs."""
    template['task_name'] = task_name
    template['description'] = description
    template['creation_date'] = datetime.now().isoformat()
    template['creation_tool'] = 'create_ds_plan.py'
    
    return template

def generate_plan_filename(task_name):
    """Generate standardized filename for plan."""
    # Clean task name and create filename
    clean_name = task_name.lower().replace(' ', '-').replace('_', '-')
    return f"plan-ds-{clean_name}.json"

def save_plan(plan, filename, output_dir='.'):
    """Save the planning file."""
    output_path = Path(output_dir) / filename
    
    with open(output_path, 'w') as f:
        json.dump(plan, f, indent=2)
    
    return output_path

def main():
    parser = argparse.ArgumentParser(
        description='Create DS planning files based on complexity assessment'
    )
    parser.add_argument(
        '--complexity', 
        choices=['simple', 'moderate', 'complex', 'enterprise'],
        required=True,
        help='DS project complexity level'
    )
    parser.add_argument(
        '--task', 
        required=True,
        help='Brief description of the DS task/project'
    )
    parser.add_argument(
        '--description',
        help='Detailed description of the project goals'
    )
    parser.add_argument(
        '--output-dir',
        default='.',
        help='Output directory for the planning file'
    )
    parser.add_argument(
        '--interactive',
        action='store_true',
        help='Interactive mode for additional customization'
    )
    
    args = parser.parse_args()
    
    try:
        # Load template
        template = load_template(args.complexity)
        
        # Use description if provided, otherwise use task
        description = args.description or args.task
        
        # Customize template
        plan = customize_template(template, args.task, description)
        
        # Interactive mode for additional customization
        if args.interactive:
            print(f"\nCustomizing plan for: {args.task}")
            print(f"Complexity level: {args.complexity}")
            
            # Get additional inputs
            duration = input(f"Estimated duration [{plan.get('estimated_duration', '8-12 weeks')}]: ").strip()
            if duration:
                plan['estimated_duration'] = duration
                
            stakeholders = input("Key stakeholders (comma-separated): ").strip()
            if stakeholders:
                plan['stakeholders'] = [s.strip() for s in stakeholders.split(',')]
        
        # Generate filename and save
        filename = generate_plan_filename(args.task)
        output_path = save_plan(plan, filename, args.output_dir)
        
        print(f"\n✅ DS Planning file created successfully!")
        print(f"📁 Location: {output_path}")
        print(f"📊 Complexity: {args.complexity}")
        print(f"🎯 Task: {args.task}")
        
        print(f"\n📝 Next steps:")
        print(f"1. Review and customize the planning file")
        print(f"2. Validate with: python scripts/validate_ds_plan.py {filename}")
        print(f"3. Check for risks: python scripts/check_leakage_risks.py --plan {filename}")
        
    except Exception as e:
        print(f"❌ Error creating DS planning file: {e}")
        return 1
    
    return 0

if __name__ == '__main__':
    exit(main())