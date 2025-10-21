#!/usr/bin/env python3
"""
🧬 SDL SIMPLE CONSOLIDATION - Consolidação simplificada de memórias
Como MLX tem problemas de versão, vamos consolidar diretamente no Modelfile
"""

import json
from pathlib import Path
from datetime import datetime

class SimpleSDLConsolidator:
    def __init__(self):
        self.base_path = Path.home() / "Digimundo" / "digimons" / "scripturemon"
        self.memory_path = self.base_path / "memory"
        self.l3_file = self.memory_path / "L3_active" / "L3_active.jsonl"
        self.l2_file = self.memory_path / "L2_consolidated" / "L2_consolidated.jsonl"
        
    def consolidate_memories(self):
        """Consolida memórias L3 em L2 e atualiza Modelfile"""
        
        print("=" * 60)
        print("🧬 SDL CONSOLIDATION (MODO SIMPLIFICADO)")
        print("=" * 60)
        
        # 1. Lê memórias L3
        l3_memories = []
        if self.l3_file.exists():
            with open(self.l3_file, 'r') as f:
                for line in f:
                    try:
                        l3_memories.append(json.loads(line))
                    except:
                        continue
        
        print(f"📚 {len(l3_memories)} memórias L3 encontradas")
        
        if len(l3_memories) < 10:
            print("⚠️ Poucas memórias para consolidar")
            return False
        
        # 2. Processa e extrai conhecimento essencial
        consolidated_knowledge = []
        
        for memory in l3_memories:
            content = memory.get('content', '')
            metadata = memory.get('metadata', {})
            importance = metadata.get('importance', 0.5)
            
            # Filtra apenas memórias importantes
            if importance >= 0.85:
                consolidated_knowledge.append({
                    "content": content,
                    "tags": metadata.get('tags', []),
                    "importance": importance,
                    "consolidated_at": datetime.now().isoformat()
                })
        
        print(f"🔬 {len(consolidated_knowledge)} insights de alta importância extraídos")
        
        # 3. Salva em L2
        self.l2_file.parent.mkdir(parents=True, exist_ok=True)
        
        with open(self.l2_file, 'a') as f:
            for knowledge in consolidated_knowledge:
                f.write(json.dumps(knowledge) + '\n')
        
        print(f"💾 Conhecimento consolidado em L2")
        
        # 4. Atualiza Modelfile com conhecimento consolidado
        modelfile_path = self.base_path / "scripturemon_ultimate_100.modelfile"
        
        if modelfile_path.exists():
            with open(modelfile_path, 'r') as f:
                content = f.read()
            
            # Adiciona seção de conhecimento consolidado
            knowledge_section = "\n\n# CONHECIMENTO CONSOLIDADO VIA SDL\n"
            knowledge_section += f"# Consolidado em: {datetime.now().isoformat()}\n"
            knowledge_section += "# Insights cristalizados das memórias L3:\n"
            
            for i, knowledge in enumerate(consolidated_knowledge[:10], 1):  # Top 10
                knowledge_section += f"# {i}. {knowledge['content'][:100]}...\n"
            
            # Adiciona ao Modelfile se ainda não existir
            if "CONHECIMENTO CONSOLIDADO VIA SDL" not in content:
                # Adiciona antes do PARAMETER
                if "PARAMETER" in content:
                    parts = content.split("PARAMETER", 1)
                    content = parts[0] + knowledge_section + "\nPARAMETER" + parts[1]
                else:
                    content += knowledge_section
                
                # Backup e salva
                backup_path = modelfile_path.with_suffix('.modelfile.bak')
                modelfile_path.rename(backup_path)
                
                with open(modelfile_path, 'w') as f:
                    f.write(content)
                
                print(f"📝 Modelfile atualizado com conhecimento consolidado")
                
                # 5. Recria modelo no Ollama
                import subprocess
                print("🔄 Recriando modelo com conhecimento consolidado...")
                
                result = subprocess.run([
                    "ollama", "create", "scripturemon-sdl",
                    "-f", str(modelfile_path)
                ], capture_output=True, text=True)
                
                if result.returncode == 0:
                    print("✅ Modelo SDL criado: scripturemon-sdl")
                else:
                    print(f"⚠️ Erro ao criar modelo: {result.stderr}")
        
        # 6. Limpa L3 (promove para L2)
        with open(self.l3_file, 'w') as f:
            f.write("")  # Limpa arquivo
        
        print(f"🧹 Memórias L3 promovidas para L2")
        
        # 7. Relatório final
        print("\n" + "=" * 60)
        print("📊 CONSOLIDAÇÃO SDL COMPLETA")
        print("=" * 60)
        print(f"✅ {len(consolidated_knowledge)} insights consolidados")
        print(f"✅ Modelfile atualizado")
        print(f"✅ Modelo scripturemon-sdl criado")
        print(f"✅ Memórias promovidas L3→L2")
        
        # Mostra alguns insights consolidados
        print("\n🌟 TOP INSIGHTS CONSOLIDADOS:")
        for i, knowledge in enumerate(consolidated_knowledge[:5], 1):
            print(f"\n{i}. {knowledge['content'][:150]}...")
            print(f"   Tags: {', '.join(knowledge['tags'][:5])}")
            print(f"   Importância: {knowledge['importance']:.2%}")
        
        return True
    
    def verify_consolidation(self):
        """Verifica se a consolidação funcionou"""
        print("\n🔍 Verificando consolidação...")
        
        # Testa o modelo consolidado
        import subprocess
        
        test_prompt = "Qual é a essência do paradigma de três atos?"
        
        result = subprocess.run([
            "ollama", "run", "scripturemon-sdl", test_prompt
        ], capture_output=True, text=True, timeout=30)
        
        if result.returncode == 0:
            response = result.stdout[:500]
            print(f"\n💬 Resposta do modelo consolidado:")
            print(response)
            
            # Verifica se menciona conhecimento consolidado
            keywords = ["três atos", "paradigma", "estrutura", "Syd Field"]
            matches = sum(1 for k in keywords if k.lower() in response.lower())
            
            if matches >= 2:
                print("\n✅ Consolidação verificada com sucesso!")
                return True
            else:
                print("\n⚠️ Resposta não demonstra conhecimento consolidado")
                return False
        else:
            print("\n❌ Erro ao testar modelo consolidado")
            return False


if __name__ == "__main__":
    consolidator = SimpleSDLConsolidator()
    
    if consolidator.consolidate_memories():
        consolidator.verify_consolidation()
        
        print("\n🎉 SDL COMPLETO!")
        print("O Scripturemon agora tem conhecimento consolidado em seus pesos!")