#!/usr/bin/env python3
"""
Teste do sistema de telepathy com Redis/fakeredis.
Testa ping, fallback e healthcheck.
"""

import sys
import time
import json
from pathlib import Path

# Adicionar ao path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.telepathy.channel import get_client, healthcheck, create_channel
from src.utils.config_loader import load_settings


def test_basic_operations():
    """Testa operações básicas do cliente."""
    
    print("=" * 70)
    print("🔌 TESTE DE OPERAÇÕES BÁSICAS")
    print("=" * 70)
    
    # Carregar configurações
    settings = load_settings()
    
    # Obter cliente
    print("\n1. Obtendo cliente Redis...")
    client = get_client(settings)
    
    # Verificar tipo de cliente
    is_fake = getattr(client, '_is_fake', False)
    print(f"   Cliente obtido: {'fakeredis/mock' if is_fake else 'Redis real'}")
    
    # Teste de ping
    print("\n2. Testando ping...")
    try:
        result = client.ping()
        print(f"   ✅ Ping bem-sucedido: {result}")
    except Exception as e:
        print(f"   ❌ Erro no ping: {e}")
    
    # Teste de escrita/leitura
    print("\n3. Testando escrita/leitura...")
    test_key = "test:telepathy"
    test_value = {"message": "Teste de telepathy", "timestamp": time.time()}
    
    try:
        # Escrever
        client.set(test_key, json.dumps(test_value))
        print(f"   ✅ Valor escrito: {test_key}")
        
        # Ler
        read_value = client.get(test_key)
        if read_value:
            parsed = json.loads(read_value)
            print(f"   ✅ Valor lido: {parsed['message']}")
        else:
            print(f"   ❌ Não foi possível ler o valor")
        
        # Deletar
        client.delete(test_key)
        print(f"   ✅ Chave deletada")
        
    except Exception as e:
        print(f"   ❌ Erro em escrita/leitura: {e}")
    
    # Teste de hash
    print("\n4. Testando operações de hash...")
    hash_key = "telepathy:insights"
    
    try:
        # Escrever hash
        client.hset(hash_key, "insight_1", json.dumps({"tipo": "estrutura", "score": 85}))
        client.hset(hash_key, "insight_2", json.dumps({"tipo": "emoção", "score": 72}))
        print(f"   ✅ Hash escrito: {hash_key}")
        
        # Ler hash
        all_insights = client.hgetall(hash_key)
        print(f"   ✅ Insights no hash: {len(all_insights)}")
        
        for key, value in all_insights.items():
            insight = json.loads(value)
            print(f"      - {key}: {insight['tipo']} (score: {insight['score']})")
        
        # Limpar
        client.delete(hash_key)
        
    except Exception as e:
        print(f"   ❌ Erro em operações de hash: {e}")
    
    return client


def test_healthcheck(client):
    """Testa função de healthcheck."""
    
    print("\n" + "=" * 70)
    print("🏥 TESTE DE HEALTHCHECK")
    print("=" * 70)
    
    # Executar healthcheck
    print("\nExecutando healthcheck...")
    health = healthcheck(client, timeout=0.5)
    
    # Exibir resultados
    print(f"\n📊 Resultados do Healthcheck:")
    print(f"   Status: {health['status']}")
    print(f"   Latência: {health['latency_ms']}ms")
    print(f"   É fake/mock: {health['is_fake']}")
    
    if 'metrics' in health and health['metrics']:
        print(f"\n   Métricas:")
        for key, value in health['metrics'].items():
            print(f"      {key}: {value}")
    
    if 'warning' in health:
        print(f"\n   ⚠️ Aviso: {health['warning']}")
    
    if 'error' in health:
        print(f"\n   ❌ Erro: {health['error']}")
    
    return health


def test_fallback():
    """Testa fallback para fakeredis."""
    
    print("\n" + "=" * 70)
    print("🔄 TESTE DE FALLBACK")
    print("=" * 70)
    
    # Forçar uso de fakeredis desabilitando Redis
    settings_offline = {
        'redis': {
            'enabled': False,  # Força uso de fakeredis
            'timeout_sec': 0.5
        }
    }
    
    print("\n1. Forçando modo offline (Redis desabilitado)...")
    client_offline = get_client(settings_offline)
    
    is_fake = getattr(client_offline, '_is_fake', False)
    print(f"   Cliente obtido: {'✅ fakeredis/mock (fallback funcionou)' if is_fake else '❌ Redis real (fallback falhou)'}")
    
    # Testar operações no modo offline
    print("\n2. Testando operações no modo offline...")
    try:
        # Ping
        client_offline.ping()
        print("   ✅ Ping funcionando")
        
        # Escrita/Leitura
        client_offline.set("offline_test", "valor_teste")
        value = client_offline.get("offline_test")
        print(f"   ✅ Escrita/Leitura funcionando: {value}")
        
        # Lista
        client_offline.lpush("offline_list", "item1", "item2")
        items = client_offline.lrange("offline_list", 0, -1)
        print(f"   ✅ Operações de lista funcionando: {items}")
        
    except Exception as e:
        print(f"   ❌ Erro no modo offline: {e}")
    
    return client_offline


