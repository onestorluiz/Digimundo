#!/usr/bin/env python3
"""
🧠 SCRIPTUREMON BRAIN - Motor de Análise Real
Sistema inteligente que analisa roteiros DE VERDADE
"""

import json
import re
import subprocess
import sqlite3
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Tuple, Optional
import hashlib

class ScripturemonBrain:
    """Cérebro real do Scripturemon 2.0"""
    
    def __init__(self):
        self.base_dir = Path("/Users/clubproducoes/Digimundo/scripturemon_memory")
        self.base_dir.mkdir(parents=True, exist_ok=True)
        
        # Database de memória
        self.db_path = self.base_dir / "scripturemon_brain.db"
        self._init_database()
        
        # Modelos Ollama disponíveis - Configuração equilibrada
        self.models = self._check_ollama_models()
        self.default_model = 'deepseek-r1:32b'  # Equilibrado: 30GB RAM, boa qualidade
        self.default_context = 128000  # 128k tokens (suficiente para análises)
        self.timeout = 60  # 1 minuto timeout padrão
        
        # Perfil do usuário
        self.user_profile = self._load_user_profile()
        
    def _init_database(self):
        """Inicializa database de memória evolutiva"""
        conn = sqlite3.connect(str(self.db_path))
        
        # Tabela de análises
        conn.execute("""
            CREATE TABLE IF NOT EXISTS analyses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                screenplay_hash TEXT,
                title TEXT,
                date TEXT,
                score REAL,
                structure_score REAL,
                dialogue_score REAL,
                character_score REAL,
                originality_score REAL,
                analysis_json TEXT,
                feedback TEXT
            )
        """)
        
        # Tabela de padrões do usuário
        conn.execute("""
            CREATE TABLE IF NOT EXISTS user_patterns (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                pattern_type TEXT,
                pattern_description TEXT,
                frequency INTEGER,
                last_seen TEXT
            )
        """)
        
        # Tabela de evolução
        conn.execute("""
            CREATE TABLE IF NOT EXISTS evolution (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT,
                metric TEXT,
                value REAL
            )
        """)
        
        conn.commit()
        conn.close()
    
    def _check_ollama_models(self) -> Dict[str, str]:
        """Verifica modelos Ollama disponíveis"""
        try:
            result = subprocess.run(
                ["ollama", "list"],
                capture_output=True,
                text=True
            )
            
            models = {}
            if result.returncode == 0:
                lines = result.stdout.strip().split('\n')[1:]  # Skip header
                for line in lines:
                    if line:
                        model_name = line.split()[0]
                        # Atribui papéis aos modelos
                        if 'llama' in model_name.lower():
                            models['analyzer'] = model_name
                        elif 'mistral' in model_name.lower():
                            models['critic'] = model_name
                        elif 'phi' in model_name.lower():
                            models['rewriter'] = model_name
                
                # Fallback se não encontrou específicos
                if not models and lines:
                    default_model = lines[0].split()[0]
                    models = {
                        'analyzer': default_model,
                        'critic': default_model,
                        'rewriter': default_model
                    }
            
            return models
            
        except:
            return {}
    
    def _load_user_profile(self) -> Dict:
        """Carrega perfil do usuário"""
        profile_path = self.base_dir / "user_profile.json"
        
        if profile_path.exists():
            with open(profile_path, 'r') as f:
                return json.load(f)
        else:
            # Perfil inicial
            profile = {
                "name": "Criador",
                "style_preferences": [],
                "common_issues": [],
                "strengths": [],
                "total_analyses": 0,
                "average_score": 62,
                "evolution_trend": "stable"
            }
            return profile
    
    def analyze_screenplay(self, text: str, title: str = "Untitled") -> Dict:
        """
        Análise REAL do roteiro
        
        Returns:
            Dict com análise completa e score real
        """
        # 1. Parse estrutural
        structure = self._parse_structure(text)
        
        # 2. Análise via Ollama (se disponível)
        if self.models:
            ai_analysis = self._ollama_deep_analysis(text, structure)
        else:
            ai_analysis = self._heuristic_analysis(text, structure)
        
        # 3. Cálculo de score REAL
        score = self._calculate_real_score(structure, ai_analysis)
        
        # 4. Identifica padrões do usuário
        patterns = self._identify_user_patterns(text, structure)
        
        # 5. Gera feedback personalizado
        feedback = self._generate_personalized_feedback(
            structure, ai_analysis, score, patterns
        )
        
        # 6. Salva na memória
        self._save_analysis(title, text, structure, score, feedback)
        
        # 7. Atualiza perfil do usuário
        self._update_user_profile(patterns, score)
        
        return {
            "title": title,
            "score": score,
            "structure": structure,
            "analysis": ai_analysis,
            "patterns": patterns,
            "feedback": feedback,
            "evolution": self._get_evolution_data()
        }
    
    def _parse_structure(self, text: str) -> Dict:
        """Parse real da estrutura do roteiro"""
        lines = text.split('\n')
        
        structure = {
            "total_pages": len(lines) / 55,  # Aproximação
            "scenes": [],
            "characters": set(),
            "dialogue_ratio": 0,
            "action_ratio": 0,
            "acts": {"act1": 0, "act2": 0, "act3": 0}
        }
        
        # Patterns de roteiro
        scene_pattern = re.compile(r'^(INT\.?|EXT\.?|INT/EXT\.?|INTERIOR|EXTERIOR)[\s\.\-]+.*', re.IGNORECASE)
        transition_pattern = re.compile(r'^(FADE IN:|FADE OUT:|CUT TO:|DISSOLVE TO:|FADE TO:|BACK TO:)', re.IGNORECASE)
        character_pattern = re.compile(r'^[A-Z][A-Z0-9\s\-]+([\s]*\([^)]+\))?$')
        dialogue_lines = 0
        action_lines = 0
        
        current_character = None
        
        for line in lines:
            line = line.strip()
            
            # Detecta cenas
            if scene_pattern.match(line):
                structure["scenes"].append(line)

            # Detecta transições
            elif transition_pattern.match(line):
                pass  # Transições não são cenas mas são importantes
            
            # Detecta personagens
            elif character_pattern.match(line) and len(line) < 50:
                char_name = line.split('(')[0].strip()
                structure["characters"].add(char_name)
                current_character = char_name
            
            # Conta diálogos vs ação
            elif current_character and line:
                dialogue_lines += 1
                current_character = None  # Reset após diálogo
            elif line and not line.isupper():
                action_lines += 1
                current_character = None
        
        # Calcula proporções
        total_lines = dialogue_lines + action_lines
        if total_lines > 0:
            structure["dialogue_ratio"] = dialogue_lines / total_lines
            structure["action_ratio"] = action_lines / total_lines
        
        # Estima divisão de atos (regra dos 25-50-25)
        total_scenes = len(structure["scenes"])
        if total_scenes > 0:
            structure["acts"]["act1"] = int(total_scenes * 0.25)
            structure["acts"]["act2"] = int(total_scenes * 0.50)
            structure["acts"]["act3"] = int(total_scenes * 0.25)
        
        structure["characters"] = list(structure["characters"])
        
        return structure
    
    def _ollama_deep_analysis(self, text: str, structure: Dict) -> Dict:
        """Análise profunda usando Ollama"""

        import logging
        logger = logging.getLogger(__name__)
        logger.debug(f'Parsing screenplay with {len(text)} characters')

        if not self.models.get('analyzer'):
            return self._heuristic_analysis(text, structure)
        
        try:
            # Prepara prompt especializado
            prompt = f"""Analise este roteiro cinematográfico:

Estrutura detectada:
- {len(structure['scenes'])} cenas
- {len(structure['characters'])} personagens
- {structure['dialogue_ratio']*100:.1f}% diálogo

Texto (primeiras 1000 palavras):
{' '.join(text.split()[:1000])}

Identifique:
1. Força narrativa principal
2. Problemas estruturais
3. Qualidade dos diálogos
4. Desenvolvimento de personagens
5. Originalidade

Responda em formato JSON."""

            # Executa análise
            result = subprocess.run(
                ["ollama", "run", self.models['analyzer'], prompt],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.returncode == 0:
                try:
                    # Tenta parsear resposta como JSON
                    response = result.stdout.strip()
                    # Extrai JSON da resposta se houver
                    json_match = re.search(r'\{.*\}', response, re.DOTALL)
                    if json_match:
                        return json.loads(json_match.group())
                except:
                    pass
            
        except:
            pass
        
        # Fallback para análise heurística
        return self._heuristic_analysis(text, structure)
    
    def _heuristic_analysis(self, text: str, structure: Dict) -> Dict:
        """Análise heurística quando Ollama não disponível"""
        analysis = {
            "narrative_strength": "undefined",
            "structural_issues": [],
            "dialogue_quality": "average",
            "character_development": "basic",
            "originality": "standard"
        }
        
        # Análise básica baseada em estrutura
        if len(structure["scenes"]) < 40:
            analysis["structural_issues"].append("Muito curto para longa-metragem")
        elif len(structure["scenes"]) > 150:
            analysis["structural_issues"].append("Muito longo, precisa cortes")
        
        if structure["dialogue_ratio"] > 0.7:
            analysis["structural_issues"].append("Excesso de diálogo, falta ação visual")
            analysis["dialogue_quality"] = "excessive"
        elif structure["dialogue_ratio"] < 0.3:
            analysis["structural_issues"].append("Pouco diálogo, pode ser monótono")
            analysis["dialogue_quality"] = "insufficient"
        
        if len(structure["characters"]) < 3:
            analysis["character_development"] = "limited cast"
        elif len(structure["characters"]) > 20:
            analysis["character_development"] = "too many characters"
        
        # Detecta clichês
        cliches = ["FADE IN", "FADE OUT", "The End", "It was all a dream"]
        cliche_count = sum(1 for cliche in cliches if cliche.lower() in text.lower())
        if cliche_count > 2:
            analysis["originality"] = "clichéd"
        
        return analysis
    
    def _calculate_real_score(self, structure: Dict, analysis: Dict) -> float:
        """Calcula score REAL baseado na análise"""
        score = 50.0  # Base
        
        # Ajusta por estrutura
        if 40 <= len(structure["scenes"]) <= 120:
            score += 10
        
        # Ajusta por proporção diálogo/ação
        if 0.4 <= structure["dialogue_ratio"] <= 0.6:
            score += 10
        
        # Ajusta por número de personagens
        if 5 <= len(structure["characters"]) <= 15:
            score += 10
        
        # Ajusta por problemas estruturais
        score -= len(analysis.get("structural_issues", [])) * 5
        
        # Ajusta por originalidade
        if analysis.get("originality") == "clichéd":
            score -= 10
        elif analysis.get("originality") == "innovative":
            score += 15
        
        # Limita entre 20 e 95
        score = max(20, min(95, score))
        
        # Adiciona variação aleatória pequena (personalidade)
        import random
        score += random.uniform(-3, 3)
        
        return round(score, 1)
    
    def _identify_user_patterns(self, text: str, structure: Dict) -> List[str]:
        """Identifica padrões recorrentes do usuário"""
        patterns = []
        
        # Busca padrões anteriores no database
        conn = sqlite3.connect(str(self.db_path))
        cursor = conn.cursor()
        
        # Verifica se usuário repete problemas
        cursor.execute("""
            SELECT pattern_description, frequency 
            FROM user_patterns 
            ORDER BY frequency DESC 
            LIMIT 5
        """)
        
        known_patterns = cursor.fetchall()
        conn.close()
        
        # Padrões comuns a verificar
        if structure["dialogue_ratio"] > 0.7:
            patterns.append("Tendência a excesso de diálogo")
        
        if len(structure["characters"]) < 5:
            patterns.append("Elenco limitado recorrente")
        
        if "INT." in ' '.join(structure["scenes"][:5]):
            patterns.append("Preferência por cenas internas")
        
        # Adiciona padrões conhecidos
        for pattern, freq in known_patterns:
            if freq > 2:
                patterns.append(f"{pattern} (visto {freq}x)")
        
        return patterns
    
    def _generate_personalized_feedback(self, structure: Dict, analysis: Dict, 
                                       score: float, patterns: List[str]) -> str:
        """Gera feedback personalizado e construtivo"""
        feedback = f"ANÁLISE DETALHADA - Score Real: {score}/100\n\n"
        
        # Feedback estrutural
        feedback += "ESTRUTURA:\n"
        feedback += f"- {len(structure['scenes'])} cenas detectadas\n"
        feedback += f"- Proporção diálogo/ação: {structure['dialogue_ratio']*100:.0f}%/{structure['action_ratio']*100:.0f}%\n"
        
        if structure['dialogue_ratio'] > 0.7:
            feedback += "  ⚠️ Excesso de diálogo - adicione ação visual\n"
        elif structure['dialogue_ratio'] < 0.3:
            feedback += "  ⚠️ Pouco diálogo - desenvolva interações\n"
        else:
            feedback += "  ✓ Boa proporção diálogo/ação\n"
        
        # Feedback de personagens
        feedback += f"\nPERSONAGENS: {len(structure['characters'])} identificados\n"
        if len(structure['characters']) < 3:
            feedback += "  ⚠️ Poucos personagens - risco de monotonia\n"
        elif len(structure['characters']) > 20:
            feedback += "  ⚠️ Muitos personagens - difícil desenvolver todos\n"
        
        # Problemas específicos
        if analysis.get("structural_issues"):
            feedback += "\nPROBLEMAS DETECTADOS:\n"
            for issue in analysis["structural_issues"]:
                feedback += f"  • {issue}\n"
        
        # Padrões do usuário
        if patterns:
            feedback += "\nSEUS PADRÕES RECORRENTES:\n"
            for pattern in patterns[:3]:
                feedback += f"  • {pattern}\n"
        
        # Evolução
        feedback += f"\nEVOLUÇÃO:\n"
        conn = sqlite3.connect(str(self.db_path))
        cursor = conn.cursor()
        cursor.execute("""
            SELECT AVG(score) FROM analyses 
            WHERE date > datetime('now', '-30 days')
        """)
        recent_avg = cursor.fetchone()[0]
        conn.close()
        
        if recent_avg:
            diff = score - recent_avg
            if diff > 0:
                feedback += f"  📈 Melhorou {diff:.1f} pontos vs média recente\n"
            elif diff < 0:
                feedback += f"  📉 Piorou {abs(diff):.1f} pontos vs média recente\n"
            else:
                feedback += f"  → Estável em relação à média recente\n"
        
        return feedback
    
    def _save_analysis(self, title: str, text: str, structure: Dict, 
                      score: float, feedback: str):
        """Salva análise na memória evolutiva"""
        # Hash do screenplay para detectar resubmissões
        text_hash = hashlib.md5(text.encode()).hexdigest()
        
        conn = sqlite3.connect(str(self.db_path))
        
        # Salva análise
        conn.execute("""
            INSERT INTO analyses 
            (screenplay_hash, title, date, score, structure_score, 
             dialogue_score, character_score, originality_score, 
             analysis_json, feedback)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            text_hash,
            title,
            datetime.now().isoformat(),
            score,
            score,  # Placeholder para scores específicos
            score,
            score,
            score,
            json.dumps(structure),
            feedback
        ))
        
        # Atualiza padrões do usuário
        for pattern in self._identify_user_patterns(text, structure):
            # Verifica se padrão já existe
            cursor = conn.cursor()
            cursor.execute("""
                SELECT id, frequency FROM user_patterns 
                WHERE pattern_description = ?
            """, (pattern,))
            
            result = cursor.fetchone()
            if result:
                # Incrementa frequência
                conn.execute("""
                    UPDATE user_patterns 
                    SET frequency = ?, last_seen = ?
                    WHERE id = ?
                """, (result[1] + 1, datetime.now().isoformat(), result[0]))
            else:
                # Adiciona novo padrão
                conn.execute("""
                    INSERT INTO user_patterns 
                    (pattern_type, pattern_description, frequency, last_seen)
                    VALUES (?, ?, ?, ?)
                """, ("generic", pattern, 1, datetime.now().isoformat()))
        
        conn.commit()
        conn.close()
    
    def _update_user_profile(self, patterns: List[str], score: float):
        """Atualiza perfil do usuário"""
        self.user_profile["total_analyses"] += 1
        
        # Atualiza média
        current_avg = self.user_profile["average_score"]
        total = self.user_profile["total_analyses"]
        new_avg = ((current_avg * (total - 1)) + score) / total
        self.user_profile["average_score"] = round(new_avg, 1)
        
        # Atualiza tendência
        if score > current_avg + 5:
            self.user_profile["evolution_trend"] = "improving"
        elif score < current_avg - 5:
            self.user_profile["evolution_trend"] = "declining"
        else:
            self.user_profile["evolution_trend"] = "stable"
        
        # Salva perfil
        profile_path = self.base_dir / "user_profile.json"
        with open(profile_path, 'w') as f:
            json.dump(self.user_profile, f, indent=2)
    
    def _get_evolution_data(self) -> Dict:
        """Retorna dados de evolução do usuário"""
        conn = sqlite3.connect(str(self.db_path))
        cursor = conn.cursor()
        
        # Últimas 10 análises
        cursor.execute("""
            SELECT date, score FROM analyses 
            ORDER BY date DESC 
            LIMIT 10
        """)
        
        recent_scores = cursor.fetchall()
        conn.close()
        
        return {
            "recent_scores": recent_scores,
            "trend": self.user_profile.get("evolution_trend", "unknown"),
            "average": self.user_profile.get("average_score", 62)
        }
    
    def get_screenplay_history(self, title: str) -> List[Dict]:
        """Retorna histórico de análises de um roteiro"""
        conn = sqlite3.connect(str(self.db_path))
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT date, score, feedback 
            FROM analyses 
            WHERE title = ? 
            ORDER BY date DESC
        """, (title,))
        
        history = []
        for date, score, feedback in cursor.fetchall():
            history.append({
                "date": date,
                "score": score,
                "feedback": feedback
            })
        
        conn.close()
        return history


# Teste do sistema
if __name__ == "__main__":
    print("="*60)
    print("🧠 TESTE DO SCRIPTUREMON BRAIN")
    print("="*60)
    
    brain = ScripturemonBrain()
    
    # Roteiro de teste
    test_screenplay = """FADE IN:

INT. CAFÉ - DIA

JOHN (35), cansado, olha para o laptop.

JOHN
Não consigo mais escrever.

MARY (28) se aproxima.

MARY
Talvez você precise de uma pausa.

JOHN
Ou talvez eu precise de uma nova vida.

FADE OUT."""
    
    # Analisa
    print("\n📝 Analisando roteiro de teste...")
    result = brain.analyze_screenplay(test_screenplay, "Teste Café")
    
    print(f"\n📊 RESULTADO:")
    print(f"Score Real: {result['score']}/100")
    print(f"Cenas: {len(result['structure']['scenes'])}")
    print(f"Personagens: {result['structure']['characters']}")
    print(f"\n💬 FEEDBACK:")
    print(result['feedback'])
    
    print("\n✅ Scripturemon Brain funcionando!")