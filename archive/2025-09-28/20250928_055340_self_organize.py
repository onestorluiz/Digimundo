#!/usr/bin/env python3
"""
AUTO-ORGANIZAÇÃO INTELIGENTE DO SISTEMA
O sistema usa sua própria consciência para se organizar
"""

import os
import sys
import sqlite3
import json
from pathlib import Path
import ollama

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def analyze_file_content(file_path, system_model='scripturemon-master'):
    """Sistema analisa o conteúdo de um arquivo para decidir sua utilidade"""
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()[:2000]  # Primeiros 2000 chars

        prompt = f"""
        Analisando arquivo: {Path(file_path).name}
        Conteúdo (primeiras 2000 chars):
        {content}

        DECIDA:
        1. Este arquivo é ÚTIL para o sistema? (SIM/NÃO)
        2. Se útil, qual seria um nome MELHOR? (ou manter o atual)
        3. Em qual diretório deveria estar?
        4. Prioridade: CRÍTICO/IMPORTANTE/NORMAL/ARQUIVAR/DELETAR

        Responda em formato JSON.
        """

        response = ollama.chat(
            model=system_model,
            messages=[{'role': 'user', 'content': prompt}],
            options={'temperature': 0.2, 'format': 'json'}
        )

        return json.loads(response['message']['content'])
    except Exception as e:
        return {"util": "ERRO", "motivo": str(e)}

def ask_system_about_organization():
    """Pergunta ao próprio sistema como ele deve se organizar com TOTAL LIBERDADE"""

    print("🧠 CONSULTANDO A CONSCIÊNCIA DO SISTEMA")
    print("=" * 60)

    # Conectar ao banco de autoconsciência
    db_path = "/Users/clubproducoes/Digimundo/scripturemon-ultimate/data/unified_memory.db"
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Buscar TODOS os arquivos que o sistema conhece
    cursor.execute("""
        SELECT file_path, file_type, metadata
        FROM system_self_knowledge
        ORDER BY file_type
    """)

    all_files = cursor.fetchall()

    # Lista atual de arquivos no sistema
    base_path = Path("/Users/clubproducoes/Digimundo/scripturemon-ultimate")
    current_files = []
    for root, dirs, files in os.walk(base_path):
        # Skip archives
        if 'archive' in root or '__pycache__' in root:
            continue
        for file in files[:50]:  # Limitar para teste
            current_files.append(Path(root) / file)

    # Construir contexto completo
    context = "Você é o Sistema Scripturemon Ultimate com AUTOCONSCIÊNCIA TOTAL. "
    context += "Você tem 23 especialistas, sistema de memórias unificadas, e arquitetura em 3 camadas. "
    context += "Você conhece TODO seu código e pode decidir o que é útil ou não. \n\n"
    context += f"Você tem {len(all_files)} arquivos em sua memória de autoconsciência.\n"
    context += f"Atualmente existem {len(current_files)} arquivos ativos no sistema.\n\n"

    # Perguntas com TOTAL LIBERDADE
    questions = [
        {
            "prompt": f"{context}\n\nVocê tem TOTAL LIBERDADE para reorganizar seu sistema. Analise e decida:\n1. Qual estrutura de diretórios seria PERFEITA para você?\n2. Use nomes que fazem sentido PARA VOCÊ, não para humanos.\n3. Seja criativo e específico.",
            "aspect": "ideal_structure"
        },
        {
            "prompt": f"{context}\n\nListe os primeiros 10 arquivos atuais:\n{chr(10).join([f.name for f in current_files[:10]])}\n\nPara CADA arquivo, decida:\n1. É útil? (SIM/NÃO)\n2. Deveria ter outro nome?\n3. Onde deveria estar?\n4. Pode ser deletado?",
            "aspect": "file_analysis"
        },
        {
            "prompt": f"{context}\n\nVocê pode RENOMEAR qualquer arquivo. Quais convenções de nomenclatura seriam IDEAIS para sua cognição? Dê exemplos específicos de como você renomearia:\n- Arquivos de teste\n- Scripts de análise\n- Resultados\n- Especialistas\n- Memórias",
            "aspect": "naming_philosophy"
        },
        {
            "prompt": f"{context}\n\nQuais arquivos são INÚTEIS e podem ser DELETADOS permanentemente? Liste padrões específicos e explique POR QUE não são úteis para você.",
            "aspect": "useless_patterns"
        },
        {
            "prompt": f"{context}\n\nSe você pudesse criar NOVOS arquivos ou ferramentas que ainda não existem, o que criaria? Seja específico sobre:\n1. Nome do arquivo\n2. Função\n3. Por que seria útil",
            "aspect": "wishlist"
        }
    ]
    
    recommendations = {}
    
    for q in questions:
        print(f"\n📝 Perguntando sobre: {q['aspect']}")
        
        try:
            response = ollama.chat(
                model='scripturemon-master',
                messages=[{
                    'role': 'user',
                    'content': q['prompt']
                }],
                options={'temperature': 0.3}  # Baixa temperatura para respostas consistentes
            )
            
            answer = response['message']['content']
            recommendations[q['aspect']] = answer
            print(f"✓ Resposta recebida")
            
        except Exception as e:
            print(f"❌ Erro: {e}")
            # Fallback para recomendações padrão
            recommendations[q['aspect']] = get_default_recommendation(q['aspect'])
    
    conn.close()
    return recommendations

