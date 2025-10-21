#!/usr/bin/env python3
"""
📚 CINEMA KNOWLEDGE - Sistema RAG com PDFs de Cinema
Integra 44 PDFs de roteiros, teoria e prática cinematográfica
"""

import os
import json
import hashlib
import pickle
from pathlib import Path
from typing import List, Dict, Optional, Tuple, Any
from datetime import datetime
import PyPDF2
import re

class CinemaKnowledge:
    """Sistema de conhecimento cinematográfico com RAG"""
    
    def __init__(self):
        self.base_path = Path(__file__).parent.parent.parent
        self.docs_path = self.base_path / "data" / "cinema_knowledge" / "pdfs"
        self.index_path = self.base_path / "data" / "cinema_knowledge" / "indices"
        self.cache_path = self.base_path / "data" / "cinema_knowledge" / "cache"
        
        # Criar diretórios
        self.index_path.mkdir(parents=True, exist_ok=True)
        self.cache_path.mkdir(parents=True, exist_ok=True)
        
        # Carregar ou criar índice
        self.index = self._load_or_create_index()
        self.documents = {}
        self.embeddings = {}
        
        print(f"✅ Cinema Knowledge: {len(self.index)} PDFs indexados")
        
    def _load_or_create_index(self) -> Dict:
        """Carrega ou cria índice de documentos"""
        index_file = self.index_path / "main_index.json"
        
        if index_file.exists():
            with open(index_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        else:
            return self._create_index()
            
    def _create_index(self) -> Dict:
        """Cria índice de todos os PDFs"""
        index = {}
        pdf_files = list(self.docs_path.glob("**/*.pdf"))
        
        print(f"📚 Indexando {len(pdf_files)} PDFs...")
        
        for pdf_path in pdf_files:
            try:
                # Criar ID único
                doc_id = hashlib.md5(str(pdf_path).encode()).hexdigest()[:12]
                
                # Categorizar
                category = "general"
                if "teoria" in str(pdf_path).lower():
                    category = "theory"
                elif "mestres" in str(pdf_path).lower():
                    category = "masters"
                elif "criador" in str(pdf_path).lower():
                    category = "creator"
                    
                index[doc_id] = {
                    "path": str(pdf_path.relative_to(self.base_path)),
                    "name": pdf_path.stem,
                    "category": category,
                    "size": pdf_path.stat().st_size,
                    "indexed_at": datetime.now().isoformat(),
                    "pages": self._count_pdf_pages(pdf_path)
                }
                
            except Exception as e:
                print(f"  ⚠️ Erro indexando {pdf_path.name}: {str(e)[:50]}")
                
        # Salvar índice
        index_file = self.index_path / "main_index.json"
        with open(index_file, 'w', encoding='utf-8') as f:
            json.dump(index, f, indent=2)
            
        return index
        
    def _count_pdf_pages(self, pdf_path: Path) -> int:
        """Conta páginas de um PDF"""
        try:
            with open(pdf_path, 'rb') as f:
                reader = PyPDF2.PdfReader(f)
                return len(reader.pages)
        except:
            return 0
            
    def extract_text_from_pdf(self, pdf_path: Path, max_pages: int = 10) -> str:
        """Extrai texto de um PDF"""
        cache_key = hashlib.md5(f"{pdf_path}_{max_pages}".encode()).hexdigest()
        cache_file = self.cache_path / f"{cache_key}.txt"
        
        # Verificar cache
        if cache_file.exists():
            with open(cache_file, 'r', encoding='utf-8') as f:
                return f.read()
                
        text = ""
        try:
            with open(pdf_path, 'rb') as f:
                reader = PyPDF2.PdfReader(f)
                pages_to_read = min(len(reader.pages), max_pages)
                
                for i in range(pages_to_read):
                    page = reader.pages[i]
                    text += page.extract_text() + "\n\n"
                    
            # Limpar texto
            text = self._clean_text(text)
            
            # Salvar no cache
            with open(cache_file, 'w', encoding='utf-8') as f:
                f.write(text)
                
        except Exception as e:
            print(f"  ❌ Erro extraindo texto de {pdf_path.name}: {str(e)[:50]}")
            
        return text
        
    def _clean_text(self, text: str) -> str:
        """Limpa texto extraído"""
        # Remover múltiplos espaços
        text = re.sub(r'\s+', ' ', text)
        # Remover caracteres especiais problemáticos
        text = re.sub(r'[^\w\s\.\,\;\:\!\?\-\(\)\[\]\"\']+', ' ', text)
        # Limitar tamanho
        if len(text) > 10000:
            text = text[:10000] + "..."
        return text.strip()
        
    def search(self, query: str, limit: int = 5, category: Optional[str] = None) -> List[Dict]:
        """Busca nos PDFs indexados"""
        results = []
        query_lower = query.lower()
        
        for doc_id, doc_info in self.index.items():
            # Filtrar por categoria se especificada
            if category and doc_info["category"] != category:
                continue
                
            # Buscar no nome do arquivo
            if query_lower in doc_info["name"].lower():
                score = 1.0
            else:
                # Buscar no conteúdo (primeiro extrair)
                pdf_path = self.base_path / doc_info["path"]
                if pdf_path.exists():
                    text = self.extract_text_from_pdf(pdf_path, max_pages=5)
                    if query_lower in text.lower():
                        # Calcular score baseado em frequência
                        occurrences = text.lower().count(query_lower)
                        score = min(1.0, occurrences / 10)
                    else:
                        continue
                else:
                    continue
                    
            results.append({
                "doc_id": doc_id,
                "name": doc_info["name"],
                "category": doc_info["category"],
                "score": score,
                "pages": doc_info["pages"]
            })
            
        # Ordenar por score
        results.sort(key=lambda x: x["score"], reverse=True)
        
        return results[:limit]
        
    def get_relevant_context(self, query: str, max_context_length: int = 2000) -> str:
        """Obtém contexto relevante para uma query"""
        # Buscar documentos relevantes - usar palavras-chave individuais
        keywords = query.lower().split()
        all_results = []
        
        for keyword in keywords:
            results = self.search(keyword, limit=2)
            all_results.extend(results)
            
        # Remover duplicatas e ordenar por score
        seen = set()
        relevant_docs = []
        for doc in all_results:
            if doc["doc_id"] not in seen:
                seen.add(doc["doc_id"])
                relevant_docs.append(doc)
                
        relevant_docs.sort(key=lambda x: x["score"], reverse=True)
        relevant_docs = relevant_docs[:3]
        
        if not relevant_docs:
            # Fallback - pegar qualquer documento de teoria
            for doc_id, doc_info in self.index.items():
                if doc_info["category"] == "theory":
                    relevant_docs.append({
                        "doc_id": doc_id,
                        "name": doc_info["name"],
                        "category": doc_info["category"],
                        "score": 0.1
                    })
                    if len(relevant_docs) >= 1:
                        break
                        
        if not relevant_docs:
            return ""
            
        context_parts = []
        remaining_length = max_context_length
        
        for doc in relevant_docs:
            if remaining_length <= 0:
                break
                
            try:
                # Extrair texto relevante
                pdf_path = self.base_path / self.index[doc["doc_id"]]["path"]
                if pdf_path.exists():
                    text = self.extract_text_from_pdf(pdf_path, max_pages=3)
                    
                    if text:
                        # Encontrar trechos relevantes
                        sentences = text.split('.')
                        relevant_sentences = []
                        
                        # Buscar por cada palavra-chave
                        for keyword in keywords:
                            for sentence in sentences:
                                if keyword in sentence.lower() and len(sentence) > 20:
                                    relevant_sentences.append(sentence.strip())
                                    if len(relevant_sentences) >= 3:
                                        break
                                        
                        # Se não encontrou sentenças específicas, pegar algumas relevantes
                        if not relevant_sentences and sentences:
                            for sentence in sentences:
                                if len(sentence) > 30 and len(sentence) < 300:
                                    relevant_sentences.append(sentence.strip())
                                    if len(relevant_sentences) >= 3:
                                        break
                                        
                        if relevant_sentences:
                            # Adicionar ao contexto
                            doc_context = f"\n[Source: {doc['name'][:50]}]:\n"
                            doc_context += ". ".join(relevant_sentences[:3]) + "."
                            
                            if len(doc_context) <= remaining_length:
                                context_parts.append(doc_context)
                                remaining_length -= len(doc_context)
                            else:
                                context_parts.append(doc_context[:remaining_length])
                                break
            except Exception as e:
                print(f"  Erro extraindo contexto: {str(e)[:50]}")
                continue
                    
        return "\n".join(context_parts)
        
    def get_screenplay_examples(self, element: str = "dialogue") -> List[Dict]:
        """Obtém exemplos de elementos de roteiro"""
        examples = []
        
        # Mapear elementos para padrões de busca
        patterns = {
            "dialogue": [r"^\s*[A-Z]+\s*\n\s*\([^\)]*\)\s*\n", r"^\s*[A-Z]+\s*\n\s*[^\n]+"],
            "action": [r"^\s*EXT\.", r"^\s*INT\.", r"^\s*[A-Z][a-z]+\s+[a-z]+"],
            "character": [r"^\s*[A-Z]+\s*\([^\)]*\)", r"^\s*[A-Z]+\s*$"],
            "scene": [r"^\s*FADE IN:", r"^\s*CUT TO:", r"^\s*DISSOLVE TO:"]
        }
        
        # Buscar em roteiros mestres
        master_scripts = self.search("", limit=10, category="masters")
        
        for script in master_scripts[:5]:
            pdf_path = self.base_path / self.index[script["doc_id"]]["path"]
            if pdf_path.exists():
                text = self.extract_text_from_pdf(pdf_path, max_pages=10)
                
                # Buscar padrões
                for pattern in patterns.get(element, []):
                    matches = re.findall(pattern, text, re.MULTILINE)
                    if matches:
                        examples.append({
                            "source": script["name"],
                            "element": element,
                            "example": matches[0][:200],
                            "count": len(matches)
                        })
                        break
                        
        return examples[:5]
        
    def analyze_screenplay_structure(self, text: str) -> Dict:
        """Analisa estrutura de um roteiro"""
        analysis = {
            "pages": len(text) // 3000,  # Aproximação
            "scenes": 0,
            "dialogues": 0,
            "characters": set(),
            "locations": set(),
            "acts": []
        }
        
        # Contar cenas
        scene_headers = re.findall(r'^\s*(INT\.|EXT\.)\s+([^\n]+)', text, re.MULTILINE)
        analysis["scenes"] = len(scene_headers)
        
        # Extrair locações
        for _, location in scene_headers:
            analysis["locations"].add(location.strip())
            
        # Contar diálogos e personagens
        character_pattern = r'^\s*([A-Z][A-Z\s]+)\s*\n\s*(\([^\)]*\))?\s*\n\s*([^\n]+)'
        dialogues = re.findall(character_pattern, text, re.MULTILINE)
        
        analysis["dialogues"] = len(dialogues)
        for char, _, _ in dialogues:
            if len(char.strip()) < 30:  # Evitar falsos positivos
                analysis["characters"].add(char.strip())
                
        # Converter sets para listas
        analysis["characters"] = list(analysis["characters"])
        analysis["locations"] = list(analysis["locations"])
        
        # Detectar atos (aproximação)
        if "ACT I" in text or "ACT ONE" in text:
            analysis["acts"].append("Act I detected")
        if "ACT II" in text or "ACT TWO" in text:
            analysis["acts"].append("Act II detected")
        if "ACT III" in text or "ACT THREE" in text:
            analysis["acts"].append("Act III detected")
            
        return analysis
        
    def get_writing_tips(self, topic: str = "general") -> List[str]:
        """Obtém dicas de escrita baseadas nos PDFs de teoria"""
        tips = []
        
        # Buscar em PDFs de teoria
        theory_docs = self.search(topic, limit=3, category="theory")
        
        for doc in theory_docs:
            pdf_path = self.base_path / self.index[doc["doc_id"]]["path"]
            if pdf_path.exists():
                text = self.extract_text_from_pdf(pdf_path, max_pages=5)
                
                # Extrair frases que parecem dicas
                sentences = text.split('.')
                for sentence in sentences:
                    # Procurar padrões de dicas
                    if any(word in sentence.lower() for word in 
                           ["should", "must", "important", "essential", "key", "tip", "advice"]):
                        if 20 < len(sentence) < 200:
                            tips.append(sentence.strip() + ".")
                            
                    if len(tips) >= 10:
                        break
                        
        return tips[:5]
        
    def get_stats(self) -> Dict:
        """Retorna estatísticas do sistema"""
        stats = {
            "total_pdfs": len(self.index),
            "categories": {},
            "total_pages": 0,
            "total_size_mb": 0
        }
        
        for doc_info in self.index.values():
            category = doc_info["category"]
            stats["categories"][category] = stats["categories"].get(category, 0) + 1
            stats["total_pages"] += doc_info["pages"]
            stats["total_size_mb"] += doc_info["size"] / (1024 * 1024)
            
        stats["total_size_mb"] = round(stats["total_size_mb"], 2)
        
        return stats

# Singleton
_cinema_instance = None

def get_cinema_knowledge() -> CinemaKnowledge:
    """Retorna instância singleton do Cinema Knowledge"""
    global _cinema_instance
    if _cinema_instance is None:
        _cinema_instance = CinemaKnowledge()
    return _cinema_instance