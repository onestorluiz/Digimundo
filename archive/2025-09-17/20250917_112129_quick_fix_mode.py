"""
🎬 QUICK FIX MODE SUPREME
Instant fixes for common screenplay problems
"""
import asyncio
import re
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, field
from datetime import datetime
import json
from enum import Enum

class ProblemType(Enum):
    OVERLONG_ACTION = 'overlong_action'
    MISSING_SLUGLINE = 'missing_slugline'
    INCORRECT_MARGINS = 'incorrect_margins'
    ORPHANED_DIALOGUE = 'orphaned_dialogue'
    WIDOWS_ORPHANS = 'widows_orphans'
    WEAK_OPENING = 'weak_opening'
    SLOW_PACING = 'slow_pacing'
    MISSING_CONFLICT = 'missing_conflict'
    UNCLEAR_PROTAGONIST = 'unclear_protagonist'
    WEAK_ENDING = 'weak_ending'
    ON_THE_NOSE = 'on_the_nose'
    TALKING_HEADS = 'talking_heads'
    OVERLONG_SPEECHES = 'overlong_speeches'
    REPETITIVE_DIALOGUE = 'repetitive_dialogue'
    MISSING_SUBTEXT = 'missing_subtext'
    PASSIVE_PROTAGONIST = 'passive_protagonist'
    UNCLEAR_MOTIVATION = 'unclear_motivation'
    FLAT_CHARACTERS = 'flat_characters'
    TOO_MANY_CHARACTERS = 'too_many_characters'
    INCONSISTENT_VOICE = 'inconsistent_voice'
    EXCESSIVE_CAMERA = 'excessive_camera'
    TOO_MANY_FLASHBACKS = 'too_many_flashbacks'
    UNCLEAR_TIME_JUMPS = 'unclear_time_jumps'
    MISSING_TRANSITIONS = 'missing_transitions'
    POOR_SCENE_DESCRIPTION = 'poor_scene_description'

@dataclass
class Problem:
    type: ProblemType
    location: str
    severity: str
    description: str
    context: str = ''

@dataclass
class QuickFix:
    problem_type: ProblemType
    original_text: str
    fixed_text: str
    explanation: str
    confidence: float = 0.0
    alternatives: List[str] = field(default_factory=list)

