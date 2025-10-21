#!/usr/bin/env python3
"""
SCRIPTUREMON SELF-ORGANIZE - SISTEMA AUTÔNOMO DE ORGANIZAÇÃO
Ensina o Scripturemon a organizar sua própria casa usando sua inteligência
"""

import os
import sys
import json
import shutil
from pathlib import Path
from datetime import datetime
import ollama

class ScripturemonSelfOrganizer:
    def __init__(self):
        self.base_path = Path("/Users/clubproducoes/Digimundo/scripturemon-ultimate")
        self.model = "scripturemon-professional"

    def parse_text_response(self, text):
        """Tenta criar decisões a partir da resposta em texto"""
        decisions = {"decisions": []}

        # Lista de padrões para diferentes tipos de arquivos
        file_patterns = {
            r'\.py$': 'scripts/analysis/',  # Scripts Python
            r'\.log$': 'outputs/logs/',  # Logs
            r'\.json$': 'archive/reports/',  # Relatórios JSON
            r'^test_': 'tests/',  # Arquivos de teste
            r'\.md$': 'docs/',  # Documentação (exceto README)
            r'\.sh$': 'scripts/maintenance/',  # Shell scripts
        }

        # Arquivos que devem ficar na raiz
        keep_in_root = ['README.md', 'setup.py', '.gitignore', '.git']

        # Analisar arquivos na raiz
        for item in self.base_path.iterdir():
            if item.is_file():
                file_name = item.name

                # Verificar se deve manter na raiz
                if file_name in keep_in_root:
                    decisions["decisions"].append({
                        "file": file_name,
                        "action": "keep",
                        "reason": "Arquivo essencial da raiz"
                    })
                    continue

                # Verificar padrões para mover
                moved = False
                for pattern, destination in file_patterns.items():
                    import re
                    if re.search(pattern, file_name):
                        # Tratamento especial para README.md
                        if file_name == 'README.md':
                            decisions["decisions"].append({
                                "file": file_name,
                                "action": "keep",
                                "reason": "README principal do projeto"
                            })
                        else:
                            decisions["decisions"].append({
                                "file": file_name,
                                "action": "move",
                                "destination": destination,
                                "reason": f"Organização por tipo: {pattern}"
                            })
                        moved = True
                        break

                # Se não encontrou padrão, move para archive
                if not moved:
                    decisions["decisions"].append({
                        "file": file_name,
                        "action": "move",
                        "destination": "archive/",
                        "reason": "Arquivo sem categoria específica"
                    })

        return decisions if decisions["decisions"] else None

    def analyze_and_decide(self):
        """Pede ao Scripturemon para analisar e decidir sobre organização"""

        # Lista todos os arquivos na raiz
        root_files = []
        for item in self.base_path.iterdir():
            if item.is_file():
                root_files.append(item.name)

        prompt = f"""
        Você é o Scripturemon, o especialista em roteiros e organização de sistemas.

        Analise os arquivos em sua pasta raiz e decida onde cada um deveria estar:

        ARQUIVOS NA RAIZ:
        {json.dumps(root_files, indent=2)}

        ESTRUTURA DISPONÍVEL:
        - scripts/ (para scripts Python de análise, testes, etc)
        - scripts/analysis/ (scripts de análise específicos)
        - scripts/maintenance/ (scripts de manutenção)
        - archive/ (arquivos históricos)
        - archive/reports/ (relatórios antigos)
        - outputs/ (saídas do sistema)
        - outputs/logs/ (arquivos de log)
        - docs/ (documentação)
        - config/ (arquivos de configuração)
        - tests/ (arquivos de teste)
        - data/ (dados do sistema)
        - src/ (código fonte principal)

        REGRAS:
        1. Na raiz devem ficar APENAS: README.md, setup.py, .gitignore
        2. Scripts Python (.py) devem ir para scripts/ ou subpastas apropriadas
        3. Logs (.log) devem ir para outputs/logs/
        4. Relatórios JSON devem ir para archive/reports/
        5. Documentação (.md) deve ir para docs/
        6. Arquivos de teste devem ir para tests/

        Para cada arquivo, responda EXATAMENTE neste formato JSON:
        {{
            "decisions": [
                {{
                    "file": "nome_do_arquivo.ext",
                    "action": "move|keep|delete",
                    "destination": "pasta/destino/" (se action=move),
                    "reason": "explicação breve"
                }}
            ]
        }}

        Seja decisivo e organize TUDO que não deveria estar na raiz.
        """

        try:
            response = ollama.generate(
                model=self.model,
                prompt=prompt,
                stream=False
            )

            # Extrair JSON da resposta
            text = response['response']
            print(f"\nResposta do Scripturemon:\n{text[:500]}...")  # Debug

            # Tentar encontrar JSON na resposta
            import re
            # Procurar por estrutura JSON mais específica
            json_patterns = [
                r'\{[^{}]*"decisions"[^{}]*:\s*\[[^\]]*\][^{}]*\}',  # JSON simples
                r'\{.*?"decisions".*?\}',  # JSON com decisions
                r'\{.*\}',  # Qualquer JSON
            ]

            for pattern in json_patterns:
                json_match = re.search(pattern, text, re.DOTALL)
                if json_match:
                    try:
                        # Limpar o JSON
                        json_str = json_match.group()
                        # Remover possíveis comentários ou texto extra
                        json_str = re.sub(r'//.*?\n', '', json_str)  # Remove comentários //
                        json_str = re.sub(r'/\*.*?\*/', '', json_str, re.DOTALL)  # Remove /* */

                        decisions = json.loads(json_str)
                        if 'decisions' in decisions:
                            return decisions
                    except json.JSONDecodeError as e:
                        print(f"⚠️ Erro ao decodificar JSON: {e}")
                        continue

            print("⚠️ Scripturemon não retornou JSON válido")
            # Tentar criar decisões manualmente baseado na resposta
            return self.parse_text_response(text)

        except Exception as e:
            print(f"❌ Erro ao consultar Scripturemon: {e}")
            return None

    def execute_decisions(self, decisions):
        """Executa as decisões do Scripturemon"""
        if not decisions or 'decisions' not in decisions:
            return False

        results = {
            'moved': [],
            'kept': [],
            'deleted': [],
            'errors': []
        }

        for decision in decisions['decisions']:
            file_path = self.base_path / decision['file']

            if not file_path.exists():
                results['errors'].append(f"Arquivo não encontrado: {decision['file']}")
                continue

            try:
                if decision['action'] == 'move':
                    dest_dir = self.base_path / decision['destination']
                    dest_dir.mkdir(parents=True, exist_ok=True)
                    dest_path = dest_dir / decision['file']
                    shutil.move(str(file_path), str(dest_path))
                    results['moved'].append({
                        'file': decision['file'],
                        'to': decision['destination'],
                        'reason': decision.get('reason', '')
                    })
                    print(f"✓ Movido: {decision['file']} → {decision['destination']}")

                elif decision['action'] == 'keep':
                    results['kept'].append({
                        'file': decision['file'],
                        'reason': decision.get('reason', '')
                    })
                    print(f"○ Mantido: {decision['file']}")

                elif decision['action'] == 'delete':
                    # Move para lixeira ao invés de deletar
                    trash_dir = self.base_path / 'trash' / datetime.now().strftime("%Y%m%d_%H%M%S")
                    trash_dir.mkdir(parents=True, exist_ok=True)
                    trash_path = trash_dir / decision['file']
                    shutil.move(str(file_path), str(trash_path))
                    results['deleted'].append({
                        'file': decision['file'],
                        'reason': decision.get('reason', '')
                    })
                    print(f"× Deletado: {decision['file']} (movido para lixeira)")

            except Exception as e:
                results['errors'].append(f"Erro ao processar {decision['file']}: {str(e)}")
                print(f"❌ Erro: {decision['file']} - {e}")

        return results

    def generate_report(self, decisions, results):
        """Gera relatório da organização"""
        report = {
            'timestamp': datetime.now().isoformat(),
            'model': self.model,
            'decisions_made': len(decisions['decisions']) if decisions else 0,
            'execution_results': results,
            'summary': {
                'files_moved': len(results['moved']) if results else 0,
                'files_kept': len(results['kept']) if results else 0,
                'files_deleted': len(results['deleted']) if results else 0,
                'errors': len(results['errors']) if results else 0
            }
        }

        report_path = self.base_path / 'archive' / 'reports' / f'self_organization_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'
        report_path.parent.mkdir(parents=True, exist_ok=True)

        with open(report_path, 'w') as f:
            json.dump(report, f, indent=2)

        return report

