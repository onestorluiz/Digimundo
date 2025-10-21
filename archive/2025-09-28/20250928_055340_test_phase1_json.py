#!/usr/bin/env python3
"""
PHASE 1 - TEST 2: JSON Output Validation
Verifica se o modelo produz output JSON estruturado corretamente
"""

import subprocess
import json
import sys

def test_json_output():
    """Testa output JSON com roteiro mínimo"""

    print("=" * 60)
    print("SCRIPTUREMON v9 - PHASE 1 - JSON OUTPUT VALIDATION")
    print("=" * 60)

    # Roteiro mínimo para teste
    test_script = """Analise este roteiro curto e retorne JSON estruturado:

FADE IN:

INT. CASA - DIA

João entra nervoso na sala. Suas mãos tremem.

JOÃO
Preciso sair daqui agora.

Maria bloqueia a porta com determinação.

MARIA
Não até conversarmos sobre ontem.

João tenta passar. Maria não cede.

JOÃO
(gritando)
Você não entende!

MARIA
(calma)
Então me explique.

João para. Olha nos olhos dela. Sua raiva derrete em lágrimas.

JOÃO
Eu... eu tenho medo de te perder.

Maria se aproxima e o abraça.

MARIA
Você nunca vai me perder.

FADE OUT.

Análise completa em JSON:"""

    print("\n[1/4] Enviando roteiro para análise...")

    try:
        # Executar análise
        result = subprocess.run(
            ["ollama", "run", "scripturemon-v9-final", test_script],
            capture_output=True,
            text=True,
            timeout=120  # 2 minutos máximo
        )

        if result.returncode != 0:
            print(f"❌ Erro na execução: {result.stderr}")
            return False

        output = result.stdout
        print("✅ Resposta recebida")

        # Extrair JSON da resposta
        print("\n[2/4] Extraindo JSON da resposta...")

        # Procurar por JSON entre ```
        if "```json" in output:
            json_start = output.find("```json") + 7
            json_end = output.find("```", json_start)
            json_str = output[json_start:json_end].strip()
        elif "```" in output:
            json_start = output.find("```") + 3
            json_end = output.find("```", json_start)
            json_str = output[json_start:json_end].strip()
        elif "{" in output:
            # Tentar extrair JSON diretamente
            json_start = output.find("{")
            json_end = output.rfind("}") + 1
            json_str = output[json_start:json_end]
        else:
            print("❌ Nenhum JSON encontrado na resposta")
            print(f"Resposta recebida:\n{output[:500]}...")
            return False

        # Validar JSON
        print("\n[3/4] Validando estrutura JSON...")

        try:
            analysis = json.loads(json_str)
            print("✅ JSON válido e parseável")
        except json.JSONDecodeError as e:
            print(f"❌ JSON inválido: {e}")
            print(f"JSON recebido:\n{json_str[:500]}...")
            return False

        # Verificar campos obrigatórios
        print("\n[4/4] Verificando campos obrigatórios...")

        required_fields = {
            "metadata": ["titulo", "formato", "duracao_minutos", "total_paginas"],
            "evidence_log": [],  # Array
            "convergencias_universais": ["detectadas", "percentuais_estruturais"],
            "analise_estrutural": ["beats_snyder_completos"],
            "analise_personagem": ["protagonista", "unity_of_opposites"],
            "analise_conflito": ["tipo_egri", "progressao_validada"],
            "analise_tematica": ["premissa_egri", "controlling_idea_mckee"],
            "analise_execucao": ["dialogos", "cenas"],
            "validation": ["score_9d", "qgates_status", "verdict"],
            "synthesis": ["convergencias_atingidas", "score_final"]
        }

        missing_fields = []
        present_fields = []

        for field, subfields in required_fields.items():
            if field not in analysis:
                missing_fields.append(f"❌ Campo ausente: {field}")
            else:
                present_fields.append(f"✅ {field}")

                # Verificar subcampos se existirem
                if subfields and isinstance(analysis[field], dict):
                    for subfield in subfields:
                        if subfield not in analysis[field]:
                            missing_fields.append(f"❌ Subcampo ausente: {field}.{subfield}")

        # Validações específicas
        validation_errors = []

        # Verificar evidence_log
        if "evidence_log" in analysis:
            if not isinstance(analysis["evidence_log"], list):
                validation_errors.append("❌ evidence_log deve ser array")
            elif len(analysis["evidence_log"]) < 1:
                validation_errors.append("⚠️  evidence_log vazio (esperado ≥1 evidência)")
            else:
                present_fields.append(f"✅ evidence_log com {len(analysis['evidence_log'])} evidências")

        # Verificar score 9D
        if "validation" in analysis and "score_9d" in analysis["validation"]:
            score = analysis["validation"]["score_9d"]
            if "total" in score:
                total = score["total"]
                if 0 <= total <= 45:
                    present_fields.append(f"✅ Score 9D: {total}/45")
                else:
                    validation_errors.append(f"❌ Score fora do range: {total}/45")

                # Verificar dimensões
                dimensions = [
                    "structure_value_turn",
                    "controlling_idea_link",
                    "dialogue_subtext_action",
                    "character_truth_pressure",
                    "evidence_specificity",
                    "causalidade_narrativa",
                    "economia_de_cena",
                    "contrato_de_genero",
                    "ritmo_e_momentum"
                ]

                for dim in dimensions:
                    if dim not in score:
                        validation_errors.append(f"❌ Dimensão ausente: {dim}")

        # Verificar convergências
        if "convergencias_universais" in analysis:
            conv = analysis["convergencias_universais"]
            if "detectadas" in conv and isinstance(conv["detectadas"], list):
                num_conv = len(conv["detectadas"])
                if num_conv > 0:
                    present_fields.append(f"✅ {num_conv} convergências detectadas")
                else:
                    validation_errors.append("⚠️  Nenhuma convergência detectada")

        # Relatório
        print("\n" + "=" * 60)
        print("RELATÓRIO DE VALIDAÇÃO JSON")
        print("=" * 60)

        if present_fields:
            print("\n✅ CAMPOS PRESENTES:")
            for field in present_fields[:10]:  # Mostrar primeiros 10
                print(f"   {field}")
            if len(present_fields) > 10:
                print(f"   ... e {len(present_fields)-10} outros")

        if missing_fields:
            print("\n❌ CAMPOS AUSENTES:")
            for field in missing_fields[:5]:  # Mostrar primeiros 5
                print(f"   {field}")
            if len(missing_fields) > 5:
                print(f"   ... e {len(missing_fields)-5} outros")

        if validation_errors:
            print("\n⚠️  ERROS DE VALIDAÇÃO:")
            for error in validation_errors:
                print(f"   {error}")

        # Análise de qualidade
        print("\n" + "=" * 60)
        print("ANÁLISE DE QUALIDADE")
        print("=" * 60)

        quality_score = 0
        quality_max = 5

        # Check 1: JSON válido
        quality_score += 1
        print("✅ [1/5] JSON válido e parseável")

        # Check 2: Campos principais presentes
        if len(missing_fields) == 0:
            quality_score += 1
            print("✅ [2/5] Todos campos principais presentes")
        else:
            print(f"❌ [2/5] {len(missing_fields)} campos ausentes")

        # Check 3: Evidence log populado
        if "evidence_log" in analysis and len(analysis["evidence_log"]) >= 3:
            quality_score += 1
            print(f"✅ [3/5] Evidence log com {len(analysis['evidence_log'])} evidências")
        else:
            print("❌ [3/5] Evidence log insuficiente")

        # Check 4: Score calculado
        if "validation" in analysis and "score_9d" in analysis["validation"]:
            if "total" in analysis["validation"]["score_9d"]:
                quality_score += 1
                score_val = analysis["validation"]["score_9d"]["total"]
                print(f"✅ [4/5] Score 9D calculado: {score_val}/45")
        else:
            print("❌ [4/5] Score 9D não calculado")

        # Check 5: Convergências detectadas
        if "convergencias_universais" in analysis:
            if "detectadas" in analysis["convergencias_universais"]:
                if len(analysis["convergencias_universais"]["detectadas"]) >= 3:
                    quality_score += 1
                    print(f"✅ [5/5] Convergências detectadas")
        else:
            print("❌ [5/5] Convergências não detectadas")

        print(f"\nQUALIDADE: {quality_score}/{quality_max}")

        # Resultado final
        print("\n" + "=" * 60)

        if quality_score >= 3 and len(missing_fields) <= 5:
            print("✅ OUTPUT JSON APROVADO")
            print(f"Qualidade: {quality_score}/{quality_max}")
            print("\nPróximo teste: python3 test_phase1_evidence.py")
            return True
        else:
            print("❌ OUTPUT JSON REPROVADO")
            print(f"Qualidade insuficiente: {quality_score}/{quality_max}")
            print("Ajustes necessários no modelo antes de prosseguir")
            return False

    except subprocess.TimeoutExpired:
        print("❌ Timeout na análise (>120s)")
        return False

    except Exception as e:
        print(f"❌ Erro inesperado: {e}")
        return False

if __name__ == "__main__":
    print("\n🎬 SCRIPTUREMON v9 - SUITE DE TESTES - FASE 1")
    print("Validação de Output JSON")
    print("\n")

    # Executar teste
    passed = test_json_output()

    # Resultado final
    print("\n" + "=" * 60)
    print("RESULTADO FINAL - FASE 1 - TESTE JSON")
    print("=" * 60)

    if passed:
        print("✅ TESTE APROVADO")
        sys.exit(0)
    else:
        print("❌ TESTE REPROVADO")
        sys.exit(1)