class QuickFixMode:

    def __init__(self):
        self.fixes_database = self.load_fixes_database()
        self.fix_history = []
        self.learning_mode = True
        self.confidence_threshold = 0.7
        self.output_dir = Path('output/quick_fixes')
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.fix_patterns = self.initialize_fix_patterns()

    def load_fixes_database(self) -> Dict:
        """Load database of common fixes"""
        return {ProblemType.OVERLONG_ACTION: {'max_lines': 4, 'max_words': 50, 'fix_method': 'split_action', 'examples': ['Break into multiple paragraphs', 'Use white space for pacing', 'Focus on essential visual information']}, ProblemType.ON_THE_NOSE: {'indicators': ['I feel', 'I think', 'Let me explain', 'You see'], 'fix_method': 'add_subtext', 'examples': ['Replace direct emotion with action', 'Use subtext and implication', 'Show through behavior, not words']}, ProblemType.PASSIVE_PROTAGONIST: {'indicators': ['waits', 'watches', 'is told', 'learns that'], 'fix_method': 'activate_character', 'examples': ['Give protagonist active choices', 'Make them drive the action', 'Add decisive moments']}, ProblemType.WEAK_OPENING: {'page_range': (1, 10), 'fix_method': 'strengthen_opening', 'checklist': ['Hook within first 3 pages', 'Establish tone immediately', 'Introduce protagonist quickly', 'Set up central question']}, ProblemType.EXCESSIVE_CAMERA: {'limit_per_page': 0.5, 'forbidden': ['ZOOM', 'PAN', 'DOLLY', 'CRANE'], 'fix_method': 'remove_camera_directions', 'replacement': 'Focus on what we see, not how we see it'}}

    def initialize_fix_patterns(self) -> Dict:
        """Initialize regex patterns for fixes"""
        return {'camera_directions': re.compile('(CLOSE UP|CUT TO|PAN|ZOOM|ANGLE ON|POV|CRANE SHOT|DOLLY)', re.IGNORECASE), 'weak_verbs': re.compile('\\b(is|are|was|were|been|being|seems|appears|looks)\\b', re.IGNORECASE), 'filter_words': re.compile('\\b(very|really|quite|just|perhaps|maybe|somewhat|rather)\\b', re.IGNORECASE), 'telling_phrases': re.compile('(we see|we hear|we notice|the camera)', re.IGNORECASE), 'parenthetical_overuse': re.compile('\\([^)]+\\)', re.MULTILINE)}

    def scan_screenplay(self, filepath: Path) -> List[Problem]:
        """Scan screenplay for problems"""
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        lines = content.split('\n')
        problems = []
        problems.extend(self.scan_format_problems(lines))
        problems.extend(self.scan_structure_problems(content))
        problems.extend(self.scan_dialogue_problems(content))
        problems.extend(self.scan_character_problems(content))
        problems.extend(self.scan_technical_problems(content))
        problems.sort(key=lambda p: (self.severity_rank(p.severity), p.location))
        return problems

    def scan_format_problems(self, lines: List[str]) -> List[Problem]:
        """Scan for formatting issues"""
        problems = []
        for i, line in enumerate(lines):
            if line and (not re.match('^[A-Z][A-Z\\s]+$', line)):
                if len(line) > 60:
                    problems.append(Problem(type=ProblemType.OVERLONG_ACTION, location=f'Line {i + 1}', severity='minor', description=f'Action line too long ({len(line)} chars)', context=line[:50] + '...'))
                if not line.startswith(' ') and len(line.split()) > 50:
                    problems.append(Problem(type=ProblemType.OVERLONG_ACTION, location=f'Line {i + 1}', severity='major', description='Action block needs breaking up', context=line[:50] + '...'))
        for i in range(len(lines) - 1):
            if re.match('^[A-Z][A-Z\\s]+$', lines[i]):
                if i + 1 < len(lines) and (not lines[i + 1].strip()):
                    problems.append(Problem(type=ProblemType.ORPHANED_DIALOGUE, location=f'Line {i + 1}', severity='minor', description='Character name with no dialogue', context=lines[i]))
        return problems

    def scan_structure_problems(self, content: str) -> List[Problem]:
        """Scan for structural issues"""
        problems = []
        pages = content.split('\n\n\n')
        first_10_pages = '\n'.join(pages[:10]) if len(pages) >= 10 else content
        if not re.search('(INT\\.|EXT\\.)', first_10_pages[:500]):
            problems.append(Problem(type=ProblemType.WEAK_OPENING, location='Pages 1-3', severity='critical', description='No scene heading in opening', context='Opening needs immediate visual scene'))
        conflict_words = ['but', 'however', 'fights', 'argues', 'confronts', 'challenges']
        if not any((word in first_10_pages.lower() for word in conflict_words)):
            problems.append(Problem(type=ProblemType.MISSING_CONFLICT, location='Pages 1-10', severity='major', description='No clear conflict established early', context='Story needs tension/conflict in opening'))
        scene_count = len(re.findall('(INT\\.|EXT\\.)', content))
        page_count = len(pages)
        if page_count > 0:
            scenes_per_page = scene_count / page_count
            if scenes_per_page < 0.5:
                problems.append(Problem(type=ProblemType.SLOW_PACING, location='Overall', severity='major', description=f'Low scene density ({scenes_per_page:.2f} per page)', context='Consider breaking up long scenes'))
        return problems

    def scan_dialogue_problems(self, content: str) -> List[Problem]:
        """Scan for dialogue issues"""
        problems = []
        dialogue_pattern = re.compile('^([A-Z][A-Z\\s]+)\\n((?:(?!^[A-Z][A-Z\\s]+\\n).)+)', re.MULTILINE | re.DOTALL)
        dialogues = dialogue_pattern.findall(content)
        for char_name, dialogue in dialogues:
            if any((phrase in dialogue.lower() for phrase in ['i feel', 'i think', 'let me explain'])):
                problems.append(Problem(type=ProblemType.ON_THE_NOSE, location=f'Character: {char_name}', severity='major', description='Dialogue too direct/explanatory', context=dialogue[:50]))
            if len(dialogue.split()) > 50:
                problems.append(Problem(type=ProblemType.OVERLONG_SPEECHES, location=f'Character: {char_name}', severity='minor', description=f'Speech too long ({len(dialogue.split())} words)', context=dialogue[:50] + '...'))
        all_dialogue = ' '.join((d[1] for d in dialogues))
        words = all_dialogue.lower().split()
        word_count = {}
        for word in words:
            if len(word) > 4:
                word_count[word] = word_count.get(word, 0) + 1
        repetitive = [word for word, count in word_count.items() if count > 10]
        if repetitive:
            problems.append(Problem(type=ProblemType.REPETITIVE_DIALOGUE, location='Overall', severity='minor', description=f"Overused words: {', '.join(repetitive[:5])}", context='Vary vocabulary for better dialogue'))
        return problems

    def scan_character_problems(self, content: str) -> List[Problem]:
        """Scan for character issues"""
        problems = []
        char_pattern = re.compile('^([A-Z][A-Z\\s]+)$', re.MULTILINE)
        characters = list(set(char_pattern.findall(content)))
        if len(characters) > 30:
            problems.append(Problem(type=ProblemType.TOO_MANY_CHARACTERS, location='Overall', severity='major', description=f'Too many characters ({len(characters)})', context='Consider consolidating minor characters'))
        protagonist_actions = re.findall('([A-Z][A-Z\\s]+)\\s+(waits|watches|listens|is told|learns)', content, re.IGNORECASE)
        if len(protagonist_actions) > 5:
            problems.append(Problem(type=ProblemType.PASSIVE_PROTAGONIST, location='Multiple', severity='major', description='Protagonist often passive', context='Give protagonist more active verbs/choices'))
        return problems

    def scan_technical_problems(self, content: str) -> List[Problem]:
        """Scan for technical issues"""
        problems = []
        camera_directions = self.fix_patterns['camera_directions'].findall(content)
        page_count = len(content.split('\n')) // 55
        if page_count > 0:
            camera_per_page = len(camera_directions) / page_count
            if camera_per_page > 0.5:
                problems.append(Problem(type=ProblemType.EXCESSIVE_CAMERA, location='Overall', severity='major', description=f'Too many camera directions ({len(camera_directions)} total)', context='Let director decide camera angles'))
        flashbacks = len(re.findall('FLASHBACK', content, re.IGNORECASE))
        if flashbacks > 3:
            problems.append(Problem(type=ProblemType.TOO_MANY_FLASHBACKS, location='Multiple', severity='minor', description=f'Many flashbacks ({flashbacks})', context='Consider linear storytelling'))
        return problems

    def severity_rank(self, severity: str) -> int:
        """Convert severity to rank for sorting"""
        ranks = {'critical': 0, 'major': 1, 'minor': 2}
        return ranks.get(severity, 3)

    def apply_quick_fix(self, problem: Problem, content: str, auto_mode: bool=False) -> QuickFix:
        """Apply a quick fix to a problem"""
        fix_method = self.fixes_database.get(problem.type, {}).get('fix_method')
        if fix_method == 'split_action':
            return self.fix_overlong_action(problem, content)
        elif fix_method == 'add_subtext':
            return self.fix_on_the_nose(problem, content)
        elif fix_method == 'activate_character':
            return self.fix_passive_character(problem, content)
        elif fix_method == 'strengthen_opening':
            return self.fix_weak_opening(problem, content)
        elif fix_method == 'remove_camera_directions':
            return self.fix_camera_directions(problem, content)
        else:
            return QuickFix(problem_type=problem.type, original_text='', fixed_text='', explanation='No automatic fix available', confidence=0.0)

    def fix_overlong_action(self, problem: Problem, content: str) -> QuickFix:
        """Fix overlong action lines"""
        lines = content.split('\n')
        line_num = int(re.search('\\d+', problem.location).group()) - 1
        if line_num >= len(lines):
            return QuickFix(problem_type=problem.type, original_text='', fixed_text='', explanation='Line not found', confidence=0.0)
        original = lines[line_num]
        sentences = re.split('(?<=[.!?])\\s+', original)
        fixed_lines = []
        current_chunk = ''
        for sentence in sentences:
            if len(current_chunk) + len(sentence) < 50:
                current_chunk += sentence + ' '
            else:
                if current_chunk:
                    fixed_lines.append(current_chunk.strip())
                current_chunk = sentence + ' '
        if current_chunk:
            fixed_lines.append(current_chunk.strip())
        fixed_text = '\n\n'.join(fixed_lines)
        return QuickFix(problem_type=problem.type, original_text=original, fixed_text=fixed_text, explanation='Split action into readable chunks with white space', confidence=0.9, alternatives=['Cut unnecessary details', 'Focus on essential visual information'])

    def fix_on_the_nose(self, problem: Problem, content: str) -> QuickFix:
        """Fix on-the-nose dialogue"""
        suggestions = ["Replace 'I feel sad' with action: 'She turns away, wiping her eyes'", "Use subtext: 'Fine. Whatever you want.' instead of explaining feelings", "Show through behavior: Character slams door instead of saying 'I'm angry'", 'Use metaphor or indirection', 'Let silence speak']
        return QuickFix(problem_type=problem.type, original_text=problem.context, fixed_text='[Manual rewrite needed]', explanation='On-the-nose dialogue needs human rewriting for subtext', confidence=0.3, alternatives=suggestions)

    def fix_passive_character(self, problem: Problem, content: str) -> QuickFix:
        """Fix passive character actions"""
        replacements = {'waits': 'decides', 'watches': 'confronts', 'listens': 'interrupts', 'is told': 'discovers', 'learns': 'uncovers', 'observes': 'investigates', 'notices': 'pursues'}
        fixed = content
        for passive, active in replacements.items():
            pattern = re.compile('\\b' + passive + '\\b', re.IGNORECASE)
            fixed = pattern.sub(active, fixed)
        return QuickFix(problem_type=problem.type, original_text='Multiple passive constructions', fixed_text='Replaced with active verbs', explanation='Protagonist given more agency through active verbs', confidence=0.7, alternatives=['Add character decisions', 'Create obstacles character must overcome', 'Give character goals to pursue'])

    def fix_weak_opening(self, problem: Problem, content: str) -> QuickFix:
        """Suggest fixes for weak opening"""
        template = 'FADE IN:\n\nEXT. [COMPELLING LOCATION] - [TIME OF DAY]\n\n[IMMEDIATE VISUAL HOOK - something happening, not description]\n\n[CHARACTER NAME], [age], [defining trait visible in action], [DOES SOMETHING ACTIVE].\n\n[CONFLICT or QUESTION raised within first page]\n\n[End with a hook - question, reversal, or compelling image]'
        return QuickFix(problem_type=problem.type, original_text='Weak opening detected', fixed_text=template, explanation='Opening needs immediate hook and conflict', confidence=0.5, alternatives=['Start in medias res - middle of action', 'Open with compelling image', 'Introduce protagonist in defining moment', 'Establish central question immediately'])

    def fix_camera_directions(self, problem: Problem, content: str) -> QuickFix:
        """Remove excessive camera directions"""
        fixed = content
        camera_terms = ['CLOSE UP:', 'CU:', 'WIDE SHOT:', 'WS:', 'PAN TO:', 'ZOOM IN:', 'ZOOM OUT:', 'ANGLE ON:', 'POV:', 'CRANE SHOT:', 'TRACKING SHOT:', 'DOLLY IN:', 'DOLLY OUT:']
        for term in camera_terms:
            fixed = fixed.replace(term, '')
            fixed = fixed.replace(term.lower(), '')
        fixed = re.sub('\\n\\n\\n+', '\n\n', fixed)
        return QuickFix(problem_type=problem.type, original_text='Multiple camera directions', fixed_text='Camera directions removed', explanation='Removed camera directions - focus on what we see, not how', confidence=0.95, alternatives=['Describe the emotional impact instead', 'Focus on character reactions', "Use action to guide reader's eye"])

    async def batch_fix(self, problems: List[Problem], content: str, auto_approve: bool=False) -> Tuple[str, List[QuickFix]]:
        """Apply multiple fixes to screenplay"""
        fixes_applied = []
        fixed_content = content
        for problem in problems:
            if not auto_approve and problem.severity == 'minor':
                continue
            fix = await self.apply_quick_fix(problem, fixed_content, auto_approve)
            if fix.confidence >= self.confidence_threshold:
                if fix.fixed_text and fix.fixed_text != '[Manual rewrite needed]':
                    fixed_content = fixed_content.replace(fix.original_text, fix.fixed_text)
                    fixes_applied.append(fix)
        return (fixed_content, fixes_applied)

    def generate_fix_report(self, screenplay_path: Path, problems: List[Problem], fixes: List[QuickFix]) -> Dict:
        """Generate detailed fix report"""
        report = {'screenplay': str(screenplay_path), 'scan_date': datetime.now().isoformat(), 'problems_found': len(problems), 'fixes_applied': len(fixes), 'problem_breakdown': {}, 'severity_breakdown': {'critical': 0, 'major': 0, 'minor': 0}, 'fixes_by_type': {}, 'confidence_average': 0, 'estimated_improvement': 0, 'recommendations': []}
        for problem in problems:
            prob_type = problem.type.value
            report['problem_breakdown'][prob_type] = report['problem_breakdown'].get(prob_type, 0) + 1
            report['severity_breakdown'][problem.severity] += 1
        if fixes:
            total_confidence = 0
            for fix in fixes:
                fix_type = fix.problem_type.value
                report['fixes_by_type'][fix_type] = report['fixes_by_type'].get(fix_type, 0) + 1
                total_confidence += fix.confidence
            report['confidence_average'] = total_confidence / len(fixes)
        critical_fixed = sum((1 for p in problems if p.severity == 'critical' and any((f.problem_type == p.type for f in fixes))))
        major_fixed = sum((1 for p in problems if p.severity == 'major' and any((f.problem_type == p.type for f in fixes))))
        if report['problems_found'] > 0:
            improvement = (critical_fixed * 3 + major_fixed * 2 + len(fixes)) / (report['problems_found'] * 3)
            report['estimated_improvement'] = min(improvement * 100, 100)
        if report['severity_breakdown']['critical'] > 0:
            report['recommendations'].append('Address critical issues immediately - they affect readability')
        if report['problem_breakdown'].get('on_the_nose', 0) > 5:
            report['recommendations'].append('Consider a dialogue pass focusing on subtext')
        if report['problem_breakdown'].get('passive_protagonist', 0) > 0:
            report['recommendations'].append('Strengthen protagonist agency throughout')
        if report['confidence_average'] < 0.6:
            report['recommendations'].append('Many fixes need human review - automated confidence is low')
        report_path = self.output_dir / f'fix_report_{datetime.now():%Y%m%d_%H%M%S}.json'
        with open(report_path, 'w') as f:
            json.dump(report, f, indent=2, default=str)
        return report

    def learn_from_fix(self, original: str, fixed: str, problem_type: ProblemType):
        """Learn from manual fixes to improve automatic fixes"""
        if self.learning_mode:
            self.fix_history.append({'timestamp': datetime.now().isoformat(), 'problem_type': problem_type.value, 'original': original[:100], 'fixed': fixed[:100], 'pattern_extracted': self.extract_fix_pattern(original, fixed)})
            if len(self.fix_history) % 10 == 0:
                self.save_learning_data()

    def extract_fix_pattern(self, original: str, fixed: str) -> Dict:
        """Extract pattern from manual fix"""
        pattern = {'length_change': len(fixed) - len(original), 'added_words': [], 'removed_words': [], 'structural_change': False}
        original_words = set(original.lower().split())
        fixed_words = set(fixed.lower().split())
        pattern['added_words'] = list(fixed_words - original_words)[:10]
        pattern['removed_words'] = list(original_words - fixed_words)[:10]
        if '\n' in fixed and '\n' not in original:
            pattern['structural_change'] = True
        return pattern

    def save_learning_data(self):
        """Save learning data for improvement"""
        learning_path = self.output_dir / 'learning_data.json'
        with open(learning_path, 'w') as f:
            json.dump(self.fix_history, f, indent=2)

