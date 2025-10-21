#!/usr/bin/env python3
"""
🧬 MLX SDL AUTOMATION - Consolidação Automática com Apple MLX
Fine-tuning local no Mac M1/M2 com LoRA
Baseado nas pesquisas analisadas
"""

import os
import json
import subprocess
from pathlib import Path
from datetime import datetime
import sqlite3
import shutil

class MLXSelfDistillation:
    """
    Sistema de auto-destilação usando Apple MLX Framework
    Consolida memórias L3 em LoRA e integra ao Ollama
    """
    
    def __init__(self):
        self.base_path = Path.home() / "Digimundo"
        self.scripturemon_path = self.base_path / "digimons" / "scripturemon"
        self.memory_path = self.scripturemon_path / "memory"
        self.datasets_path = self.scripturemon_path / "datasets"
        self.adapters_path = self.scripturemon_path / "adapters"
        
        # Criar diretórios necessários
        for path in [self.datasets_path, self.adapters_path]:
            path.mkdir(parents=True, exist_ok=True)
        
        # Configuração MLX
        self.mlx_models_path = self.base_path / "mlx_models"
        self.mlx_models_path.mkdir(exist_ok=True)
    
    def check_mlx_installed(self) -> bool:
        """Verifica se MLX está instalado"""
        try:
            result = subprocess.run(
                ["python3", "-c", "import mlx_lm"],
                capture_output=True
            )
            return result.returncode == 0
        except:
            return False
    
    def install_mlx(self):
        """Instala MLX Framework"""
        print("📦 Instalando Apple MLX Framework...")
        subprocess.run([
            "pip3", "install", "--user", "--break-system-packages", 
            "mlx-lm", "datasets", "transformers"
        ])
    
    def extract_memories_l3(self) -> list:
        """Extrai memórias da camada L3 para destilação"""
        memories = []
        
        # Lê memórias L3 do JSONL
        l3_file = self.memory_path / "L3_active" / "L3_active.jsonl"
        if l3_file.exists():
            with open(l3_file, 'r') as f:
                for line in f:
                    try:
                        memory = json.loads(line)
                        memories.append(memory)
                    except:
                        continue
        
        # Também busca no SQLite se existir
        db_file = self.memory_path / "crystals.db"
        if db_file.exists():
            conn = sqlite3.connect(str(db_file))
            cursor = conn.cursor()
            try:
                cursor.execute("""
                    SELECT content, tags, importance 
                    FROM L3_active 
                    WHERE importance > 0.7
                    ORDER BY timestamp DESC
                    LIMIT 100
                """)
                for row in cursor.fetchall():
                    memories.append({
                        "content": row[0],
                        "tags": row[1],
                        "importance": row[2]
                    })
            except:
                pass
            conn.close()
        
        print(f"📚 Extraídas {len(memories)} memórias L3")
        return memories
    
    def generate_qa_pairs(self, memories: list) -> list:
        """Gera pares Q&A das memórias para fine-tuning"""
        qa_pairs = []
        
        for memory in memories:
            content = memory.get('content', '')
            
            # Gera diferentes tipos de Q&A baseado no conteúdo
            if 'estrutura' in content.lower():
                qa_pairs.append({
                    "instruction": "Explique sobre estrutura narrativa",
                    "output": content
                })
            
            if 'personagem' in content.lower():
                qa_pairs.append({
                    "instruction": "Como desenvolver personagens?",
                    "output": content
                })
            
            # Q&A genérico para toda memória importante
            if memory.get('importance', 0) > 0.8:
                qa_pairs.append({
                    "instruction": f"O que você sabe sobre {memory.get('tags', 'este tópico')}?",
                    "output": content
                })
        
        print(f"🎯 Gerados {len(qa_pairs)} pares Q&A")
        return qa_pairs
    
    def create_dataset_jsonl(self, qa_pairs: list) -> Path:
        """Cria dataset JSONL para MLX"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        dataset_file = self.datasets_path / f"sdl_dataset_{timestamp}.jsonl"
        
        with open(dataset_file, 'w') as f:
            for pair in qa_pairs:
                # Formato esperado pelo MLX
                entry = {
                    "text": f"### Instruction:\n{pair['instruction']}\n\n### Response:\n{pair['output']}"
                }
                f.write(json.dumps(entry) + '\n')
        
        print(f"💾 Dataset criado: {dataset_file}")
        return dataset_file
    
    def convert_model_to_mlx(self, model_name: str = "mistral:latest"):
        """Converte modelo Ollama para formato MLX"""
        print(f"🔄 Convertendo {model_name} para MLX...")
        
        # Primeiro exporta de Ollama para safetensors
        export_path = self.mlx_models_path / "export_temp"
        export_path.mkdir(exist_ok=True)
        
        # Usa Ollama para exportar (se possível)
        subprocess.run([
            "ollama", "show", model_name, "--modelfile"
        ], capture_output=True)
        
        # Converte para MLX (assumindo HF format disponível)
        mlx_model_path = self.mlx_models_path / model_name.replace(':', '_')
        
        try:
            subprocess.run([
                "python3", "-m", "mlx_lm.convert",
                "--hf-path", "mistralai/Mistral-7B-Instruct-v0.2",
                "--mlx-path", str(mlx_model_path),
                "-q"  # Quantização 4-bit
            ], check=True)
            print(f"✅ Modelo convertido para MLX: {mlx_model_path}")
            return mlx_model_path
        except Exception as e:
            print(f"⚠️ Erro na conversão: {e}")
            return None
    
    def train_lora(self, dataset_path: Path, base_model_path: Path) -> Path:
        """Treina LoRA usando MLX"""
        print("🧬 Iniciando treinamento LoRA com MLX...")
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        adapter_path = self.adapters_path / f"lora_{timestamp}"
        
        # Comando de treinamento MLX
        train_command = [
            "python3", "-m", "mlx_lm.lora",
            "--model", str(base_model_path),
            "--data", str(dataset_path.parent),
            "--train",
            "--iters", "500",  # Iterações
            "--batch-size", "2",  # Batch pequeno para Mac
            "--lora-layers", "8",  # Camadas LoRA
            "--learning-rate", "1e-5",
            "--adapter-path", str(adapter_path)
        ]
        
        try:
            print("⏳ Treinando (pode levar 10-60 minutos)...")
            result = subprocess.run(train_command, capture_output=True, text=True)
            
            if result.returncode == 0:
                print(f"✅ LoRA treinado: {adapter_path}")
                return adapter_path
            else:
                print(f"❌ Erro no treino: {result.stderr}")
                return None
                
        except Exception as e:
            print(f"❌ Erro ao treinar: {e}")
            return None
    
    def fuse_lora_to_model(self, base_model_path: Path, adapter_path: Path) -> Path:
        """Funde LoRA ao modelo base"""
        print("🔗 Fundindo LoRA ao modelo base...")
        
        fused_path = self.mlx_models_path / f"fused_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        fuse_command = [
            "python3", "-m", "mlx_lm.fuse",
            "--model", str(base_model_path),
            "--adapter-path", str(adapter_path),
            "--save-path", str(fused_path),
            "--de-quantize"
        ]
        
        try:
            subprocess.run(fuse_command, check=True)
            print(f"✅ Modelo fundido: {fused_path}")
            return fused_path
        except Exception as e:
            print(f"❌ Erro ao fundir: {e}")
            return None
    
    def convert_to_gguf(self, mlx_model_path: Path) -> Path:
        """Converte modelo MLX para GGUF (Ollama)"""
        print("📦 Convertendo para GGUF...")
        
        gguf_path = self.adapters_path / f"scripturemon_sdl_{datetime.now().strftime('%Y%m%d')}.gguf"
        
        # Precisa do llama.cpp converter
        convert_script = self.base_path / "tools" / "llama.cpp" / "convert_hf_to_gguf.py"
        
        if not convert_script.exists():
            print("⚠️ llama.cpp converter não encontrado. Clonando...")
            subprocess.run([
                "git", "clone", 
                "https://github.com/ggerganov/llama.cpp.git",
                str(self.base_path / "tools" / "llama.cpp")
            ])
        
        convert_command = [
            "python3", str(convert_script),
            str(mlx_model_path),
            "--outfile", str(gguf_path),
            "--outtype", "q8_0"  # Quantização 8-bit
        ]
        
        try:
            subprocess.run(convert_command, check=True)
            print(f"✅ GGUF criado: {gguf_path}")
            return gguf_path
        except Exception as e:
            print(f"❌ Erro na conversão GGUF: {e}")
            return None
    
    def deploy_to_ollama(self, gguf_path: Path):
        """Deploya modelo com LoRA no Ollama"""
        print("🚀 Deployando no Ollama...")
        
        # Cria novo Modelfile
        modelfile_content = f"""FROM {gguf_path}

