#!/usr/bin/env python3
"""
Planning Workflow Dependencies Checker

This script analyzes and visualizes dependencies in agent collaboration
planning files, helping identify bottlenecks and parallel execution opportunities.

Usage: python check_dependencies.py <plan_file.json> [options]
"""

import json
import sys
import os
import argparse
from typing import Dict, List, Set, Any, Tuple
from collections import defaultdict, deque

class DependencyAnalyzer:
    def __init__(self, plan_file: str):
        self.plan_file = plan_file
        self.plan_data = None
        self.steps = []
        self.dependency_graph = {}
        self.reverse_graph = {}
        
    def load_plan(self) -> bool:
        """Load the planning file."""
        try:
            with open(self.plan_file, 'r', encoding='utf-8') as f:
                self.plan_data = json.load(f)
            self.steps = self.plan_data.get('steps', [])
            return True
        except Exception as e:
            print(f"Error loading plan: {e}")
            return False
    
    def build_dependency_graph(self):
        """Build dependency graphs for analysis."""
        # Reset graphs
        self.dependency_graph = {}
        self.reverse_graph = {}
        
        # Build forward and reverse dependency graphs
        for step in self.steps:
            step_id = step['id']
            dependencies = step.get('dependencies', [])
            
            self.dependency_graph[step_id] = dependencies
            
            # Build reverse graph (what depends on this step)
            if step_id not in self.reverse_graph:
                self.reverse_graph[step_id] = []
            
            for dep in dependencies:
                if dep not in self.reverse_graph:
                    self.reverse_graph[dep] = []
                self.reverse_graph[dep].append(step_id)
    
    def topological_sort(self) -> List[List[int]]:
        """Return steps grouped by execution level (parallel groups)."""
        in_degree = {}
        for step_id in self.dependency_graph:
            in_degree[step_id] = len(self.dependency_graph[step_id])
        
        levels = []
        remaining_nodes = set(self.dependency_graph.keys())
        
        while remaining_nodes:
            # Find all nodes with no dependencies (in_degree = 0)
            current_level = [node for node in remaining_nodes if in_degree[node] == 0]
            
            if not current_level:
                # Circular dependency detected
                break
            
            levels.append(current_level)
            remaining_nodes -= set(current_level)
            
            # Update in_degree for remaining nodes
            for node in current_level:
                for dependent in self.reverse_graph.get(node, []):
                    if dependent in remaining_nodes:
                        in_degree[dependent] -= 1
        
        return levels
    
    def find_critical_path(self) -> Tuple[List[int], int]:
        """Find the critical path (longest dependency chain)."""
        def get_step_duration_days(step_id: int) -> int:
            """Estimate step duration in days."""
            step = next((s for s in self.steps if s['id'] == step_id), None)
            if not step:
                return 1
            
            time_est = step.get('estimated_time', '1 day')
            
            # Simple parsing for day estimation
            import re
            if 'week' in time_est.lower():
                weeks = re.findall(r'(\d+)', time_est)
                return int(weeks[-1]) * 7 if weeks else 7
            elif 'month' in time_est.lower():
                months = re.findall(r'(\d+)', time_est)
                return int(months[-1]) * 30 if months else 30
            else:
                days = re.findall(r'(\d+)', time_est)
                return int(days[-1]) if days else 1
        
        # Calculate longest path using DFS with memoization
        memo = {}
        
        def longest_path_from(node: int) -> Tuple[int, List[int]]:
            if node in memo:
                return memo[node]
            
            node_duration = get_step_duration_days(node)
            dependents = self.reverse_graph.get(node, [])
            
            if not dependents:
                # Leaf node
                memo[node] = (node_duration, [node])
                return memo[node]
            
            max_path_length = 0
            max_path = []
            
            for dependent in dependents:
                dep_length, dep_path = longest_path_from(dependent)
                if dep_length > max_path_length:
                    max_path_length = dep_length
                    max_path = dep_path
            
            total_length = node_duration + max_path_length
            total_path = [node] + max_path
            memo[node] = (total_length, total_path)
            return memo[node]
        
        # Find the critical path starting from any node
        max_length = 0
        critical_path = []
        
        for step_id in self.dependency_graph.keys():
            length, path = longest_path_from(step_id)
            if length > max_length:
                max_length = length
                critical_path = path
        
        return critical_path, max_length
    
    def analyze_parallelization(self) -> Dict[str, Any]:
        """Analyze parallelization opportunities."""
        levels = self.topological_sort()
        
        analysis = {
            'total_steps': len(self.steps),
            'execution_levels': len(levels),
            'max_parallel_steps': max(len(level) for level in levels) if levels else 0,
            'parallelization_factor': 0,
            'bottlenecks': [],
            'parallel_opportunities': []
        }
        
        if analysis['total_steps'] > 0:
            sequential_time = analysis['total_steps']
            parallel_time = analysis['execution_levels']
            analysis['parallelization_factor'] = round(sequential_time / parallel_time, 2)
        
        # Identify bottlenecks (single-step levels)
        for i, level in enumerate(levels):
            if len(level) == 1:
                step_id = level[0]
                step = next((s for s in self.steps if s['id'] == step_id), None)
                if step:
                    analysis['bottlenecks'].append({
                        'level': i + 1,
                        'step_id': step_id,
                        'agent': step.get('agent'),
                        'task': step.get('task', '')[:50] + '...' if len(step.get('task', '')) > 50 else step.get('task', '')
                    })
        
        # Identify good parallelization opportunities
        for i, level in enumerate(levels):
            if len(level) > 2:
                analysis['parallel_opportunities'].append({
                    'level': i + 1,
                    'step_count': len(level),
                    'steps': level
                })
        
        return analysis
    
    def analyze_agent_workload(self) -> Dict[str, Any]:
        """Analyze workload distribution across agents."""
        agent_workload = defaultdict(list)
        
        for step in self.steps:
            agent = step.get('agent', 'unknown')
            agent_workload[agent].append({
                'step_id': step['id'],
                'task': step.get('task', 'No task'),
                'estimated_time': step.get('estimated_time', 'Unknown')
            })
        
        # Calculate workload balance
        step_counts = [len(steps) for steps in agent_workload.values()]
        avg_workload = sum(step_counts) / len(step_counts) if step_counts else 0
        max_workload = max(step_counts) if step_counts else 0
        min_workload = min(step_counts) if step_counts else 0
        
        return {
            'agent_distribution': dict(agent_workload),
            'workload_balance': {
                'average': round(avg_workload, 1),
                'max': max_workload,
                'min': min_workload,
                'balance_ratio': round(max_workload / avg_workload, 2) if avg_workload > 0 else 0
            }
        }
    
    def find_potential_deadlocks(self) -> List[Dict[str, Any]]:
        """Find potential issues in the dependency structure."""
        issues = []
        
        # Check for orphaned steps (steps with no dependents and non-final)
        levels = self.topological_sort()
        if levels:
            final_level_steps = set(levels[-1])
            
            for step_id, dependents in self.reverse_graph.items():
                if not dependents and step_id not in final_level_steps:
                    step = next((s for s in self.steps if s['id'] == step_id), None)
                    if step:
                        issues.append({
                            'type': 'orphaned_step',
                            'step_id': step_id,
                            'description': f"Step {step_id} has no dependents but is not final",
                            'agent': step.get('agent'),
                            'task': step.get('task', '')
                        })
        
        # Check for steps with too many dependencies
        for step in self.steps:
            dependencies = step.get('dependencies', [])
            if len(dependencies) > 5:  # Threshold for complexity
                issues.append({
                    'type': 'complex_dependencies',
                    'step_id': step['id'],
                    'description': f"Step {step['id']} has {len(dependencies)} dependencies",
                    'dependency_count': len(dependencies),
                    'dependencies': dependencies
                })
        
        return issues
    
    def generate_ascii_timeline(self) -> str:
        """Generate a simple ASCII timeline visualization."""
        levels = self.topological_sort()
        if not levels:
            return "No valid dependency structure found"
        
        lines = []
        lines.append("Execution Timeline (→ = depends on)")
        lines.append("=" * 50)
        
        for level_num, level_steps in enumerate(levels, 1):
            lines.append(f"\n📅 Level {level_num} (Parallel Execution):")
            
            for step_id in level_steps:
                step = next((s for s in self.steps if s['id'] == step_id), None)
                if step:
                    agent = step.get('agent', 'unknown')
                    task = step.get('task', 'No task')
                    duration = step.get('estimated_time', '?')
                    
                    # Show dependencies
                    deps = step.get('dependencies', [])
                    dep_str = f" → {deps}" if deps else ""
                    
                    lines.append(f"  [{step_id}] {agent}: {task[:40]}... ({duration}){dep_str}")
        
        return "\n".join(lines)
    
    def generate_report(self) -> str:
        """Generate comprehensive dependency analysis report."""
        if not self.load_plan():
            return "Failed to load planning file"
        
        self.build_dependency_graph()
        
        lines = []
        lines.append(f"🔍 Dependency Analysis Report: {self.plan_file}")
        lines.append("=" * 60)
        
        # Basic stats
        lines.append(f"\n📊 Basic Statistics:")
        lines.append(f"  • Total steps: {len(self.steps)}")
        lines.append(f"  • Total dependencies: {sum(len(deps) for deps in self.dependency_graph.values())}")
        
        # Parallelization analysis
        parallel_analysis = self.analyze_parallelization()
        lines.append(f"\n⚡ Parallelization Analysis:")
        lines.append(f"  • Execution levels: {parallel_analysis['execution_levels']}")
        lines.append(f"  • Max parallel steps: {parallel_analysis['max_parallel_steps']}")
        lines.append(f"  • Parallelization factor: {parallel_analysis['parallelization_factor']}x")
        
        if parallel_analysis['bottlenecks']:
            lines.append(f"\n🚧 Bottlenecks ({len(parallel_analysis['bottlenecks'])}):")
            for bottleneck in parallel_analysis['bottlenecks'][:3]:  # Show first 3
                lines.append(f"  • Level {bottleneck['level']}: Step {bottleneck['step_id']} ({bottleneck['agent']})")
        
        # Critical path
        critical_path, critical_time = self.find_critical_path()
        lines.append(f"\n⏰ Critical Path:")
        lines.append(f"  • Path: {' → '.join(map(str, critical_path))}")
        lines.append(f"  • Estimated time: {critical_time} days")
        
        # Agent workload
        workload_analysis = self.analyze_agent_workload()
        lines.append(f"\n👥 Agent Workload Distribution:")
        for agent, steps in workload_analysis['agent_distribution'].items():
            lines.append(f"  • {agent}: {len(steps)} step(s)")
        
        balance = workload_analysis['workload_balance']
        lines.append(f"  • Balance ratio: {balance['balance_ratio']} (1.0 = perfect balance)")
        
        # Potential issues
        issues = self.find_potential_deadlocks()
        if issues:
            lines.append(f"\n⚠️ Potential Issues ({len(issues)}):")
            for issue in issues[:3]:  # Show first 3
                lines.append(f"  • {issue['type']}: {issue['description']}")
        
        # ASCII timeline
        lines.append(f"\n{self.generate_ascii_timeline()}")
        
        return "\n".join(lines)

