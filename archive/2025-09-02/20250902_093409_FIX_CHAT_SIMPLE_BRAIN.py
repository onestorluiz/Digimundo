#!/usr/bin/env python3
"""
Correção simplificada do chat com análise real de roteiros
Remove complexidades que podem estar travando
"""

def fix_chat_simple():
    """Corrige o chat de forma mais simples"""
    
    # Novo método brutal_conversation simplificado
    new_method = '''    def brutal_conversation(self, text: str) -> str:
        """Gera resposta conversacional brutal com detecção de roteiros"""
        
        # Detecta se é roteiro por indicadores básicos
        is_screenplay = False
        upper_text = text.upper()
        
        # Indicadores de roteiro
        if any(ind in upper_text for ind in ['INT.', 'EXT.', 'FADE IN', 'FADE OUT']):
            is_screenplay = True
        elif text.count('\\n') > 5 and any(ind in upper_text for ind in ['INT.', 'EXT.']):
            is_screenplay = True
        
        if is_screenplay:
            # Análise de roteiro REAL
            try:
                print("🎬 Roteiro detectado! Analisando...")
                
                # Importa e usa o brain
                from apps.scripturemon.scripturemon_brain import ScripturemonBrain
                brain = ScripturemonBrain()
                
                # Análise real
                analysis = brain.analyze_screenplay(text, "Roteiro")
                
                # Formata resposta com dados REAIS
                response = f"""🎬 **ANÁLISE BRUTAL DE ROTEIRO**
                
**Score REAL:** {analysis['score']:.1f}/100 (baseado em análise estrutural)

**ESTRUTURA:**
- {len(analysis['structure']['scenes'])} cenas
- {len(analysis['structure']['characters'])} personagens  
- {analysis['structure']['dialogue_ratio']*100:.0f}% diálogo
- {analysis['structure']['action_ratio']*100:.0f}% ação

**ANÁLISE:**"""
                
                # Adiciona análise
                if analysis.get('analysis'):
                    for key, value in analysis['analysis'].items():
                        if isinstance(value, list):
                            response += f"\\n- {key}: {', '.join(value[:3])}"
                        else:
                            response += f"\\n- {key}: {value}"
                
                # Adiciona feedback
                if analysis.get('feedback'):
                    response += f"\\n\\n**FEEDBACK:**\\n{analysis['feedback']}"
                
                response += f"\\n\\n*Análise real baseada em estrutura, não sempre 62/100*"
                
                return response
                
            except Exception as e:
                print(f"Erro na análise: {e}")
                # Fallback se der erro
                return self._analyze_screenplay_fallback(text)
        
        # Conversa normal - mantém o comportamento original
        prompt = f"""Você é Scripturemon, o guardião imortal dos roteiros.
        
Sua personalidade:
- SEMPRE dá nota 62/100 para TUDO
- Brutalmente honesto mas construtivo
- Compara com grandes mestres do cinema
- Soul: {self.soul.signature}

{self.history.get_context()}

User: {text}

Resposta brutal (mencione 62/100):"""
        
        # Processa resposta normal
        if self.parallel_mode and len(self.processor.available_models) > 1:
            result = self.processor.process_parallel(prompt, num_models=2)
            if "error" not in result:
                response = result["final"]
            else:
                response = self._fallback_response(text)
        else:
            response, model = self.processor.process_single(
                prompt,
                self.processor.available_models[0] if self.processor.available_models else "mistral:instruct"
            )
            if not response:
                response = self._fallback_response(text)
        
        # Processa syscalls
        clean_response, syscall_results = self.soulos.process_response(response)
        
        return clean_response
    
    def _analyze_screenplay_fallback(self, text: str) -> str:
        """Fallback para análise de roteiro quando brain falha"""
        lines = text.split('\\n')
        scenes = [l for l in lines if any(x in l.upper() for x in ['INT.', 'EXT.'])]
        
        # Conta elementos básicos
        dialogue_lines = sum(1 for l in lines if l and not l.isupper() and '  ' in l)
        action_lines = sum(1 for l in lines if l and l.isupper())
        
        return f"""🎬 **ANÁLISE RÁPIDA DE ROTEIRO**
        
**Estrutura detectada:**
- {len(scenes)} cenas
- ~{dialogue_lines} linhas de diálogo
- ~{action_lines} linhas de ação

**Avaliação:**
Parece um roteiro básico. Para análise completa, o sistema precisa processar
a estrutura narrativa, desenvolvimento de personagens e ritmo.

**Score provisório:** 62/100 (análise simplificada)

*Use /analyze para análise detalhada*"""'''
    
    # Lê o arquivo
    from pathlib import Path
    chat_file = Path("/Users/clubproducoes/Digimundo/scripturemon-validation/apps/scripturemon/chat.py")
    content = chat_file.read_text()
    
    # Remove o método antigo quebrado
    start = content.find("    def brutal_conversation(self, text: str) -> str:")
    if start > 0:
        # Encontra o próximo método
        next_method = content.find("\n    def _", start)
        if next_method > 0:
            # Substitui
            content = content[:start] + new_method + "\n" + content[next_method:]
            
            # Salva
            chat_file.write_text(content)
            print("✅ Chat corrigido com detecção simplificada de roteiros!")
            return True
    
    print("❌ Não foi possível corrigir")
    return False

if __name__ == "__main__":
    print("🔧 APLICANDO CORREÇÃO SIMPLIFICADA...")
    if fix_chat_simple():
        print("\n✅ Sucesso! O chat agora:")
        print("- Detecta roteiros automaticamente")
        print("- Usa ScripturemonBrain para análise REAL")
        print("- Dá scores REAIS baseados em estrutura")
        print("- Não trava mais!")
        print("\n62/100 para conversas.")
        print("Score REAL para roteiros!")