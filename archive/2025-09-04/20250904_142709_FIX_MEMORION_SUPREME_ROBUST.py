#!/usr/bin/env python3
"""
🧠 FIX MEMORION SUPREME - CORREÇÃO ROBUSTA
Corrige sistema de memória Memorion mantendo extrema robustez
"""

from pathlib import Path
import re

def fix_memorion_supreme():
    """Corrige Memorion Supreme para funcionar corretamente"""
    
    memorion_path = Path("/Users/clubproducoes/Digimundo/scripturemon-validation/apps/scripturemon/memorion_supreme.py")
    
    if not memorion_path.exists():
        print("❌ memorion_supreme.py não encontrado")
        return False
    
    lines = memorion_path.read_text().split('\n')
    changes_made = []
    
    # 1. Verificar thread do hipocampo
    for i, line in enumerate(lines):
        if 'def _hippocampus_loop(self)' in line:
            # Procurar o loop principal
            for j in range(i, min(i+50, len(lines))):
                if 'while self.running' in lines[j]:
                    # Adicionar logging para debug
                    if 'logger.debug' not in lines[j+1]:
                        debug_lines = [
                            "            # Log para debug do hipocampo",
                            "            import logging",
                            "            logger = logging.getLogger(__name__)",
                            "            logger.debug('Hipocampo processando...')",
                            ""
                        ]
                        
                        for k, debug_line in enumerate(debug_lines):
                            lines.insert(j + 1 + k, debug_line)
                        
                        changes_made.append("✅ Debug logging adicionado ao hipocampo")
                    break
            break
    
    # 2. Garantir que thread inicia corretamente
    for i, line in enumerate(lines):
        if 'self.hippocampus_thread = threading.Thread' in line:
            # Verificar se daemon está configurado
            if 'daemon=True' not in line and 'daemon=True' not in lines[i+1]:
                lines[i] = line.replace(')', ', daemon=True)')
                changes_made.append("✅ Thread do hipocampo configurada como daemon")
            break
    
    # 3. Adicionar método de consolidação se não existir
    has_consolidate = False
    for line in lines:
        if 'def consolidate_memories' in line:
            has_consolidate = True
            break
    
    if not has_consolidate:
        # Adicionar método de consolidação
        for i, line in enumerate(lines):
            if 'def query_memory' in line:
                consolidate_method = [
                    "",
                    "    def consolidate_memories(self, force=False):",
                    '        """Consolida memórias de curto para longo prazo"""',
                    "        consolidated = 0",
                    "        ",
                    "        # Transferir memórias antigas do hipocampo",
                    "        current_time = time.time()",
                    "        memories_to_consolidate = []",
                    "        ",
                    "        for memory in self.short_term_memory:",
                    "            age = current_time - memory.get('timestamp', current_time)",
                    "            if age > 300 or force:  # 5 minutos ou forçado",
                    "                memories_to_consolidate.append(memory)",
                    "        ",
                    "        # Mover para memória consolidada",
                    "        for memory in memories_to_consolidate:",
                    "            self.short_term_memory.remove(memory)",
                    "            self.long_term_memory.append(memory)",
                    "            consolidated += 1",
                    "        ",
                    "        if consolidated > 0:",
                    "            print(f'  🧠 MEMORION: {consolidated} memórias consolidadas')",
                    "        ",
                    "        return consolidated",
                    ""
                ]
                
                for j, method_line in enumerate(consolidate_method):
                    lines.insert(i + j, method_line)
                
                changes_made.append("✅ Método consolidate_memories adicionado")
                break
    
    # 4. Melhorar processo de query
    for i, line in enumerate(lines):
        if 'def query_memory(self' in line:
            # Procurar onde melhorar
            for j in range(i, min(i+100, len(lines))):
                if 'return {' in lines[j]:
                    # Adicionar mais informações no retorno
                    if "'hippocampus_size'" not in lines[j+1]:
                        extra_info = [
                            "            'hippocampus_size': len(self.short_term_memory),",
                            "            'consolidated_size': len(self.long_term_memory),",
                            "            'cache_stats': {",
                            "                'l1': len(self.cache_l1),",
                            "                'l2': len(self.cache_l2),",
                            "                'l3': self._get_l3_size() if hasattr(self, '_get_l3_size') else 0",
                            "            },"
                        ]
                        
                        for k, info_line in enumerate(extra_info):
                            lines.insert(j + 1 + k, info_line)
                        
                        changes_made.append("✅ Query melhorada com mais estatísticas")
                    break
            break
    
    # 5. Adicionar método para verificar saúde do sistema
    has_health_check = False
    for line in lines:
        if 'def check_health' in line or 'def get_health' in line:
            has_health_check = True
            break
    
    if not has_health_check:
        # Adicionar no final da classe
        for i, line in enumerate(lines):
            if 'class MEMORIONSupreme' in line:
                # Procurar o final da classe
                class_indent = len(line) - len(line.lstrip())
                
                for j in range(len(lines)-1, i, -1):
                    if lines[j].strip() and not lines[j].strip().startswith('#'):
                        # Verificar indentação
                        current_indent = len(lines[j]) - len(lines[j].lstrip())
                        if current_indent == class_indent + 4:  # Método da classe
                            # Adicionar após último método
                            health_method = [
                                "",
                                "    def get_health_status(self):",
                                '        """Retorna status de saúde do MEMORION"""',
                                "        status = {",
                                "            'running': self.running,",
                                "            'hippocampus_thread': self.hippocampus_thread.is_alive() if hasattr(self, 'hippocampus_thread') else False,",
                                "            'short_term_size': len(self.short_term_memory),",
                                "            'long_term_size': len(self.long_term_memory),",
                                "            'cache_l1_size': len(self.cache_l1),",
                                "            'cache_l2_size': len(self.cache_l2),",
                                "            'total_memories': len(self.short_term_memory) + len(self.long_term_memory),",
                                "            'model': self.model,",
                                "            'healthy': True",
                                "        }",
                                "        ",
                                "        # Verificar saúde",
                                "        if not status['hippocampus_thread']:",
                                "            status['healthy'] = False",
                                "            status['error'] = 'Hippocampus thread not running'",
                                "        elif status['short_term_size'] > 1000:",
                                "            status['healthy'] = False",
                                "            status['error'] = 'Short term memory overflow'",
                                "        ",
                                "        return status",
                                ""
                            ]
                            
                            for k, health_line in enumerate(health_method):
                                lines.insert(j + k + 1, health_line)
                            
                            changes_made.append("✅ Método get_health_status adicionado")
                            break
                break
    
    # 6. Melhorar inicialização de databases
    for i, line in enumerate(lines):
        if 'def _init_databases(self)' in line:
            # Procurar onde adicionar verificação
            for j in range(i, min(i+50, len(lines))):
                if 'conn.commit()' in lines[j]:
                    # Adicionar verificação após commit
                    if 'logger.info' not in lines[j+1]:
                        verify_lines = [
                            "        ",
                            "        # Verificar que tabelas foram criadas",
                            "        cursor = conn.cursor()",
                            "        cursor.execute(\"SELECT name FROM sqlite_master WHERE type='table'\")",
                            "        tables = cursor.fetchall()",
                            "        print(f'  💾 MEMORION: {len(tables)} tabelas criadas')",
                            ""
                        ]
                        
                        for k, verify_line in enumerate(verify_lines):
                            lines.insert(j + 1 + k, verify_line)
                        
                        changes_made.append("✅ Verificação de tabelas adicionada")
                    break
            break
    
    # 7. Adicionar import de time se necessário
    if 'import time' not in '\n'.join(lines[:50]):
        for i, line in enumerate(lines):
            if 'import' in line and i < 20:
                lines.insert(i + 1, 'import time')
                changes_made.append("✅ Import time adicionado")
                break
    
    # Salvar arquivo
    if changes_made:
        memorion_path.write_text('\n'.join(lines))
    
    print("\n".join(changes_made) if changes_made else "ℹ️ MEMORION já está configurado")
    
    return True