def main():
    parser = argparse.ArgumentParser(description='Analyze dependencies in agent collaboration plans')
    parser.add_argument('plan_file', help='Path to the planning JSON file')
    parser.add_argument('--critical-path-only', action='store_true', 
                       help='Show only critical path analysis')
    parser.add_argument('--timeline-only', action='store_true',
                       help='Show only timeline visualization')
    parser.add_argument('--workload-only', action='store_true',
                       help='Show only agent workload analysis')
    
    args = parser.parse_args()
    
    if not os.path.exists(args.plan_file):
        print(f"Error: File not found: {args.plan_file}")
        sys.exit(1)
    
    analyzer = DependencyAnalyzer(args.plan_file)
    
    try:
        if args.critical_path_only:
            analyzer.load_plan()
            analyzer.build_dependency_graph()
            critical_path, critical_time = analyzer.find_critical_path()
            print(f"Critical Path: {' → '.join(map(str, critical_path))}")
            print(f"Estimated Duration: {critical_time} days")
        elif args.timeline_only:
            analyzer.load_plan()
            analyzer.build_dependency_graph()
            print(analyzer.generate_ascii_timeline())
        elif args.workload_only:
            analyzer.load_plan()
            workload = analyzer.analyze_agent_workload()
            print("Agent Workload Distribution:")
            for agent, steps in workload['agent_distribution'].items():
                print(f"  {agent}: {len(steps)} step(s)")
        else:
            print(analyzer.generate_report())
    
    except Exception as e:
        print(f"Error analyzing dependencies: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()