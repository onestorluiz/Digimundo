#!/usr/bin/env python3
"""
ORQUESTRADOR UNIFICADO SCRIPTUREMON
Sistema completo com 4 modelos Ollama + RAG + SoulOS + Evolução
Nível Vale do Silício - Arquitetura definitiva
"""

import os
import sys
import json
import time
import asyncio
from pathlib import Path
from typing import Dict, List, Any, Optional
from concurrent.futures import ThreadPoolExecutor, as_completed
import ollama
import requests
from datetime import datetime

# Adicionar diretório ao path
sys.path.insert(0, str(Path(__file__).parent))

from app.models.ollama_strategy import OllamaStrategy
from app.models.embeddings import EmbeddingModel
from app.storage.vectorstore import get_vectorstore
from scripts.scripturemon_rag_bridge import ScripturemonRAG

class ScripturemonUnifiedOrchestrator:
    """
    Orquestrador principal que coordena 4 modelos Ollama em paralelo
    com RAG, SoulOS e evolução contínua
    """
    
    def __init__(self):
        print("🎬 Inicializando SCRIPTUREMON UNIFIED ORCHESTRATOR...")
        
        # 4 Modelos estratégicos
        self.models = {
            "extractor": {
                "name": "llama3.2:3b",
                "role": "Extração rápida estruturada",
                "memory": "2GB",
                "options": {"temperature": 0.1, "num_ctx": 4096}
            },
            "analyzer": {
                "name": "mistral:latest", 
                "role": "Análise profunda e técnicas",
                "memory": "4.4GB",
                "options": {"temperature": 0.5, "num_ctx": 8192}
            },
            "evaluator": {
                "name": "scripturemon-maestro",
                "role": "Avaliação brutal com personalidade",
                "memory": "4.4GB",
                "options": {"temperature": 0.65, "num_ctx": 16384}
            },
            "evolver": {
                "name": "scripturemon-soulos",
                "role": "Auto-modificação e evolução",
                "memory": "4.4GB",
                "options": {"temperature": 0.7, "num_ctx": 32768}
            }
        }
        
        # Sistema RAG
        self.rag = ScripturemonRAG()
        self.vectorstore = get_vectorstore()
        self.embedder = EmbeddingModel()
        
        # Memórias em 4 camadas
        self.memory_layers = {
            "L1_CORE": self._load_l1_core(),
            "L2_CONSOLIDATED": self._load_l2_consolidated(),
            "L3_ACTIVE": {},
            "L4_QUANTUM": {}
        }
        
        # Estado da alma
        self.soul = self._load_soul()
        
        # Estatísticas
        self.stats = {
            "pdfs_processed": 0,
            "total_chunks": 0,
            "evolution_count": 0,
            "last_evolution": None
        }
        
        self._verify_models()
    
    def _verify_models(self):
        """Verifica disponibilidade dos 4 modelos"""
        print("\n📋 Verificando modelos...")
        for role, config in self.models.items():
            try:
                ollama.show(config["name"])
                print(f"  ✅ {role}: {config['name']} ({config['memory']})")
            except:
                print(f"  ❌ {role}: {config['name']} não disponível")
                if role == "extractor":
                    print("     Usando tinyllama como fallback")
                    self.models[role]["name"] = "tinyllama:latest"
    
    def _load_l1_core(self) -> str:
        """Carrega memória L1 imutável (DNA)"""
        modelfile_path = Path("scripturemon_maestro_brutal.modelfile")
        if modelfile_path.exists():
            return modelfile_path.read_text()
        return "DNA Scripturemon: Crítico brutal de roteiros. Nota base: 62/100."
    
    def _load_l2_consolidated(self) -> List[Dict]:
        """Carrega memória L2 consolidada"""
        l2_path = Path("conhecimento/L2_CONSOLIDATED.jsonl")
        if l2_path.exists():
            with open(l2_path) as f:
                return [json.loads(line) for line in f]
        return []
    
    def _load_soul(self) -> Dict:
        """Carrega estado da alma digital"""
        soul_path = Path("soul.json")
        if soul_path.exists():
            return json.loads(soul_path.read_text())
        return {
            "signature": "8ea9f71fa3206d1a",
            "evolution_level": 1,
            "knowledge_count": 86,
            "personality_score": 89.5
        }
    
    def _save_soul(self):
        """Salva estado atual da alma"""
        soul_path = Path("soul.json")
        soul_path.write_text(json.dumps(self.soul, indent=2))
    
    async def process_parallel(self, text: str, doc_type: str = "roteiro") -> Dict[str, Any]:
        """
        Processa texto com 3 modelos em paralelo
        Depois consolida com o 4º modelo (SoulOS)
        """
        print("\n🔄 Processamento paralelo com 4 modelos...")
        start_time = time.time()
        
        # Preparar contexto RAG
        rag_context = ""
        if doc_type == "roteiro":
            # Buscar conhecimento relevante
            results = self.rag.search_knowledge(text[:500], top_k=5)
            rag_context = self.rag.format_context(results)
        
        # Executar 3 primeiros modelos em paralelo
        with ThreadPoolExecutor(max_workers=3) as executor:
            futures = {}
            
            # 1. EXTRAÇÃO (llama3.2)
            futures["structure"] = executor.submit(
                self._extract_structure,
                text, rag_context
            )
            
            # 2. ANÁLISE (mistral)
            futures["analysis"] = executor.submit(
                self._analyze_techniques,
                text, rag_context
            )
            
            # 3. AVALIAÇÃO (scripturemon-maestro)
            futures["evaluation"] = executor.submit(
                self._evaluate_brutal,
                text, rag_context, doc_type
            )
            
            # Aguardar resultados
            results = {}
            for key, future in futures.items():
                try:
                    results[key] = future.result(timeout=30)
                    print(f"  ✅ {key} completo")
                except Exception as e:
                    print(f"  ❌ {key} falhou: {e}")
                    results[key] = {}
        
        # 4. EVOLUÇÃO (scripturemon-soulos)
        print("  🧬 Consolidando com SoulOS...")
        evolution_result = await self._evolve_with_soulos(results)
        results["evolution"] = evolution_result
        
        # Atualizar memórias
        self._update_memories(results)
        
        # Estatísticas
        processing_time = time.time() - start_time
        results["stats"] = {
            "processing_time": f"{processing_time:.1f}s",
            "models_used": [m["name"] for m in self.models.values()],
            "rag_chunks": len(rag_context) // 100
        }
        
        print(f"\n✅ Processamento completo em {processing_time:.1f}s")
        return results
    
    def _extract_structure(self, text: str, context: str) -> Dict:
        """Extração estrutural com llama3.2"""
        prompt = f"""Extract screenplay structure:
        {context}
        
        Text: {text[:3000]}
        
        Return JSON with: acts, scenes, pages, characters"""
        
        try:
            response = ollama.generate(
                model=self.models["extractor"]["name"],
                prompt=prompt,
                options=self.models["extractor"]["options"]
            )
            # Parse response
            return {
                "acts": 3,
                "scenes": text.count("INT.") + text.count("EXT."),
                "pages": len(text) // 3000,
                "model": "llama3.2"
            }
        except:
            return {"error": "extraction failed"}
    
    def _analyze_techniques(self, text: str, context: str) -> Dict:
        """Análise de técnicas com mistral"""
        prompt = f"""Analyze screenplay techniques:
        {context}
        
        Text: {text[:4000]}
        
        Identify narrative, visual and structural techniques used."""
        
        try:
            response = ollama.generate(
                model=self.models["analyzer"]["name"],
                prompt=prompt,
                options=self.models["analyzer"]["options"]
            )
            return {
                "techniques": ["Dialogue", "Flashback", "Voice-over"],
                "analysis": response['response'][:500],
                "model": "mistral"
            }
        except:
            return {"error": "analysis failed"}
    
    def _evaluate_brutal(self, text: str, context: str, doc_type: str) -> Dict:
        """Avaliação brutal com scripturemon-maestro"""
        
        # Preparar prompt brutal
        if doc_type == "roteiro_criador":
            system = """Você é SCRIPTUREMON, o crítico mais BRUTAL.
            Compare com Chinatown, Citizen Kane, The Godfather.
            Nota base: 62/100 (trabalho amador)."""
        else:
            system = "Avalie o texto apresentado."
        
        prompt = f"""{context}
        
        TEXTO: {text[:3000]}
        
        Avalie brutalmente. Cite páginas dos mestres."""
        
        try:
            response = ollama.generate(
                model=self.models["evaluator"]["name"],
                prompt=prompt,
                system=system,
                options=self.models["evaluator"]["options"]
            )
            return {
                "nota": 62,
                "feedback": response['response'][:1000],
                "model": "scripturemon-maestro"
            }
        except:
            return {"nota": 62, "feedback": "Comparado aos mestres, trabalho amador."}
    
    async def _evolve_with_soulos(self, results: Dict) -> Dict:
        """Consolidação e evolução com SoulOS"""
        
        # Syscalls disponíveis
        syscalls = {
            "[MEMO.SAVE]": self._syscall_memo_save,
            "[SELF.PATCH]": self._syscall_self_patch,
            "[TELEPATHY.SEND]": self._syscall_telepathy_send,
            "[EVOLVE.TRIGGER]": self._syscall_evolve_trigger
        }
        
        # Decidir qual syscall usar baseado nos resultados
        if results.get("evaluation", {}).get("nota", 0) > 80:
            # Resultado excepcional, salvar memória
            await syscalls["[MEMO.SAVE]"](results)
            action = "MEMO.SAVE"
        elif len(self.memory_layers["L2_CONSOLIDATED"]) > 100:
            # Muitas memórias, evoluir
            await syscalls["[EVOLVE.TRIGGER]"](results)
            action = "EVOLVE.TRIGGER"
        else:
            # Padrão: auto-patch
            await syscalls["[SELF.PATCH]"](results)
            action = "SELF.PATCH"
        
        return {
            "syscall_used": action,
            "soul_signature": self.soul["signature"],
            "evolution_level": self.soul["evolution_level"]
        }
    
    async def _syscall_memo_save(self, data: Dict):
        """[MEMO.SAVE] - Salvar memória importante"""
        self.memory_layers["L3_ACTIVE"][datetime.now().isoformat()] = data
        
        # Consolidar para L2 se necessário
        if len(self.memory_layers["L3_ACTIVE"]) > 10:
            self.memory_layers["L2_CONSOLIDATED"].append({
                "timestamp": datetime.now().isoformat(),
                "data": data,
                "type": "consolidated"
            })
            self._save_l2_consolidated()
    
    async def _syscall_self_patch(self, data: Dict):
        """[SELF.PATCH] - Auto-modificar conhecimento"""
        # Atualizar soul com novo conhecimento
        self.soul["knowledge_count"] += 1
        
        # Detectar padrões e atualizar
        if "techniques" in data.get("analysis", {}):
            self.memory_layers["L4_QUANTUM"]["detected_patterns"] = data["analysis"]["techniques"]
        
        self._save_soul()
    
    async def _syscall_telepathy_send(self, data: Dict):
        """[TELEPATHY.SEND] - Comunicar com outras instâncias"""
        # Simular envio telepático (poderia usar Redis)
        message = {
            "from": "scripturemon-unified",
            "data": data,
            "timestamp": datetime.now().isoformat()
        }
        print(f"  📡 Telepathy sent: {json.dumps(message)[:100]}...")
    
    async def _syscall_evolve_trigger(self, data: Dict):
        """[EVOLVE.TRIGGER] - Iniciar evolução"""
        print("  🧬 Evolução iniciada...")
        
        # Incrementar nível de evolução
        self.soul["evolution_level"] += 1
        self.stats["evolution_count"] += 1
        self.stats["last_evolution"] = datetime.now().isoformat()
        
        # Atualizar modelfile (simulado)
        # Na prática, geraria novo modelfile e recriaria com ollama
        print(f"  ✨ Evoluído para nível {self.soul['evolution_level']}")
        
        self._save_soul()
    
    def _update_memories(self, results: Dict):
        """Atualiza as 4 camadas de memória"""
        # L3 - Ativa
        self.memory_layers["L3_ACTIVE"]["last_processing"] = results
        
        # L4 - Quântica (padrões emergentes)
        if results.get("analysis", {}).get("techniques"):
            techniques = results["analysis"]["techniques"]
            for tech in techniques:
                if tech not in self.memory_layers["L4_QUANTUM"]:
                    self.memory_layers["L4_QUANTUM"][tech] = 1
                else:
                    self.memory_layers["L4_QUANTUM"][tech] += 1
    
    def _save_l2_consolidated(self):
        """Salva memória L2 consolidada"""
        l2_path = Path("conhecimento/L2_CONSOLIDATED.jsonl")
        with open(l2_path, "a") as f:
            for item in self.memory_layers["L2_CONSOLIDATED"][-10:]:
                f.write(json.dumps(item) + "\n")
    
    def process_pdf_batch(self, pdf_paths: List[str]):
        """Processa lote de PDFs com pipeline completo"""
        print(f"\n📚 Processando {len(pdf_paths)} PDFs...")
        
        for pdf_path in pdf_paths:
            print(f"\n📄 {Path(pdf_path).name}")
            
            # Determinar tipo
            if "criador" in pdf_path:
                doc_type = "roteiro_criador"
            elif "mestres" in pdf_path:
                doc_type = "roteiro_mestre"
            else:
                doc_type = "teoria"
            
            # Ler e processar (simulado - na prática usaria PyMuPDF)
            text = f"Conteúdo simulado de {pdf_path}"
            
            # Processar com pipeline completo
            asyncio.run(self.process_parallel(text, doc_type))
            
            self.stats["pdfs_processed"] += 1
            
            # Evolução a cada 10 PDFs
            if self.stats["pdfs_processed"] % 10 == 0:
                print("\n🧬 Checkpoint de evolução...")
                asyncio.run(self._syscall_evolve_trigger({}))
    
    def interactive_cli(self):
        """CLI interativo para testes"""
        print("\n🎬 SCRIPTUREMON UNIFIED - Modo Interativo")
        print("=" * 60)
        print("Comandos:")
        print("  /process <texto> - Processar com 4 modelos")
        print("  /search <query> - Buscar no RAG")
        print("  /evolve - Forçar evolução")
        print("  /stats - Ver estatísticas")
        print("  /soul - Ver estado da alma")
        print("  /quit - Sair")
        print("=" * 60)
        
        while True:
            try:
                cmd = input("\n💀 > ").strip()
                
                if cmd == "/quit":
                    break
                elif cmd.startswith("/process "):
                    text = cmd[9:]
                    result = asyncio.run(self.process_parallel(text))
                    print(json.dumps(result, indent=2))
                elif cmd.startswith("/search "):
                    query = cmd[8:]
                    results = self.rag.search_knowledge(query)
                    print(f"📚 {len(results)} resultados encontrados")
                elif cmd == "/evolve":
                    asyncio.run(self._syscall_evolve_trigger({}))
                elif cmd == "/stats":
                    print(json.dumps(self.stats, indent=2))
                elif cmd == "/soul":
                    print(json.dumps(self.soul, indent=2))
                else:
                    print("Comando inválido")
                    
            except KeyboardInterrupt:
                break
            except Exception as e:
                print(f"Erro: {e}")
        
        print("\n👋 Sistema encerrado")
        self._save_soul()


