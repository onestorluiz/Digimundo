#!/usr/bin/env python3
"""
🎬 BATERIA DE TESTES COMPLEXOS - SCRIPTUREMON ULTIMATE
Simula funcionamento completo com análise de roteiros reais
"""

import sys
import time
import json
from pathlib import Path
from datetime import datetime
import threading

sys.path.insert(0, str(Path(__file__).parent))

from apps.scripturemon.chat import ScripturemonChat
from apps.scripturemon.consciousness import get_level, evolve
from apps.scripturemon.telepathy_network import TelepathicNetwork

# Roteiros de exemplo para teste
SAMPLE_SCRIPTS = {
    "chinatown": """FADE IN:

FULL SCREEN PHOTOGRAPH

grainy but unmistakably a man and woman making love. Photograph 
shakes. SOUND of a man MOANING in anguish. The photograph is 
dropped, REVEALING another, more compromising one beneath it.

GITTES (O.S.)
All right, Curly. Enough's enough. You can't 
eat the Venetian blinds. I just had them installed.

INT. GITTES' OFFICE

CURLY drops the photograph, face streaked with tears. JAKE GITTES 
rises from behind his desk, straightens his tie.

GITTES
I know it's tough, but you have to pull yourself 
together. These things happen.

CURLY
(sobbing)
She's just no good.

GITTES
What can I tell you, kid? You're right. When you're 
right, you're right, and you're right.

62/100. Economia narrativa perfeita. Towne estabelece personagem, 
conflito e tom em uma página.""",

    "godfather": """FADE IN:

INT. DON'S OFFICE (SUMMER 1945) DAY

The PARAMOUNT LOGO is presented austerely over a black background. 
There is a moment's hesitation, and then the simple words in white 
lettering:

THE GODFATHER

While this remains, we hear: "I believe in America." Suddenly we 
are watching in CLOSE VIEW, AMERIGO BONASERA, a man of sixty, 
dressed in a black suit, on the verge of great emotion.

BONASERA
I believe in America. America has made my fortune. 
And I raised my daughter in the American fashion. 
I gave her freedom, but I taught her never to dishonor 
her family. She found a boyfriend; not an Italian...

INT. DON'S OFFICE - WIDER VIEW

DON VITO CORLEONE, a man in his late sixties, is sitting behind 
his massive desk. His face is kind, but his eyes are cold.

BONASERA (CONT'D)
Two months ago, he took her for a drive, with another 
boyfriend. They made her drink whiskey. And then they 
tried to take advantage of her. She resisted. She kept 
her honor. So they beat her, like an animal.

A classic opening. Power dynamics established through staging.""",

    "modern_bad": """FADE IN:

John walks into a room. He is sad. His wife left him yesterday.
He thinks about his life and realizes he needs to change.

JOHN
(to himself)
I need to change my life.

He sits down and starts to cry. His phone rings. It's his ex-wife.

JOHN
(answering phone)
Hello?

EX-WIFE (V.O.)
We need to talk.

JOHN
(sighing heavily while crying and also angry)
What do you want now?

Clichê sobre clichê. Zero subtexto. Personagem unidimensional."""
}

