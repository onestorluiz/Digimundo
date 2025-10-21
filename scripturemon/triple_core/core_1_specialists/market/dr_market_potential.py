#!/usr/bin/env python3
"""
Script Doctor Marketmon - Market Potential Specialist
Commercial viability, audience appeal, market positioning, revenue potential analysis.
"""

import re
import yaml
from typing import Dict, List, Optional, Tuple, Set, Any
from pathlib import Path
from dataclasses import dataclass, field
from collections import defaultdict, Counter
import statistics


@dataclass
class MarketSegment:
    """Represents a market segment opportunity."""
    segment: str  # theatrical, streaming, cable, etc.
    viability: float  # 0.0 to 1.0
    reasoning: str
    revenue_potential: str  # low, medium, high, very_high


@dataclass
class AudienceQuadrant:
    """Represents an audience demographic quadrant."""
    demographic: str
    appeal_score: float  # 0.0 to 1.0
    size: str  # small, medium, large, massive
    engagement_potential: float


@dataclass
class CompetitiveAnalysis:
    """Analysis of competitive landscape."""
    similar_successes: List[str]
    similar_failures: List[str]
    differentiation_score: float
    market_gap_fit: float


@dataclass
class CommercialElement:
    """Represents a commercial element in the screenplay."""
    element_type: str  # hook, set_piece, star_moment, franchise_seed
    description: str
    market_value: float
    scene_num: int


@dataclass
class MarketRisk:
    """Represents a market risk factor."""
    risk_type: str
    description: str
    severity: float  # 0.0 to 1.0
    mitigation: str


@dataclass
class MarketAnalysis:
    """Complete market potential analysis."""
    overall_market_score: float
    market_category: str  # blockbuster, mainstream, indie, niche, festival
    primary_market: str  # theatrical, streaming, cable, etc.
    audience_size: str  # massive, large, medium, small, niche
    revenue_potential: str  # very_high, high, medium, low
    roi_projection: float
    break_even_likelihood: float
    genre_marketability: float
    hook_strength: float
    competition_readiness: float
    global_potential: float


@dataclass
class MarketPotentialResult:
    """Result from market potential analysis."""
    specialist: Dict[str, str]
    score: int
    market_analysis: MarketAnalysis
    market_segments: List[MarketSegment]
    audience_quadrants: List[AudienceQuadrant]
    competitive_analysis: CompetitiveAnalysis
    commercial_elements: List[CommercialElement]
    market_risks: List[MarketRisk]
    revenue_projection: Dict[str, Any]
    recommendations: List[str]
    rule_violations: List[Dict[str, Any]]

    # Additional analysis
    marketing_strategy: Dict[str, str] = field(default_factory=dict)
    festival_potential: float = 0.0
    awards_potential: float = 0.0
    franchise_potential: float = 0.0
    merchandising_potential: float = 0.0


