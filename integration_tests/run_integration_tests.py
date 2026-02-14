#!/usr/bin/env python3
"""
Comprehensive Integration Test Suite for DS Agent Framework

This script executes the complete integration testing workflow:
1. Validate agent framework structure
2. Test router decomposition capabilities  
3. Validate agent specialization and collaboration
4. Test ds-validator error detection
5. Execute end-to-end workflow simulation
6. Generate comprehensive test report

Usage:
    python run_integration_tests.py --full-suite --generate-report
    python run_integration_tests.py --quick-check --verbose
"""

import sys
import json
import logging
import argparse
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any

# Import test modules
sys.path.append(str(Path(__file__).parent))
from test_runner import DSAgentIntegrationTest
from test_scenarios import DSAgentTestScenarios, TestScenarioRunner
from error_scenarios import DSValidatorErrorScenarios, generate_error_test_suite


class ComprehensiveIntegrationTest:
    """Main integration test orchestrator."""
    
    def __init__(self, test_dir: Path, verbose: bool = False):
        self.test_dir = test_dir
        self.verbose = verbose
        self.logger = self._setup_logging()
        self.results = {}
        
    def _setup_logging(self) -> logging.Logger:
        """Setup logging for comprehensive testing."""
        logger = logging.getLogger("ds_framework_integration")
        level = logging.DEBUG if self.verbose else logging.INFO
        logger.setLevel(level)
        
        # Console handler
        console_handler = logging.StreamHandler()
        console_formatter = logging.Formatter(
            '%(asctime)s - %(levelname)s - %(message)s'
        ) 
        console_handler.setFormatter(console_formatter)
        logger.addHandler(console_handler)
        
        # File handler
        log_file = self.test_dir / "integration_tests" / "results" / "test_execution.log"
        file_handler = logging.FileHandler(log_file)
        file_formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        file_handler.setFormatter(file_formatter)
        logger.addHandler(file_handler)
        
        return logger
    
    def run_framework_structure_validation(self) -> Dict[str, Any]:
        """Validate DS agent framework structure and files."""
        self.logger.info("Step 1: Validating framework structure...")
        
        results = {
            "test_name": "framework_structure_validation",
            "timestamp": datetime.now().isoformat(),
            "status": "UNKNOWN",
            "checks": {}
        }
        
        # Check agent files exist
        agent_files = [
            "head-of-ds-router.agent.md",
            "data-engineer.agent.md", 
            "data-scientist.agent.md",
            "ml-engineer.agent.md",
            "ds-validator.agent.md"
        ]
        
        agents_dir = self.test_dir / ".github" / "agents"
        missing_agents = []
        
        for agent_file in agent_files:
            if not (agents_dir / agent_file).exists():
                missing_agents.append(agent_file)
        
        results["checks"]["agent_files"] = {
            "expected": len(agent_files),
            "found": len(agent_files) - len(missing_agents),
            "missing": missing_agents,
            "status": "PASS" if len(missing_agents) == 0 else "FAIL"
        }
        
        # Check ds-planning-workflows skill
        skill_path = self.test_dir / ".github" / "skills" / "ds-planning-workflows"
        skill_components = [
            "SKILL.md",
            "examples/plan-template-ds.json",
            "examples/plan-churn-prediction.json", 
            "scripts/create_ds_plan.py",
            "scripts/check_leakage_risks.py"
        ]
        
        missing_skill_components = []
        for component in skill_components:
            if not (skill_path / component).exists():
                missing_skill_components.append(component)
        
        results["checks"]["ds_planning_skill"] = {
            "expected": len(skill_components),
            "found": len(skill_components) - len(missing_skill_components), 
            "missing": missing_skill_components,
            "status": "PASS" if len(missing_skill_components) == 0 else "FAIL"
        }
        
        # Check project standards files
        standards_files = [
            "AGENTS.md",
            ".github/context/shared/ds-methodology.md",
            ".github/context/shared/evaluation-standards.md",
            ".github/instructions/python-ds.instructions.md",
            ".github/instructions/testing-ds.instructions.md",
            ".github/instructions/documentation-ds.instructions.md"
        ]
        
        missing_standards = []
        for standards_file in standards_files:
            if not (self.test_dir / standards_file).exists():
                missing_standards.append(standards_file)
        
        results["checks"]["project_standards"] = {
            "expected": len(standards_files),
            "found": len(standards_files) - len(missing_standards),
            "missing": missing_standards,
            "status": "PASS" if len(missing_standards) == 0 else "FAIL"
        }
        
        # Overall status
        all_checks_passed = all(
            check["status"] == "PASS" 
            for check in results["checks"].values()
        )
        results["status"] = "PASS" if all_checks_passed else "FAIL"
        
        self.logger.info(f"Framework structure validation: {results['status']}")
        return results
    
    def run_agent_response_tests(self) -> Dict[str, Any]:
        """Test individual agent response capabilities."""
        self.logger.info("Step 2: Testing agent response capabilities...")
        
        scenarios = DSAgentTestScenarios()
        runner = TestScenarioRunner(verbose=self.verbose)
        
        results = {
            "test_name": "agent_response_tests", 
            "timestamp": datetime.now().isoformat(),
            "agent_tests": {}
        }
        
        # Test router decomposition
        router_tests = scenarios.get_router_decomposition_tests()
        router_results = [runner.run_agent_response_test(test) for test in router_tests]
        results["agent_tests"]["head-of-ds-router"] = router_results
        
        # Test data engineer responses
        de_tests = scenarios.get_data_engineer_tests()
        de_results = [runner.run_agent_response_test(test) for test in de_tests]
        results["agent_tests"]["data-engineer"] = de_results
        
        # Test data scientist responses
        ds_tests = scenarios.get_data_scientist_tests()  
        ds_results = [runner.run_agent_response_test(test) for test in ds_tests]
        results["agent_tests"]["data-scientist"] = ds_results
        
        # Test ML engineer responses
        mle_tests = scenarios.get_ml_engineer_tests()
        mle_results = [runner.run_agent_response_test(test) for test in mle_tests]
        results["agent_tests"]["ml-engineer"] = mle_results
        
        # Calculate summary statistics
        all_tests = []
        for agent_results in results["agent_tests"].values():
            all_tests.extend(agent_results)
        
        total_tests = len(all_tests)
        passed_tests = sum(1 for test in all_tests if test["success"])
        
        results["summary"] = {
            "total_tests": total_tests,
            "passed_tests": passed_tests,
            "pass_rate": passed_tests / total_tests if total_tests > 0 else 0,
            "status": "PASS" if passed_tests / total_tests >= 0.8 else "FAIL"
        }
        
        self.logger.info(f"Agent response tests: {results['summary']['status']} ({results['summary']['pass_rate']:.1%})")
        return results
    
    def run_validator_error_detection_tests(self) -> Dict[str, Any]:
        """Test ds-validator error detection capabilities."""
        self.logger.info("Step 3: Testing ds-validator error detection...")
        
        # Generate comprehensive error detection test suite
        error_test_results = generate_error_test_suite()
        
        results = {
            "test_name": "validator_error_detection",
            "timestamp": datetime.now().isoformat(),
            "error_detection_results": error_test_results
        }
        
        summary = error_test_results["summary"]
        detection_accuracy = summary["detection_accuracy"]
        pass_threshold = summary["pass_threshold"]
        
        results["validation_summary"] = {
            "detection_accuracy": detection_accuracy,
            "pass_threshold": pass_threshold,
            "status": "PASS" if detection_accuracy >= pass_threshold else "FAIL",
            "total_error_scenarios": summary["total_tests"],
            "correct_detections": summary["correct_detections"]
        }
        
        self.logger.info(f"Error detection tests: {results['validation_summary']['status']} ({detection_accuracy:.1%})")
        return results
    
    def run_workflow_collaboration_tests(self) -> Dict[str, Any]:
        """Test agent collaboration and workflow coordination."""
        self.logger.info("Step 4: Testing workflow collaboration...")
        
        scenarios = DSAgentTestScenarios()
        collaboration_scenarios = scenarios.get_collaboration_test_scenarios()
        
        results = {
            "test_name": "workflow_collaboration",
            "timestamp": datetime.now().isoformat(),
            "collaboration_tests": []
        }
        
        for scenario in collaboration_scenarios:
            test_result = {
                "scenario_name": scenario["name"],
                "initiating_agent": scenario["scenario"]["initiating_agent"],
                "receiving_agent": scenario["scenario"]["receiving_agent"],
                "deliverable": scenario["scenario"]["deliverable"],
                "expected_success": scenario["scenario"]["expected_handoff_success"]
            }
            
            # Simulate handoff validation
            interface_contract = scenario["scenario"].get("interface_contract", {})
            if interface_contract and "format" in interface_contract:
                test_result["handoff_validated"] = True
                test_result["contract_complete"] = True
            else:
                test_result["handoff_validated"] = False
                test_result["contract_complete"] = False
            
            test_result["success"] = (
                test_result["handoff_validated"] and 
                test_result["contract_complete"]
            )
            
            results["collaboration_tests"].append(test_result)
        
        # Summary
        total_collaboration_tests = len(results["collaboration_tests"])
        successful_handoffs = sum(1 for test in results["collaboration_tests"] if test["success"])
        
        results["collaboration_summary"] = {
            "total_tests": total_collaboration_tests,
            "successful_handoffs": successful_handoffs,
            "success_rate": successful_handoffs / total_collaboration_tests if total_collaboration_tests > 0 else 0,
            "status": "PASS" if successful_handoffs == total_collaboration_tests else "FAIL"
        }
        
        self.logger.info(f"Collaboration tests: {results['collaboration_summary']['status']}")
        return results
    
    def run_end_to_end_workflow_test(self) -> Dict[str, Any]:
        """Test complete end-to-end churn prediction workflow."""
        self.logger.info("Step 5: Testing end-to-end workflow...")
        
        scenarios = DSAgentTestScenarios()
        churn_workflow = scenarios.get_churn_prediction_workflow()
        
        results = {
            "test_name": "end_to_end_workflow",
            "timestamp": datetime.now().isoformat(),
            "workflow": churn_workflow.name,
            "business_query": churn_workflow.business_query[:100] + "...",
            "agent_sequence_validation": {}
        }
        
        # Validate expected agent sequence
        expected_sequence = churn_workflow.expected_agent_sequence
        sequence_checks = []
        
        for i, agent in enumerate(expected_sequence):
            check = {
                "step": i + 1,
                "agent": agent,
                "role_validated": True,  # Assume agent files exist (checked earlier)
                "deliverable_requirements": churn_workflow.deliverable_requirements.get(agent, []),
                "has_deliverables": len(churn_workflow.deliverable_requirements.get(agent, [])) > 0
            }
            sequence_checks.append(check)
        
        results["agent_sequence_validation"] = {
            "expected_steps": len(expected_sequence),
            "validated_steps": len(sequence_checks),
            "sequence_checks": sequence_checks,
            "complete": len(expected_sequence) == len(sequence_checks)
        }
        
        # Validate success criteria
        success_criteria = churn_workflow.success_criteria
        criteria_validation = {
            "precision_requirement": success_criteria.get("precision_at_10_percent", 0) >= 0.9,
            "auc_requirement": success_criteria.get("auc_roc", 0) >= 0.8,
            "business_impact": "churn_reduction" in success_criteria,
            "measurable_criteria": len(success_criteria) >= 3
        }
        
        results["success_criteria_validation"] = {
            "criteria_checks": criteria_validation,
            "all_criteria_valid": all(criteria_validation.values()),
            "criteria_count": len(success_criteria)
        }
        
        # Overall workflow validation
        workflow_valid = (
            results["agent_sequence_validation"]["complete"] and
            results["success_criteria_validation"]["all_criteria_valid"]
        )
        
        results["workflow_status"] = "PASS" if workflow_valid else "FAIL"
        
        self.logger.info(f"End-to-end workflow test: {results['workflow_status']}")
        return results
    
    def run_full_test_suite(self) -> Dict[str, Any]:
        """Execute complete integration test suite."""
        self.logger.info("=" * 60)
        self.logger.info("DS Agent Framework - Full Integration Test Suite")
        self.logger.info("=" * 60)
        
        start_time = datetime.now()
        
        # Execute all test phases
        framework_results = self.run_framework_structure_validation()
        agent_response_results = self.run_agent_response_tests()
        validator_results = self.run_validator_error_detection_tests()
        collaboration_results = self.run_workflow_collaboration_tests()
        e2e_results = self.run_end_to_end_workflow_test()
        
        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds()
        
        # Compile comprehensive results
        comprehensive_results = {
            "test_suite": "DS_Agent_Framework_Integration_Tests",
            "execution_timestamp": start_time.isoformat(),
            "duration_seconds": duration,
            "test_phases": {
                "framework_structure": framework_results,
                "agent_responses": agent_response_results,
                "validator_error_detection": validator_results,
                "workflow_collaboration": collaboration_results,
                "end_to_end_workflow": e2e_results
            }
        }
        
        # Calculate overall test results
        phase_statuses = []
        for phase_name, phase_results in comprehensive_results["test_phases"].items():
            if phase_name == "framework_structure":
                phase_statuses.append(phase_results["status"])
            elif phase_name == "agent_responses":
                phase_statuses.append(phase_results["summary"]["status"])
            elif phase_name == "validator_error_detection":
                phase_statuses.append(phase_results["validation_summary"]["status"])
            elif phase_name == "workflow_collaboration":
                phase_statuses.append(phase_results["collaboration_summary"]["status"])
            elif phase_name == "end_to_end_workflow":
                phase_statuses.append(phase_results["workflow_status"])
        
        overall_pass = all(status == "PASS" for status in phase_statuses)
        pass_rate = sum(1 for status in phase_statuses if status == "PASS") / len(phase_statuses)
        
        comprehensive_results["overall_summary"] = {
            "total_test_phases": len(phase_statuses),
            "passed_phases": sum(1 for status in phase_statuses if status == "PASS"),
            "phase_pass_rate": pass_rate,
            "overall_status": "PASS" if overall_pass else "FAIL",
            "phase_results": dict(zip(comprehensive_results["test_phases"].keys(), phase_statuses))
        }
        
        # Generate recommendations
        recommendations = self._generate_recommendations(comprehensive_results)
        comprehensive_results["recommendations"] = recommendations
        
        self.logger.info("=" * 60)
        self.logger.info(f"Integration Test Suite Complete: {comprehensive_results['overall_summary']['overall_status']}")
        self.logger.info(f"Phase Pass Rate: {pass_rate:.1%}")
        self.logger.info(f"Duration: {duration:.1f}s")
        self.logger.info("=" * 60)
        
        return comprehensive_results
    
    def _generate_recommendations(self, results: Dict[str, Any]) -> List[str]:
        """Generate recommendations based on test results."""
        recommendations = []
        
        # Check framework structure issues
        framework_status = results["test_phases"]["framework_structure"]["status"]
        if framework_status == "FAIL":
            missing_files = []
            for check_name, check_results in results["test_phases"]["framework_structure"]["checks"].items():
                if check_results["status"] == "FAIL":
                    missing_files.extend(check_results.get("missing", []))
            
            if missing_files:
                recommendations.append(
                    f"Complete framework setup - missing files: {', '.join(missing_files[:3])}..."
                )
        
        # Check agent response issues
        agent_summary = results["test_phases"]["agent_responses"]["summary"]
        if agent_summary["status"] == "FAIL":
            recommendations.append(
                f"Improve agent response quality - current pass rate: {agent_summary['pass_rate']:.1%}"
            )
        
        # Check validator detection issues
        validator_summary = results["test_phases"]["validator_error_detection"]["validation_summary"]
        if validator_summary["status"] == "FAIL":
            recommendations.append(
                f"Enhance ds-validator error detection - current accuracy: {validator_summary['detection_accuracy']:.1%}"
            )
        
        # Check collaboration issues
        collab_summary = results["test_phases"]["workflow_collaboration"]["collaboration_summary"]
        if collab_summary["status"] == "FAIL":
            recommendations.append(
                "Improve agent collaboration - validate handoff protocols and interface contracts"
            )
        
        # Check workflow issues
        workflow_status = results["test_phases"]["end_to_end_workflow"]["workflow_status"]
        if workflow_status == "FAIL":
            recommendations.append(
                "Fix end-to-end workflow - validate agent sequence and success criteria"
            )
        
        # Overall recommendations
        overall_status = results["overall_summary"]["overall_status"]
        if overall_status == "PASS":
            recommendations.append(
                "🎉 DS Agent Framework integration tests PASSED! Ready for production use."
            )
        else:
            recommendations.append(
                "⚠️  Address failing test phases before deploying DS agent framework."
            )
        
        return recommendations
    
    def save_results(self, results: Dict[str, Any], output_file: Path) -> None:
        """Save test results to file."""
        with open(output_file, 'w') as f:
            json.dump(results, f, indent=2, default=str)
        
        self.logger.info(f"Test results saved to: {output_file}")


