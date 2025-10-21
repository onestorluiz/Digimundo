#!/usr/bin/env python3
"""
TESTE SETORIAL PARA APROVAÇÃO DO SISTEMA
Valida cada setor individualmente antes da correção
"""

import time
import json
from pathlib import Path

class TestadorSetorial:
    """Classe para executar testes setoriais"""

    def __init__(self):
        self.resultados = {}
        self.aprovado = False

    def teste_parser(self):
        """Testa o parser JSON"""
        print("\n🧪 SETOR 1: Parser JSON")
        print("-"*40)

        try:
            from improved_json_parser import robust_json_parse

            casos_teste = [
                ('{"valid": true}', 0.8, "JSON válido"),
                ('```json\n{"test": true}\n```', 0.8, "Markdown"),
                ("{'single': 'quotes'}", 0.5, "Aspas simples"),
                ('{broken', 0.3, "JSON quebrado")
            ]

            sucessos = 0
            for entrada, min_conf, desc in casos_teste:
                result, conf = robust_json_parse(entrada)
                passou = result is not None and conf >= min_conf
                sucessos += passou
                print(f"  {'✅' if passou else '❌'} {desc}: conf={conf:.2f}")

            taxa = sucessos / len(casos_teste) * 100
            self.resultados['parser'] = taxa >= 75
            print(f"\n  Taxa: {taxa:.0f}% - {'APROVADO' if taxa >= 75 else 'REPROVADO'}")
            return self.resultados['parser']

        except Exception as e:
            print(f"  ❌ ERRO: {e}")
            self.resultados['parser'] = False
            return False

    def teste_memoria(self):
        """Testa sistema de memória"""
        print("\n🧪 SETOR 2: Sistema de Memória")
        print("-"*40)

        try:
            from rag_integration import SimpleRAG

            rag = SimpleRAG()
            stats = rag.get_stats()
            total = stats.get('total_memories', 0)

            print(f"  📊 Memórias: {total}")

            # Teste de salvamento
            test_id = f"setor_test_{int(time.time())}"
            success = rag.save_analysis(
                f'{{"test": "{test_id}"}}',
                {'type': 'test'},
                0.95
            )

            # Teste de busca
            results = rag.search_similar(test_id, limit=1)
            found = len(results) > 0 and test_id in str(results[0])

            print(f"  {'✅' if success else '❌'} Salvamento")
            print(f"  {'✅' if found else '❌'} Recuperação")

            self.resultados['memoria'] = success and found
            print(f"\n  {'APROVADO' if self.resultados['memoria'] else 'REPROVADO'}")
            return self.resultados['memoria']

        except Exception as e:
            print(f"  ❌ ERRO: {e}")
            self.resultados['memoria'] = False
            return False

    def teste_ollama(self):
        """Testa conexão com Ollama"""
        print("\n🧪 SETOR 3: Modelo Ollama")
        print("-"*40)

        try:
            import subprocess

            # Verificar se modelo existe
            result = subprocess.run(
                ["ollama", "list"],
                capture_output=True,
                text=True,
                timeout=5
            )

            tem_modelo = "scripturemon-v9-final" in result.stdout
            print(f"  {'✅' if tem_modelo else '❌'} Modelo disponível")

            if tem_modelo:
                # Teste rápido
                start = time.time()
                result = subprocess.run(
                    ["ollama", "run", "scripturemon-v9-final", "Hi"],
                    capture_output=True,
                    text=True,
                    timeout=30
                )
                tempo = time.time() - start

                respondeu = len(result.stdout) > 0
                print(f"  {'✅' if respondeu else '❌'} Resposta em {tempo:.1f}s")

                self.resultados['ollama'] = tem_modelo and respondeu
            else:
                self.resultados['ollama'] = False

            print(f"\n  {'APROVADO' if self.resultados['ollama'] else 'REPROVADO'}")
            return self.resultados['ollama']

        except Exception as e:
            print(f"  ❌ ERRO: {e}")
            self.resultados['ollama'] = False
            return False

    def teste_knowledge_packs(self):
        """Testa knowledge packs"""
        print("\n🧪 SETOR 4: Knowledge Packs")
        print("-"*40)

        pack_dir = Path('knowledge_packs')

        # Verificar diretório
        if pack_dir.exists():
            packs = list(pack_dir.glob('*.txt'))
            print(f"  📚 {len(packs)} packs encontrados")

            if packs:
                for pack in packs[:3]:
                    size = pack.stat().st_size
                    print(f"    • {pack.name} ({size} bytes)")
                self.resultados['knowledge'] = True
            else:
                print(f"  ⚠️ Diretório vazio")
                self.resultados['knowledge'] = False
        else:
            print(f"  ❌ Diretório não existe")
            self.resultados['knowledge'] = False

        print(f"\n  {'APROVADO' if self.resultados['knowledge'] else 'REPROVADO'}")
        return self.resultados['knowledge']

    def teste_integracao(self):
        """Testa integração completa"""
        print("\n🧪 SETOR 5: Integração Completa")
        print("-"*40)

        try:
            from ollama_with_memory import OllamaWithMemory

            analyzer = OllamaWithMemory(debug=False)

            # Verificar componentes
            tem_rag = analyzer.rag is not None
            tem_ollama = analyzer.check_ollama()

            print(f"  {'✅' if tem_rag else '❌'} RAG conectado")
            print(f"  {'✅' if tem_ollama else '❌'} Ollama conectado")

            if tem_rag and tem_ollama:
                # Teste rápido
                test_text = "Test screenplay: Hero saves the day."
                start = time.time()
                result = analyzer.analyze_simple(test_text)
                tempo = time.time() - start

                funcionou = 'error' not in result
                print(f"  {'✅' if funcionou else '❌'} Análise em {tempo:.1f}s")

                self.resultados['integracao'] = funcionou and tempo < 30
            else:
                self.resultados['integracao'] = False

            print(f"\n  {'APROVADO' if self.resultados['integracao'] else 'REPROVADO'}")
            return self.resultados['integracao']

        except Exception as e:
            print(f"  ❌ ERRO: {e}")
            self.resultados['integracao'] = False
            return False

    def executar_todos_testes(self):
        """Executa todos os testes setoriais"""
        print("\n" + "="*50)
        print("🎯 TESTES SETORIAIS DE APROVAÇÃO")
        print("="*50)

        # Executar cada setor
        self.teste_parser()
        self.teste_memoria()
        self.teste_ollama()
        self.teste_knowledge_packs()
        self.teste_integracao()

        # Calcular aprovação
        print("\n" + "="*50)
        print("📊 RESULTADO FINAL")
        print("="*50)

        total_setores = len(self.resultados)
        setores_aprovados = sum(1 for v in self.resultados.values() if v)

        print(f"\nSetores testados: {total_setores}")
        print(f"Setores aprovados: {setores_aprovados}")

        for setor, aprovado in self.resultados.items():
            status = "✅ PASSOU" if aprovado else "❌ FALHOU"
            print(f"  {setor}: {status}")

        taxa_aprovacao = (setores_aprovados / total_setores * 100) if total_setores > 0 else 0

        print(f"\nTaxa de aprovação: {taxa_aprovacao:.0f}%")

        # Critério: >= 80% para aprovar
        self.aprovado = taxa_aprovacao >= 80

        if self.aprovado:
            print("\n🎉 SISTEMA APROVADO PARA CORREÇÕES!")
            print("Proceda com o plano de correção.")
        else:
            print("\n❌ SISTEMA REPROVADO")
            print(f"Necessário aprovar {4 - setores_aprovados} setores adicionais")

        return self.aprovado

def main():
    """Função principal"""
    testador = TestadorSetorial()
    aprovado = testador.executar_todos_testes()

    # Salvar relatório
    relatorio = {
        'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
        'resultados': testador.resultados,
        'aprovado': aprovado
    }

    with open('relatorio_setorial.json', 'w') as f:
        json.dump(relatorio, f, indent=2)

    print("\n💾 Relatório salvo em relatorio_setorial.json")
    print("\n🥷 DIGIMUNDO PRESENTE")

    return 0 if aprovado else 1

if __name__ == "__main__":
    exit(main())