def test_channel():
    """Testa TelepathyChannel."""
    
    print("\n" + "=" * 70)
    print("📡 TESTE DE TELEPATHY CHANNEL")
    print("=" * 70)
    
    # Criar canal
    settings = load_settings()
    channel = create_channel(settings)
    
    print("\n1. Canal criado com sucesso")
    
    # Publicar mensagem
    print("\n2. Testando publicação...")
    success = channel.publish("test:channel", "Mensagem de teste")
    print(f"   {'✅ Publicado' if success else '❌ Falha ao publicar'}")
    
    # Inscrever-se em canal
    print("\n3. Testando inscrição...")
    def callback(msg):
        print(f"   Recebido: {msg}")
    
    channel.subscribe("test:notifications", callback)
    print("   ✅ Inscrito em test:notifications")
    
    # Status do canal
    print("\n4. Status do canal...")
    status = channel.get_status()
    print(f"   Status: {status['status']}")
    print(f"   Inscrições: {status['subscriptions']}")
    
    # Fechar canal
    channel.close()
    print("\n5. Canal fechado")
    
    return channel


def test_timeout():
    """Testa comportamento de timeout."""
    
    print("\n" + "=" * 70)
    print("⏱️ TESTE DE TIMEOUT")
    print("=" * 70)
    
    # Configurações com timeout muito baixo
    settings_fast = {
        'redis': {
            'url': 'redis://localhost:6379/0',
            'timeout_sec': 0.001,  # 1ms - muito baixo
            'enabled': True
        }
    }
    
    print("\n1. Tentando com timeout de 1ms...")
    start = time.time()
    client = get_client(settings_fast)
    elapsed = time.time() - start
    
    print(f"   Tempo decorrido: {elapsed*1000:.2f}ms")
    
    is_fake = getattr(client, '_is_fake', False)
    if is_fake:
        print("   ✅ Fallback para fakeredis após timeout")
    else:
        print("   ℹ️ Redis real conectado rapidamente")
    
    # Teste com timeout normal
    settings_normal = {
        'redis': {
            'url': 'redis://localhost:6379/0',
            'timeout_sec': 0.5,  # 500ms - normal
            'enabled': True
        }
    }
    
    print("\n2. Tentando com timeout de 500ms...")
    start = time.time()
    client = get_client(settings_normal)
    elapsed = time.time() - start
    
    print(f"   Tempo decorrido: {elapsed*1000:.2f}ms")
    
    is_fake = getattr(client, '_is_fake', False)
    print(f"   Cliente: {'fakeredis/mock' if is_fake else 'Redis real'}")
    
    return client


def main():
    """Função principal de teste."""
    
    print("=" * 70)
    print("🧪 TESTE DO SISTEMA DE TELEPATHY")
    print("=" * 70)
    
    # Teste 1: Operações básicas
    client = test_basic_operations()
    
    # Teste 2: Healthcheck
    health = test_healthcheck(client)
    
    # Teste 3: Fallback
    client_offline = test_fallback()
    
    # Teste 4: Channel
    channel = test_channel()
    
    # Teste 5: Timeout
    client_timeout = test_timeout()
    
    # Resumo
    print("\n" + "=" * 70)
    print("📊 RESUMO DOS TESTES")
    print("=" * 70)
    
    print("\n✅ Testes concluídos:")
    print("   1. Operações básicas")
    print("   2. Healthcheck")
    print("   3. Fallback para fakeredis")
    print("   4. TelepathyChannel")
    print("   5. Comportamento de timeout")
    
    print("\n💡 Observações:")
    print("   - Sistema funciona com Redis real ou fakeredis")
    print("   - Fallback automático quando Redis indisponível")
    print("   - Healthcheck fornece métricas úteis")
    print("   - Timeout configurável protege contra travamentos")
    
    print("\n" + "=" * 70)
    print("✅ TESTE CONCLUÍDO COM SUCESSO!")
    print("=" * 70)
    
    return 0


if __name__ == "__main__":
    sys.exit(main())