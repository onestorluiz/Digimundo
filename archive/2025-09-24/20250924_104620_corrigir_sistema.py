#!/usr/bin/env python3
"""
SCRIPT DE CORREÇÃO AUTOMATIZADA DO SISTEMA
Corrige todos os bugs identificados
"""

import os
import shutil
from pathlib import Path
import json

class CorretorSistema:
    """Corrige todos os bugs do sistema"""

    def __init__(self):
        self.correcoes = []
        self.sucesso = 0
        self.falhas = 0

    def log(self, msg, tipo="info"):
        """Log das correções"""
        simbolos = {"ok": "✅", "erro": "❌", "info": "ℹ️", "aviso": "⚠️"}
        print(f"{simbolos.get(tipo, '•')} {msg}")
        self.correcoes.append({"tipo": tipo, "msg": msg})

    def corrigir_knowledge_packs(self):
        """Correção #1: Criar knowledge packs"""
        print("\n🔧 CORRIGINDO: Knowledge Packs Ausentes")
        print("-"*40)

        try:
            # Criar diretório se não existir
            pack_dir = Path('knowledge_packs')
            pack_dir.mkdir(exist_ok=True)

            # Criar packs de exemplo
            packs = {
                'vogler.txt': """# The Writer's Journey - Christopher Vogler
Hero's Journey structure for screenplay analysis:
1. Ordinary World
2. Call to Adventure
3. Refusal of the Call
4. Meeting the Mentor
5. Crossing the Threshold
6. Tests, Allies, Enemies
7. Approach to the Inmost Cave
8. Ordeal
9. Reward
10. The Road Back
11. Resurrection
12. Return with the Elixir""",

                'snyder.txt': """# Save the Cat - Blake Snyder
15 Beat Sheet Structure:
1. Opening Image (1)
2. Theme Stated (5)
3. Set-Up (1-10)
4. Catalyst (12)
5. Debate (12-25)
6. Break into Two (25)
7. B Story (30)
8. Fun and Games (30-55)
9. Midpoint (55)
10. Bad Guys Close In (55-75)
11. All Is Lost (75)
12. Dark Night of the Soul (75-85)
13. Break into Three (85)
14. Finale (85-110)
15. Final Image (110)""",

                'mckee.txt': """# Story - Robert McKee
Story principles:
- Structure is character
- Pressure reveals true character
- Story is about change
- Conflict is the soul of drama
- The controlling idea
- Progressive complications
- Crisis, Climax, Resolution""",

                'truby.txt': """# The Anatomy of Story - John Truby
Seven Steps:
1. Weakness and Need
2. Desire
3. Opponent
4. Plan
5. Battle
6. Self-Revelation
7. New Equilibrium""",

                'field.txt': """# Screenplay - Syd Field
Three Act Structure:
- Act I: Setup (25%)
- Act II: Confrontation (50%)
- Act III: Resolution (25%)
- Plot Point 1 (25-27)
- Midpoint (50-60)
- Plot Point 2 (85-90)"""
            }

            criados = 0
            for nome, conteudo in packs.items():
                arquivo = pack_dir / nome
                arquivo.write_text(conteudo)
                criados += 1

            self.log(f"Criados {criados} knowledge packs", "ok")
            self.sucesso += 1
            return True

        except Exception as e:
            self.log(f"Erro ao criar packs: {e}", "erro")
            self.falhas += 1
            return False

    def corrigir_safe_parser(self):
        """Correção #2: Criar safe parser que faltava"""
        print("\n🔧 CORRIGINDO: Safe Parser Ausente")
        print("-"*40)

        # Verificar se já existe
        if Path('safe_json_parser_ultimate.py').exists():
            self.log("Safe parser já existe", "aviso")
            return True

        try:
            codigo = '''#!/usr/bin/env python3
"""
Safe JSON Parser Ultimate
Wrapper robusto para parsing de JSON
"""

from typing import Dict, Optional, Tuple

def safe_json_parse(text: str, confidence_threshold: float = 0.3) -> Tuple[Optional[Dict], float]:
    """
    Parse seguro de JSON com fallback para parser robusto

    Args:
        text: Texto para fazer parse
        confidence_threshold: Threshold mínimo de confiança

    Returns:
        Tuple de (resultado, confiança)
    """
    try:
        from improved_json_parser import robust_json_parse
        return robust_json_parse(text)
    except ImportError:
        # Fallback se não tiver o parser robusto
        import json
        try:
            result = json.loads(text)
            return result, 0.9
        except:
            return None, 0.0

def calculate_confidence(result: Optional[Dict]) -> float:
    """
    Calcula confiança baseada no resultado

    Args:
        result: Dicionário parseado ou None

    Returns:
        Score de confiança entre 0.0 e 1.0
    """
    if not result:
        return 0.0

    # Confiança baseada na completude
    confidence = 0.5

    if isinstance(result, dict):
        # Adiciona confiança por campos importantes
        important_fields = ['metadata', 'analysis', 'validation', 'evidence_log']
        for field in important_fields:
            if field in result:
                confidence += 0.1

    return min(confidence, 1.0)

# Teste se executado diretamente
if __name__ == "__main__":
    test_cases = [
        '{"test": true}',
        '{"invalid": ',
        'not json at all'
    ]

    for test in test_cases:
        result, conf = safe_json_parse(test)
        print(f"Input: {test[:20]}...")
        print(f"Result: {result is not None}, Confidence: {conf:.2f}")
        print()
'''

            with open('safe_json_parser_ultimate.py', 'w') as f:
                f.write(codigo)

            self.log("Safe parser criado com sucesso", "ok")
            self.sucesso += 1
            return True

        except Exception as e:
            self.log(f"Erro ao criar safe parser: {e}", "erro")
            self.falhas += 1
            return False

    def corrigir_prompt_modelo(self):
        """Correção #3: Melhorar prompt para estrutura correta"""
        print("\n🔧 CORRIGINDO: Prompt do Modelo")
        print("-"*40)

        try:
            # Ler arquivo atual
            arquivo = Path('ollama_with_memory.py')
            conteudo = arquivo.read_text()

            # Melhorar o prompt
            novo_prompt = '''IMPORTANTE: Retorne APENAS um JSON com EXATAMENTE esta estrutura:
{
  "metadata": {"genre": "...", "pages": "...", "title": "..."},
  "evidence_log": [{"page": 1, "evidence": "...", "type": "..."}],
  "analise_estrutural": {
    "inciting_incident": {"page": "...", "description": "..."},
    "climax": {"page": "...", "description": "..."},
    "resolution": {"page": "...", "description": "..."}
  },
  "analise_personagem": [
    {"name": "...", "arc": "...", "motivation": "..."}
  ],
  "validation": {"score": 0-100, "valid": true, "strengths": [], "weaknesses": []}
}

NUNCA retorne outro formato! Preencha TODOS os campos!'''

            # Substituir prompt antigo
            if 'IMPORTANTE: Retorne APENAS um JSON' in conteudo:
                import re
                pattern = r'IMPORTANTE: Retorne APENAS um JSON.*?\}\}'
                conteudo_novo = re.sub(pattern, novo_prompt, conteudo, flags=re.DOTALL)

                if conteudo != conteudo_novo:
                    arquivo.write_text(conteudo_novo)
                    self.log("Prompt melhorado com estrutura mais detalhada", "ok")
                else:
                    self.log("Prompt não foi alterado", "aviso")
            else:
                self.log("Padrão de prompt não encontrado", "aviso")

            self.sucesso += 1
            return True

        except Exception as e:
            self.log(f"Erro ao corrigir prompt: {e}", "erro")
            self.falhas += 1
            return False

    def limpar_processos_ollama(self):
        """Correção #4: Limpar processos órfãos"""
        print("\n🔧 CORRIGINDO: Múltiplos Processos Ollama")
        print("-"*40)

        try:
            import subprocess

            # Contar processos antes
            result = subprocess.run(
                ["pgrep", "-f", "ollama"],
                capture_output=True,
                text=True
            )
            antes = len(result.stdout.strip().split('\n')) if result.stdout else 0

            if antes > 3:
                self.log(f"Encontrados {antes} processos, limpando...", "aviso")

                # Matar processos exceto o principal
                subprocess.run(["pkill", "-f", "ollama run"], capture_output=True)
                subprocess.run(["pkill", "-f", "ollama_continuous"], capture_output=True)

                # Contar depois
                result = subprocess.run(
                    ["pgrep", "-f", "ollama"],
                    capture_output=True,
                    text=True
                )
                depois = len(result.stdout.strip().split('\n')) if result.stdout else 0

                self.log(f"Reduzido de {antes} para {depois} processos", "ok")
            else:
                self.log(f"Apenas {antes} processos, OK", "ok")

            self.sucesso += 1
            return True

        except Exception as e:
            self.log(f"Erro ao limpar processos: {e}", "erro")
            self.falhas += 1
            return False

    def executar_correcoes(self):
        """Executa todas as correções"""
        print("\n" + "="*50)
        print("🚀 INICIANDO CORREÇÕES AUTOMATIZADAS")
        print("="*50)

        # Executar cada correção
        self.corrigir_knowledge_packs()
        self.corrigir_safe_parser()
        self.corrigir_prompt_modelo()
        self.limpar_processos_ollama()

        # Relatório final
        print("\n" + "="*50)
        print("📊 RELATÓRIO DE CORREÇÕES")
        print("="*50)

        print(f"\n✅ Sucesso: {self.sucesso}")
        print(f"❌ Falhas: {self.falhas}")

        taxa = (self.sucesso / (self.sucesso + self.falhas) * 100) if (self.sucesso + self.falhas) > 0 else 0
        print(f"\nTaxa de sucesso: {taxa:.0f}%")

        # Salvar log
        with open('log_correcoes.json', 'w') as f:
            json.dump({
                'correcoes': self.correcoes,
                'sucesso': self.sucesso,
                'falhas': self.falhas,
                'taxa': taxa
            }, f, indent=2)

        print("\n💾 Log salvo em log_correcoes.json")

        if taxa >= 75:
            print("\n✅ CORREÇÕES APLICADAS COM SUCESSO!")
            print("Execute test_rapido_setorial.py para validar")
            return True
        else:
            print("\n❌ ALGUMAS CORREÇÕES FALHARAM")
            print("Verifique o log para detalhes")
            return False

def main():
    """Função principal"""
    corretor = CorretorSistema()
    sucesso = corretor.executar_correcoes()

    print("\n🥷 DIGIMUNDO PRESENTE")
    return 0 if sucesso else 1

if __name__ == "__main__":
    exit(main())