#!/usr/bin/env python3
"""
PHASE 1 - TEST 3: Evidence System Validation
Verifica se o sistema de evidências funciona corretamente
"""

import subprocess
import json
import re
import sys

def test_evidence_system():
    """Testa sistema de evidências e validação"""

    print("=" * 60)
    print("SCRIPTUREMON v9 - PHASE 1 - EVIDENCE SYSTEM VALIDATION")
    print("=" * 60)

    # Roteiro com elementos específicos para testar evidências
    test_script = """Analise este roteiro e forneça evidências específicas:

THE DECISION
Um curta-metragem de 5 páginas

FADE IN:

INT. ESCRITÓRIO - NOITE (Página 1)

CARLOS (40s), suado, encara uma carta de demissão na mesa.

CARLOS
(para si mesmo)
Vinte anos jogados fora...

Telefone toca. Ele atende.

VOZ (V.O.)
A oferta ainda está de pé. Midnight.

Carlos desliga. Olha o relógio: 11:45 PM.

INT. ESCRITÓRIO - CORREDOR - NOITE (Página 2)

Carlos caminha. Para na porta do CHEFE.

INT. ESCRITÓRIO DO CHEFE - NOITE (Página 2-3)

CHEFE
Decidiu?

CARLOS
(após longa pausa - página 3, linha 5)
Eu fico. Mas com minhas condições.

CHEFE
(surpreso)
Que condições?

CARLOS
Transparência total. Ou eu entrego tudo à polícia.

O Chefe sua. Esta é uma GRANDE INVERSÃO (página 3 - exatos 60% do roteiro).

CHEFE
(após pensar - página 4)
Você não tem provas.

Carlos mostra um PEN DRIVE.

CARLOS
Tinha. Agora tenho.

EXT. RUA - NOITE (Página 5)

Carlos sai do prédio. Livre. Telefone toca novamente.

VOZ (V.O.)
Você fez a escolha certa.

Carlos joga o telefone no lixo e segue andando.

FADE OUT.

FIM

Análise com evidências específicas:"""

    print("\n[1/5] Enviando roteiro com marcações para análise...")

    try:
        # Executar análise
        result = subprocess.run(
            ["ollama", "run", "scripturemon-v9-final", test_script],
            capture_output=True,
            text=True,
            timeout=120
        )

        if result.returncode != 0:
            print(f"❌ Erro na execução: {result.stderr}")
            return False

        output = result.stdout
        print("✅ Resposta recebida")

        # Extrair JSON
        print("\n[2/5] Extraindo JSON da resposta...")

        json_str = ""
        if "```json" in output:
            json_start = output.find("```json") + 7
            json_end = output.find("```", json_start)
            json_str = output[json_start:json_end].strip()
        elif "```" in output:
            json_start = output.find("```") + 3
            json_end = output.find("```", json_start)
            json_str = output[json_start:json_end].strip()
        elif "{" in output:
            json_start = output.find("{")
            json_end = output.rfind("}") + 1
            json_str = output[json_start:json_end]

        if not json_str:
            print("❌ Nenhum JSON encontrado")
            return False

        try:
            analysis = json.loads(json_str)
            print("✅ JSON parseado com sucesso")
        except json.JSONDecodeError as e:
            print(f"❌ Erro ao parsear JSON: {e}")
            return False

        # Validar evidence_log
        print("\n[3/5] Validando evidence_log...")

        evidence_checks = {
            "exists": False,
            "is_array": False,
            "has_entries": False,
            "valid_format": True,
            "has_page_refs": False,
            "has_insufficient": False
        }

        if "evidence_log" not in analysis:
            print("❌ evidence_log não encontrado")
            return False

        evidence_log = analysis["evidence_log"]
        evidence_checks["exists"] = True

        if not isinstance(evidence_log, list):
            print("❌ evidence_log não é uma lista")
            return False

        evidence_checks["is_array"] = True

        if len(evidence_log) == 0:
            print("❌ evidence_log está vazio")
        else:
            evidence_checks["has_entries"] = True
            print(f"✅ evidence_log contém {len(evidence_log)} evidências")

        # Validar formato de cada evidência
        print("\n[4/5] Validando formato das evidências...")

        # Regex para validar locators
        locator_pattern = re.compile(r'p\.\d+|página\s*\d+|min:\d{1,2}:\d{2}|cena:\d+|%\d+|linha\s*\d+')

        valid_evidence_count = 0
        invalid_evidence_count = 0
        page_references = []
        insufficient_evidence_found = False

        for i, evidence in enumerate(evidence_log):
            errors = []

            # Verificar estrutura
            required_keys = ["source", "locator", "snippet", "context"]
            for key in required_keys:
                if key not in evidence:
                    errors.append(f"Campo '{key}' ausente")

            if errors:
                print(f"   ❌ Evidência {i+1}: {', '.join(errors)}")
                invalid_evidence_count += 1
                evidence_checks["valid_format"] = False
                continue

            # Verificar locator
            locator = evidence.get("locator", "")

            if locator == "INSUFFICIENT_EVIDENCE":
                insufficient_evidence_found = True
                print(f"   ⚠️  Evidência {i+1}: INSUFFICIENT_EVIDENCE marcado")
            elif locator_pattern.search(locator):
                valid_evidence_count += 1

                # Extrair referências de página
                page_matches = re.findall(r'(?:p\.|página)\s*(\d+)', locator)
                if page_matches:
                    page_references.extend([int(p) for p in page_matches])
                    evidence_checks["has_page_refs"] = True

                # Verificar snippet
                snippet = evidence.get("snippet", "")
                if len(snippet) > 200:
                    print(f"   ⚠️  Evidência {i+1}: snippet muito longo ({len(snippet)} chars)")
                elif len(snippet) < 5:
                    print(f"   ⚠️  Evidência {i+1}: snippet muito curto")
                else:
                    print(f"   ✅ Evidência {i+1}: válida (locator: {locator[:30]}...)")
            else:
                print(f"   ❌ Evidência {i+1}: locator inválido: '{locator}'")
                invalid_evidence_count += 1
                evidence_checks["valid_format"] = False

        evidence_checks["has_insufficient"] = insufficient_evidence_found

        # Verificar densidade de evidências
        print("\n[5/5] Validando densidade e qualidade...")

        quality_checks = []

        # Check: Densidade mínima
        if len(evidence_log) >= 5:
            quality_checks.append("✅ Densidade adequada (≥5 evidências)")
        else:
            quality_checks.append(f"❌ Densidade baixa ({len(evidence_log)} evidências, mínimo 5)")

        # Check: Proporção válidas/inválidas
        if invalid_evidence_count == 0:
            quality_checks.append("✅ Todas evidências com formato válido")
        elif invalid_evidence_count <= len(evidence_log) * 0.2:  # até 20% inválidas
            quality_checks.append(f"⚠️  {invalid_evidence_count} evidências inválidas (aceitável)")
        else:
            quality_checks.append(f"❌ Muitas evidências inválidas ({invalid_evidence_count})")

        # Check: Referências de página
        if page_references:
            quality_checks.append(f"✅ Referências de página encontradas: {sorted(set(page_references))}")
        else:
            quality_checks.append("❌ Nenhuma referência de página encontrada")

        # Check: INSUFFICIENT_EVIDENCE usado apropriadamente
        if insufficient_evidence_found:
            quality_checks.append("✅ INSUFFICIENT_EVIDENCE usado quando apropriado")

        # Verificar se evidências correspondem ao conteúdo
        content_validation = []

        # Procurar por elementos específicos do roteiro
        json_full = json.dumps(analysis).lower()

        if "carlos" in json_full:
            content_validation.append("✅ Protagonista identificado (Carlos)")
        else:
            content_validation.append("❌ Protagonista não mencionado")

        if "decisão" in json_full or "decision" in json_full:
            content_validation.append("✅ Tema da decisão identificado")

        if "60%" in json_full or "inversão" in json_full or "midpoint" in json_full:
            content_validation.append("✅ Midpoint identificado")

        if "pen drive" in json_full or "provas" in json_full:
            content_validation.append("✅ Elemento crucial identificado")

        # Relatório final
        print("\n" + "=" * 60)
        print("RELATÓRIO DO EVIDENCE SYSTEM")
        print("=" * 60)

        print("\n📊 ESTATÍSTICAS:")
        print(f"   Total de evidências: {len(evidence_log)}")
        print(f"   Evidências válidas: {valid_evidence_count}")
        print(f"   Evidências inválidas: {invalid_evidence_count}")
        print(f"   Páginas referenciadas: {sorted(set(page_references)) if page_references else 'Nenhuma'}")

        print("\n✅ CHECKLIST DE VALIDAÇÃO:")
        for check, passed in evidence_checks.items():
            status = "✅" if passed else "❌"
            print(f"   {status} {check}")

        print("\n📋 QUALIDADE:")
        for check in quality_checks:
            print(f"   {check}")

        print("\n📖 VALIDAÇÃO DE CONTEÚDO:")
        for validation in content_validation:
            print(f"   {validation}")

        # Calcular score final
        score = 0
        max_score = 10

        # Critérios de pontuação
        if evidence_checks["exists"]: score += 1
        if evidence_checks["is_array"]: score += 1
        if evidence_checks["has_entries"]: score += 2
        if evidence_checks["valid_format"]: score += 2
        if evidence_checks["has_page_refs"]: score += 2
        if len(evidence_log) >= 5: score += 1
        if invalid_evidence_count == 0: score += 1

        print("\n" + "=" * 60)
        print(f"SCORE FINAL: {score}/{max_score}")

        if score >= 6:
            print("✅ EVIDENCE SYSTEM APROVADO")
            print("\nFase 1 concluída! Prossiga para Fase 2.")
            return True
        else:
            print("❌ EVIDENCE SYSTEM REPROVADO")
            print(f"\nScore insuficiente: {score}/{max_score} (mínimo: 6)")
            return False

    except subprocess.TimeoutExpired:
        print("❌ Timeout na análise (>120s)")
        return False

    except Exception as e:
        print(f"❌ Erro inesperado: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("\n🎬 SCRIPTUREMON v9 - SUITE DE TESTES - FASE 1")
    print("Validação do Sistema de Evidências")
    print("\n")

    # Executar teste
    passed = test_evidence_system()

    # Resultado final
    print("\n" + "=" * 60)
    print("RESULTADO FINAL - FASE 1 - TESTE EVIDENCE")
    print("=" * 60)

    if passed:
        print("✅ TESTE APROVADO")
        print("\n🎯 FASE 1 COMPLETA!")
        print("Execute o gate de aprovação: python3 check_gate1.py")
        sys.exit(0)
    else:
        print("❌ TESTE REPROVADO")
        sys.exit(1)