class DrMarketPotential:
    """The Script Doctor™ Market Potential Specialist."""

    def __init__(self):
        """Initialize the Market Potential specialist."""
        self.name = "Script Doctor Marketmon"
        self.specialty = "Commercial viability, audience appeal, market positioning, revenue potential"

        # Load rules
        rules_path = Path(__file__).parent.parent / "rules" / "market_potential_rules.yaml"
        with open(rules_path, 'r') as f:
            self.rules_config = yaml.safe_load(f)

        # Genre market values (current market trends)
        self.genre_market_values = {
            'action': {'value': 0.9, 'audience': 'massive', 'trend': 'stable'},
            'comedy': {'value': 0.7, 'audience': 'large', 'trend': 'rising'},
            'drama': {'value': 0.6, 'audience': 'medium', 'trend': 'stable'},
            'horror': {'value': 0.8, 'audience': 'large', 'trend': 'rising'},
            'thriller': {'value': 0.8, 'audience': 'large', 'trend': 'stable'},
            'romance': {'value': 0.5, 'audience': 'medium', 'trend': 'declining'},
            'sci_fi': {'value': 0.85, 'audience': 'large', 'trend': 'rising'},
            'fantasy': {'value': 0.75, 'audience': 'large', 'trend': 'stable'},
            'animation': {'value': 0.9, 'audience': 'massive', 'trend': 'rising'},
            'documentary': {'value': 0.4, 'audience': 'small', 'trend': 'stable'}
        }

        # Platform preferences
        self.platform_preferences = {
            'theatrical': ['action', 'sci_fi', 'animation', 'horror', 'fantasy'],
            'streaming': ['thriller', 'drama', 'comedy', 'documentary', 'romance'],
            'cable': ['drama', 'thriller', 'comedy'],
            'network': ['drama', 'comedy', 'romance'],
            'festival': ['drama', 'documentary', 'experimental']
        }

        # Commercial elements database
        self.commercial_indicators = {
            'set_piece': ['explosion', 'chase', 'fight', 'battle', 'spectacle'],
            'star_moment': ['monologue', 'emotional scene', 'hero moment', 'transformation'],
            'hook': ['unique', 'never before', 'twist', 'high concept', 'fresh take'],
            'franchise': ['universe', 'sequel', 'origin', 'mythology', 'world building']
        }

        # Audience appeal factors
        self.audience_factors = {
            'emotional': ['love', 'family', 'friendship', 'sacrifice', 'redemption'],
            'excitement': ['action', 'adventure', 'danger', 'thrill', 'suspense'],
            'escapism': ['fantasy', 'magical', 'superhero', 'otherworldly', 'dream'],
            'relatability': ['everyday', 'real', 'authentic', 'common', 'universal'],
            'spectacle': ['epic', 'grand', 'spectacular', 'massive', 'breathtaking']
        }

    def analyze(self, screenplay: str) -> Dict[str, Any]:
        """Analyze market potential of screenplay."""
        # Parse screenplay
        scenes = self._parse_scenes(screenplay)

        # Identify genre and market category
        genre = self._identify_primary_genre(scenes)
        market_category = self._determine_market_category(scenes, genre)

        # Analyze market segments
        market_segments = self._analyze_market_segments(scenes, genre)

        # Analyze audience quadrants
        audience_quadrants = self._analyze_audience_quadrants(scenes, genre)

        # Perform competitive analysis
        competitive_analysis = self._perform_competitive_analysis(genre, scenes)

        # Identify commercial elements
        commercial_elements = self._identify_commercial_elements(scenes)

        # Assess market risks
        market_risks = self._assess_market_risks(scenes, genre, commercial_elements)

        # Create revenue projection
        revenue_projection = self._create_revenue_projection(
            market_segments, audience_quadrants, genre
        )

        # Calculate market metrics
        market_analysis = self._create_market_analysis(
            genre, market_segments, audience_quadrants,
            competitive_analysis, commercial_elements, market_risks
        )

        # Generate marketing strategy
        marketing_strategy = self._generate_marketing_strategy(
            market_analysis, commercial_elements, audience_quadrants
        )

        # Calculate special potentials
        festival_potential = self._calculate_festival_potential(scenes, genre)
        awards_potential = self._calculate_awards_potential(scenes, genre)
        franchise_potential = self._calculate_franchise_potential(scenes, commercial_elements)
        merchandising_potential = self._calculate_merchandising_potential(
            scenes, genre, audience_quadrants
        )

        # Check rules
        rule_violations = self._check_rules(
            market_analysis, market_segments, commercial_elements
        )

        # Generate recommendations
        recommendations = self._generate_recommendations(
            market_analysis, market_risks, rule_violations
        )

        # Calculate score
        score = self._calculate_score(market_analysis, rule_violations)

        # Convert nested dataclasses to dicts
        market_segments_dict = [
            {
                'segment': seg.segment,
                'viability': seg.viability,
                'reasoning': seg.reasoning,
                'revenue_potential': seg.revenue_potential
            } for seg in market_segments
        ]

        audience_quadrants_dict = [
            {
                'demographic': quad.demographic,
                'appeal_score': quad.appeal_score,
                'size': quad.size,
                'engagement_potential': quad.engagement_potential
            } for quad in audience_quadrants
        ]

        competitive_analysis_dict = {
            'similar_successes': competitive_analysis.similar_successes,
            'similar_failures': competitive_analysis.similar_failures,
            'differentiation_score': competitive_analysis.differentiation_score,
            'market_gap_fit': competitive_analysis.market_gap_fit
        }

        commercial_elements_dict = [
            {
                'element_type': elem.element_type,
                'description': elem.description,
                'market_value': elem.market_value,
                'scene_num': elem.scene_num
            } for elem in commercial_elements
        ]

        market_risks_dict = [
            {
                'risk_type': risk.risk_type,
                'description': risk.description,
                'severity': risk.severity,
                'mitigation': risk.mitigation
            } for risk in market_risks
        ]

        # Generate diagnosis
        diagnosis = self._generate_diagnosis(score, market_analysis, market_risks)

        # Return dict instead of dataclass
        return {
            'specialist': {
                'name': self.name,
                'specialty': self.specialty,
                'version': '1.0.0'
            },
            'score': score,
            # Flatten MarketAnalysis fields
            'overall_market_score': market_analysis.overall_market_score,
            'market_category': market_analysis.market_category,
            'primary_market': market_analysis.primary_market,
            'audience_size': market_analysis.audience_size,
            'revenue_potential': market_analysis.revenue_potential,
            'roi_projection': market_analysis.roi_projection,
            'break_even_likelihood': market_analysis.break_even_likelihood,
            'genre_marketability': market_analysis.genre_marketability,
            'hook_strength': market_analysis.hook_strength,
            'competition_readiness': market_analysis.competition_readiness,
            'global_potential': market_analysis.global_potential,
            # Converted lists and dicts
            'market_segments': market_segments_dict,
            'audience_quadrants': audience_quadrants_dict,
            'competitive_analysis': competitive_analysis_dict,
            'commercial_elements': commercial_elements_dict,
            'market_risks': market_risks_dict,
            'revenue_projection': revenue_projection,
            'recommendations': recommendations,
            'rule_violations': rule_violations,
            'marketing_strategy': marketing_strategy,
            'festival_potential': festival_potential,
            'awards_potential': awards_potential,
            'franchise_potential': franchise_potential,
            'merchandising_potential': merchandising_potential,
            'diagnosis': diagnosis
        }

    def _generate_diagnosis(self, score: int, analysis: MarketAnalysis,
                          market_risks: List[MarketRisk]) -> str:
        """Generate diagnosis based on market potential analysis."""
        diagnosis_parts = []

        if score >= 85:
            diagnosis_parts.append("✅ EXCELLENT market potential - strong commercial viability")
        elif score >= 70:
            diagnosis_parts.append("👍 GOOD market potential with solid prospects")
        elif score >= 50:
            diagnosis_parts.append("⚠️  MODERATE market potential - niche audience")
        else:
            diagnosis_parts.append("❌ LOW market potential - high commercial risk")

        # Highlight category and primary market
        diagnosis_parts.append(f"{analysis.market_category} ({analysis.primary_market})")

        # Highlight strengths
        if analysis.global_potential > 0.7:
            diagnosis_parts.append(f"Strong global potential ({analysis.global_potential:.2f})")
        if analysis.hook_strength > 0.7:
            diagnosis_parts.append(f"Strong hook ({analysis.hook_strength:.2f})")

        # Highlight risks
        high_risks = [r for r in market_risks if r.severity > 0.7]
        if high_risks:
            diagnosis_parts.append(f"{len(high_risks)} high-severity market risks")

        # Revenue and ROI
        diagnosis_parts.append(f"{analysis.revenue_potential} revenue, ROI {analysis.roi_projection:.2f}")

        return " ".join(diagnosis_parts)

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

    def _identify_primary_genre(self, scenes: List[Dict]) -> str:
        """Identify primary genre for market analysis."""
        genre_indicators = defaultdict(int)

        for scene in scenes:
            scene_text = ' '.join(a['text'].lower() for a in scene['action'])
            scene_text += ' '.join(d['text'].lower() for d in scene['dialogue'])

            # Check for genre indicators
            if any(word in scene_text for word in ['fight', 'explosion', 'chase', 'battle']):
                genre_indicators['action'] += 2
            if any(word in scene_text for word in ['funny', 'laugh', 'joke', 'hilarious']):
                genre_indicators['comedy'] += 2
            if any(word in scene_text for word in ['love', 'kiss', 'heart', 'romantic']):
                genre_indicators['romance'] += 2
            if any(word in scene_text for word in ['scary', 'horror', 'monster', 'blood']):
                genre_indicators['horror'] += 2
            if any(word in scene_text for word in ['space', 'future', 'technology', 'alien']):
                genre_indicators['sci_fi'] += 2
            if any(word in scene_text for word in ['magic', 'dragon', 'wizard', 'quest']):
                genre_indicators['fantasy'] += 2
            if any(word in scene_text for word in ['investigate', 'mystery', 'clue', 'suspect']):
                genre_indicators['thriller'] += 2

        # Default to drama if no clear genre
        if not genre_indicators:
            return 'drama'

        return max(genre_indicators.items(), key=lambda x: x[1])[0]

    def _determine_market_category(self, scenes: List[Dict], genre: str) -> str:
        """Determine market category based on scope and genre."""
        # Check scope indicators
        total_characters = len(set(char for scene in scenes for char in scene['characters']))
        total_locations = len(set(scene['heading'].split('-')[0].strip() for scene in scenes))
        action_scenes = sum(1 for scene in scenes
                           for action in scene['action']
                           if any(word in action['text'].lower()
                                 for word in ['explosion', 'battle', 'chase', 'fight']))

        # Determine category
        if genre in ['action', 'sci_fi', 'fantasy'] and action_scenes >= 3:
            if total_locations >= 10 and total_characters >= 15:
                return 'blockbuster'
            else:
                return 'mainstream'
        elif genre in ['drama', 'romance'] and total_characters <= 5:
            return 'indie'
        elif genre == 'horror' and action_scenes >= 2:
            return 'mainstream'
        elif total_locations <= 3 and total_characters <= 4:
            return 'festival'
        else:
            return 'mainstream'

    def _analyze_market_segments(self, scenes: List[Dict], genre: str) -> List[MarketSegment]:
        """Analyze viability across different market segments."""
        segments = []

        # Theatrical
        theatrical_viable = genre in self.platform_preferences['theatrical']
        theatrical_score = 0.8 if theatrical_viable else 0.4

        segments.append(MarketSegment(
            segment='theatrical',
            viability=theatrical_score,
            reasoning=f"{'Strong' if theatrical_viable else 'Limited'} theatrical potential for {genre}",
            revenue_potential='high' if theatrical_score >= 0.7 else 'medium'
        ))

        # Streaming
        streaming_viable = genre in self.platform_preferences['streaming'] or len(scenes) >= 15
        streaming_score = 0.9 if streaming_viable else 0.6

        segments.append(MarketSegment(
            segment='streaming',
            viability=streaming_score,
            reasoning="Strong streaming potential - fits platform needs",
            revenue_potential='high' if streaming_score >= 0.8 else 'medium'
        ))

        # Cable/Premium
        cable_viable = genre in self.platform_preferences['cable']
        cable_score = 0.7 if cable_viable else 0.4

        segments.append(MarketSegment(
            segment='premium_cable',
            viability=cable_score,
            reasoning=f"{'Good' if cable_viable else 'Limited'} cable potential",
            revenue_potential='medium'
        ))

        # International
        has_universal_themes = self._check_universal_themes(scenes)
        international_score = 0.8 if has_universal_themes else 0.5

        segments.append(MarketSegment(
            segment='international',
            viability=international_score,
            reasoning="Universal themes appeal globally" if has_universal_themes else "Limited international appeal",
            revenue_potential='high' if international_score >= 0.7 else 'medium'
        ))

        return segments

    def _check_universal_themes(self, scenes: List[Dict]) -> bool:
        """Check for universal themes that cross cultural boundaries."""
        universal_themes = ['family', 'love', 'survival', 'justice', 'freedom',
                          'friendship', 'sacrifice', 'redemption', 'hope']

        theme_count = 0
        for scene in scenes:
            scene_text = ' '.join(d['text'].lower() for d in scene['dialogue'])
            for theme in universal_themes:
                if theme in scene_text:
                    theme_count += 1
                    break

        return theme_count >= len(scenes) * 0.2

    def _analyze_audience_quadrants(self, scenes: List[Dict], genre: str) -> List[AudienceQuadrant]:
        """Analyze appeal across audience demographics."""
        quadrants = []

        # Analyze content for demographic indicators
        has_action = any('fight' in a['text'].lower() or 'chase' in a['text'].lower()
                        for scene in scenes for a in scene['action'])
        has_romance = any('love' in d['text'].lower() or 'kiss' in a['text'].lower()
                         for scene in scenes
                         for d in scene['dialogue']
                         for a in scene['action'])
        has_youth_appeal = any(word in ' '.join(d['text'].lower() for scene in scenes for d in scene['dialogue'])
                              for word in ['cool', 'awesome', 'epic'])

        # Male Under 25
        male_young_score = 0.8 if (genre in ['action', 'sci_fi', 'horror'] and has_action) else 0.4
        quadrants.append(AudienceQuadrant(
            demographic='male_under_25',
            appeal_score=male_young_score,
            size='large',
            engagement_potential=0.7 if male_young_score >= 0.6 else 0.3
        ))

        # Male Over 25
        male_adult_score = 0.7 if genre in ['thriller', 'action', 'sci_fi'] else 0.5
        quadrants.append(AudienceQuadrant(
            demographic='male_over_25',
            appeal_score=male_adult_score,
            size='large',
            engagement_potential=0.6
        ))

        # Female Under 25
        female_young_score = 0.8 if (has_romance or genre in ['romance', 'comedy']) else 0.5
        quadrants.append(AudienceQuadrant(
            demographic='female_under_25',
            appeal_score=female_young_score,
            size='large',
            engagement_potential=0.8 if female_young_score >= 0.6 else 0.4
        ))

        # Female Over 25
        female_adult_score = 0.7 if genre in ['drama', 'romance', 'thriller'] else 0.5
        quadrants.append(AudienceQuadrant(
            demographic='female_over_25',
            appeal_score=female_adult_score,
            size='massive',
            engagement_potential=0.7
        ))

        # Family Audience
        family_appropriate = not any(word in ' '.join(a['text'].lower() for scene in scenes for a in scene['action'])
                                    for word in ['blood', 'gore', 'death', 'kill'])
        family_score = 0.8 if (family_appropriate and genre in ['animation', 'comedy', 'fantasy']) else 0.3
        quadrants.append(AudienceQuadrant(
            demographic='family_audience',
            appeal_score=family_score,
            size='massive' if family_score >= 0.7 else 'medium',
            engagement_potential=0.9 if family_score >= 0.7 else 0.3
        ))

        return quadrants

    def _perform_competitive_analysis(self, genre: str, scenes: List[Dict]) -> CompetitiveAnalysis:
        """Analyze competitive landscape."""
        # Simplified competitive analysis based on genre
        genre_competition = {
            'action': {
                'successes': ['Top Gun: Maverick', 'John Wick series', 'Fast & Furious franchise'],
                'failures': ['Generic action film #47'],
                'saturation': 0.8
            },
            'comedy': {
                'successes': ['The Hangover', 'Bridesmaids', 'Deadpool'],
                'failures': ['Generic comedy sequel'],
                'saturation': 0.6
            },
            'drama': {
                'successes': ['Everything Everywhere All at Once', 'The Whale', 'CODA'],
                'failures': ['Oscar bait film #23'],
                'saturation': 0.7
            },
            'horror': {
                'successes': ['Get Out', 'A Quiet Place', 'The Conjuring'],
                'failures': ['Generic jump scare movie'],
                'saturation': 0.7
            },
            'sci_fi': {
                'successes': ['Dune', 'Everything Everywhere', 'Avatar series'],
                'failures': ['Generic dystopia #15'],
                'saturation': 0.6
            }
        }

        comp_data = genre_competition.get(genre, {
            'successes': ['Recent hit in genre'],
            'failures': ['Recent flop in genre'],
            'saturation': 0.5
        })

        # Calculate differentiation based on unique elements
        unique_elements = len(set(scene['heading'] for scene in scenes))
        differentiation = min(unique_elements * 0.05, 1.0)

        # Market gap fit (inverse of saturation)
        market_gap = 1.0 - comp_data['saturation']

        return CompetitiveAnalysis(
            similar_successes=comp_data['successes'][:3],
            similar_failures=comp_data['failures'][:1],
            differentiation_score=differentiation,
            market_gap_fit=market_gap
        )

    def _identify_commercial_elements(self, scenes: List[Dict]) -> List[CommercialElement]:
        """Identify commercial elements in screenplay."""
        elements = []

        for scene in scenes:
            scene_text = ' '.join(a['text'].lower() for a in scene['action'])

            # Check for set pieces
            for indicator in self.commercial_indicators['set_piece']:
                if indicator in scene_text:
                    elements.append(CommercialElement(
                        element_type='set_piece',
                        description=f"Action set piece: {indicator}",
                        market_value=0.8,
                        scene_num=scene['scene_num']
                    ))
                    break

            # Check for star moments
            if len(scene['dialogue']) > 5:  # Substantial dialogue scene
                for dialogue in scene['dialogue']:
                    if len(dialogue['text'].split()) > 30:  # Monologue
                        elements.append(CommercialElement(
                            element_type='star_moment',
                            description="Powerful monologue opportunity",
                            market_value=0.7,
                            scene_num=scene['scene_num']
                        ))
                        break

            # Check for hooks
            if scene['scene_num'] <= 3:  # Early scenes
                for indicator in self.commercial_indicators['hook']:
                    if indicator in scene_text:
                        elements.append(CommercialElement(
                            element_type='hook',
                            description=f"Strong hook: {indicator} concept",
                            market_value=0.9,
                            scene_num=scene['scene_num']
                        ))
                        break

        return elements

    def _assess_market_risks(self, scenes: List[Dict], genre: str,
                            commercial_elements: List[CommercialElement]) -> List[MarketRisk]:
        """Assess market risk factors."""
        risks = []

        # Budget vs. scope risk
        location_count = len(set(scene['heading'].split('-')[0].strip() for scene in scenes))
        if location_count > 20:
            risks.append(MarketRisk(
                risk_type='budget',
                description="High location count increases budget",
                severity=0.7,
                mitigation="Consolidate locations or increase budget"
            ))

        # Genre saturation risk
        if genre in ['superhero', 'zombie', 'vampire']:
            risks.append(MarketRisk(
                risk_type='saturation',
                description=f"Market saturated with {genre} content",
                severity=0.8,
                mitigation="Emphasize unique elements and differentiation"
            ))

        # Limited audience risk
        character_count = len(set(char for scene in scenes for char in scene['characters']))
        if character_count < 3:
            risks.append(MarketRisk(
                risk_type='audience',
                description="Limited character ensemble may reduce audience appeal",
                severity=0.5,
                mitigation="Ensure compelling character dynamics"
            ))

        # Marketing challenge risk
        if not commercial_elements or len(commercial_elements) < 2:
            risks.append(MarketRisk(
                risk_type='marketing',
                description="Few marketable elements",
                severity=0.6,
                mitigation="Develop clear marketing hooks"
            ))

        # Seasonal timing risk
        if genre == 'horror':
            risks.append(MarketRisk(
                risk_type='timing',
                description="Horror performs best around Halloween",
                severity=0.3,
                mitigation="Plan release timing strategically"
            ))

        return risks

    def _create_revenue_projection(self, segments: List[MarketSegment],
                                  quadrants: List[AudienceQuadrant],
                                  genre: str) -> Dict[str, Any]:
        """Create revenue projection model."""
        # Calculate audience reach
        total_audience_score = sum(q.appeal_score for q in quadrants) / len(quadrants)

        # Calculate segment potential
        best_segment = max(segments, key=lambda s: s.viability)

        # Genre multiplier
        genre_data = self.genre_market_values.get(genre, {'value': 0.5})
        genre_multiplier = genre_data['value']

        # Revenue tiers
        revenue_potential = total_audience_score * genre_multiplier

        if revenue_potential >= 0.8:
            tier = 'very_high'
            range_low, range_high = 100, 500  # millions
        elif revenue_potential >= 0.6:
            tier = 'high'
            range_low, range_high = 50, 150
        elif revenue_potential >= 0.4:
            tier = 'medium'
            range_low, range_high = 10, 50
        else:
            tier = 'low'
            range_low, range_high = 1, 10

        return {
            'revenue_tier': tier,
            'projected_range': f"${range_low}M - ${range_high}M",
            'best_platform': best_segment.segment,
            'audience_reach': total_audience_score,
            'confidence': min(revenue_potential + 0.2, 1.0)
        }

    def _create_market_analysis(self, genre: str, segments: List[MarketSegment],
                               quadrants: List[AudienceQuadrant],
                               competitive: CompetitiveAnalysis,
                               commercial_elements: List[CommercialElement],
                               risks: List[MarketRisk]) -> MarketAnalysis:
        """Create comprehensive market analysis."""
        # Overall market score
        segment_avg = sum(s.viability for s in segments) / len(segments) if segments else 0.5
        audience_avg = sum(q.appeal_score for q in quadrants) / len(quadrants) if quadrants else 0.5
        commercial_strength = min(len(commercial_elements) * 0.2, 1.0)

        overall_score = (segment_avg * 0.3 + audience_avg * 0.3 +
                        commercial_strength * 0.2 + competitive.differentiation_score * 0.2)

        # Determine market category
        if overall_score >= 0.8:
            category = 'blockbuster'
        elif overall_score >= 0.65:
            category = 'mainstream'
        elif overall_score >= 0.5:
            category = 'indie'
        elif overall_score >= 0.35:
            category = 'niche'
        else:
            category = 'festival'

        # Primary market
        primary_market = max(segments, key=lambda s: s.viability).segment

        # Audience size
        avg_audience = sum(q.appeal_score for q in quadrants) / len(quadrants)
        if avg_audience >= 0.8:
            audience_size = 'massive'
        elif avg_audience >= 0.6:
            audience_size = 'large'
        elif avg_audience >= 0.4:
            audience_size = 'medium'
        elif avg_audience >= 0.2:
            audience_size = 'small'
        else:
            audience_size = 'niche'

        # Revenue potential
        if overall_score >= 0.75:
            revenue_potential = 'very_high'
        elif overall_score >= 0.6:
            revenue_potential = 'high'
        elif overall_score >= 0.4:
            revenue_potential = 'medium'
        else:
            revenue_potential = 'low'

        # ROI projection
        risk_factor = 1.0 - (sum(r.severity for r in risks) / len(risks)) if risks else 0.8
        roi_projection = overall_score * risk_factor

        # Break even likelihood
        break_even = 0.5 + (overall_score - 0.5) + (risk_factor - 0.5)
        break_even = max(0.0, min(1.0, break_even))

        # Genre marketability
        genre_data = self.genre_market_values.get(genre, {'value': 0.5})
        genre_marketability = genre_data['value']

        # Hook strength
        hook_elements = [e for e in commercial_elements if e.element_type == 'hook']
        hook_strength = min(len(hook_elements) * 0.5, 1.0) if hook_elements else 0.3

        # Global potential
        international_segment = next((s for s in segments if s.segment == 'international'), None)
        global_potential = international_segment.viability if international_segment else 0.5

        return MarketAnalysis(
            overall_market_score=overall_score,
            market_category=category,
            primary_market=primary_market,
            audience_size=audience_size,
            revenue_potential=revenue_potential,
            roi_projection=roi_projection,
            break_even_likelihood=break_even,
            genre_marketability=genre_marketability,
            hook_strength=hook_strength,
            competition_readiness=competitive.differentiation_score,
            global_potential=global_potential
        )

    def _generate_marketing_strategy(self, analysis: MarketAnalysis,
                                    commercial_elements: List[CommercialElement],
                                    quadrants: List[AudienceQuadrant]) -> Dict[str, str]:
        """Generate marketing strategy recommendations."""
        strategy = {}

        # Positioning
        if analysis.market_category == 'blockbuster':
            strategy['positioning'] = "Event film - wide release with massive marketing"
        elif analysis.market_category == 'mainstream':
            strategy['positioning'] = "Broad appeal - target multiple demographics"
        elif analysis.market_category == 'indie':
            strategy['positioning'] = "Quality-focused - festival to platform strategy"
        else:
            strategy['positioning'] = "Niche appeal - targeted marketing"

        # Primary audience
        best_quadrant = max(quadrants, key=lambda q: q.appeal_score)
        strategy['primary_audience'] = f"Target {best_quadrant.demographic}"

        # Key selling points
        if commercial_elements:
            element_types = set(e.element_type for e in commercial_elements)
            strategy['key_selling_points'] = ', '.join(element_types)
        else:
            strategy['key_selling_points'] = "Character-driven story"

        # Release strategy
        if analysis.primary_market == 'theatrical':
            strategy['release_strategy'] = "Wide theatrical release"
        elif analysis.primary_market == 'streaming':
            strategy['release_strategy'] = "Direct to streaming platform"
        else:
            strategy['release_strategy'] = "Limited theatrical then streaming"

        return strategy

    def _calculate_festival_potential(self, scenes: List[Dict], genre: str) -> float:
        """Calculate festival circuit potential."""
        potential = 0.0

        # Genre bonus
        if genre in ['drama', 'documentary']:
            potential += 0.3

        # Artistic elements
        artistic_words = ['artistic', 'beautiful', 'profound', 'meditation', 'contemplative']
        artistic_count = sum(1 for scene in scenes
                           for action in scene['action']
                           if any(word in action['text'].lower() for word in artistic_words))

        if artistic_count >= 2:
            potential += 0.3

        # Limited scope (festival-friendly)
        if len(scenes) <= 15:
            potential += 0.2

        # Character focus
        character_count = len(set(char for scene in scenes for char in scene['characters']))
        if character_count <= 5:
            potential += 0.2

        return min(potential, 1.0)

    def _calculate_awards_potential(self, scenes: List[Dict], genre: str) -> float:
        """Calculate awards potential."""
        potential = 0.0

        # Genre considerations
        if genre in ['drama', 'biopic', 'historical']:
            potential += 0.3

        # Performance opportunities (monologues)
        monologue_count = sum(1 for scene in scenes
                             for dialogue in scene['dialogue']
                             if len(dialogue['text'].split()) > 40)

        if monologue_count >= 2:
            potential += 0.3

        # Thematic depth indicators
        theme_words = ['justice', 'truth', 'freedom', 'sacrifice', 'redemption', 'identity']
        theme_presence = sum(1 for scene in scenes
                           for dialogue in scene['dialogue']
                           if any(word in dialogue['text'].lower() for word in theme_words))

        if theme_presence >= len(scenes) * 0.2:
            potential += 0.2

        # Technical showcase opportunities
        if any('one shot' in action['text'].lower() or 'continuous' in scene['heading']
              for scene in scenes for action in scene['action']):
            potential += 0.2

        return min(potential, 1.0)

    def _calculate_franchise_potential(self, scenes: List[Dict],
                                      commercial_elements: List[CommercialElement]) -> float:
        """Calculate franchise/sequel potential."""
        potential = 0.0

        # World building elements
        world_building_words = ['universe', 'mythology', 'legend', 'prophecy', 'ancient']
        world_count = sum(1 for scene in scenes
                         for action in scene['action']
                         if any(word in action['text'].lower() for word in world_building_words))

        if world_count >= 2:
            potential += 0.3

        # Character ensemble size
        character_count = len(set(char for scene in scenes for char in scene['characters']))
        if character_count >= 8:
            potential += 0.2

        # Open ending indicators
        if scenes:
            last_scene_text = ' '.join(a['text'].lower() for a in scenes[-1]['action'])
            if any(word in last_scene_text for word in ['continues', 'begins', 'next', 'future']):
                potential += 0.3

        # Commercial elements that suggest franchise
        franchise_elements = [e for e in commercial_elements if e.element_type == 'franchise']
        if franchise_elements:
            potential += 0.2

        return min(potential, 1.0)

    def _calculate_merchandising_potential(self, scenes: List[Dict], genre: str,
                                          quadrants: List[AudienceQuadrant]) -> float:
        """Calculate merchandising potential."""
        potential = 0.0

        # Genre bonus
        if genre in ['animation', 'fantasy', 'sci_fi', 'superhero']:
            potential += 0.3

        # Family audience appeal
        family_quad = next((q for q in quadrants if q.demographic == 'family_audience'), None)
        if family_quad and family_quad.appeal_score >= 0.7:
            potential += 0.4

        # Distinctive visual elements
        visual_words = ['costume', 'uniform', 'weapon', 'vehicle', 'creature', 'robot']
        visual_count = sum(1 for scene in scenes
                         for action in scene['action']
                         if any(word in action['text'].lower() for word in visual_words))

        if visual_count >= 3:
            potential += 0.2

        # Memorable characters
        character_count = len(set(char for scene in scenes for char in scene['characters']))
        if character_count >= 5:
            potential += 0.1

        return min(potential, 1.0)

    def _check_rules(self, analysis: MarketAnalysis, segments: List[MarketSegment],
                    commercial_elements: List[CommercialElement]) -> List[Dict[str, Any]]:
        """Check screenplay against market potential rules."""
        violations = []

        for rule in self.rules_config['rules']:
            violation = self._check_single_rule(rule, analysis, segments, commercial_elements)
            if violation:
                violations.append(violation)

        return violations

    def _check_single_rule(self, rule: Dict, analysis: MarketAnalysis,
                          segments: List[MarketSegment],
                          commercial_elements: List[CommercialElement]) -> Optional[Dict]:
        """Check a single rule."""
        passed = True
        details = ""

        rule_id = rule['id']

        if rule_id == 'MAR.R001':  # Audience Appeal
            passed = analysis.overall_market_score >= 0.5
            details = f"Market score: {analysis.overall_market_score:.2f}"

        elif rule_id == 'MAR.R002':  # Genre Marketability
            passed = analysis.genre_marketability >= 0.6
            details = f"Genre marketability: {analysis.genre_marketability:.2f}"

        elif rule_id == 'MAR.R003':  # Hook Strength
            passed = analysis.hook_strength >= 0.5
            details = f"Hook strength: {analysis.hook_strength:.2f}"

        elif rule_id == 'MAR.R004':  # Competition Position
            passed = analysis.competition_readiness >= 0.5
            details = f"Competition readiness: {analysis.competition_readiness:.2f}"

        elif rule_id == 'MAR.R005':  # Budget Feasibility
            passed = analysis.break_even_likelihood >= 0.5
            details = f"Break-even likelihood: {analysis.break_even_likelihood:.2f}"

        elif rule_id == 'MAR.R007':  # International Appeal
            passed = analysis.global_potential >= 0.5
            details = f"Global potential: {analysis.global_potential:.2f}"

        elif rule_id == 'MAR.R010':  # Streaming Viability
            streaming = next((s for s in segments if s.segment == 'streaming'), None)
            passed = streaming and streaming.viability >= 0.6
            details = f"Streaming viability: {streaming.viability if streaming else 0:.2f}"

        elif rule_id == 'MAR.R011':  # Marketing Clarity
            passed = len(commercial_elements) >= 2
            details = f"Commercial elements: {len(commercial_elements)}"

        elif rule_id == 'MAR.R015':  # ROI Potential
            passed = analysis.roi_projection >= 0.5
            details = f"ROI projection: {analysis.roi_projection:.2f}"

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

    def _generate_recommendations(self, analysis: MarketAnalysis,
                                 risks: List[MarketRisk],
                                 violations: List[Dict]) -> List[str]:
        """Generate market potential recommendations."""
        recommendations = []

        # Address market score
        if analysis.overall_market_score < 0.6:
            recommendations.append(
                "Strengthen commercial elements to improve market appeal"
            )

        # Hook strength
        if analysis.hook_strength < 0.5:
            recommendations.append(
                "Develop clearer, more marketable hook for easier marketing"
            )

        # Competition
        if analysis.competition_readiness < 0.5:
            recommendations.append(
                "Differentiate from competition with unique elements"
            )

        # Global potential
        if analysis.global_potential < 0.6:
            recommendations.append(
                "Add universal themes to increase international appeal"
            )

        # Risk mitigation
        if risks:
            highest_risk = max(risks, key=lambda r: r.severity)
            recommendations.append(f"Priority risk: {highest_risk.mitigation}")

        # Critical violations
        critical_violations = [v for v in violations if v['severity'] == 'critical']
        if critical_violations:
            recommendations.append(
                f"Critical issue: {critical_violations[0]['fix']}"
            )

        # Market positioning
        if analysis.market_category == 'niche':
            recommendations.append(
                "Consider broadening appeal or embracing niche positioning fully"
            )

        return recommendations[:6]  # Top 6 recommendations

    def _calculate_score(self, analysis: MarketAnalysis, violations: List[Dict]) -> int:
        """Calculate overall market potential score."""
        # Base score from market analysis
        score = int(analysis.overall_market_score * 100)

        # Ensure minimum base score
        score = max(20, score)

        # Deduct for violations
        severity_penalties = {
            'critical': 15,
            'high': 10,
            'medium': 5,
            'low': 2
        }

        for violation in violations:
            score -= severity_penalties.get(violation['severity'], 5)

        # Bonus for exceptional market potential
        if analysis.market_category == 'blockbuster':
            score += 10
        elif analysis.market_category == 'mainstream':
            score += 5

        return max(10, min(95, score))  # Minimum score of 10