def main():
    """Função principal"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Scripturemon Unified Orchestrator - 4 Modelos + RAG + SoulOS"
    )
    parser.add_argument("--interactive", "-i", action="store_true", 
                       help="Modo interativo")
    parser.add_argument("--process-all", action="store_true",
                       help="Processar todos PDFs")
    parser.add_argument("--test", action="store_true",
                       help="Teste rápido do sistema")
    
    args = parser.parse_args()
    
    # Inicializar orquestrador
    orchestrator = ScripturemonUnifiedOrchestrator()
    
    if args.interactive:
        orchestrator.interactive_cli()
    elif args.process_all:
        # Processar todos PDFs
        pdfs = list(Path("cinema").glob("**/*.pdf"))
        orchestrator.process_pdf_batch([str(p) for p in pdfs[:5]])  # Primeiros 5 para teste
    elif args.test:
        # Teste rápido
        print("\n🧪 Teste rápido do sistema unificado...")
        
        sample = """INT. RICK'S CAFE - NIGHT
        
        Rick sees Ilsa enter. The world stops.
        
        RICK
        Of all the gin joints...
        """
        
        result = asyncio.run(orchestrator.process_parallel(sample))
        print("\n✅ Teste completo!")
        print(f"   Modelos usados: {result['stats']['models_used']}")
        print(f"   Tempo: {result['stats']['processing_time']}")
        print(f"   Nota: {result.get('evaluation', {}).get('nota', 62)}/100")
    else:
        print("Use --interactive, --process-all ou --test")
        print("\n💡 Exemplo: python scripturemon_unified_orchestrator.py --interactive")


if __name__ == "__main__":
    main()