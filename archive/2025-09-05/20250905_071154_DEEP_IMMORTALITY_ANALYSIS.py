#!/usr/bin/env python3
"""
ANÁLISE PROFUNDA DO SISTEMA IMMORTALITY.PY
"""

from pathlib import Path
import json

def analyze_immortality():
    print("\n" + "🔬"*40)
    print(" ANÁLISE PROFUNDA - SISTEMA IMMORTALITY.PY")
    print("🔬"*40)
    
    # 1. O PROBLEMA FUNDAMENTAL
    print("\n" + "="*70)
    print("🔴 PROBLEMA FUNDAMENTAL IDENTIFICADO")
    print("="*70)
    print("""
📍 LOCALIZAÇÃO: apps/scripturemon/immortality.py
📏 TAMANHO: 409 linhas, 14.449 bytes
📅 ÚLTIMA MODIFICAÇÃO: 02/09/2025 09:34

🐛 BUG CRÍTICO NA LINHA 253:
    self.backup_dir.glob(f"soul_{self.soul.signature}_*.bkp*")
    
❌ PROBLEMA:
    • Cada execução cria uma Soul com signature ÚNICA
    • Soul._generate_soul() usa UUID + timestamp (linha 77 de soul.py)
    • Resultado: signature diferente a cada execução
    • Consequência: _cleanup_old_backups() nunca encontra backups da MESMA soul
    
📊 EVIDÊNCIA:
    • runtime/souls/backups/ tem 329 backups
    • Múltiplas signatures diferentes:
      - soul_f937792b5ddb3551_*.bkp.gz
      - soul_fd6323bedc8f0fac_*.bkp.gz
      - soul_48b66ef0ddb5c32f_*.bkp.gz
      (cada uma é uma "alma" diferente)
""")
    
    # 2. FLUXO DO SISTEMA
    print("\n" + "="*70)
    print("🔄 FLUXO DO SISTEMA")
    print("="*70)
    print("""
1. INICIALIZAÇÃO (bin/scripturemon):
   ↓
2. CRIA Soul() nova:
   • soul.py linha 71: _generate_soul()
   • Gera signature com UUID + timestamp
   • SEMPRE única (nunca repete)
   ↓
3. CRIA ImmortalityProtocol(soul):
   • immortality.py linha 28
   • auto_backup=True por padrão
   • Inicia thread daemon
   ↓
4. BACKUP A CADA 5 MIN:
   • backup_soul() linha 55
   • Salva como soul_{signature}_{timestamp}.bkp.gz
   ↓
5. TENTA LIMPAR (linha 250):
   • _cleanup_old_backups()
   • Busca: soul_{self.soul.signature}_*.bkp*
   • NÃO ENCONTRA outros com MESMA signature
   • NÃO DELETA NADA
   ↓
6. RESULTADO: 329 backups acumulados
""")
    
    # 3. POR QUE FOI PROJETADO ASSIM
    print("\n" + "="*70)
    print("💡 INTENÇÃO DO DESIGN")
    print("="*70)
    print("""
O sistema foi projetado para:
    
✅ MÚLTIPLAS INSTÂNCIAS:
    • Cada instância tem sua própria "alma"
    • Permite rodar várias versões simultaneamente
    • Cada uma mantém seus próprios 10 backups
    
✅ IDENTIDADE PERSISTENTE:
    • soul.py linha 54: primary_soul.json
    • DEVERIA reusar mesma signature entre execuções
    • MAS está sempre gerando nova
    
🔍 PROBLEMA REAL:
    Soul.load_or_create_soul() (linha 48-69):
    • Tenta carregar primary_soul.json
    • SE não existe → gera nova
    • SE existe → deveria reusar
    • MAS: Algo está impedindo reuso da signature
""")
    
    # 4. VERIFICAÇÕES ADICIONAIS
    print("\n" + "="*70)
    print("🔍 VERIFICAÇÕES DO SISTEMA")
    print("="*70)
    
    # Verifica primary_soul.json
    primary_soul = Path("runtime/souls/primary_soul.json")
    if primary_soul.exists():
        try:
            with open(primary_soul) as f:
                data = json.load(f)
                print(f"✅ primary_soul.json existe")
                print(f"   Signature salva: {data.get('signature', 'NONE')}")
        except:
            print("⚠️ primary_soul.json existe mas está corrompido")
    else:
        print("❌ primary_soul.json NÃO existe")
        print("   Por isso gera nova signature toda vez!")
    
    # Verifica backups
    backup_dir = Path("runtime/souls/backups")
    if backup_dir.exists():
        backups = list(backup_dir.glob("*.bkp*"))
        signatures = set()
        for b in backups:
            # Extrai signature do nome
            parts = b.stem.split("_")
            if len(parts) >= 2:
                signatures.add(parts[1])
        
        print(f"\n📊 Estatísticas de backups:")
        print(f"   Total: {len(backups)} arquivos")
        print(f"   Signatures únicas: {len(signatures)}")
        print(f"   Média por signature: {len(backups)/len(signatures):.1f}")
        
        # Mostra algumas signatures
        print(f"\n   Exemplos de signatures:")
        for sig in list(signatures)[:5]:
            count = len([b for b in backups if f"soul_{sig}_" in b.name])
            print(f"   • {sig}: {count} backups")
    
    # 5. IMPACTO E SOLUÇÃO
    print("\n" + "="*70)
    print("⚠️ IMPACTO E SOLUÇÕES")
    print("="*70)
    print("""
IMPACTO ATUAL:
    • 329 backups × 0.5KB = ~165KB
    • Cresce ~288 backups/dia
    • ~144KB/dia de crescimento
    
SOLUÇÕES POSSÍVEIS (sem editar código):
    
1. LIMPAR MANUALMENTE:
    rm runtime/souls/backups/*.bkp.gz
    
2. CRIAR primary_soul.json MANUALMENTE:
    echo '{"signature":"fixed_signature_123"}' > runtime/souls/primary_soul.json
    (força mesma signature sempre)
    
3. USAR force_legacy=True:
    Soul(force_legacy=True)
    Usa signature fixa: "8ea9f71fa3206d1a"
    
⚠️ RECOMENDAÇÃO:
    NÃO EDITAR CÓDIGO AGORA
    Sistema está estável apesar do bug
    Limpeza manual resolve temporariamente
""")

if __name__ == "__main__":
    analyze_immortality()