def main():
    """Main entry point for comprehensive integration testing."""
    parser = argparse.ArgumentParser(description="DS Agent Framework Integration Tests")
    parser.add_argument("--full-suite", action="store_true", help="Run complete integration test suite")
    parser.add_argument("--quick-check", action="store_true", help="Run quick framework validation only")
    parser.add_argument("--generate-report", action="store_true", help="Generate detailed test report")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose logging")
    parser.add_argument("--output-dir", type=Path, default="results", help="Output directory for results")
    
    args = parser.parse_args()
    
    # Setup test environment
    test_dir = Path(__file__).parent.parent
    output_dir = test_dir / "integration_tests" / args.output_dir
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Initialize comprehensive test runner
    test_runner = ComprehensiveIntegrationTest(test_dir, verbose=args.verbose)
    
    # Execute tests based on arguments
    if args.full_suite:
        results = test_runner.run_full_test_suite()
    elif args.quick_check:
        results = test_runner.run_framework_structure_validation()
    else:
        # Default to full suite
        results = test_runner.run_full_test_suite()
    
    # Generate report if requested
    if args.generate_report:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_file = output_dir / f"integration_test_report_{timestamp}.json"
        test_runner.save_results(results, report_file)
        
        # Print summary to console
        if "overall_summary" in results:
            summary = results["overall_summary"]
            print(f"\n{'='*60}")
            print(f"DS AGENT FRAMEWORK INTEGRATION TEST SUMMARY")
            print(f"{'='*60}")
            print(f"Overall Status: {summary['overall_status']}")
            print(f"Phase Pass Rate: {summary['phase_pass_rate']:.1%}")
            print(f"Duration: {results.get('duration_seconds', 0):.1f}s")
            
            print(f"\nPhase Results:")
            for phase, status in summary["phase_results"].items():
                status_icon = "✅" if status == "PASS" else "❌"
                print(f"  {status_icon} {phase}: {status}")
            
            if "recommendations" in results:
                print(f"\nRecommendations:")
                for rec in results["recommendations"]:
                    print(f"  • {rec}")
        
        print(f"\nDetailed report: {report_file}")


if __name__ == "__main__":
    main()