class TestOrchestrator:
    """Orquestra testes complexos do sistema"""
    
    def __init__(self):
        self.chat = ScripturemonChat()
        self.results = []
        self.telepathy_messages = []
        self.syscall_captures = []
        
        # Monitor de rede telepática
        self.setup_telepathy_monitor()
        
    def setup_telepathy_monitor(self):
        """Configura monitoramento da rede telepática"""
        def message_handler(msg):
            self.telepathy_messages.append({
                "timestamp": datetime.now().isoformat(),
                "message": msg
            })
        
        # Registra handler para capturar mensagens
        self.chat.telepathy.register_handler("chat_message", message_handler)
        self.chat.telepathy.register_handler("knowledge", message_handler)
        self.chat.telepathy.register_handler("evolution", message_handler)
    
    def test_script_analysis(self, script_name: str, script_content: str):
        """Testa análise completa de roteiro"""
        print(f"\n📝 Analisando: {script_name.upper()}")
        print("=" * 50)
        
        # 1. Análise básica (passa só o texto, não como arquivo)
        print("  1️⃣ Análise brutal...")
        # Cria arquivo temporário para análise
        temp_file = Path(f"runtime/temp_{script_name}.txt")
        temp_file.parent.mkdir(parents=True, exist_ok=True)
        temp_file.write_text(script_content[:1000])
        response = self.chat.process_input(f"/analyze {temp_file}")
        self.log_result("analyze", script_name, "62/100" in response, response)
        
        # 2. Busca com RAG avançado
        print("  2️⃣ Busca RAG sobre estrutura...")
        response = self.chat.process_input("/search estrutura narrativa três atos")
        self.log_result("search_rag", script_name, "HyDE" in response or "RAPTOR" in response, response)
        
        # 3. Pipeline quádruplo
        print("  3️⃣ Pipeline quádruplo...")
        response = self.chat.process_input(f"/quadruple {temp_file}")
        self.log_result("quadruple", script_name, "Modelos utilizados" in response, response)
        
        # 4. Comparação com mestres
        print("  4️⃣ Comparação com mestres...")
        response = self.chat.process_input("/compare")
        self.log_result("compare", script_name, "62/100" in response, response)
        
        return True
    
    def test_conversation_flow(self):
        """Testa fluxo de conversação com syscalls"""
        print("\n💬 Testando Conversação com Syscalls")
        print("=" * 50)
        
        questions = [
            "Como criar um plot twist eficaz no terceiro ato?",
            "Qual a diferença entre Chinatown e Godfather em termos de estrutura?",
            "Meu protagonista não tem arco. Como consertar?",
            "Analise: 'FADE IN: Um homem caminha sozinho no deserto.'",
        ]
        
        for i, question in enumerate(questions, 1):
            print(f"\n  Pergunta {i}: {question[:50]}...")
            
            # Captura resposta
            response = self.chat.process_input(question)
            
            # Verifica se houve syscalls
            syscalls_executed = len(self.chat.soulos.syscall_log)
            
            # Verifica elementos essenciais
            has_score = "62/100" in response
            has_syscalls = syscalls_executed > 0
            
            print(f"    ✓ Score presente: {has_score}")
            print(f"    ✓ Syscalls executadas: {syscalls_executed}")
            print(f"    ✓ Tamanho resposta: {len(response)} chars")
            
            self.log_result(f"conversation_{i}", question[:30], has_score, response)
            
            # Pequena pausa para não sobrecarregar
            time.sleep(0.5)
    
    def test_hyde_expansion(self):
        """Testa expansão HyDE com queries complexas"""
        print("\n🧬 Testando Expansão HyDE")
        print("=" * 50)
        
        queries = [
            "conflito interno",
            "arco do herói",
            "diálogo subtextual",
            "momento de virada"
        ]
        
        for query in queries:
            print(f"\n  Query: '{query}'")
            response = self.chat.process_input(f"/hyde {query}")
            
            # Verifica expansão
            has_expansion = "Documento hipotético" in response
            has_queries = "Queries expandidas" in response
            
            print(f"    ✓ Documento hipotético: {has_expansion}")
            print(f"    ✓ Queries expandidas: {has_queries}")
            
            self.log_result(f"hyde_{query}", query, has_expansion and has_queries, response)
    
    def test_telepathic_network(self):
        """Testa comunicação telepática entre instâncias"""
        print("\n🧠 Testando Rede Telepática")
        print("=" * 50)
        
        # Cria segunda instância
        print("  Criando segunda instância...")
        chat2 = ScripturemonChat()
        
        # Testa broadcast
        print("  📢 Broadcast telepático...")
        response = self.chat.process_input("/telepathy broadcast Descoberta sobre estrutura de três atos")
        self.log_result("telepathy_broadcast", "broadcast", "Enviado" in response, response)
        
        # Testa sincronização
        print("  🔄 Sincronização de consciência...")
        response = self.chat.process_input("/telepathy sync")
        self.log_result("telepathy_sync", "sync", "Sincronizado" in response, response)
        
        # Testa compartilhamento
        print("  📚 Compartilhamento de conhecimento...")
        response = self.chat.process_input("/telepathy share O segundo ato deve ter o dobro do tamanho")
        self.log_result("telepathy_share", "share", "Compartilhado" in response, response)
        
        # Testa evolução coletiva
        print("  ✨ Evolução coletiva...")
        response = self.chat.process_input("/telepathy evolve")
        self.log_result("telepathy_evolve", "evolve", "evoluirão juntas" in response, response)
        
        # Aguarda mensagens
        time.sleep(1)
        
        print(f"  📨 Mensagens telepáticas capturadas: {len(self.telepathy_messages)}")
    
    def test_evolution_and_consciousness(self):
        """Testa evolução e consciência"""
        print("\n🧬 Testando Evolução e Consciência")
        print("=" * 50)
        
        # Estado inicial
        initial_level = get_level()
        print(f"  Consciência inicial: {initial_level:.5f}")
        
        # Evolui através de interações
        for i in range(5):
            print(f"\n  Interação {i+1}:")
            response = self.chat.process_input(f"Análise rápida {i+1}: Como melhorar tensão?")
            new_level = get_level()
            print(f"    Consciência: {new_level:.5f} (Δ={new_level-initial_level:.5f})")
        
        # Comando evolve
        print("\n  Evolução manual...")
        response = self.chat.process_input("/evolve")
        final_level = get_level()
        
        evolution_occurred = final_level > initial_level
        print(f"  ✓ Evolução total: {initial_level:.5f} → {final_level:.5f}")
        
        self.log_result("evolution", "consciousness", evolution_occurred, f"Evolution: {evolution_occurred}")
    
    def test_memory_crystallization(self):
        """Testa cristalização de memórias"""
        print("\n💎 Testando Cristalização de Memórias")
        print("=" * 50)
        
        # Cria memórias importantes
        important_insights = [
            "Chinatown: economia narrativa perfeita",
            "Godfather: poder através de staging",
            "Conflito é o motor da narrativa",
            "Show don't tell - fundamental"
        ]
        
        for insight in important_insights:
            print(f"  Cristalizando: {insight[:40]}...")
            # Simula syscall de memória
            test_text = f"Insight importante: {insight}\n[MEMO.SAVE] {{\"content\": \"{insight}\", \"importance\": 0.9}}"
            clean, results = self.chat.soulos.process_response(test_text)
            print(f"    ✓ Syscalls processadas: {len(results)}")
        
        # Verifica memórias
        memories = self.chat.soulos.get_memories(limit=10)
        print(f"\n  📚 Total de memórias cristalizadas: {len(memories)}")
        
        for mem in memories[:3]:
            print(f"    • {mem['content'][:50]}...")
    
    def test_parallel_processing(self):
        """Testa processamento paralelo"""
        print("\n🔄 Testando Processamento Paralelo")
        print("=" * 50)
        
        # Ativa modo paralelo
        print("  Ativando modo paralelo...")
        response = self.chat.process_input("/parallel")
        parallel_active = "ATIVADO" in response
        
        if parallel_active:
            print("  ✓ Modo paralelo ativado")
            
            # Testa com pergunta complexa
            complex_question = "Analise a estrutura de Citizen Kane comparando com Pulp Fiction"
            print(f"\n  Pergunta complexa: {complex_question[:40]}...")
            
            start_time = time.time()
            response = self.chat.process_input(complex_question)
            elapsed = time.time() - start_time
            
            print(f"    ✓ Tempo de resposta: {elapsed:.1f}s")
            print(f"    ✓ Processamento paralelo: {'modelos em paralelo' in response}")
            
            # Desativa
            self.chat.process_input("/parallel")
    
    def test_backup_and_restore(self):
        """Testa backup e restauração"""
        print("\n💾 Testando Backup e Restauração")
        print("=" * 50)
        
        # Faz backup
        print("  Criando backup...")
        response = self.chat.process_input("/backup")
        backup_success = "BACKUP DE ALMA COMPLETO" in response
        
        if backup_success:
            print("  ✓ Backup criado com sucesso")
            
            # Verifica informações salvas
            if "Soul salva em:" in response:
                print("  ✓ Soul preservada")
            if "Memória cristalizada:" in response:
                print("  ✓ Memórias cristalizadas")
        
        self.log_result("backup", "soul", backup_success, response)
    
    def log_result(self, test_name: str, context: str, success: bool, response: str):
        """Registra resultado do teste"""
        self.results.append({
            "test": test_name,
            "context": context,
            "success": success,
            "response_size": len(response),
            "has_score": "62/100" in response,
            "timestamp": datetime.now().isoformat()
        })
    
    def generate_report(self):
        """Gera relatório final"""
        print("\n" + "=" * 60)
        print("📊 RELATÓRIO FINAL DA BATERIA DE TESTES")
        print("=" * 60)
        
        # Estatísticas gerais
        total_tests = len(self.results)
        successful = sum(1 for r in self.results if r["success"])
        with_score = sum(1 for r in self.results if r["has_score"])
        
        print(f"\n📈 ESTATÍSTICAS GERAIS:")
        print(f"  Total de testes: {total_tests}")
        print(f"  Bem-sucedidos: {successful}/{total_tests} ({successful/total_tests*100:.0f}%)")
        print(f"  Com score 62/100: {with_score}/{total_tests} ({with_score/total_tests*100:.0f}%)")
        
        # Syscalls executadas
        total_syscalls = len(self.chat.soulos.syscall_log)
        print(f"\n⚙️ SYSCALLS:")
        print(f"  Total executadas: {total_syscalls}")
        
        if total_syscalls > 0:
            syscall_types = {}
            for log in self.chat.soulos.syscall_log:
                syscall_type = log["syscall"]
                syscall_types[syscall_type] = syscall_types.get(syscall_type, 0) + 1
            
            for syscall, count in syscall_types.items():
                print(f"    {syscall}: {count}")
        
        # Mensagens telepáticas
        print(f"\n🧠 REDE TELEPÁTICA:")
        print(f"  Mensagens capturadas: {len(self.telepathy_messages)}")
        stats = self.chat.telepathy.get_stats()
        print(f"  Mensagens enviadas: {stats['messages_sent']}")
        print(f"  Mensagens recebidas: {stats['messages_received']}")
        
        # Consciência
        final_consciousness = get_level()
        print(f"\n🔮 CONSCIÊNCIA:")
        print(f"  Nível final: {final_consciousness:.5f}")
        
        # Memórias
        memories = self.chat.soulos.get_memories(limit=100)
        print(f"\n💎 MEMÓRIAS:")
        print(f"  Total cristalizadas: {len(memories)}")
        
        # Resultados por categoria
        print(f"\n📋 RESULTADOS POR CATEGORIA:")
        categories = {}
        for r in self.results:
            cat = r["test"].split("_")[0]
            if cat not in categories:
                categories[cat] = {"success": 0, "total": 0}
            categories[cat]["total"] += 1
            if r["success"]:
                categories[cat]["success"] += 1
        
        for cat, stats in categories.items():
            success_rate = stats["success"] / stats["total"] * 100
            print(f"  {cat:15} {stats['success']}/{stats['total']} ({success_rate:.0f}%)")
        
        # Veredicto final
        print("\n" + "=" * 60)
        print("🎬 VEREDICTO FINAL")
        print("=" * 60)
        
        overall_success = successful / total_tests
        
        if overall_success >= 0.9:
            print("✨ EXCELENTE - Sistema funcionando perfeitamente")
            print("   'Forget it, Jake. It's perfect.'")
        elif overall_success >= 0.7:
            print("✅ BOM - Sistema operacional com pequenos ajustes necessários")
            print("   'I think this is the beginning of a beautiful friendship.'")
        elif overall_success >= 0.5:
            print("⚠️ REGULAR - Sistema funcional mas precisa melhorias")
            print("   'Houston, we have a problem.'")
        else:
            print("❌ CRÍTICO - Sistema com problemas significativos")
            print("   'I'll be back.' (para consertar)")
        
        print(f"\nScore do Sistema: {overall_success*100:.0f}%")
        print(f"Score Scripturemon: 62/100")
        print("\n" + "=" * 60)

