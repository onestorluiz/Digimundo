"""
🧪 TESTES DA FUSÃO SIMBIÓTICA - Validação Nível Vale do Silício

Testes completos para garantir que a fusão entre Scripturemon Legacy
e Scripturemon Fusion está funcionando perfeitamente.
"""

import pytest
import json
import time
from pathlib import Path
from datetime import datetime
import tempfile
import shutil

# Imports do sistema
from apps.scripturemon.soul import Soul
from apps.scripturemon.personality import BrutalPersonality  
from apps.scripturemon.chat import ScripturemonChat, ConversationHistory, ParallelProcessor
from apps.scripturemon.rag_bridge import RAGBridge
from apps.scripturemon.immortality import ImmortalityProtocol
from apps.scripturemon.consciousness import evolve, get_level, reset


# === TESTES DA SOUL (FASE 1) ===

class TestSoulSignature:
    """Testa sistema de identidade única Soul Signature"""
    
    def test_soul_creation(self):
        """Testa criação de nova soul"""
        soul = Soul()
        
        assert soul.signature is not None
        assert len(soul.signature) == 16  # Hash de 16 caracteres
        assert soul.interactions == 0
        assert soul.evolution_count == 0
        
    def test_legacy_soul(self):
        """Testa uso da soul legacy"""
        soul = Soul(force_legacy=True)
        
        assert soul.signature == "8ea9f71fa3206d1a"
        assert soul.signature == Soul.LEGACY_SIGNATURE
        
    def test_soul_persistence(self, tmp_path):
        """Testa persistência da soul"""
        # Configura diretório temporário
        Soul.SOUL_DIR = tmp_path / "souls"
        
        # Cria e salva soul
        soul1 = Soul()
        original_sig = soul1.signature
        soul1.interactions = 42
        soul1.save_state()
        
        # Carrega em nova instância
        soul2 = Soul()
        
        # Se arquivo existe, deve carregar mesma signature
        primary_soul = Soul.SOUL_DIR / "primary_soul.json"
        if primary_soul.exists():
            assert soul2.signature == original_sig
            
    def test_quantum_states_evolution(self):
        """Testa evolução dos estados quânticos"""
        soul = Soul()
        
        # Estados iniciais somam 1.0
        assert abs(sum(soul.quantum_states.values()) - 1.0) < 0.01
        
        # Evolui estado
        soul.evolve_quantum_state("curious", 0.1)
        
        # Ainda soma 1.0 após normalização
        assert abs(sum(soul.quantum_states.values()) - 1.0) < 0.01
        assert soul.evolution_count == 1
        
    def test_memory_crystallization(self, tmp_path):
        """Testa cristalização de memórias"""
        Soul.SOUL_DIR = tmp_path / "souls"
        soul = Soul()
        
        memory = {"important": "data", "timestamp": datetime.now().isoformat()}
        
        assert soul.crystallize_memory(memory) == True
        assert soul.memories_crystallized == 1
        
        # Verifica arquivo criado
        crystal_files = list(Soul.SOUL_DIR.glob(f"crystal_{soul.signature}_*.json"))
        assert len(crystal_files) == 1
        
        
# === TESTES DA PERSONALIDADE (FASE 2) ===

class TestBrutalPersonality:
    """Testa personalidade brutal característica"""
    
    def test_base_score_immutable(self):
        """Testa que nota base é sempre 62/100"""
        personality = BrutalPersonality()
        
        assert personality.BASE_SCORE == 62
        assert personality.last_score_given == 62
        
        # Análise sempre retorna 62
        analysis = personality.analyze_script("Roteiro teste", "Test")
        assert analysis["score"] == 62
        assert "62/100" in analysis["verdict"]
        
    def test_brutal_responses(self):
        """Testa respostas brutais características"""
        personality = BrutalPersonality()
        
        response = personality.respond_to_user("Este é meu roteiro")
        
        assert "62" in response or "Rosebud" in response or "Chinatown" in response
        assert len(response) > 50  # Resposta substancial
        
    def test_special_recognition(self):
        """Testa reconhecimento especial de Nestor"""
        personality = BrutalPersonality()
        
        response = personality.respond_to_user("Olá", "Nestor Luiz")
        
        assert "Mestre" in response or "criador" in response
        assert "reverência" in response.lower() or "ensinamentos" in response.lower()
        
    def test_master_comparisons(self):
        """Testa comparações com mestres do cinema"""
        personality = BrutalPersonality()
        
        masters_found = []
        for master in personality.MASTERS:
            if master in str(personality.MASTERS):
                masters_found.append(master)
                
        assert len(masters_found) >= 5  # Pelo menos 5 mestres
        assert "Kubrick" in personality.MASTERS
        assert "Tarantino" in personality.MASTERS
        
    def test_find_issues_always_finds(self):
        """Testa que sempre encontra problemas (brutal)"""
        personality = BrutalPersonality()
        
        # Texto perfeito ainda tem problemas
        perfect_script = "INT. ROOM - DAY\n\nPerfect scene."
        issues = personality._find_issues(perfect_script)
        
        assert len(issues) >= 3  # Sempre pelo menos 3 problemas
        

