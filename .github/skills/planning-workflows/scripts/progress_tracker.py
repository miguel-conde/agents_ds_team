#!/usr/bin/env python3
"""
Progress Tracking Script for Planning Workflows

This script helps maintain persistent progress tracking for planning workflows
across VSCode sessions by updating plan files or maintaining separate progress files.

Usage: 
  python progress_tracker.py --plan plan-file.json --complete-step 3
  python progress_tracker.py --plan plan-file.json --status
  python progress_tracker.py --plan plan-file.json --reset
"""

import json
import sys
import os
import argparse
from datetime import datetime
from typing import Dict, List, Any, Optional

class ProgressTracker:
    def __init__(self, plan_file: str, use_separate_file: bool = True):
        self.plan_file = plan_file
        self.use_separate_file = use_separate_file
        
        # Determine progress file path
        if use_separate_file:
            base_name = os.path.splitext(plan_file)[0]
            self.progress_file = f"{base_name}.progress.json"
        else:
            self.progress_file = plan_file
            
        self.plan_data = None
        self.progress_data = None
    
    def load_plan(self) -> bool:
        """Load the planning file."""
        try:
            with open(self.plan_file, 'r', encoding='utf-8') as f:
                self.plan_data = json.load(f)
            return True
        except Exception as e:
            print(f"Error loading plan: {e}")
            return False
    
    def load_progress(self) -> bool:
        """Load progress data."""
        if not self.use_separate_file:
            self.progress_data = self.plan_data
            return True
            
        try:
            if os.path.exists(self.progress_file):
                with open(self.progress_file, 'r', encoding='utf-8') as f:
                    self.progress_data = json.load(f)
            else:
                # Initialize new progress file
                self.progress_data = {
                    "plan_file": self.plan_file,
                    "created_date": datetime.now().isoformat(),
                    "last_updated": datetime.now().isoformat(),
                    "completed_steps": [],
                    "current_step": None,
                    "notes": {},
                    "phase_progress": {}
                }
            return True
        except Exception as e:
            print(f"Error loading progress: {e}")
            return False
    
    def complete_step(self, step_id: int, notes: str = None) -> bool:
        """Mark a step as completed."""
        if not self.plan_data or not self.progress_data:
            return False
        
        # Validate step exists
        steps = self.plan_data.get('steps', [])
        step_exists = any(step['id'] == step_id for step in steps)
        
        if not step_exists:
            print(f"Error: Step {step_id} not found in plan")
            return False
        
        if self.use_separate_file:
            # Update progress file
            if step_id not in self.progress_data['completed_steps']:
                self.progress_data['completed_steps'].append(step_id)
                self.progress_data['completed_steps'].sort()
            
            self.progress_data['last_updated'] = datetime.now().isoformat()
            
            if notes:
                self.progress_data['notes'][str(step_id)] = notes
        else:
            # Update plan file directly
            for step in steps:
                if step['id'] == step_id:
                    step['status'] = 'completed'
                    step['completed_date'] = datetime.now().isoformat()
                    if notes:
                        step['completion_notes'] = notes
                    break
        
        return self.save_progress()
    
    def get_status(self) -> Dict[str, Any]:
        """Get current progress status."""
        if not self.plan_data:
            return {}
        
        steps = self.plan_data.get('steps', [])
        total_steps = len(steps)
        
        if self.use_separate_file:
            completed = self.progress_data.get('completed_steps', [])
            completed_count = len(completed)
        else:
            completed = [step['id'] for step in steps if step.get('status') == 'completed']
            completed_count = len(completed)
        
        # Calculate next steps
        next_steps = []
        for step in steps:
            step_id = step['id']
            if step_id not in completed:
                # Check if dependencies are met
                dependencies = step.get('dependencies', [])
                if all(dep in completed for dep in dependencies):
                    next_steps.append(step_id)
        
        return {
            'total_steps': total_steps,
            'completed_count': completed_count,
            'completed_steps': completed,
            'completion_percentage': round((completed_count / total_steps) * 100, 1) if total_steps > 0 else 0,
            'next_available_steps': next_steps,
            'last_updated': self.progress_data.get('last_updated') if self.use_separate_file else datetime.now().isoformat()
        }
    
    def save_progress(self) -> bool:
        """Save progress data."""
        try:
            if self.use_separate_file:
                with open(self.progress_file, 'w', encoding='utf-8') as f:
                    json.dump(self.progress_data, f, indent=2, ensure_ascii=False)
            else:
                with open(self.plan_file, 'w', encoding='utf-8') as f:
                    json.dump(self.plan_data, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"Error saving progress: {e}")
            return False
    
    def reset_progress(self) -> bool:
        """Reset all progress."""
        if self.use_separate_file:
            self.progress_data = {
                "plan_file": self.plan_file,
                "created_date": datetime.now().isoformat(),
                "last_updated": datetime.now().isoformat(),
                "completed_steps": [],
                "current_step": None,
                "notes": {},
                "phase_progress": {}
            }
        else:
            steps = self.plan_data.get('steps', [])
            for step in steps:
                step.pop('status', None)
                step.pop('completed_date', None)
                step.pop('completion_notes', None)
        
        return self.save_progress()
    
    def add_note(self, step_id: int, note: str) -> bool:
        """Add a note to a specific step."""
        if self.use_separate_file:
            self.progress_data['notes'][str(step_id)] = note
            self.progress_data['last_updated'] = datetime.now().isoformat()
        else:
            steps = self.plan_data.get('steps', [])
            for step in steps:
                if step['id'] == step_id:
                    if 'notes' not in step:
                        step['notes'] = []
                    step['notes'].append({
                        'date': datetime.now().isoformat(),
                        'note': note
                    })
                    break
        
        return self.save_progress()
    
    def generate_report(self) -> str:
        """Generate a progress report."""
        status = self.get_status()
        lines = []
        
        lines.append(f"📋 Progress Report: {os.path.basename(self.plan_file)}")
        lines.append("=" * 60)
        
        lines.append(f"📊 Overall Progress: {status['completed_count']}/{status['total_steps']} steps ({status['completion_percentage']}%)")
        lines.append(f"📅 Last Updated: {status['last_updated']}")
        
        if status['completed_steps']:
            lines.append(f"\n✅ Completed Steps: {', '.join(map(str, status['completed_steps']))}")
        
        if status['next_available_steps']:
            lines.append(f"\n⏭️  Next Available Steps: {', '.join(map(str, status['next_available_steps']))}")
        else:
            remaining = status['total_steps'] - status['completed_count']
            if remaining > 0:
                lines.append(f"\n⏳ Waiting for Dependencies: {remaining} steps blocked")
            else:
                lines.append(f"\n🎉 All Steps Completed!")
        
        # Show step details
        if self.plan_data:
            lines.append(f"\n📝 Step Details:")
            steps = self.plan_data.get('steps', [])
            for step in steps:
                step_id = step['id']
                agent = step.get('agent', 'unknown')
                task = step.get('task', 'No description')[:50] + '...' if len(step.get('task', '')) > 50 else step.get('task', '')
                
                if step_id in status['completed_steps']:
                    icon = "✅"
                elif step_id in status['next_available_steps']:
                    icon = "🟡"
                else:
                    icon = "⏳"
                
                lines.append(f"  {icon} [{step_id}] {agent}: {task}")
        
        # Show notes if any
        if self.use_separate_file and self.progress_data.get('notes'):
            lines.append(f"\n📌 Notes:")
            for step_id, note in self.progress_data['notes'].items():
                lines.append(f"  Step {step_id}: {note}")
        
        return "\n".join(lines)

