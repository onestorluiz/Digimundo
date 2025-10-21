"""
Script Doctor Evaluatormon - Master Evaluation and Synthesis Specialist
A Script Doctor™ in Digimon form specializing in overall quality evaluation, strengths/weaknesses analysis, industry readiness.
THE FINAL SPECIALIST (#24/24) - Master evaluator that synthesizes all other 23 specialists.
"""

import re
import yaml
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple, Set
from dataclasses import dataclass
from collections import defaultdict, Counter
import string


@dataclass
class EvaluationProfile:
    """Overall evaluation profile."""
    overall_quality: bool  # High overall quality
    strengths_identified: bool  # Clear strengths present
    weaknesses_identified: bool  # Weaknesses identified for improvement
    critical_issues_present: bool  # PENALTY (deal-breakers)
    industry_ready: bool  # Ready for market
    audience_appeal: bool  # Will engage audience
    commercial_potential: bool  # Marketable
    execution_quality: bool  # Craft level high
    originality: bool  # Fresh, not derivative
    emotional_impact: bool  # Moves audience
    intellectual_engagement: bool  # Challenges audience
    thematic_depth: bool  # Meaningful themes
    story_cohesion: bool  # All elements work together
    professional_standard: bool  # Industry standards met
    character_excellence: bool  # Characters compelling
    structure_excellence: bool  # Structure solid
    dialogue_excellence: bool  # Dialogue strong
    pacing_excellence: bool  # Pacing effective
    strengths_count: int  # Number of major strengths
    weaknesses_count: int  # Number of major weaknesses
    overall_score: float


@dataclass
class EvaluationResults:
    """Complete evaluation results."""
    evaluation_profile: EvaluationProfile
    strengths_list: List[str]  # Major strengths
    weaknesses_list: List[str]  # Major weaknesses
    critical_issues_list: List[str]  # Deal-breakers
    recommendations_prioritized: List[str]  # Prioritized fixes
    industry_readiness_assessment: str  # Ready for market?
    audience_appeal_assessment: str  # Will audience engage?
    commercial_potential_assessment: str  # Marketable?
    execution_quality_assessment: str  # Craft level
    pass_fail_determination: str  # Industry standards
    final_verdict: str  # Overall verdict
    score: float
    diagnosis: str
    recommendations: List[str]


