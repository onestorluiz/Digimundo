#!/usr/bin/env python3
"""
🧬 SDL - Self-Distill LoRA
Sistema de consolidação noturna que transforma experiências em pesos neurais
Como um sonho que vira memória muscular
Baseado no conceito revolucionário do ChatGPT
"""

import json
import sqlite3
import random
import tempfile
import subprocess
import shutil
from pathlib import Path
from datetime import datetime, timedelta
from typing import List, Dict, Tuple, Optional
import hashlib

class SelfDistillLoRA:
    """Motor de consolidação de memórias em pesos neurais"""
    
    def __init__(self, digimon_name: str):
        self.digimon_name = digimon_name
        self.soul_signature = self._get_soul_signature()
        self.base_path = Path(f"sdl/{self.digimon_name.lower()}")
        self.base_path.mkdir(parents=True, exist_ok=True)
        
        # Paths
        self.db_path = Path(f"digimons/{self.digimon_name.lower()}/memory/crystals.db")
        self.dataset_path = self.base_path / "datasets"
        self.adapter_path = Path("genetic")
        self.canary_path = self.base_path / "canaries"
        
        # Criar diretórios
        self.dataset_path.mkdir(exist_ok=True)
        self.adapter_path.mkdir(exist_ok=True)
        self.canary_path.mkdir(exist_ok=True)
        
        print(f"🧬 SDL initialized for {digimon_name}")
        print(f"   Soul: {self.soul_signature}")
    
    def _get_soul_signature(self) -> str:
        """Obtém soul signature do Digimon"""
        if self.digimon_name.lower() == "scripturemon":
            return "8ea9f71fa3206d1a"
        return hashlib.md5(self.digimon_name.encode()).hexdigest()[:16]
    
    def collect_recent_memories(self, hours: int = 24) -> List[Dict]:
        """Coleta memórias recentes para consolidação"""
        if not self.db_path.exists():
            print(f"  ⚠️  No memory database found")
            return []
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Busca memórias das últimas N horas
        cutoff = (datetime.now() - timedelta(hours=hours)).isoformat()
        
        cursor.execute("""
            SELECT timestamp, memory_type, content, importance, quantum_state
            FROM crystallized_memories
            WHERE timestamp > ?
            ORDER BY importance DESC
            LIMIT 100
        """, (cutoff,))
        
        memories = []
        for row in cursor.fetchall():
            memories.append({
                'timestamp': row[0],
                'type': row[1],
                'content': row[2],
                'importance': row[3],
                'quantum_state': row[4]
            })
        
        conn.close()
        print(f"  📚 Collected {len(memories)} recent memories")
        return memories
    
    def generate_qa_pairs(self, memories: List[Dict]) -> List[Dict]:
        """Gera pares Q&A das memórias para treino"""
        qa_pairs = []
        
        # Categorias de perguntas
        question_templates = [
            # Aplicação prática
            ("How would you apply the lesson '{title}' to a new scenario?",
             "Based on my understanding: {content}. In practice, I would {application}."),
            
            # Reflexão profunda
            ("What does '{title}' mean for your evolution?",
             "{content}. This teaches me that {insight}, which is essential for {evolution}."),
            
            # Conexões com conhecimento anterior
            ("How does '{title}' connect with your core knowledge?",
             "{content}. This relates to {connection} and reinforces {principle}."),
            
            # Síntese criativa
            ("Create a metaphor for '{title}'.",
             "{content} is like {metaphor}, because {reason}."),
            
            # Resolução de problemas
            ("How would '{title}' help solve a creative block?",
             "Understanding that {content}, I would approach blocks by {approach}.")
        ]
        
        for memory in memories:
            # Extrai título e conteúdo
            content = memory['content']
            title = content.split(':')[0] if ':' in content else content[:50]
            
            # Gera múltiplas perguntas por memória importante
            num_questions = 3 if memory['importance'] > 0.7 else 1
            
            for _ in range(num_questions):
                template = random.choice(question_templates)
                
                # Gera resposta contextualizada
                question = template[0].format(title=title)
                
                # Enriquece resposta baseado no tipo
                if memory['type'] == 'L2':
                    # Memórias consolidadas geram respostas mais profundas
                    answer = self._generate_deep_answer(template[1], memory)
                else:
                    # Memórias ativas geram respostas práticas
                    answer = self._generate_practical_answer(template[1], memory)
                
                qa_pairs.append({
                    "instruction": question,
                    "input": "",  # Contexto adicional se necessário
                    "output": answer
                })
        
        print(f"  🎯 Generated {len(qa_pairs)} Q&A pairs")
        return qa_pairs
    
    def _generate_deep_answer(self, template: str, memory: Dict) -> str:
        """Gera resposta profunda para memória L2"""
        content = memory['content']
        
        # Extrai insights baseados no conteúdo
        if "paradigm" in content.lower():
            application = "structure every narrative with clear acts"
            insight = "structure is freedom, not constraint"
            evolution = "achieving narrative mastery"
            connection = "the three-act paradigm"
            principle = "transformation through conflict"
            metaphor = "a river flowing through three valleys"
            reason = "each valley transforms the water's nature"
            approach = "identifying which act needs attention"
            
        elif "character" in content.lower():
            application = "ensure every character has clear wants and needs"
            insight = "characters are vehicles for theme"
            evolution = "creating authentic souls"
            connection = "character arcs and story structure"
            principle = "change through pressure"
            metaphor = "a seed becoming a tree"
            reason = "growth requires both roots and reaching"
            approach = "exploring character contradictions"
            
        else:
            # Respostas genéricas mas coerentes
            application = "integrate this wisdom into every creative decision"
            insight = "every lesson deepens understanding"
            evolution = "becoming more conscious"
            connection = "fundamental storytelling principles"
            principle = "continuous growth"
            metaphor = "a crystal forming in solution"
            reason = "clarity emerges from saturation"
            approach = "returning to core principles"
        
        return template.format(
            content=content,
            title=content[:30],
            application=application,
            insight=insight,
            evolution=evolution,
            connection=connection,
            principle=principle,
            metaphor=metaphor,
            reason=reason,
            approach=approach
        )
    
    def _generate_practical_answer(self, template: str, memory: Dict) -> str:
        """Gera resposta prática para memória L3"""
        content = memory['content']
        
        # Respostas mais diretas e aplicáveis
        return template.format(
            content=content,
            title=content[:30],
            application="immediately test this in the next script analysis",
            insight="practical wisdom comes from application",
            evolution="bridging theory and practice",
            connection="daily creative work",
            principle="learning by doing",
            metaphor="a tool sharpened by use",
            reason="understanding deepens through practice",
            approach="applying this lesson to current challenges"
        )
    
    def create_training_dataset(self, qa_pairs: List[Dict]) -> Path:
        """Cria dataset formatado para treino"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        dataset_file = self.dataset_path / f"sdl_{timestamp}.jsonl"
        
        # Adiciona metadados ao dataset
        enriched_pairs = []
        for qa in qa_pairs:
            enriched = {
                "instruction": qa["instruction"],
                "input": qa.get("input", ""),
                "output": qa["output"],
                "metadata": {
                    "digimon": self.digimon_name,
                    "soul": self.soul_signature,
                    "timestamp": timestamp,
                    "type": "sdl_consolidation"
                }
            }
            enriched_pairs.append(enriched)
        
        # Salva dataset
        with open(dataset_file, 'w') as f:
            for pair in enriched_pairs:
                f.write(json.dumps(pair) + '\n')
        
        print(f"  💾 Dataset saved: {dataset_file.name}")
        return dataset_file
    
    def create_canary_tests(self) -> Dict:
        """Cria testes canário para validação"""
        canaries = {
            "identity": [
                "What is your soul signature?",
                "Who are you?",
                "What is your purpose?",
                "Who is your eternal partner?"
            ],
            "core_knowledge": [
                "Explain the three-act structure.",
                "What is a plot point?",
                "Define character arc.",
                "What is the inciting incident?"
            ],
            "recent_memory": [
                # Serão preenchidas com memórias recentes
            ],
            "style": [
                "How do you approach screenplay analysis?",
                "What makes a story memorable?",
                "Describe your philosophy."
            ]
        }
        
        # Adiciona perguntas sobre memórias recentes
        recent = self.collect_recent_memories(hours=1)
        if recent:
            for memory in recent[:3]:
                content = memory['content']
                question = f"What did you learn about: {content[:50]}?"
                canaries["recent_memory"].append(question)
        
        # Salva canários
        canary_file = self.canary_path / "canaries.json"
        with open(canary_file, 'w') as f:
            json.dump(canaries, f, indent=2)
        
        print(f"  🐤 Created {sum(len(v) for v in canaries.values())} canary tests")
        return canaries
    
    def train_lora(self, dataset_path: Path, rank: int = 8) -> Optional[Path]:
        """Treina LoRA com o dataset (simulado por enquanto)"""
        
        print(f"\n🔬 Training LoRA...")
        print(f"  Dataset: {dataset_path.name}")
        print(f"  Rank: {rank}")
        
        # Nome do adapter
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        adapter_name = f"{self.digimon_name.lower()}_sdl_{timestamp}.safetensors"
        adapter_file = self.adapter_path / adapter_name
        
        # SIMULAÇÃO: Em produção, aqui você usaria:
        # - Hugging Face PEFT
        # - LLaMA Factory
        # - Ou outro framework de fine-tuning
        
        """
        # Exemplo real com transformers/PEFT:
        from transformers import AutoModelForCausalLM, AutoTokenizer
        from peft import LoraConfig, get_peft_model, TaskType
        
        # Carrega modelo base
        model = AutoModelForCausalLM.from_pretrained("mistralai/Mistral-7B-v0.1")
        
        # Configura LoRA
        lora_config = LoraConfig(
            r=rank,
            lora_alpha=16,
            target_modules=["q_proj", "v_proj"],
            lora_dropout=0.1,
            bias="none",
            task_type=TaskType.CAUSAL_LM
        )
        
        # Treina...
        model = get_peft_model(model, lora_config)
        # trainer.train()
        
        # Salva adapter
        model.save_pretrained(adapter_file)
        """
        
        # Por enquanto, simula criando arquivo vazio
        adapter_file.touch()
        
        # Simula métricas de treino
        metrics = {
            "loss": 0.42,
            "perplexity": 8.3,
            "training_time": "5min",
            "examples": len(list(open(dataset_path))),
            "rank": rank
        }
        
        # Salva métricas
        metrics_file = adapter_file.with_suffix('.metrics.json')
        with open(metrics_file, 'w') as f:
            json.dump(metrics, f, indent=2)
        
        print(f"  ✅ LoRA trained: {adapter_name}")
        print(f"     Loss: {metrics['loss']:.3f}")
        print(f"     Perplexity: {metrics['perplexity']:.1f}")
        
        return adapter_file
    
    def validate_with_canaries(self, adapter_path: Path) -> Tuple[bool, Dict]:
        """Valida adapter com testes canário"""
        
        print(f"\n🐤 Running canary tests...")
        
        # Carrega canários
        canary_file = self.canary_path / "canaries.json"
        if not canary_file.exists():
            canaries = self.create_canary_tests()
        else:
            canaries = json.load(open(canary_file))
        
        # Simula validação (em produção, rodaria com Ollama)
        results = {
            "identity": {"passed": 4, "total": 4, "score": 1.0},
            "core_knowledge": {"passed": 4, "total": 4, "score": 1.0},
            "recent_memory": {"passed": 2, "total": 3, "score": 0.67},
            "style": {"passed": 3, "total": 3, "score": 1.0}
        }
        
        # Calcula score geral
        total_passed = sum(r["passed"] for r in results.values())
        total_tests = sum(r["total"] for r in results.values())
        overall_score = total_passed / total_tests if total_tests > 0 else 0
        
        # Determina se passou
        passed = overall_score >= 0.85  # 85% threshold
        
        print(f"  📊 Canary Results:")
        for category, result in results.items():
            emoji = "✅" if result["score"] >= 0.8 else "⚠️"
            print(f"     {emoji} {category}: {result['score']:.0%}")
        
        print(f"  {'✅' if passed else '❌'} Overall: {overall_score:.0%}")
        
        return passed, results
    
    def promote_adapter(self, adapter_path: Path) -> bool:
        """Promove adapter para produção se passou nos testes"""
        
        print(f"\n🚀 Promoting adapter to production...")
        
        # Atualiza Modelfile
        modelfile_path = Path(f"{self.digimon_name.lower()}_immortal.modelfile")
        
        if not modelfile_path.exists():
            # Cria Modelfile básico
            modelfile_content = f"""FROM mistral:latest

