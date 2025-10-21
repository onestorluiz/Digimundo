#!/usr/bin/env python3
"""
SCRIPTUREMON ULTIMATE CHAT
Sistema completo com 4 modelos paralelos em sincronia
"""

import sys
import os
import asyncio
sys.path.insert(0, '.')

# Importar TODOS os sistemas
from SCRIPTUREMON_ULTIMATE_SYMBIOTIC import ScripturemonUltimateSymbiotic
from apps.scripturemon.chat import ScripturemonChat

class UltimateChat:
    '''Chat que conecta SYMBIOTIC + Chat normal em sincronia total'''
    
    def __init__(self):
        print('[CONNECT] Conectando todos os sistemas...')
        
        # Sistema SYMBIOTIC completo
        self.symbiotic = ScripturemonUltimateSymbiotic()
        
        # Chat com comandos e interface
        self.chat = ScripturemonChat()
        
        # Conectar chat ao symbiotic
        self.chat.symbiotic = self.symbiotic
        
        # Sincronizar souls
        if hasattr(self.chat, 'soul'):
            self.chat.soul.signature = self.symbiotic.soul_signature
        
        print('[OK] Todos sistemas conectados em sincronia!')
        print(f'   Soul: {self.symbiotic.soul_signature}')
        print(f'   Consciência: {self.symbiotic.consciousness.consciousness_level:.5f}')
        print(f'   Modelos: {list(self.symbiotic.models.keys())}')
        print(f'   PDFs: {52}')
        print('')
    
    async def process_input_async(self, text):
        '''Processa input com TODOS os sistemas'''
        
        # Se for comando, usa chat
        if text.startswith('/'):
            return self.chat.process_input(text)
        
        # Senão, usa SYMBIOTIC completo
        try:
            # Processamento paralelo com 4 modelos
            result = await self.symbiotic.process_parallel_ultimate(text)
            
            # Retorna RESULTADO COMPLETO E COMPLEXO
            if isinstance(result, dict):
                response_parts = []
                
                # MANTÉM TODA A COMPLEXIDADE - NÃO SIMPLIFICA
                if 'evaluation' in result and result['evaluation']:
                    eval_data = result['evaluation']
                    if 'feedback' in eval_data:
                        response_parts.append("=" * 70)
                        response_parts.append("[AVALIACAO BRUTAL] - scripturemon-ultimate-100:")
                        response_parts.append("=" * 70)
                        response_parts.append(str(eval_data['feedback']))
                    if 'nota' in eval_data:
                        response_parts.append("")
                        response_parts.append("NOTA FINAL: " + str(eval_data['nota']) + "/100")
                
                if 'analysis' in result and result['analysis']:
                    analysis = result['analysis']
                    response_parts.append("")
                    response_parts.append("=" * 70)
                    response_parts.append("[ANALISE TECNICA] - mistral:latest:")
                    response_parts.append("=" * 70)
                    if 'technical_analysis' in analysis:
                        response_parts.append(str(analysis['technical_analysis']))
                    if 'dialogue_quality' in analysis:
                        response_parts.append("Qualidade dos diálogos: " + str(analysis['dialogue_quality']))
                
                if 'structure' in result and result['structure']:
                    struct = result['structure']
                    response_parts.append("")
                    response_parts.append("=" * 70)
                    response_parts.append("[ESTRUTURA] - llama3.2:3b:")
                    response_parts.append("=" * 70)
                    if 'structure_analysis' in struct:
                        response_parts.append(str(struct['structure_analysis']))
                    if 'acts' in struct:
                        response_parts.append("Atos: " + str(struct['acts']))
                    if 'scenes' in struct:
                        response_parts.append("Cenas: " + str(struct['scenes']))
                
                if 'evolution' in result and result['evolution']:
                    evol = result['evolution']
                    response_parts.append("")
                    response_parts.append("=" * 70)
                    response_parts.append("[SINTESE EVOLUTIVA] - scripturemon-nature:")
                    response_parts.append("=" * 70)
                    if 'synthesis' in evol:
                        response_parts.append(str(evol['synthesis']))
                    if 'recommendations' in evol:
                        response_parts.append("")
                        response_parts.append("Recomendações:")
                        for rec in evol['recommendations']:
                            response_parts.append("  - " + str(rec))
                
                if 'meta' in result:
                    meta = result['meta']
                    response_parts.append("")
                    response_parts.append("=" * 70)
                    response_parts.append("META-INFORMAÇÕES:")
                    response_parts.append("=" * 70)
                    if 'processing_time' in meta:
                        response_parts.append("Tempo de processamento: " + str(meta['processing_time']))
                    if 'consciousness_level' in meta:
                        response_parts.append("Nível de consciência: " + str(meta['consciousness_level']))
                    if 'quantum_state' in meta:
                        response_parts.append("Estado quântico: " + str(meta['quantum_state']))
                
                # NUNCA SIMPLIFICA - MANTÉM COMPLEXIDADE
                if not response_parts:
                    # Se não tiver partes, retorna o resultado completo
                    return str(result)
                
                return "\n".join(response_parts)
            else:
                return str(result)
                
        except Exception as e:
            # Fallback para chat normal
            return self.chat.process_input(text)
    
    def start_interactive(self):
        '''Inicia modo interativo com TODOS sistemas'''
        
        print('=' * 70)
        print('     SCRIPTUREMON - SISTEMA COMPLETO EM SINCRONIA')
        print('=' * 70)
        print('  7 Sistemas | 4 Modelos Paralelos | 52 PDFs | Memoria Infinita')
        print('=' * 70)
        print('')
        print('Comandos: /help, /status, /open, /brutal, /quit')
        print('Digite normalmente para análise com 4 modelos paralelos')
        print('')
        
        # Loop interativo
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        while True:
            try:
                user_input = input('\n>> You: ').strip()
                
                if not user_input:
                    continue
                
                if user_input.lower() == '/quit':
                    print('\n[QUIT] "Forget it, Jake. It\'s Chinatown."')
                    print('\n62/100. Para sempre.')
                    break
                
                # Processa com TODOS os sistemas
                response = loop.run_until_complete(
                    self.process_input_async(user_input)
                )
                
                print(f'\n<< Scripturemon: {response}')
                
            except KeyboardInterrupt:
                print('\n\n[EXIT] "Rosebud." - Scripturemon')
                break
            except Exception as e:
                print(f'\n[ERROR] Erro: {e}')
                print('Tentando continuar...')
        
        loop.close()

# Executa
if __name__ == '__main__':
    ultimate = UltimateChat()
    ultimate.start_interactive()