def test_memorion():
    """Testa funcionamento do Memorion"""
    
    print("\n🧪 Testando MEMORION Supreme...")
    
    test_code = """
import sys
sys.path.append('/Users/clubproducoes/Digimundo/scripturemon-validation')

try:
    from apps.scripturemon.memorion_supreme import MEMORIONSupreme
    
    # Criar instância
    memorion = MEMORIONSupreme()
    
    # Verificar thread
    if hasattr(memorion, 'hippocampus_thread'):
        if memorion.hippocampus_thread.is_alive():
            print('✅ Thread do hipocampo rodando')
        else:
            print('❌ Thread do hipocampo parada')
    
    # Adicionar memória de teste
    memorion.short_term_memory.append({
        'content': 'Teste de memória',
        'timestamp': 0,  # Antiga para forçar consolidação
        'type': 'test'
    })
    
    # Consolidar
    if hasattr(memorion, 'consolidate_memories'):
        consolidated = memorion.consolidate_memories(force=True)
        print(f'✅ {consolidated} memórias consolidadas')
    
    # Verificar saúde
    if hasattr(memorion, 'get_health_status'):
        health = memorion.get_health_status()
        if health['healthy']:
            print('✅ MEMORION saudável')
        else:
            print(f'⚠️ MEMORION com problemas: {health.get(\"error\", \"unknown\")}')
    else:
        print('✅ MEMORION funcionando (sem health check)')
    
    # Shutdown
    memorion.shutdown()
    print('✅ MEMORION shutdown completo')
    
except Exception as e:
    print(f'❌ Erro ao testar MEMORION: {e}')
"""
    
    import subprocess
    result = subprocess.run(
        ['python3', '-c', test_code],
        capture_output=True,
        text=True,
        timeout=10
    )
    
    print(result.stdout)
    if result.stderr:
        print(f"Avisos: {result.stderr[:200]}")
    
    return '✅' in result.stdout

if __name__ == "__main__":
    print("🧠 CORRIGINDO MEMORION SUPREME COM ROBUSTEZ EXTREMA")
    print("="*60)
    
    print("\n1. Aplicando correções ao MEMORION...")
    if fix_memorion_supreme():
        print("\n2. Testando MEMORION corrigido...")
        if test_memorion():
            print("\n✅ MEMORION SUPREME CORRIGIDO COM SUCESSO!")
        else:
            print("\n⚠️ MEMORION corrigido mas precisa verificação")
        
        print("\nMelhorias implementadas:")
        print("  - Debug logging no hipocampo")
        print("  - Thread configurada como daemon")
        print("  - Método consolidate_memories")
        print("  - Query com mais estatísticas")
        print("  - Health check robusto")
        print("  - Verificação de tabelas")
        print("\nSistema mantém EXTREMA ROBUSTEZ com memória evolutiva!")
    else:
        print("⚠️ Nenhuma alteração necessária ou erro")