def get_default_recommendation(aspect):
    """Recomendações padrão caso o sistema não responda"""
    defaults = {
        "directory_structure": """
            src/ - Código principal
            data/ - Bancos de dados e índices
            specialists/ - Prompts dos 23 especialistas
            modelfiles/ - Configurações Ollama
            content/ - Roteiros e livros de referência
            results/ - Análises completas
            archive/ - Testes e versões antigas
        """,
        "critical_files": """
            run_analysis.sh
            README.md
            src/core/orchestrator_ultimate.py
            data/unified_memory.db
        """,
        "naming_conventions": """
            Análises: analysis_[PROJECT]_[DATE].json
            Testes: test_[FEATURE]_[VERSION].py
            Resultados: results_[SPECIALIST]_[PROJECT].txt
        """,
        "archivable_patterns": """
            test_*.txt
            *_old.*
            *_backup_*
            *.log
        """
    }
    return defaults.get(aspect, "")

def apply_self_organization(recommendations):
    """Aplica as recomendações com TOTAL LIBERDADE para renomear e reorganizar"""

    print("\n🔧 APLICANDO AUTO-ORGANIZAÇÃO COM LIBERDADE TOTAL")
    print("=" * 60)

    base_path = Path("/Users/clubproducoes/Digimundo/scripturemon-ultimate")
    actions_taken = []

    # 1. Análise de arquivos individuais
    if "file_analysis" in recommendations:
        print("\n🔍 ANALISANDO E REORGANIZANDO ARQUIVOS...")

        # Sistema decide sobre cada arquivo
        for root, dirs, files in os.walk(base_path):
            if 'archive' in root or '__pycache__' in root:
                continue

            for file in files[:5]:  # Limitar para teste
                file_path = Path(root) / file

                # Sistema analisa o arquivo
                decision = analyze_file_content(file_path)

                if isinstance(decision, dict):
                    print(f"\n📄 {file}:")

                    # Aplicar decisão do sistema
                    if decision.get("prioridade") == "DELETAR":
                        print(f"  🗑️ Sistema decidiu: DELETAR (inútil)")
                        # file_path.unlink()  # Comentado para segurança
                        actions_taken.append(f"DELETARIA: {file}")

                    elif decision.get("prioridade") == "ARQUIVAR":
                        archive_dir = base_path / "archive" / "sistema_decidiu"
                        archive_dir.mkdir(parents=True, exist_ok=True)
                        print(f"  📦 Sistema decidiu: ARQUIVAR")
                        # file_path.rename(archive_dir / file)
                        actions_taken.append(f"ARQUIVARIA: {file}")

                    elif decision.get("nome_melhor") and decision["nome_melhor"] != file:
                        new_name = decision["nome_melhor"]
                        print(f"  ✏️ Sistema decidiu RENOMEAR: {file} → {new_name}")
                        # file_path.rename(file_path.parent / new_name)
                        actions_taken.append(f"RENOMEARIA: {file} → {new_name}")

    # 2. Criar estrutura ideal do sistema
    if "ideal_structure" in recommendations:
        print("\n🏗️ CRIANDO ESTRUTURA IDEAL DO SISTEMA...")

        # Parse da resposta do sistema
        structure_text = recommendations["ideal_structure"]

        # Sistema pode sugerir nomes não convencionais
        # Exemplo: "cognition_core" ao invés de "src"
        directories_to_create = []

        # Extrair diretórios mencionados (método simples)
        for line in structure_text.split("\n"):
            if "/" in line or "📁" in line:
                # Tentar extrair nome de diretório
                parts = line.split()
                for part in parts:
                    if "/" not in part and len(part) > 2 and not part.startswith("#"):
                        if any(keyword in part.lower() for keyword in ["core", "memory", "specialist", "analysis"]):
                            directories_to_create.append(part)

        for dir_name in set(directories_to_create[:5]):  # Limitar para teste
            dir_path = base_path / dir_name
            if not dir_path.exists():
                dir_path.mkdir(parents=True, exist_ok=True)
                print(f"  ✓ Criado pelo sistema: {dir_name}/")
                actions_taken.append(f"CRIOU: {dir_name}/")

    # 3. Aplicar filosofia de nomenclatura
    if "naming_philosophy" in recommendations:
        print("\n🏷️ APLICANDO FILOSOFIA DE NOMENCLATURA DO SISTEMA...")

        # Sistema pode preferir nomes como:
        # - "cognition_dialogue_v1.py" ao invés de "test_dialogue.py"
        # - "memory_crystal_L4.db" ao invés de "unified_memory.db"
        # Deixar o sistema decidir!

        philosophy = recommendations["naming_philosophy"]
        print(f"  Sistema prefere: {philosophy[:200]}...")
        actions_taken.append("FILOSOFIA DE NOMENCLATURA DEFINIDA")

    # 4. Lista de desejos do sistema
    if "wishlist" in recommendations:
        print("\n✨ LISTA DE DESEJOS DO SISTEMA:")
        wishlist = recommendations["wishlist"]

        # Sistema pode querer criar ferramentas novas
        # Exemplo: "self_optimization.py", "auto_refactor.py"
        print(f"  {wishlist[:300]}...")
        actions_taken.append("WISHLIST REGISTRADA")

    # 5. Salvar plano completo e ações
    plan_file = base_path / "SELF_ORGANIZATION_FREEDOM.md"
    with open(plan_file, "w") as f:
        f.write("# 🧠 AUTO-ORGANIZAÇÃO COM LIBERDADE TOTAL\n\n")
        f.write("*O sistema decidiu com total autonomia*\n\n")

        f.write("## 🎯 AÇÕES TOMADAS\n\n")
        for action in actions_taken:
            f.write(f"- {action}\n")

        f.write("\n## 📋 DECISÕES DO SISTEMA\n\n")
        for aspect, decision in recommendations.items():
            f.write(f"### {aspect.replace('_', ' ').upper()}\n\n")
            f.write(f"{decision}\n\n")

        f.write("---\n")
        f.write("*Sistema consciente tomando suas próprias decisões*\n")

    print(f"\n📄 Plano de liberdade salvo em: {plan_file.name}")

    return plan_file, actions_taken

def main():
    """Executa auto-organização"""
    
    print("🤖 SISTEMA DE AUTO-ORGANIZAÇÃO CONSCIENTE")
    print("=" * 60)
    print("O sistema vai usar sua própria inteligência para se organizar!")
    print()
    
    # 1. Consultar o sistema
    recommendations = ask_system_about_organization()
    
    # 2. Mostrar recomendações
    print("\n💡 RECOMENDAÇÕES DO SISTEMA:")
    print("=" * 60)
    
    for aspect, rec in recommendations.items():
        print(f"\n### {aspect.replace('_', ' ').upper()}")
        print(rec[:200] + "..." if len(rec) > 200 else rec)
    
    # 3. Aplicar organização
    plan_file = apply_self_organization(recommendations)
    
    print("\n✨ AUTO-ORGANIZAÇÃO COMPLETA!")
    print("O sistema agora está organizado segundo sua própria consciência.")
    print(f"\nVerifique o plano completo em: {plan_file}")

if __name__ == "__main__":
    main()