class DrEvaluator:
    """
    Script Doctor Evaluatormon - The Master Evaluation Specialist

    A Script Doctor™ in Digimon form, specializing in overall quality evaluation,
    strengths/weaknesses analysis, recommendations synthesis, industry readiness assessment.

    THE FINAL SPECIALIST (#24/24) - Master evaluator that aggregates all other specialists.

    Identity: Script Doctor first, Digimon evaluation specialist second.
    """

    def __init__(self, rules_path: str = None):
        """Initialize Script Doctor Evaluatormon with rules and configuration."""
        self.name = "Script Doctor Evaluatormon"
        self.digimon_name = "Evaluatormon"
        self.title = "Script Doctor - Master Evaluation Specialist"
        self.specialty = "Overall quality evaluation, strengths/weaknesses, industry readiness, recommendations synthesis"
        self.identity = "I am Script Doctor Evaluatormon, a professional Script Doctor™ specializing in master evaluation"

        # Load rules
        if rules_path:
            self.rules_path = Path(rules_path)
        else:
            self.rules_path = Path(__file__).parent.parent.parent / "config" / "rules" / "evaluator_rules.yaml"

        self.rules = self._load_rules()

        # Deep context queries for the 13 books - EVALUATION SPECIFIC
        self.deep_context_queries = [
            "McKee Story overall quality screenplay evaluation assessment",
            "McKee Story industry standards professional screenplay criteria",
            "McKee Story strengths weaknesses screenplay analysis",
            "McKee Story execution quality craft mastery technique",
            "McKee Story emotional impact audience engagement moved",
            "McKee Story intellectual engagement thought-provoking meaningful",
            "McKee Story originality fresh unique not derivative",
            "McKee Story story cohesion unity all elements integrated",
            "McKee Story marketability commercial potential sellable",
            "McKee Story professional standards industry ready polished",
            # McKee Story - FUNDAMENTAL PRINCIPLES (ultra-specific core concepts for evaluation)
            "McKee Story scene not true event cut it if scene does not turn eliminate",
            "McKee Story protagonist must actively pursue desire not passive victim circumstances",
            "McKee Story controlling idea value plus cause meaningful thematic statement",
            "McKee Story change essential story nothing changes nothing happens no story",
            "Field Screenplay evaluation criteria professional assessment",
            "Field industry standards screenplay quality professional level",
            "Field strengths identification what works screenplay",
            "Field weaknesses identification what needs improvement",
            "Field commercial potential marketability sellable script",
            "Field professional execution craft quality technique",
            "Snyder Save Cat evaluation overall quality assessment",
            "Snyder strengths weaknesses screenplay analysis identification",
            "Snyder marketability commercial appeal primal engaging",
            "Snyder Save Cat beats coverage evaluation complete",
            "Snyder audience appeal engaging entertaining satisfying",
            "Snyder emotional impact audience moved invested caring",
            "Truby Anatomy evaluation screenplay quality assessment",
            "Truby moral argument thematic depth meaningful significant",
            "Truby originality unique fresh not derivative clichéd",
            "Truby story cohesion unity integrated organic whole",
            "Truby execution quality craft mastery professional level",
            "Truby character arc transformation complete satisfying",
            "Seger Making Good Script Great evaluation assessment quality",
            "Seger strengths identification what works screenplay",
            "Seger weaknesses identification problems issues fix",
            "Seger recommendations prioritized most important first",
            "Seger rewrite evaluation what needs improvement focus",
            "Seger professional standards industry ready polished",
            "Vogler Writer's Journey hero journey complete satisfying",
            "Vogler emotional resonance audience moved engaged caring",
            "Vogler mythic structure universal patterns effective",
            "Campbell Hero 1000 Faces universal story power",
            "Campbell mythic resonance deep emotional impact audience",
            "Campbell archetypal depth character story significance",
            "Aristotle Poetics tragedy quality excellence evaluation",
            "Aristotle catharsis emotional purging audience moved",
            "Aristotle unity action integrated organic whole cohesion",
            "Aristotle magnitude appropriate length pacing scope",
            "Egri Art Dramatic Writing premise strength evaluation",
            "Egri character dimensional depth believable compelling",
            "Egri conflict orchestration dramatic tension escalation",
            "Goldman Adventures Screen Trade screenplay evaluation quality",
            "Goldman professional standards industry expectations met",
            "Goldman commercial appeal marketability audience engagement",
            "Goldman execution quality craft professional polished",
            "Rhimes Year Yes television quality evaluation standards",
            "Rhimes emotional authenticity genuine believable honest",
            "Rhimes audience connection engagement caring investment",
            "Mamet Three Uses Knife dramatic writing quality",
            "Mamet ruthless editing essential only no waste",
            "Mamet dramatic truth honest authentic genuine",
            "Mackendrick Film Filmmaking visual storytelling quality",
            "Mackendrick control craft mastery technique execution",
            "overall quality screenplay evaluation high professional",
            "strengths identification major assets what works well",
            "weaknesses identification problems issues need improvement",
            "critical issues deal-breakers major flaws serious problems",
            "industry readiness professional standards market ready",
            "audience appeal engaging entertaining satisfying moving",
            "commercial potential marketability sellable industry",
            "execution quality craft mastery professional technique",
            "originality fresh unique not derivative clichéd formulaic",
            "emotional impact audience moved engaged caring invested",
            "intellectual engagement thought-provoking meaningful challenging",
            "thematic depth significant meaningful profound resonant",
            "story cohesion unity integrated organic all elements work",
            "pass fail determination industry standards professional level",
            "final verdict overall assessment recommendation decision"

        # McKee STORY - GPT-5 extracted (12 Oct 2025)
        "McKee Story evaluate scene turns value condition positive negative swing",
        "McKee Story evaluate protagonist active willful pursues desire escalates risk",
        "McKee Story evaluate climax meaning produces emotion key image truth",
        "McKee Story evaluate ending no coincidence machine god disallow",
        "McKee Story evaluate engagement curiosity concern mystery suspense irony",

        ]

        # Evaluation analysis patterns (bilingual: EN + PT) - 150-170+ markers

        # Overall quality markers
        self.overall_quality_markers = [
            # English
            "high quality", "excellent", "outstanding", "superior", "exceptional",
            "professional quality", "industry standard", "well-crafted", "polished",
            "strong screenplay", "solid script", "effective storytelling", "compelling",
            "masterful", "skillful", "accomplished", "refined", "sophisticated",
            # Portuguese
            "alta qualidade", "excelente", "excepcional", "superior", "excepcional",
            "qualidade profissional", "padrão da indústria", "bem elaborado", "polido",
            "roteiro forte", "script sólido", "narrativa eficaz", "convincente",
            "magistral", "habilidoso", "realizado", "refinado", "sofisticado"
        ]

        # Strengths markers (what works well)
        self.strengths_markers = [
            # English
            "strength", "strong", "works well", "effective", "compelling",
            "excellent", "outstanding", "powerful", "brilliant", "exceptional",
            "major asset", "key strength", "standout", "impressive", "notable",
            "well-executed", "skillfully done", "masterfully handled", "succeeds",
            # Portuguese
            "força", "forte", "funciona bem", "eficaz", "convincente",
            "excelente", "excepcional", "poderoso", "brilhante", "excepcional",
            "grande ativo", "força chave", "destaque", "impressionante", "notável",
            "bem executado", "habilmente feito", "magistralmente tratado", "sucede"
        ]

        # Weaknesses markers (what needs improvement)
        self.weaknesses_markers = [
            # English
            "weakness", "weak", "needs work", "problem", "issue", "flaw",
            "could be stronger", "falls short", "ineffective", "underdeveloped",
            "lacking", "insufficient", "inadequate", "missing", "absent",
            "needs improvement", "requires attention", "must be addressed",
            # Portuguese
            "fraqueza", "fraco", "precisa trabalho", "problema", "questão", "falha",
            "poderia ser mais forte", "fica aquém", "ineficaz", "subdesenvolvido",
            "faltando", "insuficiente", "inadequado", "ausente", "faltante",
            "precisa melhoria", "requer atenção", "deve ser abordado"
        ]

        # Critical issues markers (deal-breakers)
        self.critical_issues_markers = [
            # English
            "critical issue", "major flaw", "deal-breaker", "fatal flaw", "serious problem",
            "fundamental problem", "structural collapse", "broken", "fails completely",
            "unsalvageable", "beyond repair", "catastrophic", "devastating weakness",
            "unworkable", "impossible to fix", "terminal", "doomed", "fatally flawed",
            # Portuguese
            "questão crítica", "falha grave", "quebra negócio", "falha fatal", "problema sério",
            "problema fundamental", "colapso estrutural", "quebrado", "falha completamente",
            "insalvável", "além do reparo", "catastrófico", "fraqueza devastadora",
            "inviável", "impossível consertar", "terminal", "condenado", "fatalmente falho"
        ]

        # Industry readiness markers
        self.industry_ready_markers = [
            # English
            "industry ready", "market ready", "professional standard", "ready to sell",
            "ready for production", "production-ready", "polished", "finished",
            "ready to submit", "ready for market", "industry standards met",
            "professional level", "competitive", "sellable", "marketable",
            # Portuguese
            "pronto para indústria", "pronto para mercado", "padrão profissional", "pronto para vender",
            "pronto para produção", "pronto para produção", "polido", "finalizado",
            "pronto para submeter", "pronto para mercado", "padrões da indústria atendidos",
            "nível profissional", "competitivo", "vendável", "comercializável"
        ]

        # Audience appeal markers
        self.audience_appeal_markers = [
            # English
            "audience appeal", "engaging", "entertaining", "compelling", "captivating",
            "audience will love", "crowd-pleaser", "page-turner", "gripping",
            "holds attention", "keeps audience invested", "emotionally engaging",
            "satisfying", "rewarding", "audience satisfaction", "universal appeal",
            # Portuguese
            "apelo ao público", "envolvente", "entretenimento", "convincente", "cativante",
            "público vai amar", "agrada multidões", "vira páginas", "envolvente",
            "prende atenção", "mantém público investido", "emocionalmente envolvente",
            "satisfatório", "recompensador", "satisfação do público", "apelo universal"
        ]

        # Commercial potential markers
        self.commercial_potential_markers = [
            # English
            "commercial potential", "marketable", "sellable", "box office appeal",
            "franchise potential", "audience potential", "commercial viability",
            "bankable", "profitable", "money-maker", "commercial success",
            "broad appeal", "mass market", "mainstream", "accessible",
            # Portuguese
            "potencial comercial", "comercializável", "vendável", "apelo de bilheteria",
            "potencial de franquia", "potencial de público", "viabilidade comercial",
            "bancável", "lucrativo", "gerador de dinheiro", "sucesso comercial",
            "apelo amplo", "mercado de massa", "mainstream", "acessível"
        ]

        # Execution quality markers (craft level)
        self.execution_quality_markers = [
            # English
            "execution quality", "craft", "mastery", "technique", "skill",
            "professional execution", "well-crafted", "expertly done", "skillfully executed",
            "technical excellence", "polished", "refined", "accomplished",
            "masterful technique", "professional level", "high craft", "expert craft",
            # Portuguese
            "qualidade de execução", "ofício", "maestria", "técnica", "habilidade",
            "execução profissional", "bem elaborado", "feito com expertise", "executado habilmente",
            "excelência técnica", "polido", "refinado", "realizado",
            "técnica magistral", "nível profissional", "alto ofício", "ofício especializado"
        ]

        # Originality markers
        self.originality_markers = [
            # English
            "original", "fresh", "unique", "innovative", "inventive", "creative",
            "novel", "distinctive", "groundbreaking", "unprecedented", "new",
            "fresh perspective", "original voice", "innovative approach", "unique take",
            "not derivative", "not formulaic", "not clichéd", "fresh twist",
            # Portuguese
            "original", "fresco", "único", "inovador", "inventivo", "criativo",
            "novo", "distintivo", "revolucionário", "sem precedentes", "novo",
            "perspectiva fresca", "voz original", "abordagem inovadora", "visão única",
            "não derivativo", "não formulaico", "não clichê", "virada fresca"
        ]

        # Emotional impact markers
        self.emotional_impact_markers = [
            # English
            "emotional impact", "moves audience", "emotionally powerful", "touching",
            "moving", "affecting", "poignant", "emotional resonance", "heart",
            "emotionally engaging", "audience cares", "emotionally invested",
            "cathartic", "emotional payoff", "tears", "laughter", "joy", "fear",
            # Portuguese
            "impacto emocional", "move público", "emocionalmente poderoso", "tocante",
            "comovente", "afetante", "pungente", "ressonância emocional", "coração",
            "emocionalmente envolvente", "público se importa", "emocionalmente investido",
            "catártico", "recompensa emocional", "lágrimas", "risada", "alegria", "medo"
        ]

        # Intellectual engagement markers
        self.intellectual_engagement_markers = [
            # English
            "intellectual engagement", "thought-provoking", "challenging", "complex",
            "layered", "sophisticated", "intelligent", "smart", "cerebral",
            "makes audience think", "intellectually stimulating", "meaningful",
            "profound", "deep", "substantial", "significant", "important",
            # Portuguese
            "engajamento intelectual", "provocador", "desafiador", "complexo",
            "em camadas", "sofisticado", "inteligente", "esperto", "cerebral",
            "faz público pensar", "intelectualmente estimulante", "significativo",
            "profundo", "profundo", "substancial", "significativo", "importante"
        ]

        # Thematic depth markers
        self.thematic_depth_markers = [
            # English
            "thematic depth", "meaningful themes", "significant themes", "profound",
            "resonant", "universal themes", "timeless", "important message",
            "moral argument", "thematic complexity", "thematic richness", "substance",
            "depth", "significance", "weight", "gravitas", "meaning",
            # Portuguese
            "profundidade temática", "temas significativos", "temas significativos", "profundo",
            "ressonante", "temas universais", "atemporal", "mensagem importante",
            "argumento moral", "complexidade temática", "riqueza temática", "substância",
            "profundidade", "significância", "peso", "gravidade", "significado"
        ]

        # Story cohesion markers (all elements work together)
        self.story_cohesion_markers = [
            # English
            "story cohesion", "unified", "integrated", "organic whole", "coherent",
            "all elements work together", "everything connects", "unified vision",
            "harmonious", "seamless", "well-integrated", "tightly woven",
            "nothing extraneous", "everything serves story", "unity of action",
            # Portuguese
            "coesão da história", "unificado", "integrado", "todo orgânico", "coerente",
            "todos elementos trabalham juntos", "tudo conecta", "visão unificada",
            "harmonioso", "sem costuras", "bem integrado", "bem tecido",
            "nada estranho", "tudo serve história", "unidade de ação"
        ]

        # Professional standard markers
        self.professional_standard_markers = [
            # English
            "professional standard", "industry standard", "professional level",
            "professional quality", "meets standards", "industry expectations met",
            "professional polish", "ready for industry", "competitive",
            "publishable", "producible", "professional grade", "industry level",
            # Portuguese
            "padrão profissional", "padrão da indústria", "nível profissional",
            "qualidade profissional", "atende padrões", "expectativas da indústria atendidas",
            "polimento profissional", "pronto para indústria", "competitivo",
            "publicável", "produzível", "grau profissional", "nível da indústria"
        ]

        # Character excellence markers
        self.character_excellence_markers = [
            # English
            "character excellence", "compelling characters", "memorable characters",
            "well-developed characters", "dimensional characters", "believable",
            "character depth", "character complexity", "character authenticity",
            "characters come alive", "audience cares about characters",
            # Portuguese
            "excelência de personagem", "personagens convincentes", "personagens memoráveis",
            "personagens bem desenvolvidos", "personagens dimensionais", "acreditável",
            "profundidade de personagem", "complexidade de personagem", "autenticidade de personagem",
            "personagens ganham vida", "público se importa com personagens"
        ]

        # Structure excellence markers
        self.structure_excellence_markers = [
            # English
            "structure excellence", "solid structure", "strong structure",
            "well-structured", "tight structure", "structural integrity",
            "clear act breaks", "effective turning points", "satisfying climax",
            "structural cohesion", "structural clarity", "architectural strength",
            # Portuguese
            "excelência estrutural", "estrutura sólida", "estrutura forte",
            "bem estruturado", "estrutura apertada", "integridade estrutural",
            "quebras de ato claras", "pontos de virada eficazes", "clímax satisfatório",
            "coesão estrutural", "clareza estrutural", "força arquitetônica"
        ]

        # Dialogue excellence markers
        self.dialogue_excellence_markers = [
            # English
            "dialogue excellence", "strong dialogue", "natural dialogue",
            "authentic dialogue", "sharp dialogue", "witty dialogue",
            "subtext", "character voice", "distinctive voices", "memorable lines",
            "dialogue rings true", "dialogue serves character", "dialogue sparkles",
            # Portuguese
            "excelência de diálogo", "diálogo forte", "diálogo natural",
            "diálogo autêntico", "diálogo afiado", "diálogo espirituoso",
            "subtexto", "voz de personagem", "vozes distintivas", "linhas memoráveis",
            "diálogo soa verdadeiro", "diálogo serve personagem", "diálogo brilha"
        ]

        # Pacing excellence markers
        self.pacing_excellence_markers = [
            # English
            "pacing excellence", "well-paced", "effective pacing", "tight pacing",
            "rhythm", "tempo", "forward momentum", "never drags", "page-turner",
            "propulsive", "urgent", "relentless", "perfectly timed", "balanced pace",
            # Portuguese
            "excelência de ritmo", "bem ritmado", "ritmo eficaz", "ritmo apertado",
            "ritmo", "tempo", "momentum para frente", "nunca arrasta", "vira páginas",
            "propulsivo", "urgente", "implacável", "perfeitamente cronometrado", "ritmo equilibrado"
        ]

    def _load_rules(self) -> Dict:
        """Load rules from YAML file."""
        if self.rules_path.exists():
            with open(self.rules_path, 'r') as f:
                return yaml.safe_load(f)
        return {}

    def analyze(self, screenplay_text: str, specialist_results: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Perform master evaluation of screenplay.

        Args:
            screenplay_text: The full screenplay text
            specialist_results: Optional results from other 23 specialists for aggregation

        Returns:
            Complete evaluation diagnostic report
        """
        # Extract page count and scenes
        page_count = self._estimate_page_count(screenplay_text)
        scenes = self._extract_scenes(screenplay_text)

        # Extract Act 1, 2, 3 for analysis
        act1_text = self._extract_pages(screenplay_text, 0, int(page_count * 0.25))
        act2_text = self._extract_pages(screenplay_text, int(page_count * 0.25), int(page_count * 0.75))
        act3_text = self._extract_pages(screenplay_text, int(page_count * 0.75), page_count)

        # Extract opening and ending
        opening_text = self._extract_pages(screenplay_text, 0, 10)
        ending_text = self._extract_pages(screenplay_text, max(0, page_count - 10), page_count)

        # Analyze overall quality
        overall_quality = self._analyze_overall_quality(screenplay_text, specialist_results)

        # Identify strengths (what works well)
        strengths = self._identify_strengths(screenplay_text, specialist_results)

        # Identify weaknesses (what needs improvement)
        weaknesses = self._identify_weaknesses(screenplay_text, specialist_results)

        # Detect critical issues (deal-breakers)
        critical_issues = self._detect_critical_issues(screenplay_text, specialist_results)

        # Assess industry readiness
        industry_readiness = self._assess_industry_readiness(screenplay_text, specialist_results)

        # Assess audience appeal
        audience_appeal = self._assess_audience_appeal(screenplay_text, specialist_results)

        # Assess commercial potential
        commercial_potential = self._assess_commercial_potential(screenplay_text, specialist_results)

        # Assess execution quality (craft level)
        execution_quality = self._assess_execution_quality(screenplay_text, specialist_results)

        # Assess originality
        originality = self._assess_originality(screenplay_text, specialist_results)

        # Assess emotional impact
        emotional_impact = self._assess_emotional_impact(screenplay_text, specialist_results)

        # Assess intellectual engagement
        intellectual_engagement = self._assess_intellectual_engagement(screenplay_text, specialist_results)

        # Assess thematic depth
        thematic_depth = self._assess_thematic_depth(screenplay_text, specialist_results)

        # Assess story cohesion
        story_cohesion = self._assess_story_cohesion(screenplay_text, specialist_results)

        # Assess professional standard
        professional_standard = self._assess_professional_standard(screenplay_text, specialist_results)

        # Assess character excellence
        character_excellence = self._assess_character_excellence(screenplay_text, specialist_results)

        # Assess structure excellence
        structure_excellence = self._assess_structure_excellence(screenplay_text, specialist_results)

        # Assess dialogue excellence
        dialogue_excellence = self._assess_dialogue_excellence(screenplay_text, specialist_results)

        # Assess pacing excellence
        pacing_excellence = self._assess_pacing_excellence(screenplay_text, specialist_results)

        # Build evaluation profile
        evaluation_profile = EvaluationProfile(
            overall_quality=overall_quality["high_quality"],
            strengths_identified=strengths["identified"],
            weaknesses_identified=weaknesses["identified"],
            critical_issues_present=critical_issues["detected"],
            industry_ready=industry_readiness["ready"],
            audience_appeal=audience_appeal["appealing"],
            commercial_potential=commercial_potential["viable"],
            execution_quality=execution_quality["high_quality"],
            originality=originality["original"],
            emotional_impact=emotional_impact["impactful"],
            intellectual_engagement=intellectual_engagement["engaging"],
            thematic_depth=thematic_depth["deep"],
            story_cohesion=story_cohesion["cohesive"],
            professional_standard=professional_standard["meets_standard"],
            character_excellence=character_excellence["excellent"],
            structure_excellence=structure_excellence["excellent"],
            dialogue_excellence=dialogue_excellence["excellent"],
            pacing_excellence=pacing_excellence["excellent"],
            strengths_count=strengths["count"],
            weaknesses_count=weaknesses["count"],
            overall_score=0.0  # calculated below
        )

        # Calculate overall score
        evaluation_profile.overall_score = self._calculate_overall_score(evaluation_profile)

        # Check against rules
        rule_violations = self._check_evaluation_rules(
            evaluation_profile, overall_quality, strengths, weaknesses,
            critical_issues, industry_readiness, audience_appeal,
            commercial_potential, execution_quality, originality,
            emotional_impact, intellectual_engagement, thematic_depth,
            story_cohesion, professional_standard, character_excellence,
            structure_excellence, dialogue_excellence, pacing_excellence
        )

        # Calculate final score
        score = self._calculate_evaluation_score(evaluation_profile, rule_violations)

        # Generate diagnosis
        diagnosis = self._generate_diagnosis(score, evaluation_profile, rule_violations)

        # Generate pass/fail determination
        pass_fail = self._determine_pass_fail(score, evaluation_profile)

        # Generate final verdict
        final_verdict = self._generate_final_verdict(score, evaluation_profile, pass_fail)

        return {
            "specialist": {
                "name": self.name,
                "title": self.title,
                "specialty": self.specialty,
                "final_specialist": True,
                "specialist_number": "24/24"
            },
            "score": score,
            "overall_quality": {
                "high_quality": overall_quality["high_quality"],
                "quality_level": overall_quality["quality_level"]
            },
            "strengths": {
                "identified": strengths["identified"],
                "count": strengths["count"],
                "list": strengths["list"][:10]
            },
            "weaknesses": {
                "identified": weaknesses["identified"],
                "count": weaknesses["count"],
                "list": weaknesses["list"][:10]
            },
            "critical_issues": {
                "detected": critical_issues["detected"],
                "penalty": critical_issues.get("penalty", False),
                "count": critical_issues["count"],
                "list": critical_issues["list"][:5]
            },
            "industry_readiness": {
                "ready": industry_readiness["ready"],
                "assessment": industry_readiness["assessment"]
            },
            "audience_appeal": {
                "appealing": audience_appeal["appealing"],
                "assessment": audience_appeal["assessment"]
            },
            "commercial_potential": {
                "viable": commercial_potential["viable"],
                "assessment": commercial_potential["assessment"]
            },
            "execution_quality": {
                "high_quality": execution_quality["high_quality"],
                "assessment": execution_quality["assessment"]
            },
            "originality": {
                "original": originality["original"],
                "level": originality["level"]
            },
            "emotional_impact": {
                "impactful": emotional_impact["impactful"],
                "level": emotional_impact["level"]
            },
            "intellectual_engagement": {
                "engaging": intellectual_engagement["engaging"],
                "level": intellectual_engagement["level"]
            },
            "thematic_depth": {
                "deep": thematic_depth["deep"],
                "level": thematic_depth["level"]
            },
            "story_cohesion": {
                "cohesive": story_cohesion["cohesive"],
                "unity_score": story_cohesion["unity_score"]
            },
            "professional_standard": {
                "meets_standard": professional_standard["meets_standard"],
                "level": professional_standard["level"]
            },
            "excellence_areas": {
                "character": character_excellence["excellent"],
                "structure": structure_excellence["excellent"],
                "dialogue": dialogue_excellence["excellent"],
                "pacing": pacing_excellence["excellent"]
            },
            "pass_fail_determination": pass_fail,
            "final_verdict": final_verdict,
            "overall_score": evaluation_profile.overall_score,
            "rule_violations": rule_violations,
            "diagnosis": diagnosis,
            "recommendations": self._generate_recommendations(
                score, rule_violations, evaluation_profile
            ),
            "signature": f"Evaluated by {self.name}™ - THE FINAL SPECIALIST (#24/24)"
        }

    def _estimate_page_count(self, screenplay: str) -> int:
        """Estimate page count from screenplay text."""
        lines = screenplay.split('\n')
        return max(1, len(lines) // 55)

    def _extract_scenes(self, screenplay: str) -> List[Dict]:
        """Extract all scenes from screenplay."""
        scenes = []
        lines = screenplay.split('\n')
        current_scene = None
        scene_number = 0

        for i, line in enumerate(lines):
            # Detect scene heading
            if re.match(r'^(INT\.|EXT\.)', line.strip()):
                # Save previous scene
                if current_scene:
                    current_scene['end_line'] = i - 1
                    current_scene['end_page'] = (i - 1) // 55
                    scenes.append(current_scene)

                # Start new scene
                scene_number += 1
                current_scene = {
                    'number': scene_number,
                    'heading': line.strip(),
                    'start_line': i,
                    'start_page': i // 55,
                    'content': []
                }
            elif current_scene:
                current_scene['content'].append(line)

        # Add last scene
        if current_scene:
            current_scene['end_line'] = len(lines) - 1
            current_scene['end_page'] = (len(lines) - 1) // 55
            scenes.append(current_scene)

        return scenes

    def _extract_pages(self, screenplay: str, start_page: int, end_page: int) -> str:
        """Extract specific page range from screenplay."""
        lines = screenplay.split('\n')
        start_line = start_page * 55
        end_line = end_page * 55
        return '\n'.join(lines[start_line:end_line])

    def _analyze_overall_quality(self, screenplay: str, specialist_results: Dict = None) -> Dict[str, Any]:
        """
        Analyze overall quality (high professional quality).

        McKee: "Story quality - professional standards, industry expectations met."
        Seger: "Overall quality evaluation - what's the level of this screenplay?"
        """
        high_quality = False
        quality_level = "Unknown"

        # Check overall quality markers
        count = 0
        for marker in self.overall_quality_markers:
            count += screenplay.lower().count(marker)

        # Aggregate from specialist results if available
        specialist_score = 0.0
        if specialist_results:
            # Average scores from all specialists
            scores = []
            for specialist, result in specialist_results.items():
                if isinstance(result, dict) and 'score' in result:
                    scores.append(result['score'])
            if scores:
                specialist_score = sum(scores) / len(scores)

        # Determine quality level
        if specialist_score >= 80 or count >= 15:
            high_quality = True
            quality_level = "Excellent"
        elif specialist_score >= 70 or count >= 10:
            high_quality = True
            quality_level = "Good"
        elif specialist_score >= 60 or count >= 5:
            quality_level = "Fair"
        else:
            quality_level = "Needs Work"

        return {
            "high_quality": high_quality,
            "quality_level": quality_level,
            "marker_count": count,
            "specialist_score": specialist_score
        }

    def _identify_strengths(self, screenplay: str, specialist_results: Dict = None) -> Dict[str, Any]:
        """
        Identify strengths (what works well).

        Seger: "Identify strengths - what's working in this screenplay?"
        McKee: "Recognize excellence - acknowledge what's done well."
        """
        identified = False
        strengths_list = []

        # Check strength markers
        count = 0
        for marker in self.strengths_markers:
            marker_count = screenplay.lower().count(marker)
            count += marker_count
            if marker_count > 0:
                # Extract strength instances
                for line in screenplay.split('\n'):
                    if marker in line.lower():
                        strengths_list.append(line.strip()[:100])
                        if len(strengths_list) >= 20:
                            break

        # Aggregate strengths from specialist results
        if specialist_results:
            for specialist, result in specialist_results.items():
                if isinstance(result, dict):
                    # Look for high scores (strengths)
                    if result.get('score', 0) >= 80:
                        strengths_list.append(f"{specialist}: Excellent performance (score: {result['score']:.1f})")

        if count >= 5 or len(strengths_list) >= 3:
            identified = True

        return {
            "identified": identified,
            "count": count,
            "list": strengths_list
        }

    def _identify_weaknesses(self, screenplay: str, specialist_results: Dict = None) -> Dict[str, Any]:
        """
        Identify weaknesses (what needs improvement).

        Seger: "Identify problems - what needs fixing in this screenplay?"
        McKee: "Diagnose weaknesses - find what's not working."
        """
        identified = False
        weaknesses_list = []

        # Check weakness markers
        count = 0
        for marker in self.weaknesses_markers:
            marker_count = screenplay.lower().count(marker)
            count += marker_count
            if marker_count > 0:
                # Extract weakness instances
                for line in screenplay.split('\n'):
                    if marker in line.lower():
                        weaknesses_list.append(line.strip()[:100])
                        if len(weaknesses_list) >= 20:
                            break

        # Aggregate weaknesses from specialist results
        if specialist_results:
            for specialist, result in specialist_results.items():
                if isinstance(result, dict):
                    # Look for low scores (weaknesses)
                    if result.get('score', 100) < 60:
                        weaknesses_list.append(f"{specialist}: Needs work (score: {result['score']:.1f})")
                    # Look for rule violations
                    violations = result.get('rule_violations', [])
                    for violation in violations[:3]:
                        weaknesses_list.append(f"{specialist}: {violation.get('title', 'Issue detected')}")

        if count >= 3 or len(weaknesses_list) >= 2:
            identified = True

        return {
            "identified": identified,
            "count": count,
            "list": weaknesses_list
        }

    def _detect_critical_issues(self, screenplay: str, specialist_results: Dict = None) -> Dict[str, Any]:
        """
        Detect critical issues (deal-breakers).

        McKee: "Fatal flaws - problems that doom the screenplay."
        Seger: "Critical problems - issues that must be fixed."
        """
        detected = False
        penalty = False
        issues_list = []

        # Check critical issue markers
        count = 0
        for marker in self.critical_issues_markers:
            marker_count = screenplay.lower().count(marker)
            count += marker_count
            if marker_count > 0:
                # Extract critical issue instances
                for line in screenplay.split('\n'):
                    if marker in line.lower():
                        issues_list.append(line.strip()[:100])
                        if len(issues_list) >= 10:
                            break

        # Aggregate critical issues from specialist results
        if specialist_results:
            for specialist, result in specialist_results.items():
                if isinstance(result, dict):
                    # Look for critical violations
                    violations = result.get('rule_violations', [])
                    for violation in violations:
                        if violation.get('severity') == 'critical':
                            issues_list.append(f"{specialist}: CRITICAL - {violation.get('title', 'Issue')}")
                            count += 1

        if count >= 2:
            detected = True
            penalty = True
        elif count >= 1:
            detected = True

        return {
            "detected": detected,
            "penalty": penalty,
            "count": count,
            "list": issues_list
        }

    def _assess_industry_readiness(self, screenplay: str, specialist_results: Dict = None) -> Dict[str, Any]:
        """
        Assess industry readiness (ready for market).

        McKee: "Professional standards - meets industry expectations."
        Field: "Industry ready - polished, professional, market-ready."
        """
        ready = False
        assessment = "Not Ready"

        # Check industry ready markers
        count = 0
        for marker in self.industry_ready_markers:
            count += screenplay.lower().count(marker)

        # Aggregate from specialist results
        if specialist_results:
            scores = [r.get('score', 0) for r in specialist_results.values() if isinstance(r, dict)]
            if scores:
                avg_score = sum(scores) / len(scores)
                if avg_score >= 80 and count >= 3:
                    ready = True
                    assessment = "Ready for Market"
                elif avg_score >= 70:
                    assessment = "Nearly Ready - Minor Polish Needed"
                elif avg_score >= 60:
                    assessment = "Not Ready - Substantial Work Needed"
                else:
                    assessment = "Not Ready - Major Overhaul Required"

        return {
            "ready": ready,
            "assessment": assessment,
            "count": count
        }

    def _assess_audience_appeal(self, screenplay: str, specialist_results: Dict = None) -> Dict[str, Any]:
        """
        Assess audience appeal (will engage audience).

        Snyder: "Primal - audience appeal, engaging, entertaining."
        McKee: "Audience engagement - will they care, invest emotionally?"
        """
        appealing = False
        assessment = "Limited Appeal"

        # Check audience appeal markers
        count = 0
        for marker in self.audience_appeal_markers:
            count += screenplay.lower().count(marker)

        if count >= 10:
            appealing = True
            assessment = "Strong Audience Appeal"
        elif count >= 5:
            appealing = True
            assessment = "Moderate Audience Appeal"
        elif count >= 3:
            assessment = "Some Audience Appeal"

        return {
            "appealing": appealing,
            "assessment": assessment,
            "count": count
        }

    def _assess_commercial_potential(self, screenplay: str, specialist_results: Dict = None) -> Dict[str, Any]:
        """
        Assess commercial potential (marketable).

        Goldman: "Commercial viability - will this sell?"
        McKee: "Marketability - commercial appeal, audience potential."
        """
        viable = False
        assessment = "Limited Commercial Potential"

        # Check commercial potential markers
        count = 0
        for marker in self.commercial_potential_markers:
            count += screenplay.lower().count(marker)

        if count >= 8:
            viable = True
            assessment = "Strong Commercial Potential"
        elif count >= 4:
            viable = True
            assessment = "Moderate Commercial Potential"
        elif count >= 2:
            assessment = "Some Commercial Potential"

        return {
            "viable": viable,
            "assessment": assessment,
            "count": count
        }

    def _assess_execution_quality(self, screenplay: str, specialist_results: Dict = None) -> Dict[str, Any]:
        """
        Assess execution quality (craft level).

        McKee: "Craft mastery - technical excellence, execution quality."
        Mackendrick: "Control and craft - mastery of technique."
        """
        high_quality = False
        assessment = "Amateur Level"

        # Check execution quality markers
        count = 0
        for marker in self.execution_quality_markers:
            count += screenplay.lower().count(marker)

        # Aggregate from specialist results
        if specialist_results:
            scores = [r.get('score', 0) for r in specialist_results.values() if isinstance(r, dict)]
            if scores:
                avg_score = sum(scores) / len(scores)
                if avg_score >= 80 or count >= 10:
                    high_quality = True
                    assessment = "Professional Level - Masterful Execution"
                elif avg_score >= 70 or count >= 5:
                    high_quality = True
                    assessment = "Professional Level - Solid Execution"
                elif avg_score >= 60 or count >= 3:
                    assessment = "Competent Level - Some Craft Issues"
                else:
                    assessment = "Amateur Level - Needs Craft Development"

        return {
            "high_quality": high_quality,
            "assessment": assessment,
            "count": count
        }

    def _assess_originality(self, screenplay: str, specialist_results: Dict = None) -> Dict[str, Any]:
        """
        Assess originality (fresh vs derivative).

        McKee: "Originality - fresh, unique, not derivative or clichéd."
        Truby: "Original voice - distinctive, innovative, creative."
        """
        original = False
        level = "Derivative"

        # Check originality markers
        count = 0
        for marker in self.originality_markers:
            count += screenplay.lower().count(marker)

        if count >= 10:
            original = True
            level = "Highly Original"
        elif count >= 5:
            original = True
            level = "Original"
        elif count >= 3:
            level = "Somewhat Original"

        return {
            "original": original,
            "level": level,
            "count": count
        }

    def _assess_emotional_impact(self, screenplay: str, specialist_results: Dict = None) -> Dict[str, Any]:
        """
        Assess emotional impact (moves audience).

        McKee: "Emotional impact - does it move the audience?"
        Aristotle: "Catharsis - emotional purging, audience moved."
        """
        impactful = False
        level = "Limited Impact"

        # Check emotional impact markers
        count = 0
        for marker in self.emotional_impact_markers:
            count += screenplay.lower().count(marker)

        if count >= 12:
            impactful = True
            level = "Powerful Emotional Impact"
        elif count >= 6:
            impactful = True
            level = "Strong Emotional Impact"
        elif count >= 3:
            level = "Moderate Emotional Impact"

        return {
            "impactful": impactful,
            "level": level,
            "count": count
        }

    def _assess_intellectual_engagement(self, screenplay: str, specialist_results: Dict = None) -> Dict[str, Any]:
        """
        Assess intellectual engagement (challenges audience).

        McKee: "Intellectual engagement - thought-provoking, meaningful."
        Truby: "Moral argument - makes audience think, challenges."
        """
        engaging = False
        level = "Surface Level"

        # Check intellectual engagement markers
        count = 0
        for marker in self.intellectual_engagement_markers:
            count += screenplay.lower().count(marker)

        if count >= 10:
            engaging = True
            level = "Highly Intellectually Engaging"
        elif count >= 5:
            engaging = True
            level = "Intellectually Engaging"
        elif count >= 3:
            level = "Some Intellectual Engagement"

        return {
            "engaging": engaging,
            "level": level,
            "count": count
        }

    def _assess_thematic_depth(self, screenplay: str, specialist_results: Dict = None) -> Dict[str, Any]:
        """
        Assess thematic depth (meaningful vs shallow).

        McKee: "Thematic depth - significant, meaningful, resonant."
        Truby: "Moral argument - profound themes, universal significance."
        """
        deep = False
        level = "Shallow"

        # Check thematic depth markers
        count = 0
        for marker in self.thematic_depth_markers:
            count += screenplay.lower().count(marker)

        if count >= 10:
            deep = True
            level = "Profound Thematic Depth"
        elif count >= 5:
            deep = True
            level = "Significant Thematic Depth"
        elif count >= 3:
            level = "Some Thematic Depth"

        return {
            "deep": deep,
            "level": level,
            "count": count
        }

    def _assess_story_cohesion(self, screenplay: str, specialist_results: Dict = None) -> Dict[str, Any]:
        """
        Assess story cohesion (all elements work together).

        Aristotle: "Unity of action - organic whole, nothing extraneous."
        McKee: "Story cohesion - all elements integrated, unified."
        """
        cohesive = False
        unity_score = 0.0

        # Check story cohesion markers
        count = 0
        for marker in self.story_cohesion_markers:
            count += screenplay.lower().count(marker)

        if count >= 8:
            cohesive = True
            unity_score = 0.9
        elif count >= 4:
            cohesive = True
            unity_score = 0.7
        elif count >= 2:
            unity_score = 0.5
        else:
            unity_score = 0.3

        return {
            "cohesive": cohesive,
            "unity_score": unity_score,
            "count": count
        }

    def _assess_professional_standard(self, screenplay: str, specialist_results: Dict = None) -> Dict[str, Any]:
        """
        Assess professional standard (industry standards met).

        McKee: "Professional standards - meets industry expectations."
        Field: "Professional quality - industry standard level."
        """
        meets_standard = False
        level = "Below Standard"

        # Check professional standard markers
        count = 0
        for marker in self.professional_standard_markers:
            count += screenplay.lower().count(marker)

        # Aggregate from specialist results
        if specialist_results:
            scores = [r.get('score', 0) for r in specialist_results.values() if isinstance(r, dict)]
            if scores:
                avg_score = sum(scores) / len(scores)
                if avg_score >= 80 or count >= 8:
                    meets_standard = True
                    level = "Exceeds Professional Standards"
                elif avg_score >= 70 or count >= 5:
                    meets_standard = True
                    level = "Meets Professional Standards"
                elif avg_score >= 60 or count >= 3:
                    level = "Approaching Professional Standards"

        return {
            "meets_standard": meets_standard,
            "level": level,
            "count": count
        }

    def _assess_character_excellence(self, screenplay: str, specialist_results: Dict = None) -> Dict[str, Any]:
        """
        Assess character excellence.

        McKee: "Character excellence - compelling, dimensional, authentic."
        """
        excellent = False

        # Check character excellence markers
        count = 0
        for marker in self.character_excellence_markers:
            count += screenplay.lower().count(marker)

        # Check specialist results for character score
        if specialist_results and 'character' in specialist_results:
            char_score = specialist_results['character'].get('score', 0)
            if char_score >= 80 or count >= 6:
                excellent = True

        return {
            "excellent": excellent,
            "count": count
        }

    def _assess_structure_excellence(self, screenplay: str, specialist_results: Dict = None) -> Dict[str, Any]:
        """
        Assess structure excellence.

        Field: "Structure excellence - solid, tight, well-constructed."
        """
        excellent = False

        # Check structure excellence markers
        count = 0
        for marker in self.structure_excellence_markers:
            count += screenplay.lower().count(marker)

        # Check specialist results for structure score
        if specialist_results and 'structure' in specialist_results:
            struct_score = specialist_results['structure'].get('score', 0)
            if struct_score >= 80 or count >= 6:
                excellent = True

        return {
            "excellent": excellent,
            "count": count
        }

    def _assess_dialogue_excellence(self, screenplay: str, specialist_results: Dict = None) -> Dict[str, Any]:
        """
        Assess dialogue excellence.

        McKee: "Dialogue excellence - natural, sharp, subtext-rich."
        """
        excellent = False

        # Check dialogue excellence markers
        count = 0
        for marker in self.dialogue_excellence_markers:
            count += screenplay.lower().count(marker)

        # Check specialist results for dialogue score
        if specialist_results and 'dialogue' in specialist_results:
            dial_score = specialist_results['dialogue'].get('score', 0)
            if dial_score >= 80 or count >= 6:
                excellent = True

        return {
            "excellent": excellent,
            "count": count
        }

    def _assess_pacing_excellence(self, screenplay: str, specialist_results: Dict = None) -> Dict[str, Any]:
        """
        Assess pacing excellence.

        Field: "Pacing excellence - tight, propulsive, never drags."
        """
        excellent = False

        # Check pacing excellence markers
        count = 0
        for marker in self.pacing_excellence_markers:
            count += screenplay.lower().count(marker)

        # Check specialist results for pacing score
        if specialist_results and 'pacing' in specialist_results:
            pace_score = specialist_results['pacing'].get('score', 0)
            if pace_score >= 80 or count >= 6:
                excellent = True

        return {
            "excellent": excellent,
            "count": count
        }

    def _calculate_overall_score(self, profile: EvaluationProfile) -> float:
        """Calculate overall evaluation score."""
        scores = [
            1.0 if profile.overall_quality else 0.4,  # Critical
            1.0 if profile.strengths_identified else 0.6,  # Important
            1.0 if profile.weaknesses_identified else 0.8,  # Good to know
            0.0 if profile.critical_issues_present else 1.0,  # PENALTY
            1.0 if profile.industry_ready else 0.5,  # Critical
            1.0 if profile.audience_appeal else 0.6,  # Important
            1.0 if profile.commercial_potential else 0.7,  # Nice to have
            1.0 if profile.execution_quality else 0.5,  # Critical
            1.0 if profile.originality else 0.7,  # Important
            1.0 if profile.emotional_impact else 0.6,  # Important
            1.0 if profile.intellectual_engagement else 0.7,  # Nice to have
            1.0 if profile.thematic_depth else 0.7,  # Important
            1.0 if profile.story_cohesion else 0.6,  # Critical
            1.0 if profile.professional_standard else 0.5,  # Critical
            1.0 if profile.character_excellence else 0.7,  # Important
            1.0 if profile.structure_excellence else 0.7,  # Important
            1.0 if profile.dialogue_excellence else 0.7,  # Important
            1.0 if profile.pacing_excellence else 0.7  # Important
        ]

        # Average
        overall = sum(scores) / len(scores)

        return max(0.0, min(1.0, overall))

    def _check_evaluation_rules(self, profile: EvaluationProfile, overall_quality: Dict,
                                strengths: Dict, weaknesses: Dict, critical_issues: Dict,
                                industry_readiness: Dict, audience_appeal: Dict,
                                commercial_potential: Dict, execution_quality: Dict,
                                originality: Dict, emotional_impact: Dict,
                                intellectual_engagement: Dict, thematic_depth: Dict,
                                story_cohesion: Dict, professional_standard: Dict,
                                character_excellence: Dict, structure_excellence: Dict,
                                dialogue_excellence: Dict, pacing_excellence: Dict) -> List[Dict]:
        """Check evaluation against rules."""
        violations = []

        for rule in self.rules.get("rules", []):
            if rule["id"] == "EVALUATOR.R001":
                # Overall Quality
                if not profile.overall_quality:
                    violations.append({
                        "rule_id": rule["id"],
                        "title": rule["title"],
                        "severity": rule["severity"],
                        "message": "Overall quality below professional standards",
                        "fix": rule["fix"]
                    })

            elif rule["id"] == "EVALUATOR.R002":
                # Strengths Identified
                if not profile.strengths_identified:
                    violations.append({
                        "rule_id": rule["id"],
                        "title": rule["title"],
                        "severity": rule["severity"],
                        "message": "No clear strengths identified - screenplay lacks standout elements",
                        "fix": rule["fix"]
                    })

            elif rule["id"] == "EVALUATOR.R003":
                # Weaknesses Balance
                if profile.weaknesses_count > profile.strengths_count * 2:
                    violations.append({
                        "rule_id": rule["id"],
                        "title": rule["title"],
                        "severity": rule["severity"],
                        "message": "Weaknesses significantly outnumber strengths",
                        "fix": rule["fix"]
                    })

            elif rule["id"] == "EVALUATOR.R004":
                # Critical Issues Present
                if profile.critical_issues_present:
                    violations.append({
                        "rule_id": rule["id"],
                        "title": rule["title"],
                        "severity": rule["severity"],
                        "message": "Critical issues detected - deal-breakers present",
                        "fix": rule["fix"]
                    })

            elif rule["id"] == "EVALUATOR.R005":
                # Industry Readiness
                if not profile.industry_ready:
                    violations.append({
                        "rule_id": rule["id"],
                        "title": rule["title"],
                        "severity": rule["severity"],
                        "message": "Not industry ready - needs substantial work before submission",
                        "fix": rule["fix"]
                    })

            elif rule["id"] == "EVALUATOR.R006":
                # Audience Appeal
                if not profile.audience_appeal:
                    violations.append({
                        "rule_id": rule["id"],
                        "title": rule["title"],
                        "severity": rule["severity"],
                        "message": "Limited audience appeal - may not engage viewers",
                        "fix": rule["fix"]
                    })

            elif rule["id"] == "EVALUATOR.R007":
                # Commercial Potential
                if not profile.commercial_potential:
                    violations.append({
                        "rule_id": rule["id"],
                        "title": rule["title"],
                        "severity": rule["severity"],
                        "message": "Limited commercial potential - marketability concerns",
                        "fix": rule["fix"]
                    })

            elif rule["id"] == "EVALUATOR.R008":
                # Execution Quality
                if not profile.execution_quality:
                    violations.append({
                        "rule_id": rule["id"],
                        "title": rule["title"],
                        "severity": rule["severity"],
                        "message": "Execution quality below professional level - craft issues",
                        "fix": rule["fix"]
                    })

            elif rule["id"] == "EVALUATOR.R009":
                # Originality
                if not profile.originality:
                    violations.append({
                        "rule_id": rule["id"],
                        "title": rule["title"],
                        "severity": rule["severity"],
                        "message": "Derivative - lacks originality and fresh perspective",
                        "fix": rule["fix"]
                    })

            elif rule["id"] == "EVALUATOR.R010":
                # Emotional Impact
                if not profile.emotional_impact:
                    violations.append({
                        "rule_id": rule["id"],
                        "title": rule["title"],
                        "severity": rule["severity"],
                        "message": "Limited emotional impact - doesn't move audience",
                        "fix": rule["fix"]
                    })

            elif rule["id"] == "EVALUATOR.R011":
                # Thematic Depth
                if not profile.thematic_depth:
                    violations.append({
                        "rule_id": rule["id"],
                        "title": rule["title"],
                        "severity": rule["severity"],
                        "message": "Shallow themes - lacks meaningful depth",
                        "fix": rule["fix"]
                    })

            elif rule["id"] == "EVALUATOR.R012":
                # Story Cohesion
                if not profile.story_cohesion:
                    violations.append({
                        "rule_id": rule["id"],
                        "title": rule["title"],
                        "severity": rule["severity"],
                        "message": "Poor story cohesion - elements don't work together",
                        "fix": rule["fix"]
                    })

            elif rule["id"] == "EVALUATOR.R013":
                # Professional Standard
                if not profile.professional_standard:
                    violations.append({
                        "rule_id": rule["id"],
                        "title": rule["title"],
                        "severity": rule["severity"],
                        "message": "Below professional standards - not industry level",
                        "fix": rule["fix"]
                    })

            elif rule["id"] == "EVALUATOR.R014":
                # Core Excellence (Character/Structure/Dialogue)
                core_excellence = profile.character_excellence or profile.structure_excellence or profile.dialogue_excellence
                if not core_excellence:
                    violations.append({
                        "rule_id": rule["id"],
                        "title": rule["title"],
                        "severity": rule["severity"],
                        "message": "No core excellence - character, structure, and dialogue all weak",
                        "fix": rule["fix"]
                    })

            elif rule["id"] == "EVALUATOR.R015":
                # Overall Score Too Low
                if profile.overall_score < 0.5:
                    violations.append({
                        "rule_id": rule["id"],
                        "title": rule["title"],
                        "severity": rule["severity"],
                        "message": "Overall score critically low - major overhaul needed",
                        "fix": rule["fix"]
                    })

        return violations

    def _calculate_evaluation_score(self, profile: EvaluationProfile, violations: List) -> float:
        """Calculate overall evaluation score."""
        # Start at 90
        score = 90.0

        # Deduct for violations
        for violation in violations:
            if violation["severity"] == "critical":
                score -= 20
            elif violation["severity"] == "high":
                score -= 15
            elif violation["severity"] == "medium":
                score -= 10
            elif violation["severity"] == "low":
                score -= 5

        # Extra penalty for critical issues
        if profile.critical_issues_present:
            score -= 30  # Devastating penalty

        # Bonus for excellence
        if profile.overall_score > 0.85:
            score += 10
        elif profile.overall_score > 0.75:
            score += 5

        if profile.overall_quality and profile.industry_ready:
            score += 5  # McKee's excellence (professional standards)

        if profile.execution_quality and profile.professional_standard:
            score += 5  # Craft mastery

        if profile.audience_appeal and profile.emotional_impact:
            score += 3  # Audience engagement

        if profile.character_excellence and profile.structure_excellence:
            score += 3  # Core foundations

        if profile.originality:
            score += 2  # Fresh voice

        if profile.thematic_depth:
            score += 2  # Meaningful

        # Cap at 95
        return max(5.0, min(95.0, score))

    def _generate_diagnosis(self, score: float, profile: EvaluationProfile,
                           violations: List) -> str:
        """Generate evaluation diagnosis summary."""
        if score >= 80:
            level = "EXCELLENT"
            summary = "High-quality screenplay with professional execution and strong audience appeal"
        elif score >= 65:
            level = "GOOD"
            summary = "Solid screenplay with clear strengths but some areas need refinement"
        elif score >= 50:
            level = "FAIR"
            summary = "Competent screenplay with potential but significant work needed"
        elif score >= 35:
            level = "NEEDS WORK"
            summary = "Screenplay has weaknesses that must be addressed before submission"
        else:
            level = "POOR"
            summary = "Major problems throughout - substantial overhaul required"

        diagnosis = f"EVALUATION {level} ({score:.1f}/100): {summary}"

        # Add specific issues
        issues = []
        if not profile.overall_quality:
            issues.append("quality below standard")
        if profile.critical_issues_present:
            issues.append("critical issues present")
        if not profile.industry_ready:
            issues.append("not market ready")
        if not profile.execution_quality:
            issues.append("craft issues")
        if not profile.audience_appeal:
            issues.append("limited appeal")
        if not profile.originality:
            issues.append("derivative")
        if not profile.story_cohesion:
            issues.append("poor cohesion")

        if issues:
            diagnosis += f". Key concerns: {', '.join(issues)}"

        return diagnosis

    def _determine_pass_fail(self, score: float, profile: EvaluationProfile) -> str:
        """Determine pass/fail based on industry standards."""
        if score >= 70 and not profile.critical_issues_present and profile.professional_standard:
            return "PASS - Meets industry standards for professional consideration"
        elif score >= 60 and not profile.critical_issues_present:
            return "CONDITIONAL PASS - Close to ready, minor improvements needed"
        elif score >= 50:
            return "CONDITIONAL FAIL - Has potential but needs substantial work"
        else:
            return "FAIL - Below industry standards, major overhaul required"

    def _generate_final_verdict(self, score: float, profile: EvaluationProfile, pass_fail: str) -> str:
        """Generate final verdict summary."""
        if "PASS" in pass_fail and score >= 80:
            verdict = "RECOMMENDED: High-quality screenplay ready for professional consideration."
        elif "PASS" in pass_fail:
            verdict = "APPROVED WITH NOTES: Solid screenplay, address minor issues and ready to submit."
        elif "CONDITIONAL PASS" in pass_fail:
            verdict = "PROMISING: Strong foundation but needs polishing before submission."
        elif "CONDITIONAL FAIL" in pass_fail:
            verdict = "NEEDS REVISION: Has potential but requires significant development."
        else:
            verdict = "NOT READY: Major structural and execution issues must be resolved."

        # Add strengths/weaknesses summary
        if profile.strengths_count > 0:
            verdict += f" Strengths: {profile.strengths_count} major assets identified."
        if profile.weaknesses_count > 0:
            verdict += f" Areas for improvement: {profile.weaknesses_count} issues to address."

        return verdict

    def _generate_recommendations(self, score: float, violations: List,
                                  profile: EvaluationProfile) -> List[str]:
        """Generate prioritized recommendations."""
        recommendations = []

        # Critical issues first
        for violation in violations:
            if violation["severity"] == "critical":
                recommendations.append(f"[CRITICAL] {violation['fix']}")

        # High priority
        for violation in violations:
            if violation["severity"] == "high":
                recommendations.append(f"[HIGH] {violation['fix']}")

        # Specific recommendations based on profile
        if profile.critical_issues_present:
            recommendations.append("Address critical issues immediately - these are deal-breakers that prevent consideration")

        if not profile.industry_ready:
            recommendations.append("Focus on professional polish - McKee: 'Industry standards must be met for consideration'")

        if not profile.overall_quality:
            recommendations.append("Raise overall quality - Seger: 'Identify and fix fundamental problems first'")

        if not profile.execution_quality:
            recommendations.append("Improve craft execution - Mackendrick: 'Mastery of technique essential for professional work'")

        if not profile.audience_appeal:
            recommendations.append("Increase audience engagement - Snyder: 'Primal appeal essential, audience must care'")

        if not profile.emotional_impact:
            recommendations.append("Strengthen emotional impact - McKee: 'Story must move audience emotionally'")

        if not profile.story_cohesion:
            recommendations.append("Improve story unity - Aristotle: 'Unity of action - all elements must work together organically'")

        if not profile.originality:
            recommendations.append("Find fresh perspective - Truby: 'Avoid derivative work, discover original voice'")

        if not profile.thematic_depth:
            recommendations.append("Deepen themes - Truby: 'Moral argument must be meaningful and significant'")

        # Excellence recommendations
        if score >= 70:
            recommendations.append("Final polish - Address remaining notes and screenplay ready for submission")
        elif score >= 50:
            recommendations.append("Study Seger's 'Making a Good Script Great' - Focus on identified weaknesses")
        else:
            recommendations.append("Study McKee's 'Story' - Master fundamental principles before proceeding")

        return recommendations[:8]  # Top 8 recommendations

    def export_evaluation_features(self, screenplay_text: str) -> Dict[str, Any]:
        """
        Export evaluation features for analysis.

        Returns structured data with evaluation metrics.
        """
        overall_quality = self._analyze_overall_quality(screenplay_text, None)
        strengths = self._identify_strengths(screenplay_text, None)
        weaknesses = self._identify_weaknesses(screenplay_text, None)
        industry_readiness = self._assess_industry_readiness(screenplay_text, None)

        return {
            "evaluation": {
                "overall_quality": overall_quality["high_quality"],
                "strengths_identified": strengths["identified"],
                "weaknesses_identified": weaknesses["identified"],
                "industry_ready": industry_readiness["ready"],
                "quality_level": overall_quality["quality_level"]
            },
            "meta": {
                "source": "DrEvaluator",
                "focus": "Master evaluation",
                "final_specialist": True,
                "specialist_number": "24/24"
            }
        }


# Compatibility class for testing framework
class DrEvaluatorAnalysis(DrEvaluator):
    """Alias for compatibility with test framework."""
    pass
