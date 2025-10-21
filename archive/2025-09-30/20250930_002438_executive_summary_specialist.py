#!/usr/bin/env python3
"""
Script Doctor Executivemon - Executive Summary Specialist
Comprehensive synthesis, strategic overview, final verdict, executive-level insights.
The final word from the Script Doctor™ system.
"""

import re
import yaml
from typing import Dict, List, Optional, Tuple, Set, Any
from pathlib import Path
from dataclasses import dataclass, field
from collections import defaultdict
import statistics


@dataclass
class StrengthWeakness:
    """Represents a strength or weakness."""
    category: str
    description: str
    impact: str  # high, medium, low
    specialist_source: str


@dataclass
class CriticalIssue:
    """Represents a critical issue that must be addressed."""
    issue_type: str
    description: str
    severity: str  # critical, high, medium
    solution: str
    estimated_effort: str  # minor, moderate, major


@dataclass
class OpportunityRisk:
    """Represents an opportunity or risk."""
    type: str  # opportunity or risk
    category: str
    description: str
    probability: float
    impact: float


@dataclass
class ExecutiveMetrics:
    """Key executive-level metrics."""
    overall_quality: float
    story_strength: float
    market_potential: float
    production_viability: float
    creative_merit: float


@dataclass
class ExecutivePriority:
    """Executive priority assessment."""
    priority: str
    assessment: str
    score: float


@dataclass
class DevelopmentRecommendation:
    """Development recommendation."""
    priority: str  # critical, high, medium, low
    area: str
    action: str
    expected_impact: str


@dataclass
class DecisionFactor:
    """Decision factor assessment."""
    factor: str
    score: float
    assessment: str


@dataclass
class FinalVerdict:
    """Final verdict on the screenplay."""
    verdict: str
    confidence: float
    conditions: List[str]
    risks: List[str]


@dataclass
class StrategicAssessment:
    """Strategic assessment of the screenplay."""
    viability_score: float
    risk_level: str  # low, medium, high
    opportunity_score: float
    strengths: List[str]
    risks: List[str]
    market_timing: str  # excellent, good, fair, poor
    competitive_advantage: str
    unique_selling_points: List[str]
    target_platforms: List[str]
    ideal_release_window: str
    marketing_angle: str
    awards_potential: bool
    franchise_potential: bool


@dataclass
class ExecutiveSummaryResult:
    """Final executive summary from the Script Doctor™ system."""
    specialist: Dict[str, str]
    score: int
    final_verdict: FinalVerdict
    recommendation_level: str  # greenlight, conditional, development, revision, pass
    executive_priorities: List[ExecutivePriority]
    strategic_assessment: StrategicAssessment
    swot_analysis: Dict[str, List[str]]  # strengths, weaknesses, opportunities, threats
    development_recommendations: List[DevelopmentRecommendation]
    decision_factors: List[DecisionFactor]
    key_metrics: ExecutiveMetrics
    executive_summary: str
    production_go: bool
    rule_violations: List[Dict[str, Any]]

    # Additional insights
    specialist_consensus: Dict[str, Any] = field(default_factory=dict)
    investment_analysis: Dict[str, Any] = field(default_factory=dict)
    comparative_analysis: Dict[str, Any] = field(default_factory=dict)
    final_recommendation: str = ""


