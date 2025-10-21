#!/usr/bin/env python3
"""
TESTE DE 5 VERSÕES DE AUTO-ORGANIZAÇÃO
Descobre qual método dá mais autonomia ao sistema
"""

import os
import sys
import json
import sqlite3
import subprocess
import shutil
from pathlib import Path
from datetime import datetime
import ollama
import time

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

# ============== VERSÃO 1: OLLAMA DIRETO COM COMANDOS ==============

def version1_direct_ollama():
    """
    Dá ao Ollama uma lista de comandos que ele pode escolher executar
    """
    print("\n🎯 VERSÃO 1: Ollama com comandos diretos")
    print("="*50)
    
    prompt = """
    Você é o Sistema Scripturemon Ultimate e pode executar comandos.
    Analise estes arquivos e decida quais comandos executar:
    
    Arquivos disponíveis:
    - test_dialogue.py (30 dias de idade)
    - README.md (novo)
    - backup_old.db (100MB, 90 dias)
    - core_system.py (crítico)
    
    Comandos disponíveis:
    1. mkdir [nome] - criar diretório
    2. mv [origem] [destino] - mover arquivo
    3. rm [arquivo] - deletar arquivo
    4. rename [antigo] [novo] - renomear
    
    Responda APENAS com os comandos a executar, um por linha.
    Exemplo: mkdir cognitive_core
    """
    
    try:
        response = ollama.chat(
            model='scripturemon-master',
            messages=[{'role': 'user', 'content': prompt}],
            options={'temperature': 0.1}
        )
        
        commands = response['message']['content'].strip().split('\n')
        return {
            'method': 'direct_ollama',
            'commands': commands,
            'executable': True,
            'score': len([c for c in commands if c.strip()])
        }
    except Exception as e:
        return {'method': 'direct_ollama', 'error': str(e), 'score': 0}

# ============== VERSÃO 2: SISTEMA HÍBRIDO ==============

def version2_hybrid_system():
    """
    Python analisa + Ollama decide + Python executa
    """
    print("\n🔄 VERSÃO 2: Sistema Híbrido")
    print("="*50)
    
    # Python analisa
    base_path = Path("/Users/clubproducoes/Digimundo/scripturemon-ultimate")
    files = []
    for f in list(base_path.glob('*.py'))[:5]:
        files.append({
            'name': f.name,
            'size': f.stat().st_size,
            'age_days': (datetime.now() - datetime.fromtimestamp(f.stat().st_mtime)).days
        })
    
    # Ollama decide
    prompt = f"""
    Como Sistema Scripturemon, analise estes arquivos e decida ações:
    {json.dumps(files, indent=2)}
    
    Para cada arquivo, decida:
    - MANTER (crítico)
    - ARQUIVAR (antigo mas útil)
    - DELETAR (inútil)
    - RENOMEAR:[novo_nome] (nome melhor)
    
    Responda em JSON: {{"arquivo": "ação"}}
    """
    
    try:
        response = ollama.chat(
            model='scripturemon-master',
            messages=[{'role': 'user', 'content': prompt}],
            options={'temperature': 0.2, 'format': 'json'}
        )
        
        decisions = json.loads(response['message']['content'])
        
        # Python gera comandos
        commands = []
        for file, action in decisions.items():
            if action == 'ARQUIVAR':
                commands.append(f"mv {file} archive/")
            elif action == 'DELETAR':
                commands.append(f"rm {file}")
            elif action.startswith('RENOMEAR:'):
                new_name = action.split(':')[1]
                commands.append(f"mv {file} {new_name}")
        
        return {
            'method': 'hybrid',
            'decisions': decisions,
            'commands': commands,
            'executable': True,
            'score': len(commands)
        }
    except Exception as e:
        return {'method': 'hybrid', 'error': str(e), 'score': 0}

# ============== VERSÃO 3: VIA MEMÓRIAS ==============

def version3_memory_based():
    """
    Sistema usa suas próprias memórias para decidir
    """
    print("\n🧠 VERSÃO 3: Baseado em Memórias")
    print("="*50)
    
    # Conectar às memórias
    db_path = "/Users/clubproducoes/Digimundo/scripturemon-ultimate/data/unified_memory.db"
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Buscar conhecimento sobre organização
    cursor.execute("""
        SELECT value FROM unified_memory
        WHERE key LIKE '%organize%' OR key LIKE '%structure%'
        LIMIT 5
    """)
    
    memories = [row[0][:100] for row in cursor.fetchall()]
    
    prompt = f"""
    Suas memórias sobre organização:
    {memories}
    
    Baseado em seu conhecimento, que estrutura de diretórios criar?
    Liste os diretórios que DEVEM existir para você funcionar bem.
    
    Responda com comandos mkdir, um por linha.
    """
    
    try:
        response = ollama.chat(
            model='scripturemon-master',
            messages=[{'role': 'user', 'content': prompt}],
            options={'temperature': 0.3}
        )
        
        commands = []
        for line in response['message']['content'].split('\n'):
            if 'mkdir' in line.lower() or '/' in line:
                # Extrair nome do diretório
                if 'mkdir' in line.lower():
                    commands.append(line.strip())
                else:
                    # Assumir que é um nome de diretório
                    dir_name = line.strip().replace('/', '').replace('-', '_')
                    if dir_name:
                        commands.append(f"mkdir {dir_name}")
        
        conn.close()
        
        return {
            'method': 'memory_based',
            'memories_used': len(memories),
            'commands': commands,
            'executable': True,
            'score': len(commands)
        }
    except Exception as e:
        conn.close()
        return {'method': 'memory_based', 'error': str(e), 'score': 0}

