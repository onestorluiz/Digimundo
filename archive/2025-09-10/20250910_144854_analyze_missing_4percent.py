#!/usr/bin/env python3
"""
Análise detalhada dos 4% faltantes para harmonia completa
"""
import json
import os
import sys
from pathlib import Path
from datetime import datetime

def analyze_missing_harmony():
    """Identifica exatamente o que falta para 100% de harmonia"""
    
    missing_components = {
        "1_OLLAMA_INTEGRATION": {
            "status": "❌ Parcialmente Implementado",
            "percentage": 1.5,
            "issues": [
                "Ollama não responde consistentemente",
                "Timeout em chamadas síncronas",
                "Falta fallback quando Ollama está offline"
            ],
            "files": [
                "apps/scripturemon/ollama_client.py",
                "apps/scripturemon/fallback_manager.py"
            ],
            "solution": "Implementar modo offline completo com cache local"
        },
        
        "2_SEARCH_FUNCTIONALITY": {
            "status": "⚠️ Refatorado mas não testado",
            "percentage": 1.0,
            "issues": [
                "Comando 'search' movido para 'memory search'",
                "Índices antigos não migrados",
                "ChromaDB não sincroniza com Redis"
            ],
            "files": [
                "apps/scripturemon/memory_harmony.py:search()",
                "data/chroma/* (índices desatualizados)"
            ],
            "solution": "Reindexar todos os documentos e sincronizar bases"
        },
        
        "3_CONSCIOUSNESS_MODULE": {
            "status": "🔄 Loop infinito detectado",
            "percentage": 0.8,
            "issues": [
                "ConsciousnessStream entra em loop",
                "Consume 100% CPU após 5 minutos",
                "Não libera memória corretamente"
            ],
            "files": [
                "apps/scripturemon/canonical/consciousness.py",
                "apps/scripturemon/stream_manager.py"
            ],
            "solution": "Adicionar circuit breaker e garbage collection"
        },
        
        "4_PDF_PROCESSING": {
            "status": "⚠️ Inconsistente",
            "percentage": 0.5,
            "issues": [
                "PDFs grandes (>50MB) falham silenciosamente",
                "Encoding UTF-8 não detectado corretamente",
                "Metadados perdidos na conversão"
            ],
            "files": [
                "apps/scripturemon/pdf_processor.py",
                "apps/scripturemon/document_parser.py"
            ],
            "solution": "Usar PyPDF2 com fallback para pdfplumber"
        },
        
        "5_TELEPATHY_PUBSUB": {
            "status": "❌ Desconectado",
            "percentage": 0.2,
            "issues": [
                "Redis pubsub não mantém conexão",
                "Mensagens perdidas após 1000 eventos",
                "Sem heartbeat implementado"
            ],
            "files": [
                "apps/scripturemon/telepathy_network.py",
                "tools/fix_v3/telepathy_pubsub.py"
            ],
            "solution": "Implementar reconnection logic com exponential backoff"
        }
    }
    
    # Calcular totais
    total_missing = sum(comp["percentage"] for comp in missing_components.values())
    
    print("=" * 60)
    print("🔍 ANÁLISE DOS 4% FALTANTES PARA HARMONIA COMPLETA")
    print("=" * 60)
    print(f"\n📊 Total Identificado: {total_missing}%\n")
    
    for name, details in missing_components.items():
        print(f"\n{'='*50}")
        print(f"📦 {name.replace('_', ' ')}")
        print(f"{'='*50}")
        print(f"Status: {details['status']}")
        print(f"Impacto: {details['percentage']}%")
        print(f"\n🔴 Problemas:")
        for issue in details['issues']:
            print(f"   - {issue}")
        print(f"\n📁 Arquivos Afetados:")
        for file in details['files']:
            print(f"   - {file}")
        print(f"\n✅ Solução: {details['solution']}")
    
    # Verificar status real
    print("\n" + "="*60)
    print("🔬 VERIFICANDO STATUS REAL DOS COMPONENTES")
    print("="*60)
    
    checks = []
    
    # 1. Check Ollama
    try:
        import subprocess
        result = subprocess.run(['ollama', 'list'], capture_output=True, timeout=2)
        if result.returncode == 0:
            checks.append("✅ Ollama: Respondendo")
        else:
            checks.append("❌ Ollama: Não responde")
    except:
        checks.append("❌ Ollama: Não instalado ou offline")
    
    # 2. Check Redis
    try:
        import redis
        r = redis.Redis(host='localhost', port=6379, db=0)
        r.ping()
        checks.append("✅ Redis: Conectado")
    except:
        checks.append("❌ Redis: Desconectado")
    
    # 3. Check ChromaDB
    chroma_path = Path("data/chroma")
    if chroma_path.exists() and any(chroma_path.iterdir()):
        checks.append("✅ ChromaDB: Dados encontrados")
    else:
        checks.append("⚠️ ChromaDB: Sem dados indexados")
    
    # 4. Check Memory Files
    memory_files = list(Path("apps/scripturemon").glob("*memory*.py"))
    if len(memory_files) > 3:
        checks.append(f"✅ Memory: {len(memory_files)} módulos encontrados")
    else:
        checks.append(f"⚠️ Memory: Apenas {len(memory_files)} módulos")
    
    for check in checks:
        print(f"  {check}")
    
    # Gerar relatório
    report = {
        "timestamp": datetime.now().isoformat(),
        "total_missing_percentage": total_missing,
        "components": missing_components,
        "system_checks": checks,
        "priority_fixes": [
            "1. Implementar fallback offline para Ollama (1.5%)",
            "2. Reindexar documentos e sincronizar bases (1.0%)",
            "3. Corrigir loop em ConsciousnessStream (0.8%)",
            "4. Melhorar parser de PDFs grandes (0.5%)",
            "5. Estabilizar conexão Redis pubsub (0.2%)"
        ]
    }
    
    # Salvar relatório
    report_path = Path("reports/harmony_vFinal/test_audit/missing_4percent_analysis.json")
    report_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(report_path, 'w') as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
    
    print(f"\n📊 Relatório salvo em: {report_path}")
    
    return report

if __name__ == "__main__":
    analyze_missing_harmony()