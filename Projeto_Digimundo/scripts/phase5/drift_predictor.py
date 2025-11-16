#!/usr/bin/env python3
"""
🔮 AI-POWERED DRIFT PREDICTION SYSTEM

Nível: ALÉM DO ALÉM DO VALE DO SILÍCIO

Este sistema:
1. Analisa histórico de commits (git log)
2. Identifica padrões de mudanças que causam drift
3. Prevê QUANDO métricas vão driftar (próximos 7 dias)
4. Sugere ações preventivas
5. Gera alertas proativos

Usage:
    python3 scripts/phase5/drift_predictor.py
    python3 scripts/phase5/drift_predictor.py --days 14
    python3 scripts/phase5/drift_predictor.py --verbose
"""

import subprocess
import re
import json
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Tuple
from collections import defaultdict

# Colors
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
MAGENTA = '\033[95m'
BOLD = '\033[1m'
RESET = '\033[0m'


class DriftPredictor:
    """Predicts when metrics will drift based on historical patterns"""

    def __init__(self, days_ahead: int = 7, verbose: bool = False):
        self.days_ahead = days_ahead
        self.verbose = verbose
        self.project_root = self._detect_project_root()

    def _detect_project_root(self) -> Path:
        """Auto-detect project root"""
        current = Path.cwd()

        if (current / 'app').exists() and (current / 'tests').exists():
            return current

        if (current / 'cineprod-flask').exists():
            return current / 'cineprod-flask'

        if current.name == 'scripts':
            parent = current.parent.parent
            if (parent / 'cineprod-flask').exists():
                return parent / 'cineprod-flask'

        return current

    def analyze_git_history(self, days_back: int = 30) -> Dict:
        """Analyze git history for patterns"""
        print(f"{BLUE}🔍 Analyzing git history ({days_back} days)...{RESET}")

        try:
            # Get commits from last N days
            since_date = (datetime.now() - timedelta(days=days_back)).strftime('%Y-%m-%d')

            result = subprocess.run(
                ['git', 'log', f'--since={since_date}', '--numstat', '--pretty=format:%H|%ai|%s'],
                cwd=self.project_root,
                capture_output=True,
                text=True,
                timeout=30
            )

            if result.returncode != 0:
                print(f"{YELLOW}⚠️  Not a git repo or no commits{RESET}")
                return {}

            commits = self._parse_git_log(result.stdout)

            print(f"{GREEN}✅ Found {len(commits)} commits{RESET}")

            return commits

        except Exception as e:
            print(f"{RED}❌ Failed to analyze git history: {e}{RESET}")
            return {}

    def _parse_git_log(self, log_output: str) -> List[Dict]:
        """Parse git log output into structured data"""
        commits = []
        current_commit = None

        for line in log_output.split('\n'):
            if '|' in line and len(line.split('|')) == 3:
                # New commit
                if current_commit:
                    commits.append(current_commit)

                hash_val, date, message = line.split('|')
                current_commit = {
                    'hash': hash_val,
                    'date': datetime.fromisoformat(date.replace(' +0000', '')),
                    'message': message,
                    'files_changed': [],
                    'lines_added': 0,
                    'lines_deleted': 0
                }

            elif '\t' in line and current_commit:
                # File stats
                parts = line.split('\t')
                if len(parts) == 3:
                    added, deleted, filename = parts

                    if added != '-':
                        current_commit['lines_added'] += int(added)
                    if deleted != '-':
                        current_commit['lines_deleted'] += int(deleted)

                    current_commit['files_changed'].append({
                        'filename': filename,
                        'added': int(added) if added != '-' else 0,
                        'deleted': int(deleted) if deleted != '-' else 0
                    })

        if current_commit:
            commits.append(current_commit)

        return commits

    def detect_patterns(self, commits: List[Dict]) -> Dict:
        """Detect patterns that typically cause drift"""
        print(f"\n{BLUE}🧠 Detecting drift-causing patterns...{RESET}")

        patterns = {
            'refactoring_commits': 0,
            'service_changes': 0,
            'model_changes': 0,
            'test_changes': 0,
            'high_churn_days': [],
            'velocity': 0.0
        }

        # Pattern keywords that typically cause drift
        refactor_keywords = ['refactor', 'cleanup', 'simplify', 'consolidate', 'deduplicate']
        service_keywords = ['service', 'services/']
        model_keywords = ['model', 'models/']

        high_churn_threshold = 500  # lines changed

        for commit in commits:
            msg = commit['message'].lower()

            # Detect refactoring
            if any(kw in msg for kw in refactor_keywords):
                patterns['refactoring_commits'] += 1

            # Detect service/model changes
            for file_info in commit['files_changed']:
                filename = file_info['filename'].lower()

                if any(kw in filename for kw in service_keywords):
                    patterns['service_changes'] += 1

                if any(kw in filename for kw in model_keywords):
                    patterns['model_changes'] += 1

                if 'test' in filename:
                    patterns['test_changes'] += 1

            # Detect high churn
            total_churn = commit['lines_added'] + commit['lines_deleted']
            if total_churn > high_churn_threshold:
                patterns['high_churn_days'].append({
                    'date': commit['date'],
                    'churn': total_churn,
                    'message': commit['message']
                })

        # Calculate velocity (commits per day)
        if commits:
            date_range = (commits[0]['date'] - commits[-1]['date']).days or 1
            patterns['velocity'] = len(commits) / date_range

        return patterns

    def predict_drift(self, patterns: Dict) -> Dict:
        """Predict drift probability and timing"""
        print(f"\n{MAGENTA}🔮 Predicting drift...{RESET}")

        # Scoring system
        drift_score = 0.0
        factors = []

        # Factor 1: Refactoring activity
        if patterns['refactoring_commits'] > 5:
            drift_score += 0.4
            factors.append(("High refactoring activity", 0.4, "🔨"))
        elif patterns['refactoring_commits'] > 2:
            drift_score += 0.2
            factors.append(("Moderate refactoring", 0.2, "🔧"))

        # Factor 2: Service layer changes
        if patterns['service_changes'] > 10:
            drift_score += 0.3
            factors.append(("Many service changes", 0.3, "⚙️"))
        elif patterns['service_changes'] > 5:
            drift_score += 0.15
            factors.append(("Some service changes", 0.15, "⚙️"))

        # Factor 3: Model changes
        if patterns['model_changes'] > 5:
            drift_score += 0.2
            factors.append(("Model layer changes", 0.2, "📊"))

        # Factor 4: High churn
        if len(patterns['high_churn_days']) > 3:
            drift_score += 0.25
            factors.append(("High code churn", 0.25, "📈"))

        # Factor 5: Development velocity
        if patterns['velocity'] > 3:
            drift_score += 0.15
            factors.append(("High dev velocity", 0.15, "🚀"))

        # Normalize to 0-100%
        probability = min(drift_score * 100, 100)

        # Estimate timing
        if probability > 70:
            estimated_days = 2
            urgency = "HIGH"
        elif probability > 40:
            estimated_days = 5
            urgency = "MEDIUM"
        else:
            estimated_days = 10
            urgency = "LOW"

        return {
            'probability': probability,
            'estimated_days': estimated_days,
            'urgency': urgency,
            'factors': factors,
            'recommendations': self._generate_recommendations(probability, patterns)
        }

    def _generate_recommendations(self, probability: float, patterns: Dict) -> List[str]:
        """Generate actionable recommendations"""
        recommendations = []

        if probability > 70:
            recommendations.append("🚨 Run validation NOW: python3 scripts/phase5/validate_documentation.py")
            recommendations.append("🔄 Consider auto-update: python3 scripts/phase5/validate_documentation.py --auto-update")

        if patterns['refactoring_commits'] > 5:
            recommendations.append("📊 High refactoring detected - expect duplicate reduction")
            recommendations.append("📝 Plan to update baseline metrics after current sprint")

        if patterns['service_changes'] > 10:
            recommendations.append("⚙️ Service layer heavily modified - architectural patterns may have changed")

        if len(patterns['high_churn_days']) > 3:
            recommendations.append("📈 High churn period - code structure likely changed significantly")

        if not recommendations:
            recommendations.append("✅ No immediate action needed - continue normal development")

        return recommendations

    def run(self) -> int:
        """Run full drift prediction"""
        print(f"{BOLD}{MAGENTA}{'='*80}{RESET}")
        print(f"{BOLD}{MAGENTA}🔮 DRIFT PREDICTION SYSTEM{RESET}")
        print(f"{BOLD}{MAGENTA}{'='*80}{RESET}\n")

        # Analyze history
        commits = self.analyze_git_history(days_back=30)

        if not commits:
            print(f"\n{YELLOW}⚠️  No git history available - cannot predict{RESET}")
            return 1

        # Detect patterns
        patterns = self.detect_patterns(commits)

        # Predict drift
        prediction = self.predict_drift(patterns)

        # Display results
        self._display_prediction(prediction, patterns)

        # Save prediction report
        self._save_report(prediction, patterns)

        return 0

    def _display_prediction(self, prediction: Dict, patterns: Dict):
        """Display prediction results"""
        prob = prediction['probability']
        urgency = prediction['urgency']

        # Color based on urgency
        if urgency == "HIGH":
            color = RED
            icon = "🚨"
        elif urgency == "MEDIUM":
            color = YELLOW
            icon = "⚠️"
        else:
            color = GREEN
            icon = "✅"

        print(f"\n{BOLD}{'='*80}{RESET}")
        print(f"{BOLD}PREDICTION RESULTS{RESET}")
        print(f"{'='*80}")

        print(f"\n{icon} {color}{BOLD}Drift Probability: {prob:.1f}%{RESET}")
        print(f"{color}Urgency: {urgency}{RESET}")
        print(f"Estimated drift in: {prediction['estimated_days']} days")

        print(f"\n{BOLD}Contributing Factors:{RESET}")
        for factor, score, emoji in prediction['factors']:
            print(f"  {emoji} {factor:30s} +{score*100:>5.1f}%")

        print(f"\n{BOLD}Activity Summary:{RESET}")
        print(f"  Refactoring commits:    {patterns['refactoring_commits']}")
        print(f"  Service changes:        {patterns['service_changes']}")
        print(f"  Model changes:          {patterns['model_changes']}")
        print(f"  High churn events:      {len(patterns['high_churn_days'])}")
        print(f"  Dev velocity:           {patterns['velocity']:.1f} commits/day")

        print(f"\n{BOLD}📋 Recommended Actions:{RESET}")
        for i, rec in enumerate(prediction['recommendations'], 1):
            print(f"  {i}. {rec}")

        print(f"\n{'='*80}\n")

    def _save_report(self, prediction: Dict, patterns: Dict):
        """Save prediction report"""
        docs_dir = self.project_root.parent / 'docs' / 'fase_5'
        report_path = docs_dir / f'DRIFT_PREDICTION_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'

        report = {
            'timestamp': datetime.now().isoformat(),
            'prediction': {
                'probability': prediction['probability'],
                'estimated_days': prediction['estimated_days'],
                'urgency': prediction['urgency'],
                'factors': [(f, s) for f, s, _ in prediction['factors']],
                'recommendations': prediction['recommendations']
            },
            'patterns': {
                'refactoring_commits': patterns['refactoring_commits'],
                'service_changes': patterns['service_changes'],
                'model_changes': patterns['model_changes'],
                'test_changes': patterns['test_changes'],
                'high_churn_events': len(patterns['high_churn_days']),
                'velocity': patterns['velocity']
            }
        }

        report_path.write_text(json.dumps(report, indent=2))
        print(f"{GREEN}💾 Prediction saved: {report_path}{RESET}")


def main():
    import argparse

    parser = argparse.ArgumentParser(description='Predict documentation drift')
    parser.add_argument('--days', type=int, default=7, help='Days ahead to predict')
    parser.add_argument('--verbose', action='store_true', help='Verbose output')

    args = parser.parse_args()

    predictor = DriftPredictor(days_ahead=args.days, verbose=args.verbose)
    return predictor.run()


if __name__ == '__main__':
    exit(main())
