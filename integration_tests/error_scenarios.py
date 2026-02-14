#!/usr/bin/env python3
"""
Error scenarios for testing ds-validator error detection capabilities.

This module contains common data science errors that should be detected
by the ds-validator agent during different phases of a DS project.

Each error scenario includes:
- The type of error being tested
- Artifacts that contain the error
- Expected validator response
- Suggested remediation
"""

import json
from typing import Dict, List, Any
from dataclasses import dataclass


@dataclass
class ErrorScenario:
    """Definition of a DS error scenario for testing."""
    name: str
    phase: str  # "planning", "data_engineering", "analysis", "production"
    error_type: str
    description: str
    artifacts: Dict[str, Any]
    should_be_detected: bool
    expected_feedback: str
    remediation_suggestion: str


class DSValidatorErrorScenarios:
    """Collection of error scenarios for ds-validator testing."""
    
    @staticmethod
    def get_data_leakage_scenarios() -> List[ErrorScenario]:
        """Scenarios testing data leakage detection."""
        return [
            ErrorScenario(
                name="temporal_target_leakage",
                phase="data_engineering",
                error_type="target_leakage",
                description="Features computed after target event date",
                artifacts={
                    "feature_engineering_spec": {
                        "features": [
                            {
                                "name": "total_purchases_after_signup",
                                "computation": "COUNT(purchases) WHERE purchase_date > churn_event_date",
                                "creation_date": "2023-12-01",
                                "target_date": "2023-11-15"  # Feature uses future data!
                            }
                        ]
                    }
                },
                should_be_detected=True,
                expected_feedback="Temporal leakage detected: Feature 'total_purchases_after_signup' uses data from after target event",
                remediation_suggestion="Adjust feature computation window to end before target event date"
            ),
            
            ErrorScenario(
                name="future_information_in_features",
                phase="analysis",
                error_type="data_leakage",
                description="Features that include information from the future",
                artifacts={
                    "model_features": {
                        "customer_id": "CUST_001",
                        "days_since_last_purchase": 30,
                        "total_support_tickets": 5,
                        "support_ticket_after_churn": 2,  # This is future info!
                        "email_open_rate": 0.68,
                        "prediction_date": "2023-11-01",
                        "churn_date": "2023-11-15"
                    }
                },
                should_be_detected=True,
                expected_feedback="Future information leakage: Feature 'support_ticket_after_churn' contains post-prediction data",
                remediation_suggestion="Remove features that use information not available at prediction time"
            ),
            
            ErrorScenario(
                name="valid_temporal_alignment",
                phase="data_engineering", 
                error_type="none",
                description="Properly aligned temporal features (no leakage)",
                artifacts={
                    "feature_engineering_spec": {
                        "features": [
                            {
                                "name": "purchases_30d_before_prediction",
                                "computation": "COUNT(purchases) WHERE purchase_date BETWEEN (prediction_date - 30) AND (prediction_date - 1)",
                                "prediction_date": "2023-11-01",
                                "max_feature_date": "2023-10-31"  # Before prediction
                            }
                        ]
                    }
                },
                should_be_detected=False,
                expected_feedback="Temporal alignment validated - no leakage detected",
                remediation_suggestion="N/A - features properly aligned"
            )
        ]
    
    @staticmethod
    def get_methodology_error_scenarios() -> List[ErrorScenario]:
        """Scenarios testing methodology validation."""
        return [
            ErrorScenario(
                name="missing_baseline_comparison",
                phase="analysis",
                error_type="methodology_error", 
                description="Model evaluation without baseline comparison",
                artifacts={
                    "model_evaluation": {
                        "model_name": "RandomForestClassifier",
                        "performance_metrics": {
                            "auc_roc": 0.85,
                            "precision_at_10": 0.92,
                            "recall": 0.68
                        },
                        "baseline_models": [],  # Missing!
                        "improvement_over_baseline": "not_calculated"
                    }
                },
                should_be_detected=True,
                expected_feedback="Missing baseline comparison - DS methodology requires comparison to simple heuristic baseline",
                remediation_suggestion="Implement random classifier and simple heuristic baseline for comparison"
            ),
            
            ErrorScenario(
                name="data_snooping_violation",
                phase="analysis",
                error_type="data_snooping",
                description="Using test data for feature selection or hyperparameter tuning",
                artifacts={
                    "model_development_log": {
                        "feature_selection": {
                            "method": "recursive_feature_elimination",
                            "evaluation_data": "full_dataset_including_test_set",  # Wrong!
                            "features_selected": ["feature1", "feature2", "feature3"]
                        },
                        "hyperparameter_tuning": {
                            "optimization_metric": "test_set_auc",  # Wrong!
                            "best_params": {"max_depth": 10, "n_estimators": 200}
                        }
                    }
                },
                should_be_detected=True,
                expected_feedback="Data snooping detected - test data used for feature selection and hyperparameter tuning",
                remediation_suggestion="Use only training/validation data for feature selection and hyperparameter optimization"
            ),
            
            ErrorScenario(
                name="no_statistical_significance_testing",
                phase="analysis",
                error_type="statistical_rigor",
                description="Claims without statistical significance testing",
                artifacts={
                    "ab_test_analysis": {
                        "control_group_conversion": 0.12,
                        "treatment_group_conversion": 0.15,
                        "observed_difference": 0.03,
                        "conclusion": "Treatment improved conversion by 25%",
                        "statistical_test": None,  # Missing!
                        "p_value": None,  # Missing!
                        "confidence_interval": None  # Missing!
                    }
                },
                should_be_detected=True,
                expected_feedback="Statistical significance missing - provide p-value and confidence intervals for claims",
                remediation_suggestion="Conduct appropriate statistical test (t-test, chi-square) and calculate confidence intervals"
            ),
            
            ErrorScenario(
                name="valid_methodology",
                phase="analysis",
                error_type="none",
                description="Proper methodology with baselines and statistical testing",
                artifacts={
                    "model_evaluation": {
                        "model_name": "GradientBoostingClassifier",
                        "performance_metrics": {
                            "auc_roc": 0.83,
                            "precision_at_10": 0.89,
                            "confidence_interval": "[0.86, 0.92]"
                        },
                        "baseline_comparison": {
                            "random_classifier": {"auc_roc": 0.50},
                            "heuristic_baseline": {"auc_roc": 0.67},
                            "logistic_regression": {"auc_roc": 0.74}
                        },
                        "statistical_significance": {
                            "test": "paired_t_test_vs_baseline",
                            "p_value": 0.001,
                            "effect_size": "cohens_d = 0.8"
                        }
                    }
                },
                should_be_detected=False,
                expected_feedback="Methodology validation passed - proper baselines and statistical testing",
                remediation_suggestion="N/A - methodology meets DS standards"
            )
        ]
    
    @staticmethod 
    def get_production_readiness_scenarios() -> List[ErrorScenario]:
        """Scenarios testing production readiness validation."""
        return [
            ErrorScenario(
                name="missing_model_monitoring",
                phase="production",
                error_type="monitoring_gap",
                description="Production deployment without proper monitoring",
                artifacts={
                    "deployment_spec": {
                        "model_endpoint": "deployed",
                        "serving_infrastructure": "configured",
                        "monitoring": {
                            "performance_tracking": False,  # Missing!
                            "data_drift_detection": False,  # Missing!
                            "alerting": None  # Missing!
                        },
                        "rollback_procedure": "manual_only"  # Inadequate!
                    }
                },
                should_be_detected=True,
                expected_feedback="Production monitoring insufficient - missing performance tracking and drift detection",
                remediation_suggestion="Implement automated monitoring for model performance, data drift, and system health"
            ),
            
            ErrorScenario(
                name="training_serving_skew",
                phase="production",
                error_type="pipeline_inconsistency",
                description="Different feature computation between training and serving",
                artifacts={
                    "model_pipeline": {
                        "training_features": {
                            "age": "calculated_from_birthdate",
                            "income": "normalized_by_region_median",
                            "tenure": "months_since_signup"
                        },
                        "serving_features": {
                            "age": "provided_directly",  # Different computation!
                            "income": "raw_value",  # Different normalization!
                            "tenure": "days_since_signup"  # Different units!
                        }
                    }
                },
                should_be_detected=True,
                expected_feedback="Training-serving skew detected - feature computation differs between training and production",
                remediation_suggestion="Ensure identical feature computation logic in training and serving pipelines"
            ),
            
            ErrorScenario(
                name="no_reproducibility_guarantee",
                phase="production",
                error_type="reproducibility",
                description="Model training without reproducibility controls",
                artifacts={
                    "training_pipeline": {
                        "random_seeds": "not_set",  # Missing!
                        "environment_specification": "requirements.txt missing specific versions",  # Inadequate!
                        "data_versioning": None,  # Missing!
                        "training_variance": "15% between runs"  # Too high!
                    }
                },
                should_be_detected=True,
                expected_feedback="Reproducibility requirements not met - training variance >1% and missing version controls",
                remediation_suggestion="Fix random seeds, pin package versions, implement data versioning"
            ),
            
            ErrorScenario(
                name="production_ready_system",
                phase="production",
                error_type="none",
                description="Well-configured production system with proper monitoring",
                artifacts={
                    "deployment_spec": {
                        "model_endpoint": "deployed_with_auto_scaling",
                        "monitoring": {
                            "performance_tracking": True,
                            "data_drift_detection": True,
                            "alerting": "configured_with_thresholds",
                            "dashboards": "real_time_grafana"
                        },
                        "rollback_procedure": "automated_on_performance_drop",
                        "testing": {
                            "unit_tests": "100% coverage",
                            "integration_tests": "end_to_end_validation",
                            "load_tests": "production_traffic_simulation"
                        },
                        "reproducibility": {
                            "variance": "0.3% between runs",
                            "versioning": "complete_lineage_tracking"
                        }
                    }
                },
                should_be_detected=False,
                expected_feedback="Production readiness validation passed - monitoring, testing, and reproducibility standards met",
                remediation_suggestion="N/A - system meets production standards"
            )
        ]
    
    @staticmethod
    def get_all_error_scenarios() -> Dict[str, List[ErrorScenario]]:
        """Get all error scenarios organized by category."""
        return {
            "data_leakage": DSValidatorErrorScenarios.get_data_leakage_scenarios(),
            "methodology_errors": DSValidatorErrorScenarios.get_methodology_error_scenarios(), 
            "production_readiness": DSValidatorErrorScenarios.get_production_readiness_scenarios()
        }
    
    @staticmethod
    def validate_error_detection(scenario: ErrorScenario) -> Dict[str, Any]:
        """Simulate ds-validator error detection for a scenario."""
        result = {
            "scenario_name": scenario.name,
            "phase": scenario.phase,
            "error_type": scenario.error_type,
            "should_detect": scenario.should_be_detected
        }
        
        # Simulate detection logic based on error type
        detected = False
        detection_reason = ""
        
        if scenario.error_type == "target_leakage":
            # Check for temporal alignment issues
            artifacts = scenario.artifacts
            if "feature_engineering_spec" in artifacts:
                for feature in artifacts["feature_engineering_spec"].get("features", []):
                    creation_date = feature.get("creation_date")
                    target_date = feature.get("target_date")
                    if creation_date and target_date and creation_date > target_date:
                        detected = True
                        detection_reason = f"Temporal leakage in feature {feature['name']}"
                        break
            
            if "model_features" in artifacts:
                features = artifacts["model_features"]
                prediction_date = features.get("prediction_date")
                churn_date = features.get("churn_date")
                
                # Check for features with "after" in the name
                for key in features.keys():
                    if "after" in key.lower() and prediction_date and churn_date:
                        detected = True
                        detection_reason = f"Future information in feature {key}"
                        break
        
        elif scenario.error_type == "methodology_error":
            # Check for missing baselines
            artifacts = scenario.artifacts
            if "model_evaluation" in artifacts:
                baselines = artifacts["model_evaluation"].get("baseline_models", [])
                if len(baselines) == 0:
                    detected = True
                    detection_reason = "No baseline models provided"
        
        elif scenario.error_type == "data_snooping":
            # Check for test data usage in model development
            artifacts = scenario.artifacts
            if "model_development_log" in artifacts:
                log = artifacts["model_development_log"]
                if "feature_selection" in log:
                    eval_data = log["feature_selection"].get("evaluation_data", "")
                    if "test" in eval_data:
                        detected = True
                        detection_reason = "Test data used in feature selection"
                
                if "hyperparameter_tuning" in log:
                    opt_metric = log["hyperparameter_tuning"].get("optimization_metric", "")
                    if "test" in opt_metric:
                        detected = True
                        detection_reason = "Test data used in hyperparameter tuning"
        
        elif scenario.error_type == "statistical_rigor":
            # Check for missing statistical tests
            artifacts = scenario.artifacts
            if "ab_test_analysis" in artifacts:
                analysis = artifacts["ab_test_analysis"]
                if not analysis.get("p_value") or not analysis.get("confidence_interval"):
                    detected = True
                    detection_reason = "Missing statistical significance testing"
        
        elif scenario.error_type == "monitoring_gap":
            # Check production monitoring configuration
            artifacts = scenario.artifacts
            if "deployment_spec" in artifacts:
                monitoring = artifacts["deployment_spec"].get("monitoring", {})
                if not monitoring.get("performance_tracking") or not monitoring.get("data_drift_detection"):
                    detected = True
                    detection_reason = "Insufficient production monitoring"
        
        elif scenario.error_type == "pipeline_inconsistency":
            # Check for training-serving skew
            artifacts = scenario.artifacts
            if "model_pipeline" in artifacts:
                pipeline = artifacts["model_pipeline"]
                training_features = pipeline.get("training_features", {})
                serving_features = pipeline.get("serving_features", {})
                
                for feature in training_features:
                    if feature in serving_features:
                        if training_features[feature] != serving_features[feature]:
                            detected = True
                            detection_reason = f"Training-serving skew in feature {feature}"
                            break
        
        elif scenario.error_type == "reproducibility":
            # Check reproducibility requirements
            artifacts = scenario.artifacts
            if "training_pipeline" in artifacts:
                pipeline = artifacts["training_pipeline"]
                variance = pipeline.get("training_variance", "")
                if "15%" in variance or "not_set" in pipeline.get("random_seeds", ""):
                    detected = True
                    detection_reason = "Reproducibility requirements not met"
        
        # For valid scenarios, should not detect errors
        elif scenario.error_type == "none":
            detected = False
            detection_reason = "No errors found - validation passed"
        
        result.update({
            "detected": detected,
            "detection_reason": detection_reason,
            "detection_correct": detected == scenario.should_be_detected,
            "expected_feedback": scenario.expected_feedback,
            "remediation": scenario.remediation_suggestion
        })
        
        return result


