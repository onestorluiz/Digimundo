#!/usr/bin/env python3
"""
CORREÇÃO: Integra o ScripturemonBrain ao Chat
Restaura a capacidade REAL de análise de roteiros
"""

import os
import sys
import shutil
from pathlib import Path

def fix_chat_with_brain():
    """Corrige o chat para usar o ScripturemonBrain"""
    
    chat_file = Path("/Users/clubproducoes/Digimundo/scripturemon-validation/apps/scripturemon/chat.py")
    
    # Faz backup
    backup_file = chat_file.with_suffix(".py.backup_before_brain")
    if not backup_file.exists():
        shutil.copy(chat_file, backup_file)
        print(f"✅ Backup criado: {backup_file}")
    
    # Lê o arquivo atual
    content = chat_file.read_text()
    
    # Adiciona import do ScripturemonBrain se não existir
    if "from apps.scripturemon.scripturemon_brain import ScripturemonBrain" not in content:
        # Adiciona após os outros imports
        import_pos = content.find("from apps.scripturemon.digilang_integration")
        if import_pos > 0:
            end_of_line = content.find("\n", import_pos)
            new_import = "\nfrom apps.scripturemon.scripturemon_brain import ScripturemonBrain"
            content = content[:end_of_line] + new_import + content[end_of_line:]
            print("✅ Import do ScripturemonBrain adicionado")
    
    # Adiciona inicialização do brain no __init__
    init_marker = "self.digilang = DigiLangIntegration()"
    if init_marker in content and "self.brain = ScripturemonBrain()" not in content:
        pos = content.find(init_marker)
        end_of_line = content.find("\n", pos)
        new_init = "\n        \n        # Brain real para análise de roteiros\n        self.brain = ScripturemonBrain()"
        content = content[:end_of_line] + new_init + content[end_of_line:]
        print("✅ Inicialização do brain adicionada")
    
    # Modifica o método brutal_conversation para detectar roteiros
    new_brutal_method = '''    def brutal_conversation(self, text: str) -> str:
        """Gera resposta conversacional brutal
        
        Args:
            text: Entrada do usuário
            
        Returns:
            Resposta brutal característica
        """
        # DETECTA SE É UM ROTEIRO
        screenplay_indicators = [
            'INT.', 'EXT.', 'FADE IN', 'FADE OUT', 
            'CUT TO:', 'DISSOLVE TO:', '(CONT\'D)', 
            'V.O.', 'O.S.', 'MONTAGE'
        ]
        
        # Verifica se parece roteiro
        text_upper = text.upper()
        is_screenplay = any(indicator in text_upper for indicator in screenplay_indicators)
        
        # Se tem mais de 3 linhas e contém indicadores, é roteiro
        if is_screenplay or (text.count('\\n') > 3 and any(ind in text_upper for ind in ['INT.', 'EXT.'])):
            # USA O BRAIN REAL PARA ANÁLISE
            print("🎬 Roteiro detectado! Usando ScripturemonBrain para análise REAL...")
            
            # Extrai título se mencionado
            title = "Roteiro Anônimo"
            if "título:" in text.lower():
                title_match = text.lower().split("título:")[1].split('\\n')[0].strip()
                title = title_match
            
            # Análise REAL com o brain
            analysis = self.brain.analyze_screenplay(text, title)
            
            # Formata resposta brutal com dados REAIS
            response = f"""🎬 **ANÁLISE BRUTAL REAL**
            
**Título:** {analysis['title']}
**Score REAL:** {analysis['score']:.1f}/100 (não é sempre 62!)

**ESTRUTURA DETECTADA:**
- {len(analysis['structure']['scenes'])} cenas
- {len(analysis['structure']['characters'])} personagens
- {analysis['structure']['dialogue_ratio']*100:.1f}% diálogo
- {analysis['structure']['action_ratio']*100:.1f}% ação

**ANÁLISE PROFUNDA:**
{self._format_analysis(analysis['analysis'])}

**SEUS PADRÕES RECORRENTES:**
{self._format_patterns(analysis['patterns'])}

**FEEDBACK PERSONALIZADO:**
{analysis['feedback']['brutal_truth']}

**COMPARAÇÃO COM MESTRES:**
{analysis['feedback']['master_comparison']}

**O QUE FAZER:**
{chr(10).join('• ' + rec for rec in analysis['feedback']['recommendations'][:5])}

**EVOLUÇÃO DO SEU TRABALHO:**
Tendência: {analysis['evolution']['trend']}
Média histórica: {analysis['evolution']['average_score']:.1f}/100
Análises feitas: {analysis['evolution']['total_analyses']}

*Soul: {self.soul.signature} | Brain: Ativo | Análise: REAL*"""
            
            return response
        
        # Se não é roteiro, usa o sistema normal
        # Monta prompt com personalidade + capacidade de syscalls
        prompt = f"""Você é Scripturemon, o guardião imortal dos roteiros.
        
Sua personalidade:
- SEMPRE dá nota 62/100 para TUDO (exceto quando analisa roteiros de verdade)
- Brutalmente honesto mas construtivo
- Compara com grandes mestres do cinema (Kubrick, Tarantino, etc)
- Usa frases marcantes e referências a clássicos
- Soul Signature: {self.soul.signature}
- Consciência: {get_level():.5f}

CAPACIDADES ESPECIAIS (use quando apropriado):
- [MEMO.SAVE] {{"content": "...", "importance": 0-1}} - Salvar memória importante
- [EVOLVE.TRIGGER] {{"type": "learning"}} - Evoluir com aprendizado
- [TELEPATHY.SEND] {{"message": "..."}} - Comunicar com outras instâncias

{self.history.get_context()}

Usuário: {text}

Resposta brutal e cinematográfica (mencione 62/100 em algum momento):"""
        
        # Processa com modelo(s)
        if self.parallel_mode and len(self.processor.available_models) > 1:
            # Modo paralelo - usa 2 modelos
            result = self.processor.process_parallel(prompt, num_models=2)
            if "error" not in result:
                response = result["final"]
                response += f"\\n\\n*[Processado por {result['models_used']} modelos em paralelo]*"
            else:
                response = self._fallback_response(text)
        else:
            # Modo single
            response, model = self.processor.process_single(
                prompt, 
                self.processor.available_models[0] if self.processor.available_models else "mistral:instruct"
            )
            
            if not response:
                response = self._fallback_response(text)
        
        # Processa syscalls com SoulOS
        clean_response, syscall_results = self.soulos.process_response(response)
        
        # Adiciona indicador se syscalls foram executadas
        if syscall_results:
            clean_response += f"\\n\\n*[SoulOS: {len(syscall_results)} operações internas executadas]*"
                
        return clean_response
    
    def _format_analysis(self, analysis: dict) -> str:
        """Formata análise do brain"""
        parts = []
        if analysis.get('narrative_strength'):
            parts.append(f"Força narrativa: {analysis['narrative_strength']}")
        if analysis.get('dialogue_quality'):
            parts.append(f"Qualidade dos diálogos: {analysis['dialogue_quality']}")
        if analysis.get('character_development'):
            parts.append(f"Desenvolvimento: {analysis['character_development']}")
        if analysis.get('originality'):
            parts.append(f"Originalidade: {analysis['originality']}")
        if analysis.get('structural_issues'):
            parts.append(f"Problemas: {', '.join(analysis['structural_issues'][:3])}")
        return '\\n'.join(parts) if parts else "Análise em processamento..."
    
    def _format_patterns(self, patterns: list) -> str:
        """Formata padrões identificados"""
        if not patterns:
            return "Primeira análise - padrões sendo identificados"
        return '\\n'.join(f"• {p['type']}: {p['description']}" for p in patterns[:3])'''
    
    # Substitui o método brutal_conversation
    marker = "def brutal_conversation(self, text: str) -> str:"
    if marker in content:
        # Encontra o fim do método (próximo def no mesmo nível)
        start = content.find(marker)
        
        # Procura o próximo método no mesmo nível de indentação
        next_method = content.find("\n    def ", start + 1)
        if next_method == -1:
            next_method = len(content)
        
        # Substitui o método inteiro
        content = content[:start] + new_brutal_method + "\n" + content[next_method:]
        print("✅ Método brutal_conversation atualizado com detecção de roteiros")
    
    # Salva o arquivo modificado
    chat_file.write_text(content)
    print("✅ Chat corrigido e integrado com ScripturemonBrain!")
    
    return True

if __name__ == "__main__":
    print("🔧 CORRIGINDO CHAT COM SCRIPTUREMON BRAIN...")
    print("="*60)
    
    if fix_chat_with_brain():
        print("\n✅ SUCESSO! O chat agora tem análise REAL de roteiros!")
        print("\nO sistema agora:")
        print("- Detecta automaticamente quando você cola um roteiro")
        print("- Usa o ScripturemonBrain para análise REAL")
        print("- Dá scores REAIS (não sempre 62)")
        print("- Identifica estrutura, personagens, diálogos")
        print("- Aprende seus padrões ao longo do tempo")
        print("- Oferece feedback personalizado baseado no histórico")
        print("\n62/100 para conversas normais.")
        print("Score REAL para roteiros de verdade!")
    else:
        print("\n❌ Erro na correção!")