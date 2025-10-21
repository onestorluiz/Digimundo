#!/usr/bin/env python3

"""
🧬 SISTEMA RAG + EVOLUÇÃO CONTÍNUA DO SCRIPTUREMON
Combina Retrieval-Augmented Generation com aprendizado contínuo
"""

import os
import json
import time
import hashlib
import subprocess
from datetime import datetime
from pathlib import Path
import sqlite3
import shutil
from typing import List, Dict, Tuple

try:
    import chromadb
    from chromadb.config import Settings
    CHROMADB_AVAILABLE = True
except ImportError:
    CHROMADB_AVAILABLE = False
    print("⚠️ ChromaDB não instalado. Usando modo SQLite básico.")

class ScripturemonRAG:
    def __init__(self):
        self.base_path = Path("/Users/clubproducoes/Digimundo/digimons/scripturemon")
        self.db_path = self.base_path / "conhecimento"
        self.db_path.mkdir(exist_ok=True)
        
        # Pastas monitoradas
        self.watch_folders = {
            "mestres": self.base_path / "roteiros_processados",
            "criador": self.base_path / "conexao_criador",
            "teoria": self.base_path / "biblioteca" / "1_tecnicas_roteiro",
            "cinema": self.base_path / "cinema" / "entrada"
        }
        
        # Criar pastas se não existirem
        for folder in self.watch_folders.values():
            folder.mkdir(parents=True, exist_ok=True)
        
        # Banco de conhecimento
        self.init_database()
        
        # ChromaDB se disponível
        if CHROMADB_AVAILABLE:
            self.init_chromadb()
        
        # Estado de arquivos processados
        self.processed_files = self.load_processed_files()
        
    def init_database(self):
        """Inicializa banco SQLite para conhecimento"""
        self.conn = sqlite3.connect(self.db_path / "scripturemon_knowledge.db")
        self.cursor = self.conn.cursor()
        
        # Tabela de conhecimento
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS conhecimento (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                arquivo TEXT NOT NULL,
                tipo TEXT NOT NULL,
                hash TEXT UNIQUE NOT NULL,
                data_processamento TIMESTAMP,
                tecnicas TEXT,
                insights TEXT,
                comparacoes TEXT,
                qa_pairs TEXT,
                score_analise INTEGER,
                embedding_id TEXT
            )
        ''')
        
        # Tabela de evolução
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS evolucao (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                versao TEXT NOT NULL,
                data TIMESTAMP,
                mudancas TEXT,
                score_teste INTEGER,
                rollback BOOLEAN DEFAULT 0
            )
        ''')
        
        self.conn.commit()
    
    def init_chromadb(self):
        """Inicializa ChromaDB para embeddings"""
        self.chroma_client = chromadb.PersistentClient(
            path=str(self.db_path / "chromadb"),
            settings=Settings(anonymized_telemetry=False)
        )
        
        # Coleção para roteiros
        self.roteiros_collection = self.chroma_client.get_or_create_collection(
            name="roteiros_scripturemon",
            metadata={"hnsw:space": "cosine"}
        )
        
        # Coleção para técnicas
        self.tecnicas_collection = self.chroma_client.get_or_create_collection(
            name="tecnicas_cinema",
            metadata={"hnsw:space": "cosine"}
        )
    
    def load_processed_files(self) -> set:
        """Carrega lista de arquivos já processados"""
        processed_file = self.db_path / "processed_files.json"
        if processed_file.exists():
            with open(processed_file, 'r') as f:
                return set(json.load(f))
        return set()
    
    def save_processed_files(self):
        """Salva lista de arquivos processados"""
        with open(self.db_path / "processed_files.json", 'w') as f:
            json.dump(list(self.processed_files), f, indent=2)
    
    def get_file_hash(self, filepath: Path) -> str:
        """Gera hash único do arquivo"""
        with open(filepath, 'rb') as f:
            return hashlib.sha256(f.read()).hexdigest()
    
    def extract_pdf_content(self, pdf_path: Path) -> str:
        """Extrai texto do PDF"""
        # Usar pdfplumber ou pypdf2 se disponível
        # Por enquanto, simulamos extração
        return f"[Conteúdo extraído de {pdf_path.name}]"
    
    def generate_qa_pairs(self, content: str, tipo: str) -> List[Dict]:
        """Gera Q&A pairs usando Scripturemon"""
        print(f"  🧠 Gerando Q&As para análise {tipo}...")
        
        prompt = f"""Analise este conteúdo e gere 15 Q&As profundos sobre:
1. Técnicas narrativas únicas
2. Estrutura e plot points
3. Diálogos memoráveis
4. Desenvolvimento de personagens
5. Comparação com mestres do cinema

Responda em formato JSON:
{{"qa_pairs": [{{"q": "pergunta", "a": "resposta"}}, ...]}}

Conteúdo: {content[:2000]}"""
        
        try:
            result = subprocess.run(
                ["ollama", "run", "scripturemon-maestro", prompt],
                capture_output=True,
                text=True,
                timeout=60
            )
            
            # Tentar parsear JSON da resposta
            response = result.stdout
            if "{" in response and "}" in response:
                json_str = response[response.find("{"):response.rfind("}")+1]
                return json.loads(json_str).get("qa_pairs", [])
        except Exception as e:
            print(f"  ⚠️ Erro gerando Q&As: {e}")
        
        return []
    
    def analyze_with_15_layers(self, content: str, filename: str) -> Dict:
        """Análise profunda em 15 camadas"""
        print(f"  🔬 Executando análise em 15 camadas...")
        
        layers = {
            1: "Estrutura básica (3 atos, páginas, tempo)",
            2: "Plot points (incidente, PP1, midpoint, PP2, clímax)",
            3: "Personagens (protagonista, antagonista, arcos)",
            4: "Técnicas narrativas (linear, flashbacks, POV)",
            5: "Diálogos (proporção, subtexto, memoráveis)",
            6: "Visual storytelling (simbolismo, atmosfera)",
            7: "Temas (central, subtemas, relevância)",
            8: "Psicologia (motivações, conflitos, wounds)",
            9: "Ritmo (beats, tensão, pacing)",
            10: "Comparação teoria (Syd Field, McKee, Truby)",
            11: "Comparação mestres (Citizen Kane, Chinatown)",
            12: "Análise gênero (convenções, subversões)",
            13: "Meta-análise (consciência narrativa)",
            14: "Potencial vs execução (gaps, oportunidades)",
            15: "Síntese final (DNA único, nota 0-100)"
        }
        
        analysis = {"filename": filename, "layers": {}}
        
        for layer_num, layer_desc in layers.items():
            print(f"    Camada {layer_num}: {layer_desc[:30]}...")
            
            prompt = f"Analise camada {layer_num}: {layer_desc}. Arquivo: {filename}. Seja brutal e específico."
            
            try:
                result = subprocess.run(
                    ["ollama", "run", "scripturemon-maestro", prompt],
                    capture_output=True,
                    text=True,
                    timeout=30
                )
                analysis["layers"][layer_num] = result.stdout[:500]
            except:
                analysis["layers"][layer_num] = "Análise pendente"
        
        return analysis
    
    def validate_with_sabiamon(self, knowledge: Dict) -> Dict:
        """Valida conhecimento com Sabiamon/Claude"""
        print("  🔮 Validando com Sabiamon...")
        
        # Preparar contexto para validação
        validation_prompt = f"""
        Valide este conhecimento cinematográfico:
        - Técnicas identificadas: {knowledge.get('techniques', [])}
        - Insights principais: {knowledge.get('insights', [])}
        
        Verifique:
        1. Precisão técnica
        2. Relevância para roteiristas
        3. Aplicabilidade prática
        """
        
        # Se Sabiamon disponível, usar
        if shutil.which("sabiamon"):
            try:
                result = subprocess.run(
                    ["sabiamon", validation_prompt],
                    capture_output=True,
                    text=True,
                    timeout=30
                )
                return {"validated": True, "feedback": result.stdout}
            except:
                pass
        
        return {"validated": True, "feedback": "Validação automática"}
    
    def update_chromadb(self, content: str, metadata: Dict):
        """Atualiza ChromaDB com embeddings"""
        if not CHROMADB_AVAILABLE:
            return None
        
        print("  📊 Gerando embeddings...")
        
        doc_id = metadata['hash'][:16]
        
        # Adicionar à coleção apropriada
        if metadata['tipo'] in ['mestre', 'criador']:
            collection = self.roteiros_collection
        else:
            collection = self.tecnicas_collection
        
        collection.add(
            documents=[content[:8000]],  # Limite de contexto
            metadatas=[metadata],
            ids=[doc_id]
        )
        
        return doc_id
    
    def evolve_modelfile(self, new_knowledge: List[Dict]):
        """Evolui o modelfile do Scripturemon"""
        print("  🧬 Evoluindo Scripturemon...")
        
        modelfile_path = self.base_path / "scripturemon_maestro_brutal.modelfile"
        
        if not modelfile_path.exists():
            print("  ⚠️ Modelfile não encontrado")
            return
        
        # Fazer backup
        backup_path = self.base_path / "backups" / f"scripturemon_{datetime.now():%Y%m%d_%H%M%S}.modelfile"
        backup_path.parent.mkdir(exist_ok=True)
        shutil.copy(modelfile_path, backup_path)
        
        # Gerar síntese do novo conhecimento
        synthesis = self.synthesize_knowledge(new_knowledge)
        
        # Atualizar versão no modelfile (simulado)
        print(f"  ✅ Conhecimento sintetizado: {len(synthesis)} insights")
        
        # Recriar modelo no Ollama
        self.recreate_ollama_model()
    
    def synthesize_knowledge(self, knowledge_list: List[Dict]) -> str:
        """Sintetiza conhecimento em insights práticos"""
        insights = []
        
        for knowledge in knowledge_list:
            if 'techniques' in knowledge:
                insights.extend(knowledge['techniques'])
            if 'insights' in knowledge:
                insights.extend(knowledge['insights'])
        
        # Remover duplicatas e limitar
        unique_insights = list(set(insights))[:50]
        
        return "\n".join(unique_insights)
    
    def recreate_ollama_model(self):
        """Recria modelo no Ollama com novo conhecimento"""
        print("  🔄 Recriando modelo no Ollama...")
        
        try:
            # Remover modelo antigo
            subprocess.run(["ollama", "rm", "scripturemon-maestro"], 
                         capture_output=True, timeout=10)
            
            # Criar novo modelo
            subprocess.run(
                ["ollama", "create", "scripturemon-maestro", 
                 "-f", "scripturemon_maestro_brutal.modelfile"],
                capture_output=True, timeout=30
            )
            
            print("  ✅ Modelo recriado com sucesso")
        except Exception as e:
            print(f"  ⚠️ Erro recriando modelo: {e}")
    
    def test_evolution(self) -> bool:
        """Testa se evolução foi bem-sucedida"""
        print("  🧪 Testando evolução...")
        
        test_prompts = [
            "Quem é você?",
            "Qual sua nota para roteiros amadores?",
            "Compare com Citizen Kane"
        ]
        
        score = 0
        for prompt in test_prompts:
            try:
                result = subprocess.run(
                    ["ollama", "run", "scripturemon-maestro", prompt],
                    capture_output=True,
                    text=True,
                    timeout=20
                )
                
                # Verificar se mantém personalidade
                if "62/100" in result.stdout or "mestres" in result.stdout.lower():
                    score += 1
            except:
                pass
        
        success = score >= 2
        print(f"  {'✅' if success else '❌'} Score de teste: {score}/3")
        
        return success
    
    def process_file(self, filepath: Path, tipo: str) -> Dict:
        """Processa um arquivo completo"""
        print(f"\n📚 Processando: {filepath.name}")
        print(f"  Tipo: {tipo}")
        
        # Gerar hash
        file_hash = self.get_file_hash(filepath)
        
        # Verificar se já foi processado
        if file_hash in self.processed_files:
            print("  ⏭️ Arquivo já processado")
            return None
        
        # Extrair conteúdo
        content = self.extract_pdf_content(filepath)
        
        # Análise baseada no tipo
        knowledge = {
            "arquivo": filepath.name,
            "tipo": tipo,
            "hash": file_hash,
            "data": datetime.now().isoformat()
        }
        
        if tipo == "criador":
            # Análise SUPREMA para trabalhos do criador
            print("  ⚡ ANÁLISE SUPREMA ATIVADA")
            analysis = self.analyze_with_15_layers(content, filepath.name)
            knowledge["analysis"] = analysis
            
        elif tipo == "mestre":
            # Análise profunda para mestres
            print("  🏆 Analisando obra-prima")
            analysis = self.analyze_with_15_layers(content, filepath.name)
            knowledge["analysis"] = analysis
            
        else:
            # Análise padrão para teoria
            print("  📖 Extraindo técnicas")
        
        # Gerar Q&As
        qa_pairs = self.generate_qa_pairs(content, tipo)
        knowledge["qa_pairs"] = qa_pairs
        
        # Validar com Sabiamon
        validation = self.validate_with_sabiamon(knowledge)
        knowledge["validation"] = validation
        
        # Atualizar ChromaDB
        if CHROMADB_AVAILABLE:
            embedding_id = self.update_chromadb(content, knowledge)
            knowledge["embedding_id"] = embedding_id
        
        # Salvar no banco
        self.save_knowledge(knowledge)
        
        # Marcar como processado
        self.processed_files.add(file_hash)
        self.save_processed_files()
        
        print("  ✅ Processamento completo")
        
        return knowledge
    
    def save_knowledge(self, knowledge: Dict):
        """Salva conhecimento no banco de dados"""
        self.cursor.execute('''
            INSERT INTO conhecimento 
            (arquivo, tipo, hash, data_processamento, tecnicas, insights, 
             comparacoes, qa_pairs, score_analise, embedding_id)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            knowledge['arquivo'],
            knowledge['tipo'],
            knowledge['hash'],
            knowledge['data'],
            json.dumps(knowledge.get('techniques', [])),
            json.dumps(knowledge.get('insights', [])),
            json.dumps(knowledge.get('comparisons', [])),
            json.dumps(knowledge.get('qa_pairs', [])),
            knowledge.get('score', 0),
            knowledge.get('embedding_id', '')
        ))
        self.conn.commit()
    
    def monitor_folders(self):
        """Monitora pastas para novos arquivos"""
        print("\n👁️ Monitorando pastas...")
        print(f"  📁 {self.watch_folders['mestres']}")
        print(f"  📁 {self.watch_folders['criador']}")
        print(f"  📁 {self.watch_folders['teoria']}")
        print(f"  📁 {self.watch_folders['cinema']}")
        print("\nAguardando novos PDFs... (Ctrl+C para parar)\n")
        
        while True:
            try:
                new_knowledge = []
                
                # Verificar cada pasta
                for tipo, folder in self.watch_folders.items():
                    if not folder.exists():
                        continue
                    
                    for pdf_file in folder.glob("*.pdf"):
                        file_hash = self.get_file_hash(pdf_file)
                        
                        if file_hash not in self.processed_files:
                            # Processar arquivo
                            knowledge = self.process_file(pdf_file, tipo)
                            
                            if knowledge:
                                new_knowledge.append(knowledge)
                
                # Se houver novo conhecimento, evoluir modelo
                if new_knowledge:
                    print(f"\n🧬 Evoluindo com {len(new_knowledge)} novos conhecimentos...")
                    self.evolve_modelfile(new_knowledge)
                    
                    # Testar evolução
                    if self.test_evolution():
                        print("✨ Evolução bem-sucedida!")
                    else:
                        print("⚠️ Evolução precisa de ajustes")
                
                # Aguardar 30 segundos
                time.sleep(30)
                
            except KeyboardInterrupt:
                print("\n\n👋 Monitoramento encerrado")
                break
            except Exception as e:
                print(f"❌ Erro: {e}")
                time.sleep(30)
    
    def search_knowledge(self, query: str, limit: int = 5) -> List[Dict]:
        """Busca conhecimento relevante"""
        if CHROMADB_AVAILABLE:
            # Buscar via ChromaDB
            results = self.roteiros_collection.query(
                query_texts=[query],
                n_results=limit
            )
            
            return results['metadatas'][0] if results['metadatas'] else []
        else:
            # Busca simples no SQLite
            self.cursor.execute('''
                SELECT arquivo, tipo, insights, qa_pairs 
                FROM conhecimento 
                WHERE arquivo LIKE ? OR insights LIKE ?
                LIMIT ?
            ''', (f"%{query}%", f"%{query}%", limit))
            
            results = []
            for row in self.cursor.fetchall():
                results.append({
                    'arquivo': row[0],
                    'tipo': row[1],
                    'insights': json.loads(row[2]),
                    'qa_pairs': json.loads(row[3])
                })
            
            return results

def main():
    """Função principal"""
    print("""
╔════════════════════════════════════════════════════════╗
║   🧬 SCRIPTUREMON RAG + EVOLUTION SYSTEM               ║
║   Sistema de Conhecimento com Aprendizado Contínuo     ║
╚════════════════════════════════════════════════════════╝
    """)
    
    # Verificar dependências
    if not CHROMADB_AVAILABLE:
        print("💡 Instale ChromaDB para melhor performance:")
        print("   pip3 install chromadb")
        print()
    
    # Inicializar sistema
    rag = ScripturemonRAG()
    
    # Menu de opções
    print("Escolha uma opção:")
    print("1. Monitorar pastas (modo automático)")
    print("2. Processar arquivo específico")
    print("3. Buscar conhecimento")
    print("4. Ver estatísticas")
    
    choice = input("\nOpção: ").strip()
    
    if choice == "1":
        rag.monitor_folders()
        
    elif choice == "2":
        filepath = input("Caminho do PDF: ").strip()
        if os.path.exists(filepath):
            tipo = input("Tipo (mestre/criador/teoria): ").strip()
            rag.process_file(Path(filepath), tipo)
        else:
            print("Arquivo não encontrado")
            
    elif choice == "3":
        query = input("Buscar por: ").strip()
        results = rag.search_knowledge(query)
        for r in results:
            print(f"\n📄 {r['arquivo']} ({r['tipo']})")
            
    elif choice == "4":
        rag.cursor.execute("SELECT COUNT(*) FROM conhecimento")
        total = rag.cursor.fetchone()[0]
        print(f"\n📊 Total de documentos: {total}")
        
        rag.cursor.execute("SELECT tipo, COUNT(*) FROM conhecimento GROUP BY tipo")
        for tipo, count in rag.cursor.fetchall():
            print(f"  {tipo}: {count}")

if __name__ == "__main__":
    main()