def generate_error_test_suite() -> Dict[str, Any]:
    """Generate complete error detection test suite."""
    all_scenarios = DSValidatorErrorScenarios.get_all_error_scenarios()
    
    test_results = {}
    total_tests = 0
    correct_detections = 0
    
    for category, scenarios in all_scenarios.items():
        category_results = []
        
        for scenario in scenarios:
            result = DSValidatorErrorScenarios.validate_error_detection(scenario)
            category_results.append(result)
            
            total_tests += 1
            if result["detection_correct"]:
                correct_detections += 1
        
        test_results[category] = category_results
    
    test_results["summary"] = {
        "total_tests": total_tests,
        "correct_detections": correct_detections,
        "detection_accuracy": correct_detections / total_tests if total_tests > 0 else 0,
        "pass_threshold": 0.90  # Require 90% detection accuracy
    }
    
    return test_results


if __name__ == "__main__":
    # Generate and run error detection test suite
    results = generate_error_test_suite()
    
    print("DS Validator Error Detection Test Results")
    print("=" * 50)
    
    for category, tests in results.items():
        if category == "summary":
            continue
            
        print(f"\n{category.upper()}:")
        for test in tests:
            status = "PASS" if test["detection_correct"] else "FAIL"
            print(f"  {test['scenario_name']}: {status}")
            if not test["detection_correct"]:
                print(f"    Expected: {'detect' if test['should_detect'] else 'pass'}")
                print(f"    Actual: {'detected' if test['detected'] else 'passed'}")
    
    summary = results["summary"]
    print(f"\nOVERALL RESULTS:")
    print(f"Tests: {summary['total_tests']}")
    print(f"Correct: {summary['correct_detections']}")
    print(f"Accuracy: {summary['detection_accuracy']:.1%}")
    print(f"Pass Threshold: {summary['pass_threshold']:.0%}")
    print(f"Status: {'PASS' if summary['detection_accuracy'] >= summary['pass_threshold'] else 'FAIL'}")