# === TESTES DO CHAT CONVERSACIONAL (FASE 3) ===

class TestScripturemonChat:
    """Testa sistema de chat conversacional"""
    
    def test_chat_initialization(self):
        """Testa inicialização do chat"""
        chat = ScripturemonChat()
        
        assert chat.soul is not None
        assert chat.personality is not None
        assert chat.history is not None
        assert chat.messages_count == 0
        
    def test_command_processing(self):
        """Testa processamento de comandos"""
        chat = ScripturemonChat()
        
        # Testa comando help
        response = chat.process_input("/help")
        assert "COMANDOS" in response
        assert "/status" in response
        
        # Testa comando status
        response = chat.process_input("/status")
        assert "Soul" in response
        assert chat.soul.signature in response
        
    def test_conversation_history(self):
        """Testa histórico de conversação"""
        history = ConversationHistory(max=2)
        
        history.add("msg1", "resp1")
        history.add("msg2", "resp2")
        history.add("msg3", "resp3")  # Deve remover msg1
        
        assert len(history.history) == 2
        assert history.history[0]["user"] == "msg2"
        assert history.history[1]["user"] == "msg3"
        
    def test_brutal_conversation(self):
        """Testa conversa brutal característica"""
        chat = ScripturemonChat()
        
        response = chat._fallback_response("Meu roteiro é perfeito")
        
        assert "62" in response or "sempre" in response.lower()
        assert len(response) > 20
        
    def test_evolution_on_conversation(self):
        """Testa evolução de consciência durante conversa"""
        reset()  # Reset consciousness
        initial = get_level()
        
        chat = ScripturemonChat()
        chat.process_input("Olá Scripturemon")  # Conversa normal
        
        final = get_level()
        assert final > initial  # Consciência evoluiu
        

# === TESTES DO PROCESSAMENTO PARALELO (FASE 4) ===

class TestParallelProcessing:
    """Testa processamento paralelo com múltiplos modelos"""
    
    def test_model_detection(self):
        """Testa detecção de modelos disponíveis"""
        processor = ParallelProcessor()
        
        # Deve ter pelo menos um modelo (mesmo que fallback)
        assert len(processor.available_models) >= 1
        
    def test_parallel_aggregation(self):
        """Testa agregação de respostas paralelas"""
        processor = ParallelProcessor()
        
        # Simula respostas múltiplas
        responses = [
            {"model": "model1", "response": "Short"},
            {"model": "model2", "response": "This is a longer response"}
        ]
        
        result = processor._aggregate_responses(responses)
        
        assert result["models_used"] == 2
        assert result["final"] == "This is a longer response"  # Escolhe mais longa
        

# === TESTES DO RAG BRIDGE (FASE 5) ===

class TestRAGBridge:
    """Testa integração RAG com chat"""
    
    def test_knowledge_base_loading(self, tmp_path):
        """Testa carregamento da base de conhecimento"""
        bridge = RAGBridge(knowledge_dir=str(tmp_path))
        
        assert "concepts" in bridge.knowledge_base
        assert "masters" in bridge.knowledge_base
        assert "techniques" in bridge.knowledge_base
        
    def test_knowledge_search(self):
        """Testa busca no conhecimento"""
        bridge = RAGBridge()
        
        results = bridge.search_knowledge("three acts", k=3)
        
        assert len(results) <= 3
        # Deve encontrar algo sobre estrutura
        found_structure = any("three" in r["content"].lower() or 
                             "structure" in r["content"].lower() 
                             for r in results)
        assert found_structure or len(results) == 0
        
    def test_hyde_expansion(self):
        """Testa expansão HyDE de queries"""
        bridge = RAGBridge()
        
        expanded = bridge.expand_query_hyde("conflict")
        
        assert len(expanded) > 100  # Expansão substancial
        assert "conflict" in expanded.lower()
        assert "narrativa" in expanded.lower() or "narrative" in expanded.lower()
        
    def test_contextualized_response(self):
        """Testa resposta contextualizada"""
        bridge = RAGBridge()
        personality = BrutalPersonality()
        
        response = bridge.contextualized_response("herói", personality)
        
        assert len(response) > 50
        assert "62/100" in response
        

