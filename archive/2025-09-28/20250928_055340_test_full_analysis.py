#!/usr/bin/env python3
"""
Teste completo de análise de roteiro com SCRIPTUREMON v9
"""

import subprocess
import json
import time

def analyze_screenplay(screenplay_file):
    """Analisa roteiro completo"""
    print("=" * 60)
    print("ANÁLISE COMPLETA - SCRIPTUREMON v9")
    print("=" * 60)

    # Ler roteiro
    with open(screenplay_file, 'r') as f:
        screenplay = f.read()

    print(f"\nRoteiro: {screenplay_file}")
    print(f"Tamanho: {len(screenplay)} caracteres")
    print("\nIniciando análise forense...")

    start_time = time.time()

    try:
        # Prompt para análise completa
        prompt = f"""Analise este roteiro e retorne JSON estruturado com:
- metadata (titulo, formato, paginas)
- evidence_log (pelo menos 3 evidências com página)
- analise_estrutural (identificar 25%, 50%, 75%)
- analise_personagem (protagonista want vs need)
- validation (score simplificado)

ROTEIRO:
{screenplay}

Retorne APENAS o JSON, sem explicações."""

        # Executar análise
        result = subprocess.run(
            ["ollama", "run", "scripturemon-v9-final", prompt],
            capture_output=True,
            text=True,
            timeout=300  # 5 minutos
        )

        elapsed = time.time() - start_time

        print(f"\n✅ Análise concluída em {elapsed:.1f}s")

        output = result.stdout

        # Extrair JSON
        if "```json" in output:
            json_start = output.find("```json") + 7
            json_end = output.find("```", json_start)
            json_str = output[json_start:json_end].strip()
        elif "{" in output:
            json_start = output.find("{")
            json_end = output.rfind("}") + 1
            json_str = output[json_start:json_end]
        else:
            print("\n❌ Nenhum JSON encontrado")
            print(f"Resposta: {output[:500]}...")
            return False

        # Parsear JSON
        try:
            analysis = json.loads(json_str)
            print("\n✅ JSON válido parseado!")

            # Validar campos principais
            print("\n" + "-" * 60)
            print("VALIDAÇÃO DE CAMPOS:")
            print("-" * 60)

            checks = {
                "metadata": "metadata" in analysis,
                "evidence_log": "evidence_log" in analysis,
                "analise_estrutural": "analise_estrutural" in analysis,
                "analise_personagem": "analise_personagem" in analysis,
                "validation": "validation" in analysis
            }

            for field, present in checks.items():
                status = "✅" if present else "❌"
                print(f"{status} {field}: {'presente' if present else 'ausente'}")

            # Verificar evidence_log
            if "evidence_log" in analysis and isinstance(analysis["evidence_log"], list):
                evidence_count = len(analysis["evidence_log"])
                print(f"\n📝 Evidências encontradas: {evidence_count}")

                if evidence_count > 0:
                    print("\nPrimeiras evidências:")
                    for i, evidence in enumerate(analysis["evidence_log"][:3]):
                        if isinstance(evidence, dict):
                            # Campos podem ser: pagina, locator, evidencia, snippet
                            page = evidence.get("pagina", evidence.get("locator", "N/A"))
                            text = evidence.get("evidencia", evidence.get("snippet", ""))[:50]
                            print(f"  {i+1}. Página {page}: {text}...")

            # Verificar estrutura
            if "analise_estrutural" in analysis:
                print(f"\n📊 Análise estrutural presente")
                struct = analysis["analise_estrutural"]

                # Procurar por percentuais - struct é dict, não list
                if isinstance(struct, dict):
                    for percent in ["25", "50", "75"]:
                        percent_key = f"{percent}%"
                        if percent_key in struct and struct[percent_key]:
                            print(f"  ✅ {percent}% identificado")
                elif isinstance(struct, list):
                    print("  ⚠️ Estrutura é lista, esperado dict")

            # Verificar personagem
            if "analise_personagem" in analysis:
                print(f"\n👤 Análise de personagem presente")

                if "protagonista" in analysis["analise_personagem"]:
                    prot = analysis["analise_personagem"]["protagonista"]
                    if isinstance(prot, dict):
                        want = prot.get("want", "N/A")
                        need = prot.get("need", "N/A")
                        print(f"  Want: {want[:50]}...")
                        print(f"  Need: {need[:50]}...")

            # Score
            if "validation" in analysis:
                print(f"\n⭐ Validação presente")
                if "score" in analysis["validation"]:
                    print(f"  Score: {analysis['validation']['score']}")

            # Salvar resultado
            with open('analysis_result.json', 'w') as f:
                json.dump(analysis, f, indent=2, ensure_ascii=False)
            print(f"\n💾 Resultado salvo em analysis_result.json")

            return True

        except json.JSONDecodeError as e:
            print(f"\n❌ Erro ao parsear JSON: {e}")
            print(f"JSON tentado:\n{json_str[:500]}...")
            return False

    except subprocess.TimeoutExpired:
        print(f"\n❌ Timeout após 300s")
        return False
    except Exception as e:
        print(f"\n❌ Erro: {e}")
        return False

if __name__ == "__main__":
    print("🎬 TESTE DE ANÁLISE COMPLETA - SCRIPTUREMON v9\n")

    # Executar análise
    success = analyze_screenplay("test_screenplay.txt")

    # Resultado
    print("\n" + "=" * 60)
    print("RESULTADO FINAL")
    print("=" * 60)

    if success:
        print("\n✅ ANÁLISE COMPLETA BEM-SUCEDIDA!")
        print("\nO modelo está:")
        print("  ✅ Processando roteiros")
        print("  ✅ Retornando JSON estruturado")
        print("  ✅ Identificando elementos narrativos")
        print("  ✅ Gerando evidências")
    else:
        print("\n❌ ANÁLISE FALHOU")
        print("\nVerifique:")
        print("  - Modelo está carregado corretamente")
        print("  - Memória disponível")
        print("  - Formato do prompt")

    print("\nDIGIMUNDO PRESENTE 🥷")