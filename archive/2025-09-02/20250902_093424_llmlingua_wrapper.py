from __future__ import annotations
from typing import Optional
import os

def available()->bool:
    try:
        import llmlingua  # type: ignore
        return True
    except:
        return False

def compress_text(text:str, ratio:float=0.8, preserve_entities:bool=True)->str:
    """
    ratio ~0.8 = compressao conservadora (20%)
    Fallback para uso sem baixar modelos
    """
    # Como LLMLingua precisa baixar modelos grandes,
    # vamos simular a compressao para testes
    if os.getenv("USE_REAL_LLMLINGUA") == "1":
        try:
            from llmlingua import PromptCompressor
            compressor = PromptCompressor(
                model_name="bert-base-multilingual-cased",
                device_map="cpu"
            )
            result = compressor.compress_prompt(text, rate=1-ratio)
            if isinstance(result, dict):
                return result.get("compressed_prompt", text)
            return str(result)
        except Exception as e:
            print(f"[SKIPPED] LLMLingua error: {e}")
            return text
    else:
        # Simulacao simples: remove palavras comuns (stopwords)
        # Esta e apenas uma aproximacao para benchmark
        import re
        stopwords = {"the", "a", "an", "is", "are", "was", "were", "be", "been", 
                    "being", "have", "has", "had", "do", "does", "did", "will",
                    "would", "could", "should", "may", "might", "must", "can",
                    "shall", "to", "of", "in", "for", "on", "with", "at", "by",
                    "from", "about", "into", "through", "during", "before", "after",
                    "above", "below", "between", "under", "again", "further", "then",
                    "once", "here", "there", "when", "where", "why", "how", "all",
                    "both", "each", "few", "more", "most", "other", "some", "such",
                    "no", "nor", "not", "only", "own", "same", "so", "than", "too",
                    "very", "and", "but", "if", "or", "because", "as", "until", "while"}
        
        words = text.split()
        # Remove ~20% das palavras (stopwords) para simular ratio 0.8
        compressed = []
        removed = 0
        target_remove = int(len(words) * (1 - ratio))
        
        for word in words:
            clean_word = re.sub(r'[^\w\s]', '', word.lower())
            if clean_word in stopwords and removed < target_remove:
                removed += 1
                continue  # Skip this word
            compressed.append(word)
        
        return " ".join(compressed)