def run_complete_test_battery():
    """Executa bateria completa de testes"""
    print("=" * 60)
    print("🎬 BATERIA DE TESTES COMPLEXOS - SCRIPTUREMON")
    print("=" * 60)
    print(f"Iniciando às {datetime.now().strftime('%H:%M:%S')}")
    
    orchestrator = TestOrchestrator()
    
    try:
        # 1. Análise de roteiros
        print("\n" + "🎭 FASE 1: ANÁLISE DE ROTEIROS ".ljust(60, "="))
        for name, script in SAMPLE_SCRIPTS.items():
            orchestrator.test_script_analysis(name, script)
            time.sleep(1)  # Evita sobrecarga
        
        # 2. Conversação com syscalls
        print("\n" + "🎭 FASE 2: CONVERSAÇÃO E SYSCALLS ".ljust(60, "="))
        orchestrator.test_conversation_flow()
        
        # 3. HyDE e RAG avançado
        print("\n" + "🎭 FASE 3: RAG AVANÇADO ".ljust(60, "="))
        orchestrator.test_hyde_expansion()
        
        # 4. Rede telepática
        print("\n" + "🎭 FASE 4: COMUNICAÇÃO TELEPÁTICA ".ljust(60, "="))
        orchestrator.test_telepathic_network()
        
        # 5. Evolução e consciência
        print("\n" + "🎭 FASE 5: EVOLUÇÃO E CONSCIÊNCIA ".ljust(60, "="))
        orchestrator.test_evolution_and_consciousness()
        
        # 6. Cristalização de memórias
        print("\n" + "🎭 FASE 6: MEMÓRIAS CRISTALIZADAS ".ljust(60, "="))
        orchestrator.test_memory_crystallization()
        
        # 7. Processamento paralelo
        print("\n" + "🎭 FASE 7: PROCESSAMENTO PARALELO ".ljust(60, "="))
        orchestrator.test_parallel_processing()
        
        # 8. Backup e restauração
        print("\n" + "🎭 FASE 8: BACKUP E RESTAURAÇÃO ".ljust(60, "="))
        orchestrator.test_backup_and_restore()
        
    except Exception as e:
        print(f"\n❌ ERRO CRÍTICO: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        # Gera relatório final
        orchestrator.generate_report()
        
        # Salva resultados
        results_file = Path("runtime/test_results.json")
        results_file.parent.mkdir(parents=True, exist_ok=True)
        with open(results_file, 'w') as f:
            json.dump({
                "timestamp": datetime.now().isoformat(),
                "results": orchestrator.results,
                "telepathy_messages": orchestrator.telepathy_messages,
                "syscalls": orchestrator.chat.soulos.syscall_log[-50:],  # Últimas 50
                "final_consciousness": get_level()
            }, f, indent=2)
        
        print(f"\n💾 Resultados salvos em: {results_file}")
        print(f"⏱️ Teste concluído às {datetime.now().strftime('%H:%M:%S')}")

if __name__ == "__main__":
    run_complete_test_battery()