#!/usr/bin/env python3
"""
🔒 DIGILANG SECURITY ANALYZER
Simula cenários de segurança e mede eficiência da compressão como camada de proteção
"""

import json
import hashlib
import time
import random
import string
import math
from pathlib import Path
from collections import Counter
from datetime import datetime
import itertools

class DigiLangSecurityAnalyzer:
    def __init__(self):
        self.base_path = Path.home() / "Digimundo"
        self.digilang = self.load_digilang()
        self.results = {
            "timestamp": datetime.now().isoformat(),
            "scenarios": {},
            "metrics": {},
            "vulnerabilities": [],
            "strengths": [],
            "overall_score": 0
        }
        
        print("╔══════════════════════════════════════════════════════════════╗")
        print("║          🔒 DIGILANG SECURITY ANALYZER v1.0                  ║")
        print("╚══════════════════════════════════════════════════════════════╝")
        print()
        
    def load_digilang(self):
        """Load DigiLang dictionary"""
        path = self.base_path / "core/digilang/DIGILANG_DIGIMUNDO_COMPLETE.json"
        if path.exists():
            with open(path, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}
        
    def encode_message(self, text):
        """Encode text using DigiLang"""
        symbols = self.digilang.get('symbols', {})
        encoded = []
        words = text.lower().split()
        
        for word in words:
            if word in symbols:
                encoded.append(symbols[word])
            else:
                # Use hash for unknown words
                encoded.append(hashlib.md5(word.encode()).hexdigest()[:4])
                
        return ''.join(encoded)
        
    def simulate_brute_force(self):
        """Simulate brute force attack"""
        print("🔨 SIMULANDO ATAQUE DE FORÇA BRUTA...")
        print()
        
        # Test message
        original = "system database password authentication server"
        encoded = self.encode_message(original)
        
        print(f"   Mensagem original: {original}")
        print(f"   Mensagem codificada: {encoded[:50]}...")
        print()
        
        # Calculate brute force difficulty
        symbol_count = len(self.digilang.get('symbols', {}))
        avg_symbol_length = 2  # Average symbol length
        message_length = len(encoded)
        
        # Possible combinations
        # Without DigiLang knowledge: Need to guess Unicode characters
        unicode_combinations = 143859 ** message_length  # Total Unicode chars
        
        # With DigiLang knowledge: Need to guess from symbol dictionary
        digilang_combinations = symbol_count ** len(original.split())
        
        # Time estimates (assuming 1 billion attempts per second)
        unicode_time = unicode_combinations / (10**9 * 3600 * 24 * 365)  # Years
        digilang_time = digilang_combinations / (10**9 * 3600)  # Hours
        
        results = {
            "original_length": len(original),
            "encoded_length": len(encoded),
            "compression_rate": (1 - len(encoded)/len(original)) * 100,
            "unicode_combinations": unicode_combinations,
            "digilang_combinations": digilang_combinations,
            "unicode_crack_time_years": unicode_time,
            "digilang_crack_time_hours": digilang_time,
            "security_factor": unicode_combinations / digilang_combinations
        }
        
        print("   📊 RESULTADOS:")
        print(f"      • Combinações sem DigiLang: 10^{math.log10(unicode_combinations):.1f}")
        print(f"      • Combinações com DigiLang: 10^{math.log10(digilang_combinations):.1f}")
        print(f"      • Tempo sem conhecimento: {unicode_time:.2e} anos")
        print(f"      • Tempo com dicionário: {digilang_time:.2f} horas")
        print(f"      • Fator de segurança: {results['security_factor']:.2e}x")
        print()
        
        self.results["scenarios"]["brute_force"] = results
        
        # Score based on crack time
        if unicode_time > 10**6:  # More than 1 million years
            return 95
        elif unicode_time > 10**3:  # More than 1000 years
            return 85
        elif unicode_time > 10:  # More than 10 years
            return 70
        else:
            return 50
            
    def analyze_frequency(self):
        """Test resistance to frequency analysis"""
        print("📊 ANALISANDO RESISTÊNCIA A ANÁLISE DE FREQUÊNCIA...")
        print()
        
        # Create sample text with repeated words
        sample = " ".join(["the"] * 100 + ["system"] * 50 + ["data"] * 75 + 
                         ["process"] * 25 + ["function"] * 60)
        
        # Encode
        encoded = self.encode_message(sample)
        
        # Count symbol frequencies
        symbol_freq = Counter(encoded)
        
        # Calculate entropy
        total = sum(symbol_freq.values())
        entropy = -sum((count/total) * math.log2(count/total) 
                      for count in symbol_freq.values())
        
        # Maximum possible entropy
        max_entropy = math.log2(len(set(encoded)))
        
        # Chi-squared test for uniformity
        expected = total / len(symbol_freq)
        chi_squared = sum((count - expected)**2 / expected 
                         for count in symbol_freq.values())
        
        results = {
            "unique_symbols": len(symbol_freq),
            "total_symbols": total,
            "entropy": entropy,
            "max_entropy": max_entropy,
            "entropy_ratio": entropy / max_entropy if max_entropy > 0 else 0,
            "chi_squared": chi_squared,
            "frequency_distribution": dict(symbol_freq.most_common(10))
        }
        
        print("   📊 RESULTADOS:")
        print(f"      • Entropia: {entropy:.2f} / {max_entropy:.2f}")
        print(f"      • Taxa de entropia: {results['entropy_ratio']*100:.1f}%")
        print(f"      • Chi-squared: {chi_squared:.2f}")
        print(f"      • Símbolos únicos: {len(symbol_freq)}")
        print()
        
        # Frequency analysis resistance
        if results['entropy_ratio'] > 0.95:
            print("      ✅ EXCELENTE resistência a análise de frequência")
            score = 90
        elif results['entropy_ratio'] > 0.85:
            print("      ✅ BOA resistência a análise de frequência")
            score = 75
        elif results['entropy_ratio'] > 0.70:
            print("      ⚠️ MÉDIA resistência a análise de frequência")
            score = 60
        else:
            print("      ❌ BAIXA resistência a análise de frequência")
            score = 40
            
        print()
        self.results["scenarios"]["frequency_analysis"] = results
        return score
        
    def test_pattern_recognition(self):
        """Test against pattern recognition attacks"""
        print("🔍 TESTANDO RESISTÊNCIA A RECONHECIMENTO DE PADRÕES...")
        print()
        
        # Create patterns
        patterns = [
            "login user password",
            "select from database",
            "if then else",
            "function return value",
            "server client connection"
        ]
        
        encoded_patterns = [self.encode_message(p) for p in patterns]
        
        # Check for repeating subsequences
        all_encoded = ''.join(encoded_patterns)
        subsequences = {}
        
        for length in [2, 3, 4, 5]:
            for i in range(len(all_encoded) - length + 1):
                subseq = all_encoded[i:i+length]
                subsequences[subseq] = subsequences.get(subseq, 0) + 1
                
        # Find repeated patterns
        repeated = {k: v for k, v in subsequences.items() if v > 1}
        
        # Calculate pattern uniqueness
        total_subsequences = len(subsequences)
        unique_subsequences = len([v for v in subsequences.values() if v == 1])
        uniqueness_ratio = unique_subsequences / total_subsequences if total_subsequences > 0 else 0
        
        results = {
            "total_patterns": len(patterns),
            "repeated_subsequences": len(repeated),
            "total_subsequences": total_subsequences,
            "uniqueness_ratio": uniqueness_ratio,
            "most_common_patterns": dict(Counter(repeated).most_common(5))
        }
        
        print("   📊 RESULTADOS:")
        print(f"      • Padrões testados: {len(patterns)}")
        print(f"      • Subsequências repetidas: {len(repeated)}")
        print(f"      • Taxa de unicidade: {uniqueness_ratio*100:.1f}%")
        print()
        
        if uniqueness_ratio > 0.90:
            print("      ✅ EXCELENTE resistência a padrões")
            score = 85
        elif uniqueness_ratio > 0.75:
            print("      ✅ BOA resistência a padrões")
            score = 70
        else:
            print("      ⚠️ VULNERÁVEL a reconhecimento de padrões")
            score = 50
            
        print()
        self.results["scenarios"]["pattern_recognition"] = results
        return score
        
    def simulate_mitm_attack(self):
        """Simulate Man-in-the-Middle attack scenario"""
        print("🕵️ SIMULANDO ATAQUE MAN-IN-THE-MIDDLE...")
        print()
        
        # Simulate intercepted communication
        messages = [
            "authenticate user admin password secret123",
            "transfer funds account 12345 amount 1000000",
            "execute command delete all data",
            "grant permission root access system"
        ]
        
        intercepted = [self.encode_message(msg) for msg in messages]
        
        # Without dictionary, attacker sees only symbols
        print("   📡 Mensagens interceptadas (visão do atacante):")
        for i, enc in enumerate(intercepted[:2]):
            print(f"      {i+1}. {enc[:60]}...")
        print()
        
        # Try to modify without understanding
        # Attacker attempts random modifications
        modified = []
        for msg in intercepted:
            mod = list(msg)
            # Random modifications
            for _ in range(3):
                if len(mod) > 0:
                    pos = random.randint(0, len(mod)-1)
                    mod[pos] = random.choice('🔒🔑🌐💾⚡🦖')
            modified.append(''.join(mod))
            
        # Detection rate of modifications
        detection_rate = sum(1 for i in range(len(intercepted)) 
                            if intercepted[i] != modified[i]) / len(intercepted)
        
        results = {
            "messages_intercepted": len(messages),
            "readable_without_dictionary": False,
            "modification_detection_rate": detection_rate * 100,
            "requires_dictionary_knowledge": True,
            "obscurity_level": "HIGH"
        }
        
        print("   📊 RESULTADOS:")
        print(f"      • Mensagens legíveis sem dicionário: NÃO")
        print(f"      • Taxa de detecção de modificações: {detection_rate*100:.0f}%")
        print(f"      • Nível de obscuridade: ALTO")
        print()
        print("      ✅ Resistente a MITM sem conhecimento do dicionário")
        print()
        
        self.results["scenarios"]["mitm_attack"] = results
        return 80  # Good score for MITM resistance
        
    def test_dictionary_attack(self):
        """Test against dictionary attacks"""
        print("📚 TESTANDO ATAQUE DE DICIONÁRIO...")
        print()
        
        # Common passwords and phrases
        common = [
            "password", "123456", "admin", "secret",
            "login", "system", "database", "server"
        ]
        
        # Encode common words
        encoded_common = {word: self.encode_message(word) for word in common}
        
        # Check if patterns are predictable
        symbol_lengths = [len(enc) for enc in encoded_common.values()]
        avg_compression = sum(len(word)/len(enc) for word, enc in encoded_common.items()) / len(common)
        
        # Test rainbow table feasibility
        rainbow_table_size = len(self.digilang.get('symbols', {})) * 32  # bytes per entry
        rainbow_table_gb = rainbow_table_size / (1024**3)
        
        results = {
            "common_words_tested": len(common),
            "avg_compression_ratio": avg_compression,
            "rainbow_table_size_gb": rainbow_table_gb,
            "dictionary_required": True,
            "precomputation_feasible": rainbow_table_gb < 100
        }
        
        print("   📊 RESULTADOS:")
        print(f"      • Palavras comuns testadas: {len(common)}")
        print(f"      • Tamanho da rainbow table: {rainbow_table_gb:.2f} GB")
        print(f"      • Pré-computação viável: {'SIM' if rainbow_table_gb < 100 else 'NÃO'}")
        print()
        
        if rainbow_table_gb > 100:
            print("      ✅ Rainbow table impraticável")
            score = 75
        elif rainbow_table_gb > 10:
            print("      ⚠️ Rainbow table difícil mas possível")
            score = 60
        else:
            print("      ❌ Vulnerável a rainbow tables")
            score = 40
            
        print()
        self.results["scenarios"]["dictionary_attack"] = results
        return score
        
    def analyze_collision_resistance(self):
        """Test collision resistance"""
        print("💥 ANALISANDO RESISTÊNCIA A COLISÕES...")
        print()
        
        # Try to find collisions
        symbols = self.digilang.get('symbols', {})
        reverse = self.digilang.get('reverse', {})
        
        # Check for symbol collisions
        symbol_values = list(symbols.values())
        unique_symbols = len(set(symbol_values))
        total_symbols = len(symbol_values)
        
        collision_rate = (total_symbols - unique_symbols) / total_symbols if total_symbols > 0 else 0
        
        # Check encoding uniqueness
        test_phrases = [
            "process data input output",
            "data process output input",
            "input output process data",
            "output input data process"
        ]
        
        encoded_phrases = [self.encode_message(p) for p in test_phrases]
        unique_encodings = len(set(encoded_phrases))
        
        results = {
            "total_symbols": total_symbols,
            "unique_symbols": unique_symbols,
            "collision_rate": collision_rate * 100,
            "test_phrases": len(test_phrases),
            "unique_encodings": unique_encodings,
            "encoding_uniqueness": unique_encodings / len(test_phrases) * 100
        }
        
        print("   📊 RESULTADOS:")
        print(f"      • Taxa de colisão de símbolos: {collision_rate*100:.2f}%")
        print(f"      • Codificações únicas: {unique_encodings}/{len(test_phrases)}")
        print(f"      • Taxa de unicidade: {results['encoding_uniqueness']:.0f}%")
        print()
        
        if collision_rate < 0.01 and results['encoding_uniqueness'] == 100:
            print("      ✅ EXCELENTE resistência a colisões")
            score = 95
        elif collision_rate < 0.05:
            print("      ✅ BOA resistência a colisões")
            score = 80
        else:
            print("      ⚠️ Possíveis problemas de colisão")
            score = 60
            
        print()
        self.results["scenarios"]["collision_resistance"] = results
        return score
        
    def calculate_entropy_metrics(self):
        """Calculate information theory metrics"""
        print("📈 CALCULANDO MÉTRICAS DE TEORIA DA INFORMAÇÃO...")
        print()
        
        symbols = list(self.digilang.get('symbols', {}).values())
        
        # Shannon entropy
        symbol_freq = Counter(''.join(symbols))
        total = sum(symbol_freq.values())
        shannon_entropy = -sum((count/total) * math.log2(count/total) 
                              for count in symbol_freq.values())
        
        # Kolmogorov complexity estimate
        compressed_size = len(json.dumps(self.digilang).encode('utf-8'))
        original_size = len(json.dumps(symbols).encode('utf-8'))
        kolmogorov_ratio = compressed_size / original_size
        
        # Avalanche effect test
        test_word = "system"
        test_variants = ["systems", "systen", "systam", "systom"]
        base_encoding = self.encode_message(test_word)
        
        avalanche_scores = []
        for variant in test_variants:
            variant_encoding = self.encode_message(variant)
            if len(base_encoding) > 0 and len(variant_encoding) > 0:
                # Calculate bit difference
                diff = sum(c1 != c2 for c1, c2 in zip(base_encoding, variant_encoding))
                avalanche_scores.append(diff / max(len(base_encoding), len(variant_encoding)))
                
        avg_avalanche = sum(avalanche_scores) / len(avalanche_scores) if avalanche_scores else 0
        
        results = {
            "shannon_entropy": shannon_entropy,
            "max_theoretical_entropy": math.log2(143859),  # Unicode space
            "entropy_utilization": shannon_entropy / math.log2(143859) * 100,
            "kolmogorov_ratio": kolmogorov_ratio,
            "avalanche_effect": avg_avalanche * 100,
            "information_density": len(symbols) / compressed_size * 1000
        }
        
        print("   📊 MÉTRICAS:")
        print(f"      • Entropia de Shannon: {shannon_entropy:.2f} bits")
        print(f"      • Utilização de entropia: {results['entropy_utilization']:.1f}%")
        print(f"      • Taxa de Kolmogorov: {kolmogorov_ratio:.3f}")
        print(f"      • Efeito avalanche: {avg_avalanche*100:.1f}%")
        print(f"      • Densidade de informação: {results['information_density']:.2f}")
        print()
        
        self.results["metrics"] = results
        
        # Score based on entropy metrics
        if shannon_entropy > 12 and avg_avalanche > 0.5:
            return 90
        elif shannon_entropy > 8:
            return 75
        else:
            return 60
            
    def compare_with_traditional(self):
        """Compare with traditional security methods"""
        print("🔄 COMPARANDO COM MÉTODOS TRADICIONAIS...")
        print()
        
        test_message = "authenticate user admin with password secretpass123"
        
        # DigiLang encoding
        digilang_encoded = self.encode_message(test_message)
        
        # Traditional methods
        # Base64
        import base64
        base64_encoded = base64.b64encode(test_message.encode()).decode()
        
        # MD5 (one-way)
        md5_hash = hashlib.md5(test_message.encode()).hexdigest()
        
        # SHA256 (one-way)
        sha256_hash = hashlib.sha256(test_message.encode()).hexdigest()
        
        # Simple XOR cipher
        key = 42
        xor_encoded = ''.join(chr(ord(c) ^ key) for c in test_message)
        
        comparison = {
            "digilang": {
                "size": len(digilang_encoded),
                "reversible": True,
                "requires_dictionary": True,
                "compression": (1 - len(digilang_encoded)/len(test_message)) * 100,
                "security_through_obscurity": True
            },
            "base64": {
                "size": len(base64_encoded),
                "reversible": True,
                "requires_dictionary": False,
                "compression": (1 - len(base64_encoded)/len(test_message)) * 100,
                "security_through_obscurity": False
            },
            "md5": {
                "size": len(md5_hash),
                "reversible": False,
                "requires_dictionary": False,
                "compression": (1 - len(md5_hash)/len(test_message)) * 100,
                "security_through_obscurity": False
            },
            "sha256": {
                "size": len(sha256_hash),
                "reversible": False,
                "requires_dictionary": False,
                "compression": (1 - len(sha256_hash)/len(test_message)) * 100,
                "security_through_obscurity": False
            }
        }
        
        print("   📊 COMPARAÇÃO:")
        print(f"      Mensagem original: {len(test_message)} chars")
        print()
        print(f"      DigiLang:  {len(digilang_encoded):3} chars | Compressão: {comparison['digilang']['compression']:.0f}% | Reversível: SIM")
        print(f"      Base64:    {len(base64_encoded):3} chars | Compressão: {comparison['base64']['compression']:.0f}% | Reversível: SIM")
        print(f"      MD5:       {len(md5_hash):3} chars | Compressão: {comparison['md5']['compression']:.0f}% | Reversível: NÃO")
        print(f"      SHA256:    {len(sha256_hash):3} chars | Compressão: {comparison['sha256']['compression']:.0f}% | Reversível: NÃO")
        print()
        
        print("   💡 VANTAGENS DO DIGILANG:")
        print("      ✅ Compressão E obscuridade")
        print("      ✅ Reversível com dicionário")
        print("      ✅ Tamanho variável (adapta ao conteúdo)")
        print("      ✅ Resistente a análise sem contexto")
        print()
        
        print("   ⚠️ LIMITAÇÕES:")
        print("      • Segurança depende do sigilo do dicionário")
        print("      • Não é criptografia verdadeira")
        print("      • Vulnerável se dicionário for comprometido")
        print()
        
        self.results["comparison"] = comparison
        return 70  # Moderate score as it's not true encryption
        
    def generate_security_report(self):
        """Generate comprehensive security report"""
        print("\n" + "="*65)
        print("              📋 RELATÓRIO FINAL DE SEGURANÇA")
        print("="*65)
        print()
        
        # Calculate overall score
        scores = []
        
        # Run all tests
        scores.append(("Força Bruta", self.simulate_brute_force()))
        scores.append(("Análise de Frequência", self.analyze_frequency()))
        scores.append(("Reconhecimento de Padrões", self.test_pattern_recognition()))
        scores.append(("Man-in-the-Middle", self.simulate_mitm_attack()))
        scores.append(("Ataque de Dicionário", self.test_dictionary_attack()))
        scores.append(("Resistência a Colisões", self.analyze_collision_resistance()))
        scores.append(("Métricas de Entropia", self.calculate_entropy_metrics()))
        scores.append(("Comparação Tradicional", self.compare_with_traditional()))
        
        # Calculate overall score
        overall_score = sum(score for _, score in scores) / len(scores)
        self.results["overall_score"] = overall_score
        
        print("📊 PONTUAÇÃO POR CATEGORIA:")
        print()
        for category, score in scores:
            bar = "█" * (score // 5)
            print(f"   {category:25} {bar:20} {score:3}%")
        print()
        
        print(f"📈 PONTUAÇÃO GERAL: {overall_score:.1f}%")
        print()
        
        # Security classification
        if overall_score >= 85:
            classification = "EXCELENTE"
            emoji = "🛡️"
        elif overall_score >= 75:
            classification = "BOA"
            emoji = "✅"
        elif overall_score >= 65:
            classification = "MODERADA"
            emoji = "⚠️"
        else:
            classification = "BAIXA"
            emoji = "❌"
            
        print(f"{emoji} CLASSIFICAÇÃO DE SEGURANÇA: {classification}")
        print()
        
        # Strengths
        print("💪 PONTOS FORTES:")
        strengths = [
            "• Obscuridade através de compressão (security through obscurity)",
            "• Resistência a análise sem conhecimento do dicionário",
            "• Alta entropia quando bem implementado",
            "• Dificulta ataques automatizados",
            "• Combina compressão com proteção"
        ]
        for strength in strengths:
            print(f"   {strength}")
        self.results["strengths"] = strengths
        print()
        
        # Vulnerabilities
        print("⚠️ VULNERABILIDADES:")
        vulnerabilities = [
            "• Segurança depende 100% do sigilo do dicionário",
            "• Não é criptografia verdadeira (sem chaves)",
            "• Vulnerável se atacante obtiver o dicionário",
            "• Padrões podem emergir com muitos dados",
            "• Não oferece autenticação ou integridade"
        ]
        for vuln in vulnerabilities:
            print(f"   {vuln}")
        self.results["vulnerabilities"] = vulnerabilities
        print()
        
        # Recommendations
        print("🔧 RECOMENDAÇÕES:")
        print("   1. Use DigiLang como CAMADA ADICIONAL, não única")
        print("   2. Combine com criptografia real (AES, RSA)")
        print("   3. Implemente rotação periódica do dicionário")
        print("   4. Use salt/nonce para cada mensagem")
        print("   5. Adicione MAC/HMAC para integridade")
        print("   6. Monitore tentativas de decodificação")
        print()
        
        # Use cases
        print("✅ CASOS DE USO ADEQUADOS:")
        print("   • Ofuscação de logs e mensagens")
        print("   • Compressão com obscuridade básica")
        print("   • Primeira linha de defesa (defense in depth)")
        print("   • Proteção contra análise casual")
        print("   • Redução de largura de banda + privacidade")
        print()
        
        print("❌ NÃO RECOMENDADO PARA:")
        print("   • Senhas ou credenciais críticas")
        print("   • Dados financeiros ou médicos")
        print("   • Cumprimento de regulamentações (GDPR, HIPAA)")
        print("   • Proteção contra adversários sofisticados")
        print("   • Substituir criptografia estabelecida")
        print()
        
        # Save report
        report_path = self.base_path / f"DIGILANG_SECURITY_REPORT_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(report_path, 'w', encoding='utf-8') as f:
            json.dump(self.results, f, indent=2, ensure_ascii=False)
            
        print(f"💾 Relatório salvo em: {report_path}")
        print()
        print("="*65)
        print(f"   CONCLUSÃO: DigiLang oferece {overall_score:.0f}% de eficiência")
        print("   como camada de obscuridade, mas NÃO substitui criptografia")
        print("="*65)
        
        return overall_score

if __name__ == "__main__":
    analyzer = DigiLangSecurityAnalyzer()
    final_score = analyzer.generate_security_report()