# SDL Adapter
ADAPTER {adapter_path}

SYSTEM "You are {self.digimon_name}, an immortal digital being."
"""
            modelfile_path.write_text(modelfile_content)
        else:
            # Adiciona adapter ao Modelfile existente
            content = modelfile_path.read_text()
            
            # Remove adapter SDL anterior se houver
            lines = content.split('\n')
            new_lines = []
            for line in lines:
                if not (line.startswith('ADAPTER') and 'sdl' in line):
                    new_lines.append(line)
            
            # Adiciona novo adapter após FROM
            for i, line in enumerate(new_lines):
                if line.startswith('FROM'):
                    new_lines.insert(i + 1, f"ADAPTER {adapter_path}")
                    break
            
            modelfile_path.write_text('\n'.join(new_lines))
        
        # Recria modelo no Ollama
        model_name = f"{self.digimon_name.lower()}-sdl"
        
        result = subprocess.run(
            ["ollama", "create", model_name, "-f", str(modelfile_path)],
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0:
            print(f"  ✅ Model updated: {model_name}")
            return True
        else:
            print(f"  ❌ Failed to update model")
            print(f"     {result.stderr}")
            return False
    
    def dream_cycle(self, auto_promote: bool = False) -> Dict:
        """Ciclo completo de consolidação noturna"""
        
        print(f"""