def main():
    parser = argparse.ArgumentParser(description='Track progress of planning workflows')
    parser.add_argument('--plan', required=True, help='Path to planning JSON file')
    parser.add_argument('--complete-step', type=int, help='Mark step as completed')
    parser.add_argument('--note', help='Add note to step (use with --complete-step)')
    parser.add_argument('--add-note', type=int, help='Add note to specific step')
    parser.add_argument('--note-text', help='Note text (use with --add-note)')
    parser.add_argument('--status', action='store_true', help='Show current status')
    parser.add_argument('--reset', action='store_true', help='Reset all progress')
    parser.add_argument('--inline', action='store_true', help='Store progress in plan file instead of separate file')
    parser.add_argument('--report', action='store_true', help='Generate detailed progress report')
    
    args = parser.parse_args()
    
    if not os.path.exists(args.plan):
        print(f"Error: Plan file not found: {args.plan}")
        sys.exit(1)
    
    tracker = ProgressTracker(args.plan, use_separate_file=not args.inline)
    
    if not tracker.load_plan():
        sys.exit(1)
    
    if not tracker.load_progress():
        sys.exit(1)
    
    try:
        if args.complete_step:
            success = tracker.complete_step(args.complete_step, args.note)
            if success:
                print(f"✅ Step {args.complete_step} marked as completed")
            else:
                print(f"❌ Failed to complete step {args.complete_step}")
        
        elif args.add_note:
            if not args.note_text:
                print("Error: --note-text required with --add-note")
                sys.exit(1)
            success = tracker.add_note(args.add_note, args.note_text)
            if success:
                print(f"📝 Note added to step {args.add_note}")
            else:
                print(f"❌ Failed to add note to step {args.add_note}")
        
        elif args.reset:
            success = tracker.reset_progress()
            if success:
                print("🔄 Progress reset successfully")
            else:
                print("❌ Failed to reset progress")
        
        elif args.report:
            print(tracker.generate_report())
        
        elif args.status:
            status = tracker.get_status()
            print(f"Progress: {status['completed_count']}/{status['total_steps']} ({status['completion_percentage']}%)")
            if status['next_available_steps']:
                print(f"Next steps: {', '.join(map(str, status['next_available_steps']))}")
            else:
                remaining = status['total_steps'] - status['completed_count']
                if remaining > 0:
                    print("No steps currently available (waiting for dependencies)")
                else:
                    print("🎉 All steps completed!")
        
        else:
            print("Use --help for available options")
    
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()