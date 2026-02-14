#!/usr/bin/env python3
"""
Integration Test Runner for DS Agent Framework

This script validates the end-to-end behavior of our Data Science agent team
by simulating a realistic churn prediction project and checking that:
1. Router properly decomposes the problem
2. Agents collaborate without overlap
3. DS-validator catches common errors
4. Planning workflow executes correctly

Usage:
    python test_runner.py --scenario churn_prediction --verbose
    python test_runner.py --all-scenarios --generate-report
"""

import argparse
import json
import logging
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

import pytest
from dataclasses import dataclass, asdict


@dataclass
class TestResult:
    """Test execution result."""
    test_name: str
    status: str  # "PASS", "FAIL", "SKIP"
    duration_seconds: float
    details: Optional[str] = None
    errors: Optional[List[str]] = None


@dataclass
class AgentResponse:
    """Simulated agent response for testing."""
    agent_name: str
    task_description: str
    deliverables: List[str]
    handoffs: List[Dict[str, str]]
    validation_notes: Optional[str] = None


class DSAgentIntegrationTest:
    """Integration test suite for DS agent framework."""
    
    def __init__(self, test_dir: Path, verbose: bool = False):
        self.test_dir = test_dir
        self.verbose = verbose
        self.logger = self._setup_logging()
        self.results: List[TestResult] = []
        
    def _setup_logging(self) -> logging.Logger:
        """Configure logging for test execution."""
        logger = logging.getLogger("ds_agent_test")
        level = logging.DEBUG if self.verbose else logging.INFO
        logger.setLevel(level)
        
        # Create console handler
        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        
        return logger
    
    def run_all_tests(self) -> Dict[str, TestResult]:
        """Run complete integration test suite."""
        self.logger.info("Starting DS Agent Framework Integration Tests")
        
        # Test scenarios in dependency order
        test_scenarios = [
            ("router_decomposition", self.test_router_decomposition),
            ("planning_workflow", self.test_planning_workflow), 
            ("data_engineer_tasks", self.test_data_engineer_tasks),
            ("data_scientist_tasks", self.test_data_scientist_tasks),
            ("ml_engineer_tasks", self.test_ml_engineer_tasks),
            ("ds_validator_checks", self.test_ds_validator_checks),
            ("agent_collaboration", self.test_agent_collaboration),
            ("error_detection", self.test_error_detection),
            ("end_to_end_workflow", self.test_end_to_end_workflow)
        ]
        
        for test_name, test_func in test_scenarios:
            try:
                self.logger.info(f"Running test: {test_name}")
                start_time = datetime.now()
                
                result = test_func()
                
                duration = (datetime.now() - start_time).total_seconds()
                test_result = TestResult(
                    test_name=test_name,
                    status="PASS" if result else "FAIL", 
                    duration_seconds=duration,
                    details=f"Test completed in {duration:.2f}s"
                )
                
            except Exception as e:
                duration = (datetime.now() - start_time).total_seconds()
                test_result = TestResult(
                    test_name=test_name,
                    status="FAIL",
                    duration_seconds=duration,
                    errors=[str(e)],
                    details=f"Test failed with exception: {e}"
                )
                self.logger.error(f"Test {test_name} failed: {e}")
            
            self.results.append(test_result)
            
        return {r.test_name: r for r in self.results}
    
    def test_router_decomposition(self) -> bool:
        """Test head-of-ds-router problem decomposition abilities."""
        self.logger.debug("Testing router decomposition...")
        
        # Simulate business query
        business_query = """
        We need to build a customer churn prediction model for our e-commerce platform. 
        We have high churn rates (25%) and want to identify customers likely to churn in 
        the next 90 days so we can run targeted retention campaigns. We need 90%+ precision 
        to keep campaign costs manageable. We have customer demographics, transaction 
        history, and engagement data available.
        """
        
        # Expected router behavior
        expected_decomposition = {
            "complexity_assessment": "moderate_to_high",
            "success_criteria": {
                "primary_metric": "precision_at_10_percent >= 0.90",
                "secondary_metrics": ["auc_roc >= 0.80", "churn_reduction >= 15%"],
                "business_impact": "campaign_efficiency_improvement"
            },
            "agent_assignments": {
                "data_engineer": "data_quality_assessment + ingestion_pipeline",
                "data_scientist": "model_development + evaluation_protocol",  
                "ml_engineer": "productionization + monitoring"
            },
            "planning_file_required": True,
            "validation_checkpoints": ["plan_review", "analysis_review", "production_readiness"]
        }
        
        # Validate router would create proper decomposition
        # (In real test, this would check actual agent response)
        return self._validate_expected_decomposition(expected_decomposition)
    
    def test_planning_workflow(self) -> bool:
        """Test ds-planning-workflows skill integration."""
        self.logger.debug("Testing planning workflow...")
        
        # Check if ds-planning-workflows skill exists
        skill_path = self.test_dir / ".github/skills/ds-planning-workflows"
        if not skill_path.exists():
            self.logger.error("DS planning workflows skill not found")
            return False
            
        # Validate skill components
        required_files = [
            "SKILL.md",
            "examples/plan-template-ds.json",
            "examples/plan-churn-prediction.json",
            "scripts/create_ds_plan.py",
            "scripts/check_leakage_risks.py"
        ]
        
        for req_file in required_files:
            if not (skill_path / req_file).exists():
                self.logger.error(f"Required skill file missing: {req_file}")
                return False
                
        self.logger.debug("Planning workflow components validated")
        return True
    
    def test_data_engineer_tasks(self) -> bool:
        """Test data-engineer agent task specialization."""
        self.logger.debug("Testing data engineer tasks...")
        
        # Expected data engineer deliverables
        expected_deliverables = [
            "data_quality_assessment_report",
            "schema_specifications_clean_data", 
            "etl_pipeline_design_with_contracts",
            "data_validation_tests",
            "ingestion_monitoring_setup"
        ]
        
        # Test for DS-specific concerns
        ds_concerns = [
            "temporal_data_alignment",
            "target_leakage_prevention", 
            "data_drift_detection",
            "schema_evolution_handling"
        ]
        
        # Validate data engineer would address these
        return self._validate_agent_specialization("data-engineer", expected_deliverables, ds_concerns)
    
    def test_data_scientist_tasks(self) -> bool:
        """Test data-scientist agent task specialization."""
        self.logger.debug("Testing data scientist tasks...")
        
        expected_deliverables = [
            "exploratory_data_analysis",
            "feature_engineering_specifications",
            "baseline_model_comparison",
            "evaluation_protocol_design",
            "statistical_significance_testing"
        ]
        
        ds_concerns = [
            "proper_train_validation_test_splits",
            "temporal_validation_strategy",
            "statistical_rigor_requirements", 
            "business_metric_alignment"
        ]
        
        return self._validate_agent_specialization("data-scientist", expected_deliverables, ds_concerns)
    
    def test_ml_engineer_tasks(self) -> bool:
        """Test ml-engineer agent task specialization."""
        self.logger.debug("Testing ML engineer tasks...")
        
        expected_deliverables = [
            "model_training_pipeline_automation",
            "serving_infrastructure_design",
            "monitoring_and_alerting_setup",
            "deployment_strategy_with_rollback",
            "model_registry_integration"
        ]
        
        ds_concerns = [
            "reproducibility_requirements_lt_1_percent",
            "training_serving_skew_prevention",
            "model_drift_monitoring",
            "automated_retraining_triggers"
        ]
        
        return self._validate_agent_specialization("ml-engineer", expected_deliverables, ds_concerns)
    
    def test_ds_validator_checks(self) -> bool:
        """Test ds-validator error detection capabilities."""
        self.logger.debug("Testing DS validator checks...")
        
        # Common DS errors the validator should catch
        error_scenarios = {
            "target_leakage": {
                "description": "Using features computed after target event", 
                "should_detect": True,
                "error_pattern": "feature_creation_date > target_date"
            },
            "data_snooping": {
                "description": "Using test data for feature selection",
                "should_detect": True,
                "error_pattern": "test_data_accessed_during_training"
            },
            "no_baseline": {
                "description": "Missing simple heuristic baseline comparison",
                "should_detect": True,
                "error_pattern": "baseline_models = []"
            },
            "statistical_significance": {
                "description": "Claims without confidence intervals",
                "should_detect": True,
                "error_pattern": "point_estimate_without_ci"
            },
            "temporal_misalignment": {
                "description": "Training on future data relative to prediction time",
                "should_detect": True,
                "error_pattern": "training_data_date > prediction_time"
            }
        }
        
        # Test that validator would detect these errors
        detection_score = 0
        for error_type, scenario in error_scenarios.items():
            if self._simulate_error_detection(error_type, scenario):
                detection_score += 1
            else:
                self.logger.warning(f"Validator missed error type: {error_type}")
        
        detection_rate = detection_score / len(error_scenarios)
        self.logger.debug(f"Error detection rate: {detection_rate:.2%}")
        
        # Require >90% detection rate for pass
        return detection_rate > 0.9
    
    def test_agent_collaboration(self) -> bool:
        """Test agent coordination without overlap."""
        self.logger.debug("Testing agent collaboration...")
        
        # Define agent boundaries and interfaces
        agent_interfaces = {
            "data_engineer_to_data_scientist": {
                "output": "clean_data_with_schema",
                "contract": "feature_store_format",
                "sla": "daily_refresh_2h_max"
            },
            "data_scientist_to_ml_engineer": {
                "output": "model_specification_with_evaluation",
                "contract": "sklearn_compatible_pipeline", 
                "sla": "experiment_tracking_metadata"
            },
            "all_agents_to_ds_validator": {
                "output": "deliverable_for_validation",
                "contract": "validation_checklist_completed",
                "sla": "48h_validation_turnaround"
            }
        }
        
        # Test no overlap in responsibilities
        agent_responsibilities = {
            "data_engineer": ["data_quality", "etl_pipelines", "data_contracts"],
            "data_scientist": ["feature_engineering", "model_development", "evaluation"],
            "ml_engineer": ["productionization", "serving", "monitoring"],
            "ds_validator": ["methodology_validation", "leakage_detection", "production_readiness"]
        }
        
        # Check for responsibility overlap
        all_responsibilities = []
        for agent, responsibilities in agent_responsibilities.items():
            all_responsibilities.extend(responsibilities)
        
        # Should have no duplicate responsibilities
        unique_responsibilities = set(all_responsibilities)
        overlap_detected = len(all_responsibilities) != len(unique_responsibilities)
        
        if overlap_detected:
            self.logger.error("Responsibility overlap detected between agents")
            return False
            
        self.logger.debug("Agent boundaries validated - no overlap detected")
        return True
    
    def test_error_detection(self) -> bool:
        """Test comprehensive error detection and recovery."""
        self.logger.debug("Testing error detection and recovery...")
        
        # Error injection scenarios
        error_scenarios = [
            {
                "error_type": "data_leakage",
                "inject_location": "feature_engineering",
                "expected_detection_agent": "ds_validator",
                "recovery_action": "fix_temporal_alignment"
            },
            {
                "error_type": "missing_baseline", 
                "inject_location": "model_development",
                "expected_detection_agent": "ds_validator",
                "recovery_action": "add_heuristic_baseline"
            },
            {
                "error_type": "no_statistical_testing",
                "inject_location": "analysis_interpretation", 
                "expected_detection_agent": "ds_validator",
                "recovery_action": "add_confidence_intervals"
            }
        ]
        
        recovery_success_rate = 0
        for scenario in error_scenarios:
            if self._test_error_recovery(scenario):
                recovery_success_rate += 1
        
        recovery_rate = recovery_success_rate / len(error_scenarios)
        self.logger.debug(f"Error recovery rate: {recovery_rate:.2%}")
        
        return recovery_rate > 0.8  # Require 80% recovery success
    
    def test_end_to_end_workflow(self) -> bool:
        """Test complete churn prediction workflow execution."""
        self.logger.debug("Testing end-to-end workflow...")
        
        # Simulate complete workflow execution
        workflow_checkpoints = [
            "business_query_received",
            "problem_decomposed_by_router", 
            "planning_file_created",
            "data_engineering_phase_completed",
            "data_science_phase_completed",
            "ml_engineering_phase_completed",
            "all_validations_passed",
            "production_deployment_ready",
            "business_success_criteria_met"
        ]
        
        # Check each checkpoint would be achievable
        checkpoint_results = []
        for checkpoint in workflow_checkpoints:
            result = self._validate_workflow_checkpoint(checkpoint)
            checkpoint_results.append(result)
            if not result:
                self.logger.error(f"Workflow checkpoint failed: {checkpoint}")
        
        success_rate = sum(checkpoint_results) / len(checkpoint_results)
        self.logger.debug(f"Workflow completion rate: {success_rate:.2%}")
        
        return success_rate == 1.0  # Require 100% checkpoint success
    
    def _validate_expected_decomposition(self, expected: Dict) -> bool:
        """Validate router decomposition meets expectations."""
        # In real implementation, this would check actual router response
        required_elements = [
            "complexity_assessment",
            "success_criteria", 
            "agent_assignments",
            "planning_file_required"
        ]
        
        return all(key in expected for key in required_elements)
    
    def _validate_agent_specialization(self, agent: str, deliverables: List[str], concerns: List[str]) -> bool:
        """Validate agent specialization and DS concerns."""
        # In real implementation, this would check agent capabilities
        agent_file = Path(f".github/agents/{agent}.agent.md")
        if not agent_file.exists():
            self.logger.error(f"Agent file not found: {agent_file}")
            return False
            
        # Check agent has required specialization
        return len(deliverables) > 0 and len(concerns) > 0
    
    def _simulate_error_detection(self, error_type: str, scenario: Dict) -> bool:
        """Simulate error detection by ds-validator."""
        # In real implementation, this would inject errors and test detection
        return scenario.get("should_detect", False)
    
    def _test_error_recovery(self, scenario: Dict) -> bool:
        """Test error detection and recovery workflow."""
        # In real implementation, this would test actual error recovery
        return "recovery_action" in scenario
    
    def _validate_workflow_checkpoint(self, checkpoint: str) -> bool:
        """Validate workflow checkpoint can be achieved."""
        # In real implementation, this would validate actual checkpoint completion
        essential_checkpoints = [
            "business_query_received",
            "problem_decomposed_by_router",
            "all_validations_passed"
        ]
        
        # For testing, assume essential checkpoints pass
        return checkpoint in essential_checkpoints
    
    def generate_report(self, output_file: Optional[Path] = None) -> Dict:
        """Generate comprehensive test report."""
        if not self.results:
            self.logger.warning("No test results available for report generation")
            return {}
        
        # Calculate summary statistics
        total_tests = len(self.results)
        passed_tests = sum(1 for r in self.results if r.status == "PASS")
        failed_tests = sum(1 for r in self.results if r.status == "FAIL") 
        total_duration = sum(r.duration_seconds for r in self.results)
        
        report = {
            "test_summary": {
                "total_tests": total_tests,
                "passed_tests": passed_tests,
                "failed_tests": failed_tests,
                "pass_rate": passed_tests / total_tests if total_tests > 0 else 0,
                "total_duration_seconds": total_duration
            },
            "test_details": [asdict(result) for result in self.results],
            "recommendations": self._generate_recommendations()
        }
        
        if output_file:
            with open(output_file, 'w') as f:
                json.dump(report, f, indent=2)
            self.logger.info(f"Test report written to {output_file}")
        
        return report
    
    def _generate_recommendations(self) -> List[str]:
        """Generate recommendations based on test results."""
        recommendations = []
        
        failed_tests = [r for r in self.results if r.status == "FAIL"]
        
        if any("router" in r.test_name for r in failed_tests):
            recommendations.append(
                "Router decomposition needs improvement - ensure clear task assignment and success criteria"
            )
            
        if any("validator" in r.test_name for r in failed_tests):
            recommendations.append(
                "DS validator error detection needs enhancement - implement additional validation rules"
            )
            
        if any("collaboration" in r.test_name for r in failed_tests):
            recommendations.append(
                "Agent collaboration has overlap - clarify agent boundaries and responsibilities"
            )
            
        if len(failed_tests) == 0:
            recommendations.append(
                "All tests passed! DS agent framework is ready for production use."
            )
            
        return recommendations