async def main():
    """Test quick fix mode"""
    fixer = QuickFixMode()
    test_content = "FADE IN:\n\nINT. OFFICE - DAY\n\nCLOSE UP on John's face as he sits at his desk looking sad and tired from working all night on the project that his boss assigned him yesterday even though he didn't want to do it.\n\nJOHN\nI feel really tired. I think I need to explain to you why I'm so exhausted. You see, I've been working all night.\n\nSARAH waits and watches.\n\nSARAH\nI understand how you feel. Let me tell you what I think about this situation.\n\nPAN TO the window.\n\nZOOM IN on the clock.\n\nANGLE ON Sarah as she listens to John explain more.\n\nJOHN\n(continuing)\nThis is just too much. I really think we need to talk about our feelings and explain everything that's been happening between us for the past few months because I feel like you don't understand me.\n\nDOLLY IN as Sarah watches John.\n\nCRANE SHOT of the office.\n"
    test_path = Path('test_screenplay_problems.txt')
    with open(test_path, 'w') as f:
        f.write(test_content)
    print('Scanning for problems...')
    problems = await fixer.scan_screenplay(test_path)
    print(f'\nFound {len(problems)} problems:')
    for problem in problems:
        print(f'  [{problem.severity}] {problem.type.value}: {problem.description}')
        print(f'    Location: {problem.location}')
    print('\nApplying quick fixes...')
    fixed_content, fixes = await fixer.batch_fix(problems, test_content, auto_approve=True)
    print(f'\nApplied {len(fixes)} fixes:')
    for fix in fixes:
        print(f'  {fix.problem_type.value}: {fix.explanation}')
        print(f'    Confidence: {fix.confidence:.1%}')
    report = await fixer.generate_fix_report(test_path, problems, fixes)
    print(f'\nFix Report Summary:')
    print(f"  Problems found: {report['problems_found']}")
    print(f"  Fixes applied: {report['fixes_applied']}")
    print(f"  Estimated improvement: {report['estimated_improvement']:.1f}%")
    print(f"  Average confidence: {report['confidence_average']:.1%}")
    if report['recommendations']:
        print('\nRecommendations:')
        for rec in report['recommendations']:
            print(f'  • {rec}')
    fixed_path = Path('test_screenplay_fixed.txt')
    with open(fixed_path, 'w') as f:
        f.write(fixed_content)
    print(f'\nFixed screenplay saved to {fixed_path}')
if __name__ == '__main__':
    asyncio.run(main())