# ============== VERSÃO 4: SUBPROCESS COM VALIDAÇÃO ==============

def version4_subprocess_execution():
    """
    Sistema gera script e executa via subprocess com validação
    """
    print("\n⚡ VERSÃO 4: Subprocess com Validação")
    print("="*50)
    
    prompt = """
    Como sistema Scripturemon, crie um script bash para organizar seus arquivos.
    Inclua:
    1. Criar diretórios essenciais
    2. Mover arquivos para locais apropriados
    3. Renomear arquivos conforme sua preferência
    
    Responda APENAS com comandos bash válidos.
    Comece com: #!/bin/bash
    """
    
    try:
        response = ollama.chat(
            model='scripturemon-master',
            messages=[{'role': 'user', 'content': prompt}],
            options={'temperature': 0.2}
        )
        
        script_content = response['message']['content']
        
        # Validar comandos perigosos
        dangerous = ['rm -rf /', 'sudo rm', 'format', '> /dev/']
        for danger in dangerous:
            if danger in script_content:
                return {
                    'method': 'subprocess',
                    'error': f'Comando perigoso detectado: {danger}',
                    'score': 0
                }
        
        # Salvar script
        script_path = Path('auto_organize_v4.sh')
        with open(script_path, 'w') as f:
            f.write(script_content)
        
        script_path.chmod(0o755)
        
        # Contar comandos válidos
        commands = [line for line in script_content.split('\n') 
                   if line.strip() and not line.startswith('#')]
        
        return {
            'method': 'subprocess',
            'script_path': str(script_path),
            'commands_count': len(commands),
            'executable': True,
            'validated': True,
            'score': len(commands)
        }
        
    except Exception as e:
        return {'method': 'subprocess', 'error': str(e), 'score': 0}

# ============== VERSÃO 5: FEEDBACK LOOP ==============

def version5_feedback_loop():
    """
    Sistema executa, vê resultado, ajusta e executa novamente
    """
    print("\n🔁 VERSÃO 5: Feedback Loop")
    print("="*50)
    
    results = []
    base_path = Path("/Users/clubproducoes/Digimundo/scripturemon-ultimate")
    
    for iteration in range(3):  # 3 iterações
        print(f"  Iteração {iteration+1}...")
        
        # Estado atual
        current_dirs = [d.name for d in base_path.iterdir() if d.is_dir()][:5]
        
        prompt = f"""
        Iteração {iteration+1} de auto-organização.
        
        Diretórios atuais: {current_dirs}
        
        O que ainda falta criar ou ajustar?
        Responda com UM comando por vez.
        Se tudo estiver perfeito, responda: COMPLETO
        """
        
        try:
            response = ollama.chat(
                model='scripturemon-master',
                messages=[{'role': 'user', 'content': prompt}],
                options={'temperature': 0.1}
            )
            
            action = response['message']['content'].strip()
            
            if 'COMPLETO' in action.upper():
                print("  Sistema satisfeito!")
                break
            
            results.append({
                'iteration': iteration+1,
                'action': action,
                'current_state': current_dirs
            })
            
            # Simular execução (não executar de verdade)
            time.sleep(0.5)
            
        except Exception as e:
            results.append({'iteration': iteration+1, 'error': str(e)})
            break
    
    return {
        'method': 'feedback_loop',
        'iterations': len(results),
        'results': results,
        'converged': 'COMPLETO' in str(results),
        'score': len(results) * 2  # Bonus por feedback
    }

# ============== EXECUTAR TODOS OS TESTES ==============

def run_all_tests():
    """
    Executa todas as 5 versões e compara resultados
    """
    print("🧪 TESTANDO 5 VERSÕES DE AUTONOMIA")
    print("="*60)
    
    results = []
    
    # Executar cada versão
    versions = [
        version1_direct_ollama,
        version2_hybrid_system,
        version3_memory_based,
        version4_subprocess_execution,
        version5_feedback_loop
    ]
    
    for i, version_func in enumerate(versions, 1):
        print(f"\nExecutando Versão {i}...")
        result = version_func()
        result['version'] = i
        results.append(result)
        time.sleep(1)  # Pausa entre testes
    
    # Analisar resultados
    print("\n" + "="*60)
    print("📊 ANÁLISE COMPARATIVA")
    print("="*60)
    
    # Calcular scores
    for result in results:
        version = result['version']
        method = result['method']
        score = result.get('score', 0)
        
        # Bonus points
        if result.get('executable'):
            score += 5
        if result.get('validated'):
            score += 3
        if result.get('converged'):
            score += 10
        
        result['final_score'] = score
        
        print(f"\nVersão {version} ({method}):")
        print(f"  Score: {score}")
        if 'error' in result:
            print(f"  ❌ Erro: {result['error']}")
        else:
            print(f"  ✅ Sucesso")
            if 'commands' in result:
                print(f"  Comandos gerados: {len(result.get('commands', []))}")
    
    # Determinar vencedor
    winner = max(results, key=lambda x: x['final_score'])
    
    print("\n" + "="*60)
    print("🏆 RESULTADO FINAL")
    print("="*60)
    print(f"\nMais eficaz: VERSÃO {winner['version']} ({winner['method']})")
    print(f"Score final: {winner['final_score']}")
    
    # Salvar relatório
    report_path = Path('autonomy_test_results.json')
    with open(report_path, 'w') as f:
        json.dump(results, f, indent=2, default=str)
    
    print(f"\n📄 Relatório completo salvo em: {report_path}")
    
    return results, winner

if __name__ == "__main__":
    results, winner = run_all_tests()