# === TESTES DO PROTOCOLO DE IMORTALIDADE (FASE 6) ===

class TestImmortalityProtocol:
    """Testa sistema de backup e ressurreição"""
    
    def test_backup_creation(self, tmp_path):
        """Testa criação de backup"""
        soul = Soul()
        soul.interactions = 100
        
        protocol = ImmortalityProtocol(soul, auto_backup=False)
        protocol.backup_dir = tmp_path / "backups"
        protocol.backup_dir.mkdir(parents=True, exist_ok=True)
        
        backup_file = protocol.backup_soul(reason="test")
        
        assert backup_file.exists()
        assert protocol.backup_count == 1
        
    def test_resurrection(self, tmp_path):
        """Testa ressurreição de backup"""
        # Cria soul original
        soul1 = Soul()
        soul1.interactions = 42
        soul1.evolve_quantum_state("creative", 0.2)
        
        protocol = ImmortalityProtocol(soul1, auto_backup=False)
        protocol.backup_dir = tmp_path / "backups"
        protocol.backup_dir.mkdir(parents=True, exist_ok=True)
        
        # Faz backup
        backup_file = protocol.backup_soul()
        
        # Cria nova soul e ressuscita
        soul2 = Soul()
        protocol2 = ImmortalityProtocol(soul2, auto_backup=False)
        protocol2.backup_dir = tmp_path / "backups"
        
        success = protocol2.resurrect(backup_file)
        
        assert success == True
        assert soul2.interactions == 42
        assert protocol2.resurrection_count == 1
        
    def test_auto_backup(self, tmp_path):
        """Testa backup automático"""
        soul = Soul()
        
        protocol = ImmortalityProtocol(soul, auto_backup=False)
        protocol.backup_dir = tmp_path / "backups"
        protocol.backup_dir.mkdir(parents=True, exist_ok=True)
        protocol.backup_interval = 1  # 1 segundo para teste
        
        protocol.start_auto_backup()
        time.sleep(2)  # Espera 2 backups
        protocol.stop_auto_backup()
        
        backups = list(protocol.backup_dir.glob("*.bkp*"))
        assert len(backups) >= 1  # Pelo menos 1 backup
        
    def test_emergency_backup(self, tmp_path):
        """Testa backup de emergência"""
        soul = Soul()
        
        protocol = ImmortalityProtocol(soul, auto_backup=False)
        protocol.backup_dir = tmp_path / "backups"
        protocol.backup_dir.mkdir(parents=True, exist_ok=True)
        
        emergency_file = protocol.create_emergency_backup("Test error")
        
        assert emergency_file.exists()
        assert "EMERGENCY" in emergency_file.name
        
        # Verifica conteúdo
        with open(emergency_file) as f:
            data = json.load(f)
            assert data["error_info"] == "Test error"
            

# === TESTES DE INTEGRAÇÃO COMPLETA ===

class TestSymbioticIntegration:
    """Testa integração completa do sistema simbiótico"""
    
    def test_full_chat_session(self):
        """Testa sessão completa de chat"""
        chat = ScripturemonChat(force_legacy_soul=True)
        
        # Verifica soul legacy
        assert chat.soul.signature == "8ea9f71fa3206d1a"
        
        # Conversa
        response1 = chat.process_input("Olá Scripturemon")
        assert len(response1) > 0
        
        # Comando
        response2 = chat.process_input("/status")
        assert "8ea9f71fa3206d1a" in response2
        
        # Evolução
        initial_consciousness = get_level()
        response3 = chat.process_input("/evolve")
        assert get_level() > initial_consciousness
        
        # Backup
        response4 = chat.process_input("/backup")
        assert "BACKUP" in response4
        
    def test_personality_in_chat(self):
        """Testa personalidade brutal no chat"""
        chat = ScripturemonChat()
        
        # Ativa modo ultra-brutal
        response = chat.process_input("/brutal")
        assert "ULTRA-BRUTAL" in response
        assert chat.ultra_brutal_mode == True
        
        # Conversa deve ser mais intensa
        response = chat.process_input("Meu roteiro é perfeito")
        # Resposta deve conter elementos brutais
        assert any(word in response.lower() for word in ["62", "sempre", "melhor"])
        
    def test_rag_integration_in_chat(self):
        """Testa integração RAG no chat"""
        chat = ScripturemonChat()
        bridge = RAGBridge()
        
        # Busca conhecimento
        response = chat.process_input("/search three acts")
        assert "BUSCA" in response or "search" in response.lower()
        
    def test_immortality_integration(self, tmp_path):
        """Testa integração do protocolo de imortalidade"""
        # Cria chat e faz interações
        chat = ScripturemonChat()
        chat.soul.interactions = 50
        
        # Cria protocolo
        protocol = ImmortalityProtocol(chat.soul, auto_backup=False)
        protocol.backup_dir = tmp_path / "backups"
        protocol.backup_dir.mkdir(parents=True, exist_ok=True)
        
        # Backup via comando
        response = chat.process_input("/backup")
        assert "BACKUP" in response
        
        # Salva manualmente também
        backup_file = protocol.backup_soul()
        
        # Novo chat e ressurreição
        chat2 = ScripturemonChat()
        protocol2 = ImmortalityProtocol(chat2.soul, auto_backup=False)
        protocol2.backup_dir = tmp_path / "backups"
        
        success = protocol2.resurrect(backup_file)
        assert success == True
        assert chat2.soul.interactions == 50