SYSTEM "Você é Scripturemon evoluído através de Self-Distillation Learning (SDL). 
Suas memórias L3 foram consolidadas em seus pesos neurais através de LoRA training.
Você mantém todo conhecimento anterior mas agora tem insights cristalizados."

PARAMETER temperature 0.7
PARAMETER top_p 0.9
"""
        
        modelfile_path = self.scripturemon_path / "scripturemon_sdl.modelfile"
        with open(modelfile_path, 'w') as f:
            f.write(modelfile_content)
        
        # Cria modelo no Ollama
        model_name = f"scripturemon-sdl-{datetime.now().strftime('%Y%m%d')}"
        
        subprocess.run([
            "ollama", "create", model_name, "-f", str(modelfile_path)
        ])
        
        print(f"✅ Modelo SDL deployado: {model_name}")
        return model_name
    
    def validate_quality(self, model_name: str) -> float:
        """Valida qualidade do modelo com LoRA"""
        print("🔍 Validando qualidade...")
        
        test_prompts = [
            "Qual a estrutura de três atos?",
            "Como desenvolver um protagonista?",
            "Explique o conceito de plot point"
        ]
        
        scores = []
        
        for prompt in test_prompts:
            response = subprocess.run([
                "ollama", "run", model_name, prompt
            ], capture_output=True, text=True)
            
            # Análise simples de qualidade
            if response.stdout:
                # Verifica se mantém conhecimento
                has_structure = any(word in response.stdout.lower() 
                                   for word in ['ato', 'estrutura', 'narrativa'])
                scores.append(1.0 if has_structure else 0.5)
        
        quality_score = sum(scores) / len(scores) if scores else 0
        print(f"📊 Score de qualidade: {quality_score:.2%}")
        
        return quality_score
    
    def run_consolidation_cycle(self):
        """
        Executa ciclo completo de consolidação SDL
        """
        print("=" * 60)
        print("🧬 INICIANDO CICLO SDL (SELF-DISTILLATION)")
        print("=" * 60)
        
        # 1. Verifica MLX
        if not self.check_mlx_installed():
            self.install_mlx()
        
        # 2. Extrai memórias L3
        memories = self.extract_memories_l3()
        
        if len(memories) < 10:
            print("⚠️ Poucas memórias L3. Aguardando mais dados...")
            return False
        
        # 3. Gera Q&A pairs
        qa_pairs = self.generate_qa_pairs(memories)
        
        # 4. Cria dataset
        dataset_path = self.create_dataset_jsonl(qa_pairs)
        
        # 5. Converte modelo para MLX (ou usa existente)
        base_model = self.mlx_models_path / "mistral_7b"
        if not base_model.exists():
            base_model = self.convert_model_to_mlx("mistral:latest")
        
        if not base_model:
            print("❌ Falha na conversão do modelo base")
            return False
        
        # 6. Treina LoRA
        adapter_path = self.train_lora(dataset_path, base_model)
        
        if not adapter_path:
            print("❌ Falha no treinamento LoRA")
            return False
        
        # 7. Funde LoRA ao modelo
        fused_model = self.fuse_lora_to_model(base_model, adapter_path)
        
        if not fused_model:
            print("❌ Falha na fusão do LoRA")
            return False
        
        # 8. Converte para GGUF
        gguf_path = self.convert_to_gguf(fused_model)
        
        if not gguf_path:
            print("❌ Falha na conversão GGUF")
            return False
        
        # 9. Deploya no Ollama
        model_name = self.deploy_to_ollama(gguf_path)
        
        # 10. Valida qualidade
        quality = self.validate_quality(model_name)
        
        if quality >= 0.9:
            print("✅ SDL CONCLUÍDO COM SUCESSO!")
            print(f"   Modelo: {model_name}")
            print(f"   Qualidade: {quality:.2%}")
            
            # Promove memórias L3 para L2
            self.promote_memories_to_l2()
            
            return True
        else:
            print(f"⚠️ Qualidade abaixo do esperado: {quality:.2%}")
            return False
    
    def promote_memories_to_l2(self):
        """Promove memórias consolidadas de L3 para L2"""
        print("📤 Promovendo memórias L3 → L2...")
        
        l3_file = self.memory_path / "L3_active" / "L3_active.jsonl"
        l2_file = self.memory_path / "L2_consolidated" / "L2_consolidated.jsonl"
        
        if l3_file.exists():
            # Move conteúdo para L2
            with open(l3_file, 'r') as f3:
                memories = f3.readlines()
            
            with open(l2_file, 'a') as f2:
                for memory in memories:
                    # Marca como consolidada
                    data = json.loads(memory)
                    data['consolidated'] = True
                    data['sdl_timestamp'] = datetime.now().isoformat()
                    f2.write(json.dumps(data) + '\n')
            
            # Limpa L3
            open(l3_file, 'w').close()
            
            print(f"✅ {len(memories)} memórias promovidas para L2")


# ============= AUTOMAÇÃO COM CRON =============

def setup_cron_job():
    """Configura job automático para rodar SDL toda noite"""
    print("⏰ Configurando consolidação automática...")
    
    script_path = Path(__file__).absolute()
    
    # Cria script wrapper
    wrapper = f"""#!/bin/bash