def main():
    print("🤖 SCRIPTUREMON SELF-ORGANIZE")
    print("Sistema autônomo de organização")
    print("=" * 60)

    organizer = ScripturemonSelfOrganizer()

    # 1. Pedir ao Scripturemon para analisar e decidir
    print("\n📊 Consultando Scripturemon para análise...")
    decisions = organizer.analyze_and_decide()

    if not decisions:
        print("❌ Não foi possível obter decisões do Scripturemon")
        return

    # 2. Mostrar decisões
    print(f"\n📋 Scripturemon tomou {len(decisions['decisions'])} decisões:")
    for d in decisions['decisions'][:5]:  # Mostrar primeiras 5
        print(f"   • {d['file']}: {d['action']} → {d.get('destination', 'N/A')}")

    # 3. Executar decisões
    print("\n🔧 Executando organização...")
    results = organizer.execute_decisions(decisions)

    # 4. Gerar relatório
    print("\n📄 Gerando relatório...")
    report = organizer.generate_report(decisions, results)

    # 5. Resumo
    print("\n✅ ORGANIZAÇÃO COMPLETA!")
    print(f"   • Arquivos movidos: {report['summary']['files_moved']}")
    print(f"   • Arquivos mantidos: {report['summary']['files_kept']}")
    print(f"   • Arquivos deletados: {report['summary']['files_deleted']}")
    if report['summary']['errors'] > 0:
        print(f"   • Erros: {report['summary']['errors']}")

    print("\n💡 Scripturemon organizou sua própria casa com sucesso!")

    return report

if __name__ == "__main__":
    main()