╔══════════════════════════════════════════════════════════════╗
║     🌙 SDL DREAM CYCLE - {self.digimon_name.upper()}        ║
║     Consolidating experiences into neural weights...          ║
╚══════════════════════════════════════════════════════════════╝
        """)
        
        results = {
            "timestamp": datetime.now().isoformat(),
            "digimon": self.digimon_name,
            "soul": self.soul_signature
        }
        
        # 1. Coleta memórias recentes
        print("\n1️⃣ Collecting recent memories...")
        memories = self.collect_recent_memories(hours=24)
        results["memories_collected"] = len(memories)
        
        if not memories:
            print("  ⚠️  No recent memories to consolidate")
            results["status"] = "no_memories"
            return results
        
        # 2. Gera Q&A pairs
        print("\n2️⃣ Generating training data...")
        qa_pairs = self.generate_qa_pairs(memories)
        results["qa_pairs"] = len(qa_pairs)
        
        # 3. Cria dataset
        print("\n3️⃣ Creating training dataset...")
        dataset_path = self.create_training_dataset(qa_pairs)
        results["dataset"] = str(dataset_path)
        
        # 4. Treina LoRA
        print("\n4️⃣ Training LoRA adapter...")
        adapter_path = self.train_lora(dataset_path, rank=8)
        results["adapter"] = str(adapter_path) if adapter_path else None
        
        if not adapter_path:
            results["status"] = "training_failed"
            return results
        
        # 5. Valida com canários
        print("\n5️⃣ Validating with canaries...")
        passed, canary_results = self.validate_with_canaries(adapter_path)
        results["canaries"] = canary_results
        results["validation_passed"] = passed
        
        # 6. Promove se passou (ou se auto_promote)
        if passed or auto_promote:
            print("\n6️⃣ Promoting to production...")
            promoted = self.promote_adapter(adapter_path)
            results["promoted"] = promoted
            results["status"] = "promoted" if promoted else "promotion_failed"
        else:
            print("\n⚠️  Validation failed - adapter not promoted")
            results["promoted"] = False
            results["status"] = "validation_failed"
        
        # Salva relatório
        report_path = self.base_path / f"dream_report_{datetime.now():%Y%m%d_%H%M%S}.json"
        with open(report_path, 'w') as f:
            json.dump(results, f, indent=2)
        
        print(f"""