class DrExecutiveSummary:
    """The Script Doctor™ Executive Summary Specialist - The Final Authority."""

    def __init__(self):
        """Initialize the Executive Summary specialist."""
        self.name = "Script Doctor Executivemon"
        self.specialty = "Comprehensive synthesis, strategic overview, final verdict, executive-level insights"

        # Load rules
        rules_path = Path(__file__).parent.parent / "rules" / "executive_summary_rules.yaml"
        with open(rules_path, 'r') as f:
            self.rules_config = yaml.safe_load(f)

        # Decision thresholds
        self.decision_thresholds = {
            'greenlight': 85,
            'conditional_greenlight': 70,
            'development': 55,
            'major_revision': 40,
            'pass': 0
        }

        # Grade thresholds
        self.grade_thresholds = {
            'A+': 95, 'A': 90, 'A-': 85,
            'B+': 80, 'B': 75, 'B-': 70,
            'C+': 65, 'C': 60, 'C-': 55,
            'D': 45, 'F': 0
        }

    def analyze(self, screenplay: str, specialist_results: Optional[Dict[str, Any]] = None) -> ExecutiveSummaryResult:
        """
        Provide final executive summary and recommendation.

        Args:
            screenplay: The screenplay text
            specialist_results: Optional results from other specialists for comprehensive analysis
        """
        # Parse screenplay for basic analysis
        scenes = self._parse_scenes(screenplay)

        # Synthesize specialist results if provided
        if specialist_results:
            synthesis = self._synthesize_specialist_results(specialist_results)
        else:
            # Perform standalone analysis
            synthesis = self._standalone_analysis(scenes, screenplay)

        # Identify strengths and weaknesses
        strengths = self._identify_strengths(synthesis, scenes)
        weaknesses = self._identify_weaknesses(synthesis, scenes)

        # Identify opportunities and risks
        opportunities = self._identify_opportunities(synthesis, scenes)
        risks = self._identify_risks(synthesis, scenes)

        # Identify critical issues
        critical_issues = self._identify_critical_issues(synthesis, weaknesses, risks)

        # Calculate executive metrics
        executive_metrics = self._calculate_executive_metrics(
            synthesis, strengths, weaknesses, opportunities, risks, critical_issues
        )

        # Calculate key metrics for dashboard
        key_metrics = ExecutiveMetrics(
            overall_quality=synthesis.get('overall_quality', 0.5),
            story_strength=synthesis.get('story_strength', 0.5),
            market_potential=synthesis.get('market_potential', 0.5),
            production_viability=synthesis.get('production_viability', 0.5),
            creative_merit=synthesis.get('originality', 0.5)
        )

        # Create executive priorities
        executive_priorities = self._create_executive_priorities(synthesis, executive_metrics)

        # Create development recommendations
        development_recommendations = self._create_development_recommendations(
            critical_issues, weaknesses, synthesis
        )

        # Create decision factors
        decision_factors = self._create_decision_factors(synthesis, executive_metrics)

        # Create final verdict
        final_verdict = self._create_final_verdict(
            executive_metrics, critical_issues, risks
        )

        # Create SWOT analysis
        swot_analysis = self._create_swot_analysis(
            strengths, weaknesses, opportunities, risks
        )

        # Create strategic assessment
        strategic_assessment = self._create_strategic_assessment(
            synthesis, scenes, executive_metrics
        )

        # Generate executive summary text
        executive_summary = self._generate_executive_summary(
            executive_metrics, strategic_assessment, strengths, weaknesses
        )

        # Generate detailed verdict
        detailed_verdict = self._generate_detailed_verdict(
            executive_metrics, critical_issues, opportunities, risks
        )

        # Generate action items
        action_items = self._generate_action_items(
            critical_issues, weaknesses, executive_metrics
        )

        # Create specialist consensus
        specialist_consensus = self._create_specialist_consensus(synthesis)

        # Create investment analysis
        investment_analysis = self._create_investment_analysis(
            executive_metrics, risks, opportunities
        )

        # Create comparative analysis
        comparative_analysis = self._create_comparative_analysis(synthesis, executive_metrics)

        # Generate final recommendation
        final_recommendation = self._generate_final_recommendation(
            executive_metrics, critical_issues, strategic_assessment
        )

        # Check rules
        rule_violations = self._check_rules(executive_metrics, synthesis, critical_issues)

        # Calculate final score
        final_score = self._calculate_final_score(executive_metrics, rule_violations)

        # Determine production go decision
        production_go = executive_metrics.recommendation in ['greenlight', 'conditional_greenlight']

        # Map executive_metrics.recommendation to recommendation_level
        recommendation_map = {
            'greenlight': 'greenlight',
            'conditional_greenlight': 'conditional',
            'development': 'development',
            'major_revision': 'revision',
            'pass': 'pass'
        }
        recommendation_level = recommendation_map.get(executive_metrics.recommendation, 'pass')

        return ExecutiveSummaryResult(
            specialist={
                'name': self.name,
                'specialty': self.specialty,
                'version': '1.0.0',
                'authority': 'FINAL'
            },
            score=final_score,
            final_verdict=final_verdict,
            recommendation_level=recommendation_level,
            executive_priorities=executive_priorities,
            strategic_assessment=strategic_assessment,
            swot_analysis=swot_analysis,
            development_recommendations=development_recommendations,
            decision_factors=decision_factors,
            key_metrics=key_metrics,
            executive_summary=executive_summary,
            production_go=production_go,
            rule_violations=rule_violations,
            specialist_consensus=specialist_consensus,
            investment_analysis=investment_analysis,
            comparative_analysis=comparative_analysis,
            final_recommendation=final_recommendation
        )

    def _parse_scenes(self, screenplay: str) -> List[Dict[str, Any]]:
        """Parse screenplay into scenes."""
        scenes = []
        current_scene = None
        scene_num = 0

        for i, line in enumerate(screenplay.split('\n'), 1):
            line_stripped = line.strip()

            # Scene heading
            if re.match(r'^(INT\.|EXT\.|INT/EXT\.|I/E\.)', line_stripped):
                if current_scene:
                    scenes.append(current_scene)
                scene_num += 1
                current_scene = {
                    'scene_num': scene_num,
                    'heading': line_stripped,
                    'dialogue': [],
                    'action': [],
                    'characters': set(),
                    'line_num': i
                }
            elif current_scene:
                # Character name (dialogue)
                if line_stripped.isupper() and len(line_stripped) > 0 and not line_stripped.startswith('('):
                    current_scene['characters'].add(line_stripped)
                    current_scene['dialogue'].append({
                        'character': line_stripped,
                        'line_num': i,
                        'text': ''
                    })
                # Dialogue
                elif current_scene['dialogue'] and not line_stripped.startswith('('):
                    if line_stripped:
                        current_scene['dialogue'][-1]['text'] += ' ' + line_stripped
                # Action lines
                elif line_stripped and not line_stripped.startswith('('):
                    current_scene['action'].append({
                        'text': line_stripped,
                        'line_num': i
                    })

        if current_scene:
            scenes.append(current_scene)

        return scenes

    def _synthesize_specialist_results(self, specialist_results: Dict[str, Any]) -> Dict[str, Any]:
        """Synthesize results from all specialists."""
        synthesis = {
            'overall_quality': 0.0,
            'market_potential': 0.0,
            'story_strength': 0.0,
            'character_quality': 0.0,
            'dialogue_quality': 0.0,
            'structure_quality': 0.0,
            'originality': 0.0,
            'production_viability': 0.0,
            'specialist_scores': {},
            'key_findings': [],
            'consensus_issues': [],
            'unanimous_strengths': []
        }

        # Extract scores from each specialist
        for specialist_name, result in specialist_results.items():
            if hasattr(result, 'score'):
                synthesis['specialist_scores'][specialist_name] = result.score

        # Calculate averages
        if synthesis['specialist_scores']:
            synthesis['overall_quality'] = statistics.mean(synthesis['specialist_scores'].values()) / 100

        # Extract specific metrics if available
        if 'quality' in specialist_results:
            quality_result = specialist_results['quality']
            if hasattr(quality_result, 'quality_analysis'):
                synthesis['story_strength'] = quality_result.quality_analysis.narrative_quality
                synthesis['character_quality'] = quality_result.quality_analysis.character_quality
                synthesis['dialogue_quality'] = quality_result.quality_analysis.dialogue_quality
                synthesis['structure_quality'] = quality_result.quality_analysis.structural_quality

        if 'market' in specialist_results:
            market_result = specialist_results['market']
            if hasattr(market_result, 'market_analysis'):
                synthesis['market_potential'] = market_result.market_analysis.overall_market_score
                synthesis['production_viability'] = market_result.market_analysis.break_even_likelihood

        if 'originality' in specialist_results:
            originality_result = specialist_results['originality']
            if hasattr(originality_result, 'originality_analysis'):
                synthesis['originality'] = originality_result.originality_analysis.overall_originality

        return synthesis

    def _standalone_analysis(self, scenes: List[Dict], screenplay: str) -> Dict[str, Any]:
        """Perform standalone analysis without other specialist results."""
        synthesis = {
            'overall_quality': 0.3,  # Start lower
            'market_potential': 0.3,
            'story_strength': 0.3,
            'character_quality': 0.3,
            'dialogue_quality': 0.3,
            'structure_quality': 0.3,
            'originality': 0.3,
            'production_viability': 0.4,
            'specialist_scores': {},
            'key_findings': [],
            'consensus_issues': [],
            'unanimous_strengths': []
        }

        # Enhanced quality assessment
        if scenes:
            # Story strength - check for complexity and conflict
            action_text = ' '.join(' '.join(a['text'].lower() for a in scene['action']) for scene in scenes)
            conflict_words = ['conflict', 'fight', 'struggle', 'confront', 'battle', 'chase',
                            'danger', 'threat', 'crisis', 'challenge', 'tension']
            conflict_count = sum(1 for word in conflict_words if word in action_text)
            synthesis['story_strength'] += min(0.4, conflict_count * 0.05)

            # Check for story progression
            if len(scenes) > 5:
                first_third = scenes[:len(scenes)//3]
                last_third = scenes[-len(scenes)//3:]
                if first_third and last_third:
                    # Different locations suggest movement
                    early_locs = set(s['heading'].split('-')[0].strip() for s in first_third)
                    late_locs = set(s['heading'].split('-')[0].strip() for s in last_third)
                    if early_locs != late_locs:
                        synthesis['story_strength'] += 0.1

            # Character quality - depth and variety
            total_characters = len(set(char for scene in scenes for char in scene['characters']))
            character_dialogues = defaultdict(int)
            for scene in scenes:
                for dialogue in scene['dialogue']:
                    if dialogue['character']:
                        character_dialogues[dialogue['character']] += 1

            # Main characters (those with substantial dialogue)
            main_chars = [char for char, count in character_dialogues.items() if count > 3]
            synthesis['character_quality'] += min(0.3, len(main_chars) * 0.1)
            synthesis['character_quality'] += min(0.2, (total_characters - len(main_chars)) * 0.02)

            # Dialogue quality - variety and substance
            total_dialogue = sum(len(scene['dialogue']) for scene in scenes)
            dialogue_per_scene = total_dialogue / max(1, len(scenes))
            synthesis['dialogue_quality'] += min(0.3, dialogue_per_scene * 0.05)

            # Check dialogue variety
            unique_speakers = len(character_dialogues)
            if unique_speakers >= 5:
                synthesis['dialogue_quality'] += 0.15

            # Structure quality - proper formatting and flow
            has_fade_in = 'FADE IN' in screenplay
            has_fade_out = 'FADE OUT' in screenplay
            if has_fade_in and has_fade_out:
                synthesis['structure_quality'] += 0.2

            # Scene count suggests completeness
            if 20 <= len(scenes) <= 150:
                synthesis['structure_quality'] += 0.2
            elif 10 <= len(scenes) < 20:
                synthesis['structure_quality'] += 0.1

            # Originality - unique elements
            unique_words = ['twist', 'reveal', 'transform', 'surprise', 'unexpected',
                           'mysterious', 'strange', 'unique', 'never', 'impossible']
            originality_score = sum(0.05 for word in unique_words if word in screenplay.lower())
            synthesis['originality'] += min(0.3, originality_score)

            # Production viability
            location_count = len(set(scene['heading'].split('-')[0].strip() for scene in scenes))
            if location_count <= 5:
                synthesis['production_viability'] += 0.3
            elif location_count <= 10:
                synthesis['production_viability'] += 0.2
            elif location_count <= 20:
                synthesis['production_viability'] += 0.1

            # Check for expensive elements
            expensive_words = ['explosion', 'crash', 'cgi', 'effects', 'thousands', 'army']
            expensive_count = sum(1 for word in expensive_words if word in screenplay.lower())
            synthesis['production_viability'] -= min(0.2, expensive_count * 0.05)

            # Market potential - genre appeal
            genre_indicators = {
                'action': ['fight', 'chase', 'explosion', 'weapon', 'battle'],
                'drama': ['emotion', 'family', 'relationship', 'love', 'tears'],
                'comedy': ['laugh', 'funny', 'joke', 'humor', 'silly'],
                'thriller': ['danger', 'mystery', 'secret', 'conspiracy', 'suspense'],
                'horror': ['terror', 'fear', 'monster', 'blood', 'scream']
            }

            for genre, keywords in genre_indicators.items():
                genre_score = sum(1 for word in keywords if word in screenplay.lower())
                if genre_score >= 2:
                    synthesis['market_potential'] += 0.15
                    break

        # Overall quality is weighted average
        component_scores = [
            synthesis['story_strength'] * 0.35,
            synthesis['character_quality'] * 0.25,
            synthesis['dialogue_quality'] * 0.15,
            synthesis['structure_quality'] * 0.15,
            synthesis['originality'] * 0.10
        ]
        synthesis['overall_quality'] = min(0.95, sum(component_scores))

        return synthesis

    def _identify_strengths(self, synthesis: Dict[str, Any], scenes: List[Dict]) -> List[StrengthWeakness]:
        """Identify screenplay strengths."""
        strengths = []

        # Check synthesis scores
        if synthesis['story_strength'] >= 0.7:
            strengths.append(StrengthWeakness(
                category='Story',
                description='Strong narrative foundation with compelling conflict',
                impact='high',
                specialist_source='Narrative Analysis'
            ))

        if synthesis['character_quality'] >= 0.7:
            strengths.append(StrengthWeakness(
                category='Characters',
                description='Well-developed characters with clear arcs',
                impact='high',
                specialist_source='Character Analysis'
            ))

        if synthesis['dialogue_quality'] >= 0.7:
            strengths.append(StrengthWeakness(
                category='Dialogue',
                description='Sharp, distinctive dialogue that advances story',
                impact='medium',
                specialist_source='Dialogue Analysis'
            ))

        if synthesis['originality'] >= 0.7:
            strengths.append(StrengthWeakness(
                category='Originality',
                description='Fresh concept with unique elements',
                impact='high',
                specialist_source='Originality Assessment'
            ))

        if synthesis['market_potential'] >= 0.7:
            strengths.append(StrengthWeakness(
                category='Market',
                description='Strong commercial appeal and market positioning',
                impact='high',
                specialist_source='Market Analysis'
            ))

        # Scene-based strengths
        if scenes and len(scenes) >= 15:
            if len(scenes[0]['action']) >= 3:
                strengths.append(StrengthWeakness(
                    category='Opening',
                    description='Strong opening that hooks audience',
                    impact='medium',
                    specialist_source='Structure Analysis'
                ))

        return strengths

    def _identify_weaknesses(self, synthesis: Dict[str, Any], scenes: List[Dict]) -> List[StrengthWeakness]:
        """Identify screenplay weaknesses."""
        weaknesses = []

        # Check synthesis scores
        if synthesis['story_strength'] < 0.5:
            weaknesses.append(StrengthWeakness(
                category='Story',
                description='Weak narrative structure or unclear conflict',
                impact='high',
                specialist_source='Narrative Analysis'
            ))

        if synthesis['character_quality'] < 0.5:
            weaknesses.append(StrengthWeakness(
                category='Characters',
                description='Underdeveloped or uncompelling characters',
                impact='high',
                specialist_source='Character Analysis'
            ))

        if synthesis['dialogue_quality'] < 0.5:
            weaknesses.append(StrengthWeakness(
                category='Dialogue',
                description='Weak or generic dialogue',
                impact='medium',
                specialist_source='Dialogue Analysis'
            ))

        if synthesis['structure_quality'] < 0.5:
            weaknesses.append(StrengthWeakness(
                category='Structure',
                description='Poor pacing or structural issues',
                impact='high',
                specialist_source='Structure Analysis'
            ))

        if synthesis['market_potential'] < 0.5:
            weaknesses.append(StrengthWeakness(
                category='Market',
                description='Limited commercial appeal',
                impact='high',
                specialist_source='Market Analysis'
            ))

        if synthesis['originality'] < 0.4:
            weaknesses.append(StrengthWeakness(
                category='Originality',
                description='Derivative or clichéd elements',
                impact='medium',
                specialist_source='Originality Assessment'
            ))

        return weaknesses

    def _identify_opportunities(self, synthesis: Dict[str, Any], scenes: List[Dict]) -> List[OpportunityRisk]:
        """Identify opportunities."""
        opportunities = []

        # Market opportunities
        if synthesis['market_potential'] >= 0.6:
            opportunities.append(OpportunityRisk(
                type='opportunity',
                category='Market',
                description='Strong market timing for this genre',
                probability=0.7,
                impact=0.8
            ))

        # Awards opportunity
        if synthesis['overall_quality'] >= 0.8:
            opportunities.append(OpportunityRisk(
                type='opportunity',
                category='Awards',
                description='Potential for awards consideration',
                probability=0.4,
                impact=0.9
            ))

        # Franchise opportunity
        if len(set(char for scene in scenes for char in scene['characters'])) >= 5:
            opportunities.append(OpportunityRisk(
                type='opportunity',
                category='Franchise',
                description='Franchise/sequel potential',
                probability=0.5,
                impact=0.8
            ))

        # Streaming opportunity
        if synthesis['production_viability'] >= 0.7:
            opportunities.append(OpportunityRisk(
                type='opportunity',
                category='Platform',
                description='Multiple platform opportunities',
                probability=0.8,
                impact=0.7
            ))

        return opportunities

    def _identify_risks(self, synthesis: Dict[str, Any], scenes: List[Dict]) -> List[OpportunityRisk]:
        """Identify risks."""
        risks = []

        # Quality risk
        if synthesis['overall_quality'] < 0.6:
            risks.append(OpportunityRisk(
                type='risk',
                category='Quality',
                description='Quality issues may affect reception',
                probability=0.7,
                impact=0.8
            ))

        # Market risk
        if synthesis['market_potential'] < 0.5:
            risks.append(OpportunityRisk(
                type='risk',
                category='Market',
                description='Limited audience appeal',
                probability=0.8,
                impact=0.9
            ))

        # Budget risk
        location_count = len(set(scene['heading'].split('-')[0].strip() for scene in scenes)) if scenes else 0
        if location_count > 20:
            risks.append(OpportunityRisk(
                type='risk',
                category='Budget',
                description='High production costs',
                probability=0.9,
                impact=0.7
            ))

        # Competition risk
        if synthesis['originality'] < 0.5:
            risks.append(OpportunityRisk(
                type='risk',
                category='Competition',
                description='May struggle against similar content',
                probability=0.6,
                impact=0.7
            ))

        return risks

    def _identify_critical_issues(self, synthesis: Dict[str, Any],
                                 weaknesses: List[StrengthWeakness],
                                 risks: List[OpportunityRisk]) -> List[CriticalIssue]:
        """Identify critical issues that must be addressed."""
        critical_issues = []

        # Story issues
        if synthesis['story_strength'] < 0.5:
            critical_issues.append(CriticalIssue(
                issue_type='Narrative',
                description='Story lacks compelling conflict or clear throughline',
                severity='critical',
                solution='Restructure plot and strengthen central conflict',
                estimated_effort='major'
            ))

        # Character issues
        if synthesis['character_quality'] < 0.4:
            critical_issues.append(CriticalIssue(
                issue_type='Character',
                description='Characters lack depth and development',
                severity='high',
                solution='Develop character backstories and clear arcs',
                estimated_effort='moderate'
            ))

        # Market viability
        if synthesis['market_potential'] < 0.4:
            critical_issues.append(CriticalIssue(
                issue_type='Commercial',
                description='Lacks clear market positioning',
                severity='critical',
                solution='Identify target audience and strengthen commercial elements',
                estimated_effort='major'
            ))

        # Overall quality
        if synthesis['overall_quality'] < 0.5:
            critical_issues.append(CriticalIssue(
                issue_type='Quality',
                description='Overall quality below professional standards',
                severity='critical',
                solution='Comprehensive rewrite focusing on fundamentals',
                estimated_effort='major'
            ))

        return critical_issues

    def _calculate_executive_metrics(self, synthesis: Dict[str, Any],
                                    strengths: List[StrengthWeakness],
                                    weaknesses: List[StrengthWeakness],
                                    opportunities: List[OpportunityRisk],
                                    risks: List[OpportunityRisk],
                                    critical_issues: List[CriticalIssue]) -> ExecutiveMetrics:
        """Calculate executive-level metrics."""
        # Overall score
        overall_score = int(synthesis['overall_quality'] * 100)

        # Quality grade
        quality_grade = 'F'
        for grade, threshold in sorted(self.grade_thresholds.items(), key=lambda x: x[1], reverse=True):
            if overall_score >= threshold:
                quality_grade = grade
                break

        # Market potential
        market_score = synthesis['market_potential']
        if market_score >= 0.8:
            market_potential = 'excellent'
        elif market_score >= 0.65:
            market_potential = 'strong'
        elif market_score >= 0.5:
            market_potential = 'moderate'
        elif market_score >= 0.35:
            market_potential = 'weak'
        else:
            market_potential = 'poor'

        # Recommendation
        recommendation = 'pass'
        for rec_level, threshold in sorted(self.decision_thresholds.items(), key=lambda x: x[1], reverse=True):
            if overall_score >= threshold and len(critical_issues) <= 2:
                recommendation = rec_level
                break

        # Adjust for critical issues
        if len(critical_issues) > 3:
            if recommendation in ['greenlight', 'conditional_greenlight']:
                recommendation = 'major_revision'

        # Confidence level
        confidence_level = min(0.9, 0.5 + len(strengths) * 0.1 - len(critical_issues) * 0.15)

        # Success probability
        success_probability = (
            synthesis['overall_quality'] * 0.3 +
            synthesis['market_potential'] * 0.3 +
            synthesis['originality'] * 0.2 +
            (1.0 - len(risks) * 0.1) * 0.2
        )

        # ROI estimate
        if market_score >= 0.7 and overall_score >= 70:
            roi_estimate = 'High (3-5x)'
        elif market_score >= 0.5 and overall_score >= 60:
            roi_estimate = 'Moderate (2-3x)'
        elif market_score >= 0.4:
            roi_estimate = 'Low (1-2x)'
        else:
            roi_estimate = 'Break-even or loss'

        # Timeline to production
        if recommendation == 'greenlight':
            timeline = 'Ready for production (0-3 months prep)'
        elif recommendation == 'conditional_greenlight':
            timeline = 'Minor revisions needed (3-6 months)'
        elif recommendation == 'development':
            timeline = 'Development required (6-12 months)'
        elif recommendation == 'major_revision':
            timeline = 'Major work needed (12+ months)'
        else:
            timeline = 'Not viable for production'

        # Store the full metrics in a temporary object for later use
        self._temp_metrics = {
            'overall_score': overall_score,
            'quality_grade': quality_grade,
            'market_potential': market_potential,
            'recommendation': recommendation,
            'confidence_level': confidence_level,
            'success_probability': success_probability,
            'roi_estimate': roi_estimate,
            'timeline_to_production': timeline
        }

        # Return a dummy ExecutiveMetrics to maintain compatibility
        # The actual values will be used from _temp_metrics
        return type('ExecutiveMetrics', (), self._temp_metrics)()

    def _create_strategic_assessment(self, synthesis: Dict[str, Any], scenes: List[Dict],
                                    metrics: ExecutiveMetrics) -> StrategicAssessment:
        """Create strategic assessment."""
        # Market timing
        if synthesis['market_potential'] >= 0.7:
            market_timing = 'excellent'
        elif synthesis['market_potential'] >= 0.5:
            market_timing = 'good'
        elif synthesis['market_potential'] >= 0.3:
            market_timing = 'fair'
        else:
            market_timing = 'poor'

        # Competitive advantage
        if synthesis['originality'] >= 0.7:
            competitive_advantage = 'Strong differentiation and unique elements'
        elif synthesis['originality'] >= 0.5:
            competitive_advantage = 'Some differentiating factors'
        else:
            competitive_advantage = 'Limited differentiation from competition'

        # Unique selling points
        usps = []
        if synthesis['originality'] >= 0.6:
            usps.append('Fresh concept')
        if synthesis['character_quality'] >= 0.7:
            usps.append('Compelling characters')
        if synthesis['story_strength'] >= 0.7:
            usps.append('Strong narrative')
        if not usps:
            usps.append('Standard genre execution')

        # Target platforms
        platforms = []
        if synthesis['production_viability'] >= 0.7 and synthesis['market_potential'] >= 0.7:
            platforms.append('Theatrical release')
        if synthesis['overall_quality'] >= 0.6:
            platforms.append('Streaming platforms')
        if synthesis['overall_quality'] >= 0.5:
            platforms.append('Cable/Premium TV')
        if not platforms:
            platforms.append('Limited release')

        # Release window
        if market_timing == 'excellent':
            release_window = 'Next 6-12 months (capitalize on trends)'
        elif market_timing == 'good':
            release_window = 'Next 12-18 months'
        else:
            release_window = 'Flexible timing'

        # Marketing angle
        if synthesis['originality'] >= 0.7:
            marketing_angle = 'Unique concept - "Never seen before"'
        elif synthesis['character_quality'] >= 0.7:
            marketing_angle = 'Character-driven - "Unforgettable characters"'
        elif synthesis['story_strength'] >= 0.7:
            marketing_angle = 'Story-focused - "Edge of your seat"'
        else:
            marketing_angle = 'Genre appeal - Target core audience'

        # Awards potential
        awards_potential = synthesis['overall_quality'] >= 0.8 and synthesis['originality'] >= 0.6

        # Franchise potential
        franchise_potential = (
            len(set(char for scene in scenes for char in scene['characters'])) >= 5 and
            synthesis['market_potential'] >= 0.6
        )

        # Calculate strategic scores
        viability_score = (synthesis.get('overall_quality', 0.5) +
                          synthesis.get('market_potential', 0.5) +
                          synthesis.get('production_viability', 0.5)) / 3

        opportunity_score = (synthesis.get('market_potential', 0.5) +
                           synthesis.get('originality', 0.5)) / 2

        # Determine risk level
        if viability_score >= 0.7:
            risk_level = 'low'
        elif viability_score >= 0.5:
            risk_level = 'medium'
        else:
            risk_level = 'high'

        # Strategic strengths
        strategic_strengths = []
        if synthesis.get('story_strength', 0) >= 0.7:
            strategic_strengths.append('Strong narrative foundation')
        if synthesis.get('market_potential', 0) >= 0.7:
            strategic_strengths.append('High market appeal')
        if synthesis.get('originality', 0) >= 0.7:
            strategic_strengths.append('Fresh concept')

        # Strategic risks
        strategic_risks = []
        if synthesis.get('production_viability', 0) < 0.5:
            strategic_risks.append('Production challenges')
        if synthesis.get('market_potential', 0) < 0.5:
            strategic_risks.append('Limited audience')

        return StrategicAssessment(
            viability_score=viability_score,
            risk_level=risk_level,
            opportunity_score=opportunity_score,
            strengths=strategic_strengths,
            risks=strategic_risks,
            market_timing=market_timing,
            competitive_advantage=competitive_advantage,
            unique_selling_points=usps,
            target_platforms=platforms,
            ideal_release_window=release_window,
            marketing_angle=marketing_angle,
            awards_potential=awards_potential,
            franchise_potential=franchise_potential
        )

    def _generate_executive_summary(self, metrics: ExecutiveMetrics,
                                   strategy: StrategicAssessment,
                                   strengths: List[StrengthWeakness],
                                   weaknesses: List[StrengthWeakness]) -> str:
        """Generate executive summary text."""
        summary_parts = []

        # Opening verdict
        summary_parts.append(f"EXECUTIVE SUMMARY - {metrics.recommendation.upper().replace('_', ' ')}")
        summary_parts.append(f"Overall Score: {metrics.overall_score}/100 (Grade: {metrics.quality_grade})")
        summary_parts.append(f"Market Potential: {metrics.market_potential.capitalize()}")

        # Key strengths
        if strengths:
            strength_list = ', '.join(s.category.lower() for s in strengths[:3])
            summary_parts.append(f"Key Strengths: {strength_list}")

        # Key concerns
        if weaknesses:
            weakness_list = ', '.join(w.category.lower() for w in weaknesses[:3])
            summary_parts.append(f"Primary Concerns: {weakness_list}")

        # Strategic positioning
        summary_parts.append(f"Strategic Position: {strategy.marketing_angle}")

        # Financial outlook
        summary_parts.append(f"ROI Projection: {metrics.roi_estimate}")

        # Timeline
        summary_parts.append(f"Production Timeline: {metrics.timeline_to_production}")

        # Verdict
        if metrics.recommendation == 'greenlight':
            verdict = 'Recommended for immediate production'
        elif metrics.recommendation == 'conditional_greenlight':
            verdict = 'Recommended with conditions'
        elif metrics.recommendation == 'development':
            verdict = 'Requires development before production'
        elif metrics.recommendation == 'major_revision':
            verdict = 'Major revision required'
        else:
            verdict = 'Not recommended for production'

        summary_parts.append(f"\nVERDICT: {verdict}")

        return '\n'.join(summary_parts)

    def _generate_detailed_verdict(self, metrics: ExecutiveMetrics,
                                  critical_issues: List[CriticalIssue],
                                  opportunities: List[OpportunityRisk],
                                  risks: List[OpportunityRisk]) -> str:
        """Generate detailed verdict."""
        verdict_parts = []

        # Overall assessment
        if metrics.recommendation == 'greenlight':
            verdict_parts.append("This screenplay is ready for production with strong commercial and creative merit.")
        elif metrics.recommendation == 'conditional_greenlight':
            verdict_parts.append("This screenplay shows strong potential but requires specific revisions before production.")
        elif metrics.recommendation == 'development':
            verdict_parts.append("This screenplay has potential but needs further development to reach production standards.")
        elif metrics.recommendation == 'major_revision':
            verdict_parts.append("This screenplay requires substantial revision before it can be considered for production.")
        else:
            verdict_parts.append("This screenplay is not recommended for production in its current form.")

        # Critical issues
        if critical_issues:
            verdict_parts.append(f"\nCritical Issues ({len(critical_issues)}):")
            for issue in critical_issues[:3]:
                verdict_parts.append(f"- {issue.description}")

        # Opportunities
        if opportunities and metrics.overall_score >= 60:
            verdict_parts.append(f"\nKey Opportunities:")
            for opp in opportunities[:2]:
                verdict_parts.append(f"- {opp.description}")

        # Success probability
        verdict_parts.append(f"\nSuccess Probability: {metrics.success_probability:.1%}")
        verdict_parts.append(f"Confidence Level: {metrics.confidence_level:.1%}")

        return '\n'.join(verdict_parts)

    def _generate_action_items(self, critical_issues: List[CriticalIssue],
                              weaknesses: List[StrengthWeakness],
                              metrics: ExecutiveMetrics) -> List[str]:
        """Generate prioritized action items."""
        action_items = []

        # Critical issues first
        for issue in critical_issues:
            if issue.severity == 'critical':
                action_items.append(f"CRITICAL: {issue.solution}")

        # High-impact weaknesses
        for weakness in weaknesses:
            if weakness.impact == 'high':
                action_items.append(f"HIGH PRIORITY: Address {weakness.category.lower()} issues")

        # Recommendation-specific items
        if metrics.recommendation == 'conditional_greenlight':
            action_items.append("Complete revision pass focusing on identified issues")
            action_items.append("Secure talent attachments")
        elif metrics.recommendation == 'development':
            action_items.append("Engage script doctor or development executive")
            action_items.append("Create detailed development plan")

        return action_items[:7]  # Top 7 action items

    def _create_specialist_consensus(self, synthesis: Dict[str, Any]) -> Dict[str, Any]:
        """Create specialist consensus analysis."""
        consensus = {
            'unanimous_strengths': [],
            'unanimous_concerns': [],
            'divergent_opinions': [],
            'average_score': 0
        }

        if synthesis['specialist_scores']:
            consensus['average_score'] = statistics.mean(synthesis['specialist_scores'].values())

            # Check for consensus
            scores = list(synthesis['specialist_scores'].values())
            if scores:
                score_variance = statistics.variance(scores) if len(scores) > 1 else 0
                if score_variance < 100:  # Low variance = high consensus
                    consensus['unanimous_strengths'].append('Consistent quality across all dimensions')
                else:
                    consensus['divergent_opinions'].append('Mixed assessments across specialties')

        return consensus

    def _create_investment_analysis(self, metrics: ExecutiveMetrics,
                                   risks: List[OpportunityRisk],
                                   opportunities: List[OpportunityRisk]) -> Dict[str, Any]:
        """Create investment analysis."""
        # Risk-adjusted return
        risk_factor = 1.0 - (len(risks) * 0.15)
        opportunity_factor = 1.0 + (len(opportunities) * 0.1)

        investment = {
            'recommendation': metrics.recommendation,
            'risk_level': 'high' if len(risks) >= 3 else 'moderate' if len(risks) >= 1 else 'low',
            'upside_potential': 'high' if len(opportunities) >= 3 else 'moderate' if len(opportunities) >= 1 else 'limited',
            'break_even_probability': metrics.success_probability * risk_factor,
            'recommended_budget_range': self._determine_budget_range(metrics, risks)
        }

        return investment

    def _determine_budget_range(self, metrics: ExecutiveMetrics,
                               risks: List[OpportunityRisk]) -> str:
        """Determine recommended budget range."""
        if metrics.market_potential == 'excellent' and metrics.overall_score >= 80:
            return '$50M+ (Major production)'
        elif metrics.market_potential == 'strong' and metrics.overall_score >= 70:
            return '$20-50M (Mid-budget)'
        elif metrics.market_potential == 'moderate':
            return '$5-20M (Modest budget)'
        else:
            return 'Under $5M (Micro-budget)'

    def _create_comparative_analysis(self, synthesis: Dict[str, Any],
                                    metrics: ExecutiveMetrics) -> Dict[str, Any]:
        """Create comparative market analysis."""
        comparative = {
            'quality_percentile': self._calculate_percentile(metrics.overall_score),
            'market_position': metrics.market_potential,
            'genre_competitiveness': 'Strong' if synthesis['originality'] >= 0.6 else 'Average',
            'similar_recent_successes': self._identify_comparables(synthesis),
            'differentiation': 'High' if synthesis['originality'] >= 0.7 else 'Moderate' if synthesis['originality'] >= 0.5 else 'Low'
        }

        return comparative

    def _calculate_percentile(self, score: int) -> str:
        """Calculate quality percentile."""
        if score >= 90:
            return 'Top 5%'
        elif score >= 80:
            return 'Top 15%'
        elif score >= 70:
            return 'Top 30%'
        elif score >= 60:
            return 'Top 50%'
        else:
            return 'Below average'

    def _identify_comparables(self, synthesis: Dict[str, Any]) -> List[str]:
        """Identify comparable successful films."""
        # Simplified comparable identification
        if synthesis['market_potential'] >= 0.7:
            return ['Recent blockbuster in genre', 'Successful franchise starter']
        elif synthesis['market_potential'] >= 0.5:
            return ['Mid-budget genre success', 'Streaming hit in category']
        else:
            return ['Festival favorite', 'Cult classic potential']

    def _generate_final_recommendation(self, metrics: ExecutiveMetrics,
                                      critical_issues: List[CriticalIssue],
                                      strategy: StrategicAssessment) -> str:
        """Generate final recommendation statement."""
        if metrics.recommendation == 'greenlight':
            return f"GREENLIGHT - Proceed to production. {strategy.marketing_angle}. Target {', '.join(strategy.target_platforms)}."
        elif metrics.recommendation == 'conditional_greenlight':
            issues_count = len(critical_issues)
            return f"CONDITIONAL GREENLIGHT - Address {issues_count} issues then proceed. High {metrics.market_potential} market potential."
        elif metrics.recommendation == 'development':
            return f"SEND TO DEVELOPMENT - Promising but needs work. Focus on {critical_issues[0].issue_type if critical_issues else 'story fundamentals'}."
        elif metrics.recommendation == 'major_revision':
            return "MAJOR REVISION REQUIRED - Substantial rewrite needed before reconsideration."
        else:
            return "PASS - Not recommended for production. Consider alternative projects."

    def _check_rules(self, metrics: ExecutiveMetrics, synthesis: Dict[str, Any],
                    critical_issues: List[CriticalIssue]) -> List[Dict[str, Any]]:
        """Check against executive rules."""
        violations = []

        for rule in self.rules_config['rules']:
            violation = self._check_single_rule(rule, metrics, synthesis, critical_issues)
            if violation:
                violations.append(violation)

        return violations

    def _check_single_rule(self, rule: Dict, metrics: ExecutiveMetrics,
                          synthesis: Dict[str, Any],
                          critical_issues: List[CriticalIssue]) -> Optional[Dict]:
        """Check a single rule."""
        passed = True
        details = ""

        rule_id = rule['id']

        if rule_id == 'EXE.R001':  # Overall Viability
            passed = metrics.overall_score >= 60
            details = f"Overall score: {metrics.overall_score}"

        elif rule_id == 'EXE.R002':  # Investment Worthiness
            passed = metrics.success_probability >= 0.5
            details = f"Success probability: {metrics.success_probability:.2f}"

        elif rule_id == 'EXE.R003':  # Story Strength
            passed = synthesis['story_strength'] >= 0.6
            details = f"Story strength: {synthesis['story_strength']:.2f}"

        elif rule_id == 'EXE.R004':  # Market Readiness
            passed = synthesis['market_potential'] >= 0.5
            details = f"Market potential: {synthesis['market_potential']:.2f}"

        elif rule_id == 'EXE.R006':  # Risk-Reward Balance
            passed = metrics.success_probability >= 0.4
            details = f"Risk-reward assessment"

        elif rule_id == 'EXE.R012':  # Professional Standard
            passed = metrics.overall_score >= 60
            details = f"Quality: {metrics.quality_grade}"

        elif rule_id == 'EXE.R015':  # Final Recommendation
            passed = metrics.recommendation != 'pass'
            details = f"Recommendation: {metrics.recommendation}"

        if not passed:
            return {
                'rule_id': rule_id,
                'title': rule['title'],
                'severity': rule['severity'],
                'category': rule['category'],
                'message': rule['fail_msg'],
                'details': details,
                'fix': rule['fix']
            }

        return None

    def _create_executive_priorities(self, synthesis: Dict[str, Any],
                                    metrics: ExecutiveMetrics) -> List[ExecutivePriority]:
        """Create executive priorities list."""
        priorities = []

        # Story priority
        priorities.append(ExecutivePriority(
            priority='Story Quality',
            assessment='Narrative foundation assessment',
            score=synthesis.get('story_strength', 0.5)
        ))

        # Market priority
        priorities.append(ExecutivePriority(
            priority='Market Potential',
            assessment='Commercial viability assessment',
            score=synthesis.get('market_potential', 0.5)
        ))

        # Production priority
        priorities.append(ExecutivePriority(
            priority='Production Viability',
            assessment='Production feasibility assessment',
            score=synthesis.get('production_viability', 0.5)
        ))

        # Character priority
        priorities.append(ExecutivePriority(
            priority='Character Development',
            assessment='Character quality assessment',
            score=synthesis.get('character_quality', 0.5)
        ))

        # Originality priority
        priorities.append(ExecutivePriority(
            priority='Creative Merit',
            assessment='Originality and innovation assessment',
            score=synthesis.get('originality', 0.5)
        ))

        return sorted(priorities, key=lambda x: x.score, reverse=True)

    def _create_development_recommendations(self, critical_issues: List[CriticalIssue],
                                          weaknesses: List[StrengthWeakness],
                                          synthesis: Dict[str, Any]) -> List[DevelopmentRecommendation]:
        """Create development recommendations."""
        recommendations = []

        # Critical issues first
        for issue in critical_issues[:3]:
            recommendations.append(DevelopmentRecommendation(
                priority='critical' if issue.severity == 'critical' else 'high',
                area=issue.issue_type,
                action=issue.solution,
                expected_impact=f"Address {issue.description.lower()}"
            ))

        # Weaknesses
        for weakness in weaknesses[:2]:
            if weakness.impact == 'high':
                recommendations.append(DevelopmentRecommendation(
                    priority='high',
                    area=weakness.category,
                    action=f"Strengthen {weakness.category.lower()}",
                    expected_impact=f"Improve {weakness.category.lower()} quality"
                ))

        # Always provide at least one recommendation
        if not recommendations:
            if synthesis.get('story_strength', 0.5) < 0.7:
                recommendations.append(DevelopmentRecommendation(
                    priority='medium',
                    area='Story',
                    action='Strengthen narrative structure',
                    expected_impact='Improve story coherence and impact'
                ))
            elif synthesis.get('character_quality', 0.5) < 0.7:
                recommendations.append(DevelopmentRecommendation(
                    priority='medium',
                    area='Characters',
                    action='Develop character depth',
                    expected_impact='Create more compelling characters'
                ))
            else:
                recommendations.append(DevelopmentRecommendation(
                    priority='low',
                    area='Polish',
                    action='General polish and refinement',
                    expected_impact='Enhance overall quality'
                ))

        return recommendations

    def _create_decision_factors(self, synthesis: Dict[str, Any],
                                metrics: ExecutiveMetrics) -> List[DecisionFactor]:
        """Create decision factors."""
        factors = []

        factors.append(DecisionFactor(
            factor='Overall Quality',
            score=synthesis.get('overall_quality', 0.5),
            assessment='Production-ready quality assessment'
        ))

        factors.append(DecisionFactor(
            factor='Market Potential',
            score=synthesis.get('market_potential', 0.5),
            assessment='Commercial viability assessment'
        ))

        factors.append(DecisionFactor(
            factor='ROI Potential',
            score=getattr(metrics, 'success_probability', 0.5),
            assessment='Return on investment projection'
        ))

        factors.append(DecisionFactor(
            factor='Risk Level',
            score=1.0 - (len([r for r in synthesis.get('risks', [])]) / 10.0),
            assessment='Risk assessment'
        ))

        return factors

    def _create_final_verdict(self, metrics: ExecutiveMetrics,
                             critical_issues: List[CriticalIssue],
                             risks: List[OpportunityRisk]) -> FinalVerdict:
        """Create final verdict."""
        # Determine verdict
        if metrics.recommendation == 'greenlight':
            verdict = 'Recommended for immediate production'
        elif metrics.recommendation == 'conditional_greenlight':
            verdict = 'Recommended with conditions'
        elif metrics.recommendation == 'development':
            verdict = 'Requires development before production'
        elif metrics.recommendation == 'major_revision':
            verdict = 'Major revision required'
        else:
            verdict = 'Not recommended for production'

        # Conditions
        conditions = []
        for issue in critical_issues[:3]:
            if issue.severity == 'critical':
                conditions.append(issue.solution)

        # Risks
        risk_list = []
        for risk in risks[:3]:
            risk_list.append(risk.description)

        return FinalVerdict(
            verdict=verdict,
            confidence=getattr(metrics, 'confidence_level', 0.5),
            conditions=conditions,
            risks=risk_list
        )

    def _create_swot_analysis(self, strengths: List[StrengthWeakness],
                             weaknesses: List[StrengthWeakness],
                             opportunities: List[OpportunityRisk],
                             risks: List[OpportunityRisk]) -> Dict[str, List[str]]:
        """Create SWOT analysis."""
        return {
            'strengths': [s.description for s in strengths],
            'weaknesses': [w.description for w in weaknesses],
            'opportunities': [o.description for o in opportunities if o.type == 'opportunity'],
            'threats': [r.description for r in risks if r.type == 'risk']
        }

    def _calculate_final_score(self, metrics: ExecutiveMetrics,
                              violations: List[Dict]) -> int:
        """Calculate final executive score."""
        score = metrics.overall_score

        # Adjust for violations
        severity_penalties = {
            'critical': 10,
            'high': 7,
            'medium': 4,
            'low': 2
        }

        for violation in violations:
            score -= severity_penalties.get(violation['severity'], 5)

        # Bonus for strong recommendation
        if metrics.recommendation == 'greenlight':
            score += 10
        elif metrics.recommendation == 'conditional_greenlight':
            score += 5

        # Ensure minimum differentiation based on recommendation
        if metrics.recommendation == 'greenlight':
            score = max(80, score)
        elif metrics.recommendation == 'conditional_greenlight':
            score = max(65, score)
        elif metrics.recommendation == 'development':
            score = max(45, min(70, score))
        elif metrics.recommendation == 'major_revision':
            score = max(25, min(50, score))
        else:  # pass
            score = min(30, score)

        return max(5, min(100, score))