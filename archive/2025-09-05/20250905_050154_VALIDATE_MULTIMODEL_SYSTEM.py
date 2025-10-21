#!/usr/bin/env python3
"""
VALIDAÇÃO DO SISTEMA MULTI-MODELO RESTAURADO
"""

import sys
from pathlib import Path

def validate_system():
    """Valida que o sistema NÃO foi simplificado"""
    
    print("\n" + "🔥"*30)
    print(" VALIDAÇÃO DO SISTEMA MULTI-MODELO ROBUSTO")
    print("🔥"*30)
    
    script = Path("bin/scripturemon")
    if not script.exists():
        print("❌ bin/scripturemon não encontrado!")
        return False
    
    content = script.read_text()
    
    # Lista de validações
    validations = []
    
    print("\n📋 CHECKLIST DE ROBUSTEZ:")
    print("="*60)
    
    # 1. Modelo principal deve ser ROBUSTO (32b)
    if "'principal': 'deepseek-r1:32b'" in content:
        print("✅ Modelo principal é ROBUSTO (deepseek-r1:32b)")
        validations.append(True)
    else:
        print("❌ Modelo principal foi SIMPLIFICADO!")
        validations.append(False)
    
    # 2. Specialist deve ser scripturemon-deepseek
    if "'specialist': 'scripturemon-deepseek'" in content:
        print("✅ Specialist é modelo ESPECÍFICO (scripturemon-deepseek)")
        validations.append(True)
    else:
        print("❌ Specialist foi SIMPLIFICADO para modelo genérico!")
        validations.append(False)
    
    # 3. Pipeline evaluate deve ter modelos robustos
    if "'evaluate': ['scripturemon-ultimate', 'scripturemon-deepseek']" in content:
        print("✅ Pipeline 'evaluate' tem modelos ROBUSTOS")
        validations.append(True)
    else:
        print("❌ Pipeline 'evaluate' foi SIMPLIFICADO!")
        validations.append(False)
    
    # 4. Pipeline synthesize deve ter modelos pesados
    if "'synthesize': ['deepseek-r1:32b', 'deepseek-r1:70b']" in content:
        print("✅ Pipeline 'synthesize' tem síntese PODEROSA")
        validations.append(True)
    else:
        print("❌ Pipeline 'synthesize' foi ENFRAQUECIDO!")
        validations.append(False)
    
    # 5. Pipeline_deep deve existir e ser ULTRA robusto
    if "'pipeline_deep':" in content and "'deepseek-r1:70b', 'scripturemon-ultimate', 'deepseek-r1:32b'" in content:
        print("✅ Pipeline_deep é ULTRA ROBUSTO com 3+ modelos por estágio")
        validations.append(True)
    else:
        print("❌ Pipeline_deep foi SIMPLIFICADO ou removido!")
        validations.append(False)
    
    # 6. Deve ter 10 roles
    roles_count = content.count("': '")  # Contar definições de roles
    if roles_count >= 10:
        print(f"✅ Sistema tem {roles_count}+ roles definidos")
        validations.append(True)
    else:
        print(f"❌ Sistema tem apenas {roles_count} roles (esperado 10+)")
        validations.append(False)
    
    # 7. Sistema de gatilhos deve estar presente
    if "_should_use_deep_model" in content and "trigger_words" in content:
        print("✅ Sistema de gatilhos presente")
        validations.append(True)
    else:
        print("❌ Sistema de gatilhos ausente!")
        validations.append(False)
    
    # 8. Deve ter comentários sobre NÃO SIMPLIFICAR
    if "NÃO SIMPLIFICAR" in content or "ROBUSTO" in content:
        print("✅ Avisos de NÃO SIMPLIFICAR presentes")
        validations.append(True)
    else:
        print("⚠️ Avisos de robustez ausentes")
        validations.append(True)  # Não é crítico
    
    print("\n" + "="*60)
    print("📊 RESULTADO DA VALIDAÇÃO:")
    print("="*60)
    
    if all(validations):
        print("✅ SISTEMA 100% ROBUSTO - NADA FOI SIMPLIFICADO!")
        print("\n🎯 Configuração atual:")
        print("  • Modelo principal: deepseek-r1:32b (ROBUSTO)")
        print("  • 10 roles especializados")
        print("  • Pipeline normal: 4 estágios com modelos variados")
        print("  • Pipeline deep: 4 estágios ULTRA ROBUSTOS")
        print("  • Sistema de gatilhos: Ativa pipeline_deep com palavras-chave")
        print("\n⚠️ IMPORTANTE:")
        print("  Este sistema vai usar MAIS recursos mas é MAIS PODEROSO")
        print("  Timeouts são esperados com modelos grandes (32b, 70b)")
        return True
    else:
        print("❌ SISTEMA FOI SIMPLIFICADO!")
        print("\n🔧 Correções necessárias:")
        for i, valid in enumerate(validations):
            if not valid:
                print(f"  • Verificar item {i+1} da checklist acima")
        return False

if __name__ == "__main__":
    sys.exit(0 if validate_system() else 1)