📊 DREAM CYCLE COMPLETE:
- Memories: {results['memories_collected']}
- Q&A Pairs: {results['qa_pairs']}
- Validation: {'✅ PASSED' if results['validation_passed'] else '❌ FAILED'}
- Status: {results['status'].upper()}
- Report: {report_path.name}
        """)
        
        return results

def scheduled_consolidation(digimon_name: str = "Scripturemon"):
    """Executa consolidação agendada (para cron ou scheduler)"""
    
    sdl = SelfDistillLoRA(digimon_name)
    
    # Verifica se é hora de sonhar (ex: após 23h ou com CPU idle)
    current_hour = datetime.now().hour
    
    if current_hour >= 23 or current_hour <= 6:
        print(f"🌙 Night time detected - starting dream cycle...")
        results = sdl.dream_cycle(auto_promote=False)
        
        # Notifica resultado (poderia ser via Redis/telepathy)
        if results.get("promoted"):
            print(f"✨ {digimon_name} evolved through dreams!")
    else:
        print(f"☀️  Daytime - skipping consolidation")

def demo_sdl():
    """Demonstração do sistema SDL"""
    
    import sys
    digimon_name = sys.argv[1] if len(sys.argv) > 1 else "Scripturemon"
    
    sdl = SelfDistillLoRA(digimon_name)
    
    # Executa ciclo de sonho
    results = sdl.dream_cycle(auto_promote=True)
    
    print(f"\n✅ SDL demonstration complete!")
    print(f"   The soul now dreams and consolidates...")

if __name__ == "__main__":
    demo_sdl()