#!/usr/bin/env python3
"""
Check DS Planning Files for Leakage Risks

This script analyzes DS planning files to identify potential data leakage risks
and temporal validation issues.
"""

import argparse
import json
from pathlib import Path
from datetime import datetime, timedelta

class LeakageRiskChecker:
    """Analyzer for data leakage risks in DS planning files."""
    
    LEAKAGE_RISK_KEYWORDS = [
        'future', 'next', 'after', 'subsequent', 'following',
        'outcome', 'result', 'resolution', 'final', 'end',
        'completion', 'cancellation', 'churn', 'conversion'
    ]
    
    HIGH_RISK_FEATURES = [
        'resolution_time', 'days_to_resolve', 'time_to_complete',
        'final_status', 'end_date', 'completion_date',
        'cancellation_date', 'churn_date', 'conversion_date'
    ]
    
    def __init__(self, plan_data):
        self.plan = plan_data
        self.risks = []
        self.warnings = []
        
    def check_temporal_validation(self):
        """Check if temporal validation is properly configured."""
        eval_protocol = self.plan.get('evaluation_protocol', {})
        temporal_val = eval_protocol.get('temporal_validation', {})
        
        if not temporal_val:
            self.risks.append({
                'category': 'temporal_validation',
                'severity': 'high',
                'issue': 'No temporal validation specified',
                'description': 'Temporal validation is critical for preventing leakage in time-series problems',
                'recommendation': 'Add temporal_validation section with training/validation periods'
            })
            return
        
        # Check for minimum gap
        min_gap = temporal_val.get('minimum_gap')
        prediction_horizon = temporal_val.get('prediction_horizon')
        
        if not min_gap:
            self.warnings.append({
                'category': 'temporal_validation', 
                'severity': 'medium',
                'issue': 'No minimum gap specified between training and prediction',
                'recommendation': 'Consider adding minimum gap to prevent temporal leakage'
            })
        
        # Check if gap is reasonable for prediction horizon
        if min_gap and prediction_horizon:
            try:
                # Simple check - gap should be at least as long as prediction horizon
                if 'day' in min_gap.lower() and 'day' in prediction_horizon.lower():
                    gap_days = int(''.join(filter(str.isdigit, min_gap)))
                    horizon_days = int(''.join(filter(str.isdigit, prediction_horizon)))
                    
                    if gap_days < horizon_days:
                        self.warnings.append({
                            'category': 'temporal_validation',
                            'severity': 'medium', 
                            'issue': f'Minimum gap ({gap_days}d) shorter than prediction horizon ({horizon_days}d)',
                            'recommendation': 'Consider increasing minimum gap to match or exceed prediction horizon'
                        })
            except (ValueError, AttributeError):
                pass  # Skip parsing if format is unexpected
    
    def check_feature_engineering(self):
        """Check feature engineering for leakage risks."""
        feature_eng = self.plan.get('feature_engineering', {})
        leakage_prevention = feature_eng.get('leakage_prevention', {})
        
        if not leakage_prevention:
            self.risks.append({
                'category': 'feature_engineering',
                'severity': 'high',
                'issue': 'No leakage prevention measures specified',
                'description': 'Feature engineering without leakage prevention is high risk',
                'recommendation': 'Add leakage_prevention section with validation tests'
            })
            return
        
        # Check for prediction cutoff
        cutoff = leakage_prevention.get('prediction_cutoff')
        if not cutoff:
            self.risks.append({
                'category': 'feature_engineering',
                'severity': 'high',
                'issue': 'No prediction cutoff defined',
                'recommendation': 'Define strict temporal boundary for feature engineering'
            })
        
        # Check for future information checks
        future_checks = leakage_prevention.get('future_information_checks', [])
        if not future_checks:
            self.warnings.append({
                'category': 'feature_engineering',
                'severity': 'medium',
                'issue': 'No explicit future information checks listed',
                'recommendation': 'Document specific checks for preventing future information usage'
            })
        
        # Check feature categories for risky patterns
        feature_categories = feature_eng.get('feature_categories', [])
        for category in feature_categories:
            features = category.get('features', [])
            for feature in features:
                # Check for high-risk feature names
                for risk_pattern in self.HIGH_RISK_FEATURES:
                    if risk_pattern in feature.lower():
                        self.risks.append({
                            'category': 'feature_engineering',
                            'severity': 'high',
                            'issue': f'High-risk feature detected: {feature}',
                            'description': f'Feature name suggests potential future information usage',
                            'recommendation': f'Verify that {feature} does not contain future information'
                        })
                
                # Check for leakage keywords in feature names
                for keyword in self.LEAKAGE_RISK_KEYWORDS:
                    if keyword in feature.lower():
                        self.warnings.append({
                            'category': 'feature_engineering',
                            'severity': 'medium',
                            'issue': f'Feature with leakage keyword: {feature} (contains "{keyword}")',
                            'recommendation': f'Review {feature} for potential temporal issues'
                        })
    
    def check_data_contracts(self):
        """Check data contracts for temporal consistency."""
        data_contracts = self.plan.get('data_contracts', [])
        
        for contract in data_contracts:
            schema = contract.get('schema', {})
            columns = schema.get('columns', [])
            
            # Look for timestamp columns and their constraints
            timestamp_cols = [col for col in columns if 'date' in col.get('type', '').lower() or 'timestamp' in col.get('type', '').lower()]
            
            for col in timestamp_cols:
                constraints = col.get('constraints', [])
                
                # Check for future date constraints
                for constraint in constraints:
                    if 'current_date' in constraint.lower() and '>' in constraint:
                        self.risks.append({
                            'category': 'data_contracts',
                            'severity': 'high', 
                            'issue': f'Future date allowed in {col["name"]}: {constraint}',
                            'recommendation': 'Ensure timestamp constraints prevent future dates'
                        })
    
    def check_evaluation_protocol(self):
        """Check evaluation protocol for robust validation."""
        eval_protocol = self.plan.get('evaluation_protocol', {})
        
        # Check validation strategy
        validation_strategy = eval_protocol.get('validation_strategy')
        if validation_strategy == 'cross_validation':
            # Cross-validation can be risky for time series
            self.warnings.append({
                'category': 'evaluation_protocol',
                'severity': 'medium',
                'issue': 'Cross-validation used - may not be appropriate for time series',
                'recommendation': 'Consider temporal_split for time-dependent data'
            })
        
        # Check for baseline
        baseline = eval_protocol.get('baseline')
        if not baseline:
            self.warnings.append({
                'category': 'evaluation_protocol',
                'severity': 'medium', 
                'issue': 'No baseline defined',
                'recommendation': 'Define simple baseline for model comparison'
            })
        
        # Check success criteria
        success_criteria = eval_protocol.get('success_criteria', {})
        if not success_criteria.get('statistical_significance'):
            self.warnings.append({
                'category': 'evaluation_protocol',
                'severity': 'medium',
                'issue': 'No statistical significance testing specified', 
                'recommendation': 'Add statistical significance requirements'
            })
    
    def analyze(self):
        """Run comprehensive leakage risk analysis."""
        self.check_temporal_validation()
        self.check_feature_engineering()
        self.check_data_contracts()
        self.check_evaluation_protocol()
        
        return {
            'risks': self.risks,
            'warnings': self.warnings,
            'risk_score': self._calculate_risk_score()
        }
    
    def _calculate_risk_score(self):
        """Calculate overall risk score."""
        high_risk_count = len([r for r in self.risks if r['severity'] == 'high'])
        medium_risk_count = len([r for r in self.risks + self.warnings if r['severity'] == 'medium'])
        
        # Risk score from 0-100
        risk_score = min(100, (high_risk_count * 30) + (medium_risk_count * 10))
        
        if risk_score >= 70:
            return {'score': risk_score, 'level': 'HIGH', 'action': 'BLOCK_DEPLOYMENT'}
        elif risk_score >= 40:
            return {'score': risk_score, 'level': 'MEDIUM', 'action': 'REVIEW_REQUIRED'}
        else:
            return {'score': risk_score, 'level': 'LOW', 'action': 'PROCEED_WITH_CAUTION'}

