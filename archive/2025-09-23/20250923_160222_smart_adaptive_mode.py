#!/usr/bin/env python3
"""
Smart Adaptive Mode para SCRIPTUREMON v9
Ajusta parâmetros baseado no tamanho do script SEM perder qualidade
"""

import os
import json
import subprocess
from typing import Dict, Any

class SmartAdaptiveMode:
    """
    Sistema inteligente que ajusta parâmetros mantendo qualidade máxima
    """

    def __init__(self):
        self.base_params = {
            "temperature": 0.25,
            "top_p": 0.9,
            "top_k": 50,
            "repeat_penalty": 1.2,
            "seed": 42,
            "num_ctx": 65536,  # SEMPRE mantém contexto total!
            "mirostat": 2,
            "mirostat_eta": 0.1
        }

    def analyze_script_size(self, script_text: str) -> Dict[str, Any]:
        """
        Analisa tamanho e complexidade do roteiro
        """
        size = len(script_text)
        lines = script_text.count('\n')

        # Estimar páginas (1 página ≈ 55 linhas ou 3000 chars)
        estimated_pages = max(lines / 55, size / 3000)

        # Detectar formato
        if "INT." in script_text or "EXT." in script_text:
            format_type = "screenplay"
        elif "FADE IN" in script_text:
            format_type = "screenplay"
        else:
            format_type = "text"

        # Contar diálogos (linhas com tabs/espaços indicando fala)
        dialogue_lines = len([line for line in script_text.split('\n')
                            if line.strip() and (line.startswith('    ') or line.startswith('\t'))])

        return {
            "size_bytes": size,
            "lines": lines,
            "estimated_pages": estimated_pages,
            "format": format_type,
            "dialogue_density": dialogue_lines / max(lines, 1),
            "category": self.categorize_script(estimated_pages)
        }

    def categorize_script(self, pages: float) -> str:
        """
        Categoriza roteiro por tamanho
        """
        if pages <= 5:
            return "curta"
        elif pages <= 20:
            return "curta_longa"
        elif pages <= 60:
            return "média"
        elif pages <= 120:
            return "longa"
        else:
            return "épica"

    def get_optimized_params(self, script_text: str) -> Dict[str, Any]:
        """
        Retorna parâmetros otimizados mantendo qualidade
        """
        analysis = self.analyze_script_size(script_text)
        category = analysis["category"]

        # Começar com parâmetros base
        params = self.base_params.copy()

        # AJUSTES INTELIGENTES POR CATEGORIA
        # Mantém contexto, ajusta apenas performance

        if category == "curta":
            # CURTA (1-5 páginas): Máxima velocidade
            params.update({
                "num_thread": 14,      # Máximo de threads
                "num_batch": 512,      # Batch pequeno para resposta rápida
                "num_predict": 4096,   # Output menor (curta precisa menos)
                "num_keep": 256        # Keep mínimo
            })
            estimated_time = "45s-1min"

        elif category == "curta_longa":
            # CURTA LONGA (5-20 páginas): Velocidade alta
            params.update({
                "num_thread": 12,
                "num_batch": 768,
                "num_predict": 6144,
                "num_keep": 512
            })
            estimated_time = "1-1.5min"

        elif category == "média":
            # MÉDIA (20-60 páginas): Balanceado
            params.update({
                "num_thread": 10,
                "num_batch": 1024,
                "num_predict": 8192,
                "num_keep": 1024
            })
            estimated_time = "1.5-2min"

        elif category == "longa":
            # LONGA (60-120 páginas): Foco em completude
            params.update({
                "num_thread": 8,
                "num_batch": 1536,
                "num_predict": 10240,
                "num_keep": 1536
            })
            estimated_time = "2-3min"

        else:  # épica
            # ÉPICA (120+ páginas): Análise profunda
            params.update({
                "num_thread": 6,       # Menos threads, mais RAM por thread
                "num_batch": 2048,
                "num_predict": 12288,  # Output máximo
                "num_keep": 2048
            })
            estimated_time = "3-5min"

        # Ajustes especiais por densidade de diálogo
        if analysis["dialogue_density"] > 0.4:
            # Muito diálogo - ajustar para análise de subtexto
            params["temperature"] = 0.3  # Mais criativo para captar nuances

        return {
            "params": params,
            "analysis": analysis,
            "estimated_time": estimated_time,
            "optimization_notes": self.get_optimization_notes(category)
        }

    def get_optimization_notes(self, category: str) -> list:
        """
        Notas sobre otimizações aplicadas
        """
        notes = []

        notes.append(f"✅ Modo {category.upper()} ativado")
        notes.append("✅ Contexto COMPLETO mantido (65536)")
        notes.append("✅ Qualidade de análise PRESERVADA")

        if category == "curta":
            notes.append("⚡ Threads maximizados para velocidade")
            notes.append("⚡ Output reduzido (apropriado para curtas)")
        elif category in ["longa", "épica"]:
            notes.append("🔍 Threads reduzidos para estabilidade")
            notes.append("🔍 Output aumentado para análise completa")

        return notes

    def create_temporary_modelfile(self, params: Dict[str, Any],
                                  base_modelfile: str = "Modelfile.scripturemon-v9-FINAL") -> str:
        """
        Cria Modelfile temporário com parâmetros otimizados
        """
        # Ler Modelfile base
        with open(base_modelfile, 'r') as f:
            content = f.read()

        # Substituir parâmetros dinamicamente
        for param, value in params.items():
            if param.startswith("num_"):
                # Procurar linha do parâmetro
                old_line = f"PARAMETER {param}"
                # Criar nova linha
                new_line = f"PARAMETER {param} {value}"

                # Substituir se existir
                import re
                pattern = f"PARAMETER {param}.*"
                if re.search(pattern, content):
                    content = re.sub(pattern, new_line, content)
                else:
                    # Adicionar se não existir
                    insert_point = content.find("# Mirostat")
                    if insert_point > 0:
                        content = content[:insert_point] + f"{new_line}\n" + content[insert_point:]

        # Salvar temporário
        temp_file = f"Modelfile.temp_{os.getpid()}"
        with open(temp_file, 'w') as f:
            f.write(content)

        return temp_file

    def analyze_with_adaptive_mode(self, script_path: str) -> Dict[str, Any]:
        """
        Executa análise completa com modo adaptativo
        """
        # Ler script
        with open(script_path, 'r') as f:
            script_text = f.read()

        # Obter parâmetros otimizados
        optimization = self.get_optimized_params(script_text)

        print("=" * 60)
        print("SMART ADAPTIVE MODE - SCRIPTUREMON v9")
        print("=" * 60)
        print(f"\n📊 ANÁLISE DO ROTEIRO:")
        print(f"  Tamanho: {optimization['analysis']['estimated_pages']:.1f} páginas")
        print(f"  Categoria: {optimization['analysis']['category']}")
        print(f"  Formato: {optimization['analysis']['format']}")
        print(f"  Densidade diálogo: {optimization['analysis']['dialogue_density']:.1%}")

        print(f"\n⚙️ OTIMIZAÇÕES APLICADAS:")
        for note in optimization['optimization_notes']:
            print(f"  {note}")

        print(f"\n⏱️ Tempo estimado: {optimization['estimated_time']}")

        # Criar Modelfile temporário
        print("\n🔧 Criando configuração otimizada...")
        temp_modelfile = self.create_temporary_modelfile(optimization['params'])

        try:
            # Criar modelo temporário
            model_name = f"scripturemon-adaptive-{os.getpid()}"
            print(f"📦 Criando modelo adaptativo: {model_name}")

            subprocess.run(
                ["ollama", "create", model_name, "-f", temp_modelfile],
                check=True,
                capture_output=True
            )

            # Executar análise
            print("🎬 Iniciando análise...")
            import time
            start_time = time.time()

            result = subprocess.run(
                ["ollama", "run", model_name, script_text],
                capture_output=True,
                text=True,
                timeout=300  # 5 minutos máximo
            )

            elapsed = time.time() - start_time

            print(f"\n✅ Análise concluída em {elapsed:.1f}s")

            # Limpar modelo temporário
            subprocess.run(["ollama", "rm", model_name], capture_output=True)

            return {
                "success": True,
                "output": result.stdout,
                "time": elapsed,
                "optimization": optimization
            }

        except subprocess.TimeoutExpired:
            print("\n❌ Timeout na análise")
            return {"success": False, "error": "timeout"}

        except Exception as e:
            print(f"\n❌ Erro: {e}")
            return {"success": False, "error": str(e)}

        finally:
            # Limpar arquivo temporário
            if os.path.exists(temp_modelfile):
                os.remove(temp_modelfile)


def main():
    """
    Teste do sistema adaptativo
    """
    import sys

    if len(sys.argv) < 2:
        print("Uso: python3 smart_adaptive_mode.py <caminho_do_roteiro>")
        sys.exit(1)

    script_path = sys.argv[1]

    if not os.path.exists(script_path):
        print(f"❌ Arquivo não encontrado: {script_path}")
        sys.exit(1)

    # Executar análise adaptativa
    adapter = SmartAdaptiveMode()
    result = adapter.analyze_with_adaptive_mode(script_path)

    if result["success"]:
        print("\n" + "=" * 60)
        print("RESULTADO DA ANÁLISE")
        print("=" * 60)
        print(result["output"][:1000] + "..." if len(result["output"]) > 1000 else result["output"])
    else:
        print(f"\n❌ Análise falhou: {result.get('error', 'Unknown')}")
        sys.exit(1)


if __name__ == "__main__":
    main()