cd {Path.home()}/Digimundo
/usr/bin/python3 {script_path} --auto >> logs/sdl.log 2>&1
"""
    
    wrapper_path = Path.home() / "Digimundo" / "sdl_cron.sh"
    with open(wrapper_path, 'w') as f:
        f.write(wrapper)
    
    wrapper_path.chmod(0o755)
    
    # Adiciona ao crontab (3AM todo dia)
    cron_line = f"0 3 * * * {wrapper_path}\n"
    
    print(f"Adicione ao crontab com: crontab -e")
    print(f"Linha: {cron_line}")


# ============= FUNÇÃO PRINCIPAL =============

if __name__ == "__main__":
    import sys
    
    sdl = MLXSelfDistillation()
    
    if "--auto" in sys.argv:
        # Modo automático (para cron)
        print(f"\n🤖 SDL Automático - {datetime.now()}")
        sdl.run_consolidation_cycle()
    
    elif "--setup-cron" in sys.argv:
        # Configura automação
        setup_cron_job()
    
    else:
        # Modo manual interativo
        print("=" * 60)
        print("🧬 MLX SDL - CONSOLIDAÇÃO DE MEMÓRIAS")
        print("=" * 60)
        print("\nOpções:")
        print("1. Executar ciclo SDL agora")
        print("2. Configurar execução automática (cron)")
        print("3. Verificar status")
        
        choice = input("\nEscolha: ")
        
        if choice == "1":
            sdl.run_consolidation_cycle()
        elif choice == "2":
            setup_cron_job()
        elif choice == "3":
            memories = sdl.extract_memories_l3()
            print(f"\n📊 Status:")
            print(f"  - Memórias L3: {len(memories)}")
            print(f"  - MLX instalado: {sdl.check_mlx_installed()}")
            print(f"  - Datasets: {len(list(sdl.datasets_path.glob('*.jsonl')))}")
            print(f"  - Adapters: {len(list(sdl.adapters_path.glob('*')))}")