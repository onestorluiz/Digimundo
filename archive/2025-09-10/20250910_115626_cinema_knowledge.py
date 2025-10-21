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
        
        # Múltiplos caminhos para buscar PDFs - SISTEMA ROBUSTO
        self.pdf_search_paths = [
            self.base_path / "data" / "cinema_pdfs",  # Symlink
            self.base_path / "data" / "cinema_knowledge" / "pdfs",  # Path original
            Path("/Users/clubproducoes/Digimundo/digimons/scripturemon_backup_20250827_165659/cinema"),  # Backup
            Path("/Users/clubproducoes/Digimundo/cinema"),  # Alternativo
            Path("/Users/clubproducoes/Desktop/ROTEIROS"),  # Desktop do usuário
            Path("/Users/clubproducoes/Documents/ROTEIROS"),  # Documents do usuário
        ]
        
        # Encontrar o primeiro path válido com PDFs
        self.docs_path = None
        for path in self.pdf_search_paths:
            if path.exists():
                pdf_count = len(list(path.glob("**/*.pdf")))
                if pdf_count > 0:
                    self.docs_path = path
                    print(f"📚 PDFs encontrados em: {path} ({pdf_count} arquivos)")
                    break
        
        # Fallback se nenhum path tiver PDFs
        if self.docs_path is None:
            self.docs_path = self.pdf_search_paths[0]
            print(f"⚠️ Nenhum PDF encontrado. Usando path padrão: {self.docs_path}")
        
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
        """Cria índice de todos os PDFs - ROBUSTO com múltiplos paths"""
        index = {}
        pdf_files = []
        
        # Buscar PDFs em TODOS os paths disponíveis
        for search_path in self.pdf_search_paths:
            if search_path.exists():
                found = list(search_path.glob("**/*.pdf"))
                pdf_files.extend(found)
                if found:
                    print(f"  📂 {len(found)} PDFs em {search_path.name}")
        
        # Adicionar roteiro SONHOS SEM LEMBRANÇAS se existir
        sonhos_paths = [
            Path("/Users/clubproducoes/Desktop/SONHOS_SEM_LEMBRANCAS.pdf"),
            Path("/Users/clubproducoes/Documents/SONHOS_SEM_LEMBRANCAS.pdf"),
            Path("/Users/clubproducoes/Digimundo/SONHOS_SEM_LEMBRANCAS.pdf"),
        ]
        
        for sonhos_path in sonhos_paths:
            if sonhos_path.exists() and sonhos_path not in pdf_files:
                pdf_files.append(sonhos_path)
                print(f"  🎬 Roteiro do usuário encontrado: {sonhos_path.name}")
        
        # Remover duplicatas
        pdf_files = list(set(pdf_files))
        
        print(f"📚 Indexando {len(pdf_files)} PDFs únicos...")
        
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
        """Extrai texto de um PDF com fallback múltiplo"""
        # --- FixPack:S4 begin (pdf extraction) ---
        import subprocess
        
        cache_key = hashlib.md5(f"{pdf_path}_{max_pages}".encode()).hexdigest()
        cache_file = self.cache_path / f"{cache_key}.txt"
        
        # Verificar cache
        if cache_file.exists():
            with open(cache_file, 'r', encoding='utf-8') as f:
                cached_text = f.read()
                if cached_text and len(cached_text.strip()) > 20:
                    return cached_text
                
        text = ""
        extraction_method = "none"
        
        # 1) Tentar PyPDF2 primeiro
        try:
            with open(pdf_path, 'rb') as f:
                reader = PyPDF2.PdfReader(f)
                pages_to_read = min(len(reader.pages), max_pages)
                
                for i in range(pages_to_read):
                    page = reader.pages[i]
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n\n"
                
                if text and len(text.strip()) > 20:
                    extraction_method = "pypdf2"
        except Exception as e:
            print(f"  ⚠️ PyPDF2 falhou para {pdf_path.name}: {str(e)[:30]}")
            
        # 2) Se texto vazio ou muito pequeno, tentar pdfminer.six
        if not text or len(text.strip()) < 20:
            try:
                from pdfminer.high_level import extract_text as pdfm_extract
                text = pdfm_extract(str(pdf_path)) or ""
                if text and len(text.strip()) > 20:
                    extraction_method = "pdfminer"
            except ImportError:
                print(f"  ℹ️ pdfminer.six não instalado")
            except Exception as e:
                print(f"  ⚠️ pdfminer falhou: {str(e)[:30]}")
                
        # 3) Se ainda vazio, tentar pdftotext CLI
        if not text or len(text.strip()) < 20:
            try:
                result = subprocess.run(
                    ["pdftotext", str(pdf_path), "-"],
                    capture_output=True,
                    text=True,
                    timeout=20
                )
                if result.returncode == 0 and result.stdout.strip():
                    text = result.stdout
                    extraction_method = "pdftotext"
            except FileNotFoundError:
                print(f"  ℹ️ pdftotext não instalado (brew install poppler)")
            except subprocess.TimeoutExpired:
                print(f"  ⚠️ pdftotext timeout")
            except Exception as e:
                print(f"  ⚠️ pdftotext falhou: {str(e)[:30]}")
                
        # Log se ainda vazio
        if not text or len(text.strip()) < 20:
            # Registrar no log
            log_dir = self.base_path / "reports" / "harmony_vFinal" / "fixpack" / "phaseS4_pdf"
            log_dir.mkdir(parents=True, exist_ok=True)
            log_file = log_dir / "extraction_failures.log"
            
            with open(log_file, 'a', encoding='utf-8') as f:
                f.write(f"{datetime.now().isoformat()} - {pdf_path.name}: ")
                f.write(f"No extractable text (likely needs OCR or is image-only PDF)\n")
            
            print(f"  ❌ {pdf_path.name}: Sem texto extraível (precisa OCR?)")
            extraction_method = "failed"
        else:
            print(f"  ✅ {pdf_path.name}: Extraído via {extraction_method} ({len(text)} chars)")
            
        # Limpar texto se houver
        if text:
            text = self._clean_text(text)
            
            # Salvar no cache
            try:
                with open(cache_file, 'w', encoding='utf-8') as f:
                    f.write(text)
            except:
                pass
                
        return text or ""
        # --- FixPack:S4 end (pdf extraction) ---
        
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
        """Analisa estrutura de um roteiro - PARSER ROBUSTO E COMPLETO"""
        analysis = {
            "pages": max(1, len(text) // 3000),  # ~3000 chars por página
            "scenes": 0,
            "dialogues": 0,
            "characters": set(),
            "locations": set(),
            "acts": [],
            "action_lines": 0,
            "transitions": 0,
            "parentheticals": 0,
            "scene_types": {"INT": 0, "EXT": 0, "INT/EXT": 0},
            "time_of_day": {"DAY": 0, "NIGHT": 0, "DAWN": 0, "DUSK": 0}
        }
        
        # PARSER ROBUSTO DE CENAS - múltiplos formatos
        scene_patterns = [
            r'^\s*(INT\.|EXT\.|INT/EXT\.|I/E\.)\s*([^\n-]+?)(?:\s*[-–]\s*([^\n]+))?$',  # Formato padrão
            r'^\s*(INTERIOR|EXTERIOR)\s+([^\n-]+?)(?:\s*[-–]\s*([^\n]+))?$',  # Formato expandido
            r'^\s*CENA\s+\d+\s*[-–]\s*(INT\.|EXT\.)\s*([^\n]+)$',  # Formato brasileiro
            r'^([0-9]+\.)\s*(INT\.|EXT\.)\s*([^\n]+)$'  # Formato numerado
        ]
        
        all_scenes = []
        for pattern in scene_patterns:
            scenes = re.findall(pattern, text, re.MULTILINE | re.IGNORECASE)
            all_scenes.extend(scenes)
        
        # Processar cenas encontradas
        for scene in all_scenes:
            if len(scene) >= 2:
                # Tipo de cena
                scene_type = scene[0].upper()
                if 'INT' in scene_type:
                    analysis["scene_types"]["INT"] += 1
                elif 'EXT' in scene_type:
                    analysis["scene_types"]["EXT"] += 1
                else:
                    analysis["scene_types"]["INT/EXT"] += 1
                
                # Locação
                location = scene[1] if len(scene) > 1 else ""
                if location:
                    analysis["locations"].add(location.strip()[:50])  # Limitar tamanho
                
                # Tempo do dia
                time_part = scene[2] if len(scene) > 2 else scene[1]
                if time_part:
                    time_upper = time_part.upper()
                    if 'DAY' in time_upper or 'DIA' in time_upper:
                        analysis["time_of_day"]["DAY"] += 1
                    elif 'NIGHT' in time_upper or 'NOITE' in time_upper:
                        analysis["time_of_day"]["NIGHT"] += 1
                    elif 'DAWN' in time_upper or 'AMANHECER' in time_upper:
                        analysis["time_of_day"]["DAWN"] += 1
                    elif 'DUSK' in time_upper or 'ENTARDECER' in time_upper:
                        analysis["time_of_day"]["DUSK"] += 1
        
        analysis["scenes"] = len(all_scenes)
        
        # PARSER ROBUSTO DE PERSONAGENS E DIÁLOGOS
        # Padrão 1: Personagem em maiúsculas seguido de diálogo
        dialogue_patterns = [
            r'^([A-Z][A-Z\s\.\-]{1,30})(?:\s*\([^\)]*\))?\s*\n(?!\s*INT\.|EXT\.)([^\n]+)',  # Padrão americano
            r'^([A-Z][A-Z\s\.\-]{1,30})\s*:\s*([^\n]+)',  # Padrão com dois pontos
            r'^\s{10,40}([A-Z][A-Z\s\.\-]{1,30})\s*\n\s{5,}([^\n]+)'  # Padrão com indentação
        ]
        
        all_dialogues = []
        for pattern in dialogue_patterns:
            dialogues = re.findall(pattern, text, re.MULTILINE)
            all_dialogues.extend(dialogues)
        
        for char, dialogue in all_dialogues:
            char = char.strip()
            # Filtrar falsos positivos e cabeçalhos de cena
            if (len(char) > 1 and len(char) < 30 and 
                not any(skip in char for skip in ['FADE', 'CUT', 'DISSOLVE', 'THE END', 'INT.', 'EXT.', 'INT/', 'EXT/']) and
                not re.match(r'^(INT|EXT)', char)):
                analysis["characters"].add(char)
                analysis["dialogues"] += 1
        
        # Contar parentéticos (direções de ator)
        parentheticals = re.findall(r'^\s*\([^\)]+\)\s*$', text, re.MULTILINE)
        analysis["parentheticals"] = len(parentheticals)
        
        # Contar transições
        transitions = re.findall(r'^\s*(FADE IN|FADE OUT|CUT TO|DISSOLVE TO|MATCH CUT|SMASH CUT)[:\s]*$', 
                                text, re.MULTILINE | re.IGNORECASE)
        analysis["transitions"] = len(transitions)
        
        # Contar linhas de ação (aproximação)
        lines = text.split('\n')
        action_lines = 0
        for line in lines:
            line = line.strip()
            # Linha de ação: não é cena, diálogo, transição ou vazia
            if (line and len(line) > 10 and 
                not re.match(r'^(INT\.|EXT\.|[A-Z]{2,30}\s*$|FADE|CUT|\()', line) and
                not line.isupper()):
                action_lines += 1
        analysis["action_lines"] = action_lines
        
        # Detectar estrutura de atos
        text_upper = text.upper()
        act_markers = [
            ('ACT I', 'ACT ONE', 'PRIMEIRO ATO', 'ATO 1'),
            ('ACT II', 'ACT TWO', 'SEGUNDO ATO', 'ATO 2'),
            ('ACT III', 'ACT THREE', 'TERCEIRO ATO', 'ATO 3')
        ]
        
        for act_num, markers in enumerate(act_markers, 1):
            for marker in markers:
                if marker in text_upper:
                    analysis["acts"].append(f"Act {act_num}")
                    break
        
        # Se não detectou atos explícitos, estimar baseado em páginas
        if not analysis["acts"] and analysis["pages"] > 0:
            if analysis["pages"] <= 30:
                analysis["acts"] = ["Short form - possibly Act I"]
            elif analysis["pages"] <= 60:
                analysis["acts"] = ["Acts I-II estimated"]
            else:
                analysis["acts"] = ["Full three-act structure estimated"]
        
        # Converter sets para listas ordenadas
        analysis["characters"] = sorted(list(analysis["characters"]))[:20]  # Top 20 personagens
        analysis["locations"] = sorted(list(analysis["locations"]))[:20]  # Top 20 locações
        
        # Adicionar estatísticas resumidas
        analysis["summary"] = {
            "total_elements": (analysis["scenes"] + analysis["dialogues"] + 
                              analysis["action_lines"] + analysis["transitions"]),
            "dialogue_density": analysis["dialogues"] / max(1, analysis["scenes"]) if analysis["scenes"] > 0 else 0,
            "avg_scene_length": len(text) / max(1, analysis["scenes"]) if analysis["scenes"] > 0 else 0,
            "predominant_time": max(analysis["time_of_day"].items(), key=lambda x: x[1])[0] if analysis["time_of_day"] else "UNKNOWN",
            "predominant_location": "INT" if analysis["scene_types"]["INT"] > analysis["scene_types"]["EXT"] else "EXT"
        }
        
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