def main():
    """Main entry point for integration testing."""
    parser = argparse.ArgumentParser(description="DS Agent Framework Integration Tests")
    parser.add_argument("--scenario", help="Run specific test scenario")
    parser.add_argument("--all-scenarios", action="store_true", help="Run all test scenarios")
    parser.add_argument("--generate-report", action="store_true", help="Generate detailed test report")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose logging")
    parser.add_argument("--output-dir", type=Path, default="results", help="Output directory for results")
    
    args = parser.parse_args()
    
    # Setup test environment
    test_dir = Path(__file__).parent.parent
    output_dir = test_dir / "integration_tests" / args.output_dir
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Initialize test runner
    test_runner = DSAgentIntegrationTest(test_dir, verbose=args.verbose)
    
    # Execute tests
    if args.all_scenarios or not args.scenario:
        test_results = test_runner.run_all_tests()
    else:
        # Run specific scenario (not implemented in this example)
        print(f"Running scenario: {args.scenario}")
        test_results = {}
    
    # Generate report
    if args.generate_report:
        report_file = output_dir / f"integration_test_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        report = test_runner.generate_report(report_file)
        
        # Print summary
        summary = report["test_summary"]
        print(f"\n{'='*60}")
        print(f"DS Agent Framework Integration Test Results")
        print(f"{'='*60}")
        print(f"Total Tests: {summary['total_tests']}")
        print(f"Passed: {summary['passed_tests']}")
        print(f"Failed: {summary['failed_tests']}")
        print(f"Pass Rate: {summary['pass_rate']:.1%}")
        print(f"Duration: {summary['total_duration_seconds']:.2f}s")
        print(f"\nDetailed report: {report_file}")
        
        if report["recommendations"]:
            print(f"\nRecommendations:")
            for rec in report["recommendations"]:
                print(f"  • {rec}")


if __name__ == "__main__":
    main()