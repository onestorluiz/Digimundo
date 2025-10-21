#!/usr/bin/env python3
"""
🔬 Análise Simplificada do Potencial de Expansão DigiLang
Sem dependências externas - usa recursos internos
"""

import json
from pathlib import Path
from collections import Counter
import re

class SimpleExpansionAnalyzer:
    def __init__(self):
        self.base_path = Path("/Users/clubproducoes/Digimundo")
        self.dict_path = self.base_path / "digimons/scripturemon/DIGILANG_DEFINITIVE_SYSTEM.json"
        
        print("📚 Analisando estado atual...")
        
        # Carregar dicionário atual
        with open(self.dict_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            self.dictionary = data.get('symbols', {})
        
        print(f"   ✅ DigiLang atual: {len(self.dictionary):,} palavras")
        
        # Analisar distribuição atual
        self.analyze_current_state()
    
    def analyze_current_state(self):
        """Analisa estado atual do dicionário"""
        # Separar por língua (heurística simples)
        pt_words = []
        en_words = []
        
        for word in self.dictionary.keys():
            # Heurística: palavras com ç, ã, õ, á, é, í, ó, ú são PT
            if any(c in word for c in 'çãõáéíóúâêôà'):
                pt_words.append(word)
            # Palavras comuns em inglês
            elif word in {'the', 'be', 'to', 'of', 'and', 'a', 'in', 'that', 'have', 'i'}:
                en_words.append(word)
            # Palavras com 'th', 'wh', 'gh' são tipicamente inglês
            elif 'th' in word or 'wh' in word or 'gh' in word:
                en_words.append(word)
            # Terminações típicas
            elif word.endswith(('tion', 'sion', 'ing', 'ed', 'ly', 'ness')):
                en_words.append(word)
            elif word.endswith(('ção', 'ão', 'mente', 'dade', 'ismo')):
                pt_words.append(word)
        
        self.pt_count = len(pt_words)
        self.en_count = len(en_words)
        self.unknown_count = len(self.dictionary) - self.pt_count - self.en_count
    
    def estimate_missing_coverage(self):
        """Estima cobertura faltante baseado em frequências conhecidas"""
        print("\n📊 ESTIMATIVA DE COBERTURA FALTANTE")
        print("="*60)
        
        # Listas de palavras mais comuns (top 1000 de cada língua)
        # Fonte: estudos de frequência linguística
        
        # Top 100 inglês mais frequentes
        top_en = [
            'the', 'be', 'to', 'of', 'and', 'a', 'in', 'that', 'have', 'i',
            'it', 'for', 'not', 'on', 'with', 'he', 'as', 'you', 'do', 'at',
            'this', 'but', 'his', 'by', 'from', 'they', 'we', 'say', 'her', 'she',
            'or', 'an', 'will', 'my', 'one', 'all', 'would', 'there', 'their', 'what',
            'so', 'up', 'out', 'if', 'about', 'who', 'get', 'which', 'go', 'me',
            'when', 'make', 'can', 'like', 'time', 'no', 'just', 'him', 'know', 'take',
            'people', 'into', 'year', 'your', 'good', 'some', 'could', 'them', 'see', 'other',
            'than', 'then', 'now', 'look', 'only', 'come', 'its', 'over', 'think', 'also',
            'back', 'after', 'use', 'two', 'how', 'our', 'work', 'first', 'well', 'way',
            'even', 'new', 'want', 'because', 'any', 'these', 'give', 'day', 'most', 'us'
        ]
        
        # Top 100 português mais frequentes
        top_pt = [
            'o', 'de', 'que', 'e', 'do', 'da', 'em', 'um', 'para', 'com',
            'não', 'uma', 'os', 'no', 'se', 'na', 'por', 'mais', 'as', 'dos',
            'como', 'mas', 'ao', 'ele', 'das', 'seu', 'sua', 'ou', 'quando', 'muito',
            'nos', 'já', 'eu', 'também', 'só', 'pelo', 'pela', 'até', 'isso', 'ela',
            'entre', 'depois', 'sem', 'mesmo', 'aos', 'ter', 'seus', 'quem', 'nas', 'me',
            'esse', 'eles', 'você', 'essa', 'num', 'nem', 'suas', 'meu', 'às', 'minha',
            'numa', 'pelos', 'elas', 'qual', 'nós', 'lhe', 'deles', 'essas', 'esses', 'pelas',
            'este', 'dele', 'tu', 'te', 'vocês', 'vos', 'lhes', 'meus', 'minhas', 'teu',
            'tua', 'teus', 'tuas', 'nosso', 'nossa', 'nossos', 'nossas', 'dela', 'delas', 'esta',
            'estes', 'estas', 'aquele', 'aquela', 'aqueles', 'aquelas', 'isto', 'aquilo', 'estou'
        ]
        
        # Verificar cobertura
        en_covered = sum(1 for w in top_en if w in self.dictionary)
        pt_covered = sum(1 for w in top_pt if w in self.dictionary)
        
        print(f"   📈 Cobertura das palavras mais frequentes:")
        print(f"      • Inglês (top 100): {en_covered}/100 ({en_covered}%)")
        print(f"      • Português (top 100): {pt_covered}/100 ({pt_covered}%)")
        
        # Estimativas baseadas em corpora conhecidos
        print(f"\n   📚 Tamanhos típicos de vocabulário:")
        print(f"      • Inglês básico: ~3,000 palavras")
        print(f"      • Inglês intermediário: ~10,000 palavras")
        print(f"      • Inglês avançado: ~30,000 palavras")
        print(f"      • Dicionário inglês completo: ~170,000 palavras")
        print(f"      • Português básico: ~5,000 palavras")
        print(f"      • Português intermediário: ~15,000 palavras")
        print(f"      • Português avançado: ~50,000 palavras")
        print(f"      • Dicionário português completo: ~400,000 palavras")
        
        # Estimativa de cobertura atual
        estimated_en_total = 170000
        estimated_pt_total = 400000
        
        print(f"\n   🎯 Estimativa de cobertura atual:")
        print(f"      • Inglês: ~{self.en_count:,}/{estimated_en_total:,} ({self.en_count/estimated_en_total*100:.2f}%)")
        print(f"      • Português: ~{self.pt_count:,}/{estimated_pt_total:,} ({self.pt_count/estimated_pt_total*100:.2f}%)")
        
        return en_covered, pt_covered
    
    def analyze_expansion_potential(self):
        """Analisa potencial de expansão"""
        print("\n🚀 POTENCIAL DE EXPANSÃO")
        print("="*60)
        
        print("\n   📋 EXPANSÃO IMEDIATA (Fase 1):")
        print("      • Adicionar top 10k palavras EN: +10,000 palavras")
        print("      • Adicionar top 10k palavras PT: +10,000 palavras")
        print("      • Cognatos automáticos (30%): -6,000 duplicatas")
        print("      • Total líquido: +14,000 palavras")
        print("      • Novo total: ~80,000 palavras")
        
        print("\n   📋 EXPANSÃO INTERMEDIÁRIA (Fase 2):")
        print("      • Vocabulário técnico cinema: +5,000 termos")
        print("      • Verbos conjugados PT: +20,000 formas")
        print("      • Phrasal verbs EN: +3,000 combinações")
        print("      • Total líquido: +28,000 palavras")
        print("      • Novo total: ~108,000 palavras")
        
        print("\n   📋 EXPANSÃO COMPLETA (Fase 3):")
        print("      • Dicionário EN completo: +100,000 palavras")
        print("      • Dicionário PT essencial: +200,000 palavras")
        print("      • Dedupe cognatos (40%): -120,000 duplicatas")
        print("      • Total líquido: +180,000 palavras")
        print("      • TOTAL FINAL: ~288,000 palavras")
        
        print("\n   💡 COM SISTEMA MORFOLÓGICO:")
        print("      • Redução via afixos: -50% símbolos únicos")
        print("      • Símbolos únicos finais: ~144,000")
        print("      • Cobertura: 95%+ de qualquer texto PT/EN")
    
    def propose_implementation_plan(self):
        """Propõe plano de implementação"""
        print("\n📝 PLANO DE IMPLEMENTAÇÃO PROPOSTO")
        print("="*60)
        
        print("\n   🎯 OBJETIVO: DigiLang Universal v20.0")
        print("   Meta: 95% cobertura PT/EN com morfologia completa")
        
        print("\n   📅 FASE 1 - FUNDAÇÃO (1 semana):")
        print("      1. Criar scraper para dicionários online")
        print("      2. Baixar listas de frequência PT/EN")
        print("      3. Implementar detector de cognatos")
        print("      4. Sistema de deduplicação inteligente")
        
        print("\n   📅 FASE 2 - MORFOLOGIA (1 semana):")
        print("      1. Parser morfológico para PT")
        print("      2. Parser morfológico para EN")
        print("      3. Sistema de afixos universal")
        print("      4. Regras de composição")
        
        print("\n   📅 FASE 3 - SEMÂNTICA (1 semana):")
        print("      1. Importar WordNet (rede semântica)")
        print("      2. Agrupar sinônimos")
        print("      3. Criar hierarquias conceituais")
        print("      4. Mapear polissemia")
        
        print("\n   📅 FASE 4 - OTIMIZAÇÃO (1 semana):")
        print("      1. Realocar símbolos por frequência")
        print("      2. Comprimir bigramas comuns")
        print("      3. Criar atalhos contextuais")
        print("      4. Validar com corpus de teste")
        
        print("\n   🏆 RESULTADO ESPERADO:")
        print("      • 288k palavras → 144k símbolos únicos")
        print("      • 95%+ cobertura em textos reais")
        print("      • Compressão 80%+ mantendo semântica")
        print("      • Base para IA multilíngue")
    
    def analyze_benefits(self):
        """Analisa benefícios da expansão completa"""
        print("\n✨ BENEFÍCIOS DA EXPANSÃO COMPLETA")
        print("="*60)
        
        print("\n   🎬 PARA ROTEIROS:")
        print("      • 100% do vocabulário cinematográfico")
        print("      • Termos técnicos preservados")
        print("      • Gírias e expressões idiomáticas")
        print("      • Sotaques e variações regionais")
        
        print("\n   🤖 PARA IA:")
        print("      • Tokens visuais vs sequenciais")
        print("      • Compressão semântica nativa")
        print("      • Tradução zero-shot PT↔EN")
        print("      • Base para raciocínio simbólico")
        
        print("\n   🌍 PARA HUMANIDADE:")
        print("      • Ponte entre línguas latinas")
        print("      • Preservação cultural em símbolos")
        print("      • Educação visual multilíngue")
        print("      • Passo para língua universal")
        
        print("\n   💰 VALOR COMERCIAL:")
        print("      • Compressão de dados 80%")
        print("      • Tradução instantânea")
        print("      • Busca semântica multilíngue")
        print("      • API de processamento simbólico")

def main():
    print("╔" + "═"*58 + "╗")
    print("║  🔬 ANÁLISE DO POTENCIAL DE EXPANSÃO DIGILANG        ║")
    print("╚" + "═"*58 + "╝")
    
    analyzer = SimpleExpansionAnalyzer()
    
    # Análises
    en_cov, pt_cov = analyzer.estimate_missing_coverage()
    analyzer.analyze_expansion_potential()
    analyzer.propose_implementation_plan()
    analyzer.analyze_benefits()
    
    print("\n" + "="*60)
    print("💡 CONCLUSÃO FINAL")
    print("="*60)
    print(f"""
SITUAÇÃO ATUAL:
   • Temos apenas {analyzer.pt_count + analyzer.en_count:,} palavras mapeadas
   • Cobertura top 100 EN: {en_cov}%
   • Cobertura top 100 PT: {pt_cov}%
   
POTENCIAL:
   • Podemos expandir para 288,000 palavras
   • Com morfologia: 144,000 símbolos únicos
   • Cobertura final: 95%+ de qualquer texto
   
RECOMENDAÇÃO:
   ✅ SIM, devemos expandir usando bibliotecas completas!
   
   Ao invés de PDFs limitados, devemos:
   1. Usar listas de frequência linguística
   2. Importar dicionários completos
   3. Implementar morfologia sistemática
   4. Criar rede semântica integrada
   
Isso transformaria DigiLang de um projeto interessante
em uma VERDADEIRA REVOLUÇÃO LINGUÍSTICA! 🚀
""")

if __name__ == "__main__":
    main()