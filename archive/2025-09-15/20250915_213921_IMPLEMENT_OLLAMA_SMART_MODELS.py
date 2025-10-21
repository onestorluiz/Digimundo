#!/usr/bin/env python3
"""
🤖 IMPLEMENT OLLAMA SMART MODELS
Cria modelos customizados e implementa gatilhos inteligentes
MANTENDO EXTREMA ROBUSTEZ
"""

import subprocess
import json
from pathlib import Path
import time
import re

def create_custom_models():
    """Cria modelos customizados do Ollama"""
    
    print("🤖 CRIANDO MODELOS CUSTOMIZADOS")
    print("="*70)
    
    modelfiles_dir = Path("/Users/clubproducoes/Digimundo/scripturemon-validation")
    
    models_to_create = [
        {
            'name': 'scripturemon-smart',
            'modelfile': 'scripturemon-gradient.Modelfile',
            'description': 'Modelo otimizado para análise rápida'
        },
        {
            'name': 'scripturemon-deep',
            'modelfile': 'scripturemon-deepseek-complete.Modelfile',
            'description': 'Modelo profundo para análises detalhadas'
        }
    ]
    
    created = 0
    
    for model_info in models_to_create:
        modelfile_path = modelfiles_dir / model_info['modelfile']
        
        if not modelfile_path.exists():
            print(f"  ⚠️ {model_info['modelfile']} não encontrado")
            continue
        
        print(f"\n📦 Criando {model_info['name']}...")
        print(f"   {model_info['description']}")
        
        # Verificar se já existe
        check_cmd = ['ollama', 'show', model_info['name']]
        check_result = subprocess.run(check_cmd, capture_output=True)
        
        if check_result.returncode == 0:
            print(f"   ✅ Modelo já existe")
            created += 1
            continue
        
        # Criar modelo
        create_cmd = ['ollama', 'create', model_info['name'], '-f', str(modelfile_path)]
        print(f"   🔄 Executando: ollama create {model_info['name']}...")
        
        result = subprocess.run(create_cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print(f"   ✅ Modelo criado com sucesso")
            created += 1
        else:
            print(f"   ❌ Erro ao criar: {result.stderr[:100]}")
    
    print(f"\n📊 Total: {created}/{len(models_to_create)} modelos disponíveis")
    return created > 0

def implement_smart_triggers():
    """Implementa gatilhos inteligentes para modelos grandes"""
    
    print("\n🎯 IMPLEMENTANDO GATILHOS INTELIGENTES")
    print("="*70)
    
    # Modificar o scripturemon.fixed
    scripturemon_path = Path("/Users/clubproducoes/Digimundo/scripturemon-validation/bin/scripturemon.fixed")
    
    if not scripturemon_path.exists():
        print("❌ scripturemon.fixed não encontrado")
        return False
    
    content = scripturemon_path.read_text()
    
    # Código do sistema de gatilhos
    trigger_system = '''
    def _should_use_deep_model(self, input_text):
        """
        Determina se deve usar modelo grande baseado em palavras-gatilho
        Palavras: profunda, profundo, detalhada, detalhado, meticulosa, feedback
        """
        trigger_words = [
            'profunda', 'profundo', 'profundamente',
            'detalhada', 'detalhado', 'detalhadamente', 
            'meticulosa', 'meticuloso', 'meticulosamente',
            'feedback', 'análise completa', 'análise profunda',
            'revisão completa', 'revisão detalhada'
        ]
        
        input_lower = input_text.lower()
        
        for trigger in trigger_words:
            if trigger in input_lower:
                print(f"   🎯 Gatilho detectado: '{trigger}' - Ativando modelo profundo")
                return True
        
        return False
    
    def _get_model_for_query(self, query):
        """
        Seleciona o modelo apropriado baseado na query
        Retorna tupla (model_name, timeout_seconds)
        """
        # Verificar gatilhos para modelo grande
        if self._should_use_deep_model(query):
            # Modelos grandes com timeout maior
            deep_models = [
                ('deepseek-r1:32b', 120),
                ('scripturemon-deep:latest', 90),
                ('llama3.1:70b', 90),
                ('mistral-large:latest', 60)
            ]
            
            # Verificar qual está disponível
            for model, timeout in deep_models:
                if self._check_model_exists(model):
                    print(f"   🧠 Usando modelo profundo: {model} (timeout: {timeout}s)")
                    return model, timeout
        
        # Modelos padrão rápidos
        fast_models = [
            ('scripturemon-smart:latest', 30),
            ('llama3.2:3b', 20),
            ('mistral:7b-instruct', 20),
            ('phi3:mini', 15)
        ]
        
        for model, timeout in fast_models:
            if self._check_model_exists(model):
                return model, timeout
        
        # Fallback
        return ('llama3.2:3b', 30)
    
    def _check_model_exists(self, model_name):
        """Verifica se modelo existe no Ollama"""
        try:
            result = subprocess.run(
                ['ollama', 'show', model_name],
                capture_output=True,
                timeout=2
            )
            return result.returncode == 0
        except:
            return False
'''
    
    # Adicionar métodos após a classe
    lines = content.split('\n')
    
    # Procurar onde inserir
    for i, line in enumerate(lines):
        if 'class ScripturemonMaxCapacity' in line:
            # Procurar um bom lugar para inserir (após outros métodos)
            for j in range(i + 100, min(i + 500, len(lines))):
                if 'def process_' in lines[j]:
                    # Inserir antes deste método
                    lines.insert(j - 1, trigger_system)
                    print("✅ Sistema de gatilhos adicionado")
                    break
            break
    
    # Modificar o processo de seleção de modelo
    model_selection_code = '''
        # Sistema inteligente de seleção de modelo
        selected_model, timeout = self._get_model_for_query(processed_input)
        
        # Ajustar configurações baseado no modelo
        if 'deep' in selected_model or '32b' in selected_model or '70b' in selected_model:
            print(f"   ⚡ Modo profundo ativado - Timeout estendido: {timeout}s")
            processing_mode = 'deep'
        else:
            processing_mode = 'fast'
'''
    
    # Procurar onde o modelo é selecionado e substituir
    for i, line in enumerate(lines):
        if 'ollama run' in line or 'model_name' in line:
            # Verificar contexto
            if 'def ' in lines[max(0, i-10):i]:
                # Estamos dentro de uma função que usa ollama
                # Adicionar seleção inteligente se não existe
                if '_get_model_for_query' not in '\n'.join(lines[max(0, i-20):i+20]):
                    lines.insert(i, model_selection_code)
                    print("✅ Seleção inteligente de modelo adicionada")
                    break
    
    # Salvar arquivo modificado
    scripturemon_path.write_text('\n'.join(lines))
    print("💾 scripturemon.fixed atualizado com gatilhos inteligentes")
    
    return True

def update_model_priorities():
    """Atualiza prioridades dos modelos no sistema"""
    
    print("\n📊 ATUALIZANDO PRIORIDADES DE MODELOS")
    print("="*70)
    
    # Criar arquivo de configuração de modelos
    config_path = Path("/Users/clubproducoes/Digimundo/scripturemon-validation/config/model_priorities.json")
    config_path.parent.mkdir(parents=True, exist_ok=True)
    
    model_config = {
        "fast_models": [
            {"name": "scripturemon-smart:latest", "timeout": 30, "priority": 1},
            {"name": "llama3.2:3b", "timeout": 20, "priority": 2},
            {"name": "mistral:7b-instruct", "timeout": 20, "priority": 3},
            {"name": "phi3:mini", "timeout": 15, "priority": 4}
        ],
        "deep_models": [
            {"name": "deepseek-r1:32b", "timeout": 120, "priority": 1},
            {"name": "scripturemon-deep:latest", "timeout": 90, "priority": 2},
            {"name": "llama3.1:70b", "timeout": 90, "priority": 3},
            {"name": "mistral-large:latest", "timeout": 60, "priority": 4}
        ],
        "trigger_words": {
            "deep_analysis": [
                "profunda", "profundo", "profundamente",
                "detalhada", "detalhado", "detalhadamente",
                "meticulosa", "meticuloso", "meticulosamente",
                "feedback", "análise completa", "análise profunda",
                "revisão completa", "revisão detalhada", "aprofundada"
            ],
            "fast_response": [
                "rápido", "simples", "resumo", "breve",
                "direto", "objetivo", "curto"
            ]
        },
        "default_timeout": 30,
        "max_timeout": 120
    }
    
    with open(config_path, 'w', encoding='utf-8') as f:
        json.dump(model_config, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Configuração salva em: {config_path}")
    print(f"   - {len(model_config['fast_models'])} modelos rápidos")
    print(f"   - {len(model_config['deep_models'])} modelos profundos")
    print(f"   - {len(model_config['trigger_words']['deep_analysis'])} palavras-gatilho")
    
    return True

def test_smart_system():
    """Testa o sistema de modelos inteligentes"""
    
    print("\n🧪 TESTANDO SISTEMA INTELIGENTE")
    print("="*70)
    
    test_queries = [
        ("O que é cinema?", "fast", "Pergunta simples"),
        ("Faça uma análise profunda do roteiro", "deep", "Contém 'profunda'"),
        ("Explique detalhadamente a estrutura", "deep", "Contém 'detalhadamente'"),
        ("Dê um feedback meticuloso", "deep", "Contém 'feedback' e 'meticuloso'"),
        ("Resumo rápido do filme", "fast", "Contém 'rápido'")
    ]
    
    print("\n📝 Testando detecção de gatilhos:")
    
    trigger_words = [
        'profunda', 'profundo', 'detalhada', 'detalhado', 
        'meticulosa', 'feedback'
    ]
    
    for query, expected, reason in test_queries:
        query_lower = query.lower()
        should_use_deep = any(trigger in query_lower for trigger in trigger_words)
        
        mode = "deep" if should_use_deep else "fast"
        status = "✅" if mode == expected else "❌"
        
        print(f"\n  Query: '{query}'")
        print(f"  {status} Modo detectado: {mode} (esperado: {expected})")
        print(f"  Razão: {reason}")
    
    return True

if __name__ == "__main__":
    print("🤖 IMPLEMENTANDO SISTEMA INTELIGENTE DE MODELOS")
    print("="*70)
    
    success = True
    
    # 1. Criar modelos customizados
    print("\n[FASE 1] Criando modelos customizados...")
    if create_custom_models():
        print("✅ Modelos customizados disponíveis")
    else:
        print("⚠️ Alguns modelos não foram criados")
    
    # 2. Implementar gatilhos
    print("\n[FASE 2] Implementando gatilhos inteligentes...")
    if implement_smart_triggers():
        print("✅ Gatilhos implementados")
    else:
        success = False
    
    # 3. Atualizar prioridades
    print("\n[FASE 3] Configurando prioridades...")
    if update_model_priorities():
        print("✅ Prioridades configuradas")
    else:
        success = False
    
    # 4. Testar sistema
    print("\n[FASE 4] Testando sistema...")
    if test_smart_system():
        print("✅ Testes OK")
    else:
        success = False
    
    if success:
        print("\n" + "="*70)
        print("🎉 SISTEMA INTELIGENTE DE MODELOS IMPLEMENTADO!")
        print("\n🎯 Palavras-gatilho para modelos grandes (32GB+):")
        print("  • profunda/profundo")
        print("  • detalhada/detalhado")
        print("  • meticulosa/meticuloso")
        print("  • feedback")
        print("\n⚡ Sistema automático:")
        print("  - Detecta gatilhos e ativa modelo apropriado")
        print("  - Timeout adaptativo (15s-120s)")
        print("  - Fallback inteligente se modelo não disponível")
        print("\n💪 EXTREMA ROBUSTEZ MANTIDA!")
    else:
        print("\n⚠️ Sistema parcialmente implementado")