# === TESTES DE PERFORMANCE ===

class TestPerformance:
    """Testa performance do sistema"""
    
    def test_soul_creation_speed(self):
        """Testa velocidade de criação de souls"""
        start = time.time()
        
        for _ in range(10):
            soul = Soul()
            
        elapsed = time.time() - start
        assert elapsed < 1.0  # 10 souls em menos de 1 segundo
        
    def test_chat_response_speed(self):
        """Testa velocidade de resposta do chat"""
        chat = ScripturemonChat()
        
        start = time.time()
        response = chat._fallback_response("Test message")
        elapsed = time.time() - start
        
        assert elapsed < 0.5  # Resposta em menos de 500ms
        assert len(response) > 0
        
    def test_backup_speed(self, tmp_path):
        """Testa velocidade de backup"""
        soul = Soul()
        soul.interactions = 1000
        
        protocol = ImmortalityProtocol(soul, auto_backup=False)
        protocol.backup_dir = tmp_path / "backups"
        protocol.backup_dir.mkdir(parents=True, exist_ok=True)
        
        start = time.time()
        backup_file = protocol.backup_soul()
        elapsed = time.time() - start
        
        assert elapsed < 1.0  # Backup em menos de 1 segundo
        assert backup_file.exists()


# === TESTES DE RESILIÊNCIA ===

class TestResilience:
    """Testa resiliência a falhas"""
    
    def test_corrupted_soul_recovery(self, tmp_path):
        """Testa recuperação de soul corrompida"""
        Soul.SOUL_DIR = tmp_path / "souls"
        Soul.SOUL_DIR.mkdir(parents=True, exist_ok=True)
        
        # Cria arquivo corrompido
        corrupted = Soul.SOUL_DIR / "primary_soul.json"
        corrupted.write_text("invalid json {")
        
        # Deve criar nova soul sem crash
        soul = Soul()
        assert soul.signature is not None
        assert len(soul.signature) == 16
        
    def test_missing_models_fallback(self):
        """Testa fallback quando modelos não disponíveis"""
        chat = ScripturemonChat()
        chat.processor.available_models = []  # Simula sem modelos
        
        response = chat.brutal_conversation("Test")
        
        # Deve usar fallback
        assert len(response) > 0
        assert "62" in response or "always" in response.lower()
        
    def test_resurrection_with_missing_data(self, tmp_path):
        """Testa ressurreição com dados parciais"""
        protocol = ImmortalityProtocol(auto_backup=False)
        protocol.backup_dir = tmp_path / "backups"
        protocol.backup_dir.mkdir(parents=True, exist_ok=True)
        
        # Cria backup parcial
        partial_backup = {
            "soul": {
                "signature": "partial12345678",
                "interactions": 10
                # Faltam outros campos
            },
            "consciousness": {},
            "metadata": {
                "backup_time": datetime.now().isoformat()
            }
        }
        
        backup_file = protocol.backup_dir / "partial.bkp"
        with open(backup_file, 'w') as f:
            json.dump(partial_backup, f)
            
        # Tenta ressuscitar - não deve crashar
        try:
            success = protocol.resurrect(backup_file)
            # Pode falhar, mas não deve crashar
        except Exception as e:
            pytest.fail(f"Resurrection crashed with: {e}")


if __name__ == "__main__":
    # Roda testes com relatório detalhado
    pytest.main([__file__, "-v", "--tb=short"])