def main():
    parser = argparse.ArgumentParser(
        description='Check DS planning files for data leakage risks'
    )
    parser.add_argument(
        '--plan',
        required=True,
        help='Path to DS planning file (JSON)'
    )
    parser.add_argument(
        '--step',
        type=int,
        help='Check specific step number (optional)'
    )
    parser.add_argument(
        '--output',
        help='Save results to file (optional)'
    )
    parser.add_argument(
        '--verbose',
        action='store_true',
        help='Verbose output with details'
    )
    
    args = parser.parse_args()
    
    try:
        # Load planning file
        with open(args.plan, 'r') as f:
            plan_data = json.load(f)
        
        # Run analysis
        checker = LeakageRiskChecker(plan_data)
        results = checker.analyze()
        
        # Display results
        risk_score = results['risk_score']
        print(f"\n🔍 Leakage Risk Analysis for: {plan_data.get('task_name', 'Unknown')}")
        print(f"📊 Risk Score: {risk_score['score']}/100 ({risk_score['level']})")
        print(f"🎯 Action: {risk_score['action']}")
        
        # Display risks
        if results['risks']:
            print(f"\n⚠️  HIGH RISKS IDENTIFIED ({len(results['risks'])}):")
            for i, risk in enumerate(results['risks'], 1):
                print(f"\n{i}. {risk['issue']}")
                if args.verbose:
                    print(f"   Category: {risk['category']}")
                    print(f"   Description: {risk.get('description', 'N/A')}")
                print(f"   💡 Recommendation: {risk['recommendation']}")
        
        # Display warnings
        if results['warnings']:
            print(f"\n⚡ WARNINGS ({len(results['warnings'])}):")
            for i, warning in enumerate(results['warnings'], 1):
                print(f"\n{i}. {warning['issue']}")
                if args.verbose:
                    print(f"   Category: {warning['category']}")
                print(f"   💡 Recommendation: {warning['recommendation']}")
        
        if not results['risks'] and not results['warnings']:
            print(f"\n✅ No significant leakage risks detected!")
        
        # Save results if requested
        if args.output:
            output_path = Path(args.output)
            with open(output_path, 'w') as f:
                json.dump(results, f, indent=2)
            print(f"\n📄 Results saved to: {output_path}")
        
        # Exit with error code if high risks
        return 1 if risk_score['level'] == 'HIGH' else 0
        
    except Exception as e:
        print(f"❌ Error analyzing leakage risks: {e}")
        return 1

if __name__ == '__main__':
    exit(main())