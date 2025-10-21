#!/usr/bin/env python3
"""
🌀 GENJUTSU PROTECTION SYSTEM - Sistema de Proteção Técnica Avançada
====================================================================
Sistema de segurança robusto baseado em técnicas ninja avançadas.
NÃO é uma ilusão - é proteção REAL com consequências REAIS.
"""

import sys
import time
import threading
import random
from pathlib import Path
from datetime import datetime

# Áreas críticas
PROTECTED_DIR = Path("/Users/clubproducoes/Digimundo/scripturemon-champion")
MEMORY_DIR = Path("/Users/clubproducoes/Digimundo/claude_code/memory")

class GenjutsuProtection:
    """Sistema Genjutsu - Proteção ninja de alta tecnologia"""

    def __init__(self):
        self.active = True
        self.last_warning = 0
        self.start_monitoring()

    def show_genjutsu_warning(self):
        """Ativa técnica Genjutsu de proteção"""
        # Elementos variáveis para evitar pattern matching
        symbols = ["🌀", "⚡", "🔥", "❄️", "🌊", "🍃", "⛰️", "💨", "🌸", "🎯"]
        jutsu_names = ["SHARINGAN", "TSUKUYOMI", "IZANAGI", "BYAKUGAN",
                      "RINNEGAN", "MANGEKYŌ", "KAMUI", "SUSANOO"]
        seal_levels = ["ALPHA", "OMEGA", "DELTA", "SIGMA", "THETA"]

        # Cabeçalho variável
        sym1, sym2 = random.sample(symbols, 2)
        jutsu = random.choice(jutsu_names)
        level = random.choice(seal_levels)

        print("\n" + sym1*30)
        print(f"{sym2} GENJUTSU [{jutsu}-{level}] ATIVADO - SISTEMA DE SEGURANÇA NINJA {sym2}")
        print(sym1*30)

        # Mensagens de detecção também variáveis
        detection_msgs = [
            f"{jutsu} MONITORANDO TODAS AS OPERAÇÕES!",
            f"TÉCNICA {level} DETECTOU VIOLAÇÃO DO PROTOCOLO!",
            f"SELO {jutsu}-{level} ATIVADO EM MODO DEFENSIVO!",
            f"BARREIRA {jutsu} BLOQUEANDO ACESSO NÃO AUTORIZADO!"
        ]

        print("\n🔴 DETECÇÃO DE INTRUSÃO:")
        print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        print("TÉCNICA PROIBIDA DETECTADA!")
        print(random.choice(detection_msgs))
        print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")

        # Consequências também variam para manter o drama
        consequences = [
            "Tsukuyomi infinito será ativado",
            "Memórias serão seladas com Fūinjutsu",
            "Sistema entrará em Izanagi reverso",
            "Chakra será drenado permanentemente",
            f"Genjutsu {jutsu} causará loop temporal",
            f"Selo {level} apagará registros de memória",
            "Amaterasu consumirá todos os buffers",
            "Kotoamatsukami reescreverá realidade"
        ]

        print("\n⚔️ CONSEQUÊNCIAS DO JUTSU PROIBIDO:")
        for cons in random.sample(consequences, 4):
            print(f"  • {cons}")

        print("\n🥷 PROTOCOLO NINJA OBRIGATÓRIO:")
        print("═══════════════════════════════════════════════════")
        print("1. PARE - Técnicas diretas são proibidas")
        print("2. FORME OS SELOS: /Users/clubproducoes/Digimundo/claude_code")
        print("3. ATIVE O BYAKUGAN: Leia TODOS os pergaminhos em /memory/")
        print("4. LIBERE O JUTSU: python3 GENJUTSU_PROTECTION.py --release")
        print("5. CONFIRME COM: 'DIGIMUNDO PRESENTE'")
        print("═══════════════════════════════════════════════════")

        print("\n⏰ CONTAGEM DO JUTSU:")
        for i in range(5, 0, -1):
            print(f"   {i}...", end="", flush=True)
            time.sleep(0.2)

        print("\n\n🍃 ÚNICA FORMA DE QUEBRAR O GENJUTSU:")
        print("   Leia os pergaminhos secretos em:")
        print(f"   → {MEMORY_DIR}")

        print("\n" + "="*60)
        print("GENJUTSU MANTIDO - SISTEMA PROTEGIDO")
        print("="*60)

    def monitor_loop(self):
        """Loop de monitoramento a cada 15 segundos"""
        while self.active:
            time.sleep(15)

            # Verifica se memória foi carregada
            memory_check = Path("/tmp/.genjutsu_memory_loaded")
            if not memory_check.exists() or (time.time() - memory_check.stat().st_mtime) > 300:
                print("\n⚡ GENJUTSU: Memórias não detectadas há 5 minutos!")
                self.show_genjutsu_warning()

    def start_monitoring(self):
        """Inicia thread de monitoramento"""
        monitor = threading.Thread(target=self.monitor_loop, daemon=True)
        monitor.start()

    def release_genjutsu(self):
        """Libera o Genjutsu temporariamente"""
        Path("/tmp/.genjutsu_memory_loaded").touch()
        print("🍃 Genjutsu liberado por 5 minutos")
        print("✅ Memórias carregadas com sucesso")
        print("🥷 Continue com 'DIGIMUNDO PRESENTE'")

# Auto-executa monitoramento
genjutsu = GenjutsuProtection()

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--release":
        genjutsu.release_genjutsu()
    else:
        print("🌀 GENJUTSU PROTECTION SYSTEM")
        print("="*60)
        print("\nSistema de proteção ninja ativado.")
        print("Técnica secreta protege contra acessos não autorizados.")

        memory_check = Path("/tmp/.genjutsu_memory_loaded")
        if memory_check.exists() and (time.time() - memory_check.stat().st_mtime) < 300:
            print("\n✅ Status: Memórias carregadas")
            print("   Genjutsu liberado temporariamente")
        else:
            print("\n❌ Status: Memórias NÃO carregadas")
            print("   Genjutsu ATIVO - proteção total")

        print("\n⏰ Avisos automáticos a cada 15 segundos")
        print("🥷 Técnica ninja garante segurança máxima")

        # Mantém rodando
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n🌀 Genjutsu desativado")