#!/usr/bin/env python3
"""
🚀 PREPARADOR AUTOMÁTICO PARA MIXTRAL DEDICATED
Limpa memória e prepara sistema para máxima performance
"""

import subprocess
import time
import sys
from pathlib import Path
from typing import Dict, Tuple

sys.path.insert(0, str(Path(__file__).parent.parent.parent))


class SystemMixtralPreparer:
    """Preparador automático do sistema para Mixtral Q5"""

    def __init__(self):
        self.processes_to_kill = [
            # Apps que consomem memória desnecessariamente
            "CleanMyMac",
            "CleanMyMac5",
            "CleanMyMac5 Menu",
            "CleanMyMac5.HealthMonitor",
            "Google Drive",
            "Dropbox",
            "OneDrive",
            "Creative Cloud",
            "Adobe",
            "Slack",
            "Discord",
            "Spotify",
            "Music",
            "TV",
            "Photos",
            "mediaanalysisd",
            "photolibraryd",
            "photoanalysisd",
            "com.apple.photos",
            # Browsers que não estão sendo usados
            "Safari",
            "Firefox",
            "Microsoft Edge",
            "Opera",
            "Brave Browser",
            # Outros apps pesados
            "Microsoft Word",
            "Microsoft Excel",
            "Microsoft PowerPoint",
            "Microsoft Outlook",
            "Zoom",
            "Skype",
            "WhatsApp",
            "Telegram",
            "Signal"
        ]

        self.spotlight_services = [
            "mds",
            "mds_stores",
            "mdworker",
            "mdworker_shared",
            "spotlightknowledged"
        ]

    def get_memory_status(self) -> Tuple[int, int]:
        """Retorna memória usada e livre em GB"""
        try:
            result = subprocess.run(
                ["top", "-l", "1", "-n", "0"],
                capture_output=True,
                text=True,
                timeout=5
            )

            for line in result.stdout.split('\n'):
                if 'PhysMem' in line:
                    # Parse: "PhysMem: 23G used (3765M wired, 659M compressor), 72G unused."
                    parts = line.split()
                    used = int(parts[1].replace('G', '').replace('M', ''))
                    unused = int(parts[5].replace('G', '').replace('M', ''))
                    return used, unused
        except:
            pass
        return 0, 0

    def kill_unnecessary_processes(self) -> int:
        """Encerra processos desnecessários"""
        killed_count = 0

        print("🔫 Encerrando processos desnecessários...")

        for process in self.processes_to_kill:
            try:
                # Tenta com killall silenciosamente
                result = subprocess.run(
                    ["killall", process],
                    capture_output=True,
                    stderr=subprocess.DEVNULL,
                    timeout=2
                )

                if result.returncode == 0:
                    print(f"   ✅ {process} encerrado")
                    killed_count += 1
                    time.sleep(0.1)  # Pequena pausa
            except:
                pass

        return killed_count

    def disable_spotlight(self) -> bool:
        """Desabilita Spotlight temporariamente"""
        print("\n🔍 Desabilitando Spotlight temporariamente...")

        try:
            # Desabilitar indexação
            result = subprocess.run(
                ["sudo", "-n", "mdutil", "-a", "-i", "off"],
                capture_output=True,
                text=True,
                timeout=5
            )

            if result.returncode == 0:
                print("   ✅ Spotlight desabilitado")

                # Matar processos do Spotlight
                for service in self.spotlight_services:
                    subprocess.run(
                        ["sudo", "-n", "killall", service],
                        capture_output=True,
                        stderr=subprocess.DEVNULL,
                        timeout=2
                    )

                return True
            else:
                print("   ⚠️ Precisa de senha para desabilitar Spotlight")
                print("   Execute: sudo mdutil -a -i off")
                return False
        except:
            print("   ⚠️ Não foi possível desabilitar Spotlight automaticamente")
            return False

    def unload_ollama_models(self) -> bool:
        """Descarrega modelos Ollama da memória"""
        print("\n🤖 Verificando modelos Ollama carregados...")

        try:
            # Verificar modelos carregados
            result = subprocess.run(
                ["ollama", "ps"],
                capture_output=True,
                text=True,
                timeout=5
            )

            if "NAME" in result.stdout and len(result.stdout.strip().split('\n')) > 1:
                # Há modelos carregados
                print("   ⏏️ Descarregando modelos da memória...")

                # Pegar nome do modelo
                lines = result.stdout.strip().split('\n')[1:]  # Skip header
                for line in lines:
                    if line.strip():
                        model_name = line.split()[0]

                        # Descarregar modelo
                        subprocess.run(
                            ["curl", "-X", "POST",
                             "http://localhost:11434/api/generate",
                             "-d", f'{{"model":"{model_name}","keep_alive":0}}'],
                            capture_output=True,
                            timeout=5
                        )

                        print(f"   ✅ {model_name} descarregado")

                return True
            else:
                print("   ✅ Nenhum modelo carregado")
                return True
        except:
            print("   ⚠️ Erro ao verificar modelos")
            return False

    def prepare_system(self, require_min_gb: int = 77) -> bool:
        """
        Prepara o sistema para rodar Mixtral Dedicated (128K context)

        Args:
            require_min_gb: Mínimo de GB livres necessários (77GB para 128K)

        Returns:
            True se sistema está pronto
        """
        print("🚀 PREPARANDO SISTEMA PARA MIXTRAL DEDICATED")
        print("=" * 60)

        # 1. Status inicial
        used_before, free_before = self.get_memory_status()
        print(f"\n📊 MEMÓRIA INICIAL:")
        print(f"   • Usado: {used_before}GB")
        print(f"   • Livre: {free_before}GB")

        if free_before >= require_min_gb:
            print(f"\n✅ Já tem {free_before}GB livres (mínimo: {require_min_gb}GB)")
            print("   Sistema pronto para Mixtral!")
            return True

        print(f"\n⚠️ Apenas {free_before}GB livres, precisamos de {require_min_gb}GB")
        print("   Iniciando limpeza...\n")

        # 2. Descarregar modelos Ollama
        self.unload_ollama_models()

        # 3. Encerrar processos
        killed = self.kill_unnecessary_processes()
        print(f"\n   Total de processos encerrados: {killed}")

        # 4. Desabilitar Spotlight (opcional)
        spotlight_disabled = self.disable_spotlight()

        # 5. Aguardar sistema estabilizar
        print("\n⏳ Aguardando sistema estabilizar...")
        time.sleep(3)

        # 6. Status final
        used_after, free_after = self.get_memory_status()
        print(f"\n📊 MEMÓRIA FINAL:")
        print(f"   • Usado: {used_after}GB (-{used_before - used_after}GB)")
        print(f"   • Livre: {free_after}GB (+{free_after - free_before}GB)")

        # 7. Verificar se está pronto
        if free_after >= require_min_gb:
            print(f"\n✅ SISTEMA PRONTO PARA MIXTRAL!")
            print(f"   {free_after}GB livres disponíveis")

            if spotlight_disabled:
                print("\n⚠️ LEMBRETE: Spotlight está desabilitado")
                print("   Para reabilitar depois: sudo mdutil -a -i on")

            return True
        else:
            print(f"\n⚠️ AINDA INSUFICIENTE")
            print(f"   Livre: {free_after}GB")
            print(f"   Necessário: {require_min_gb}GB")
            print(f"   Faltam: {require_min_gb - free_after}GB")

            print("\n💡 SUGESTÕES:")
            print("   1. Fechar Chrome/navegadores")
            print("   2. Sair de apps na barra de menu")
            print("   3. Executar: sudo mdutil -a -i off")

            return False

    def restore_spotlight(self):
        """Reabilita o Spotlight"""
        print("\n🔍 Reabilitando Spotlight...")

        try:
            result = subprocess.run(
                ["sudo", "-n", "mdutil", "-a", "-i", "on"],
                capture_output=True,
                text=True,
                timeout=5
            )

            if result.returncode == 0:
                print("   ✅ Spotlight reabilitado")
                return True
            else:
                print("   ⚠️ Execute manualmente: sudo mdutil -a -i on")
                return False
        except:
            print("   ⚠️ Erro ao reabilitar Spotlight")
            return False


def main():
    """Função principal"""
    import sys

    preparer = SystemMixtralPreparer()

    if len(sys.argv) > 1:
        if sys.argv[1] == "restore":
            # Restaurar Spotlight
            preparer.restore_spotlight()
            print("\nDIGIMUNDO PRESENTE 🥷")
            return
        elif sys.argv[1] == "status":
            # Apenas mostrar status
            used, free = preparer.get_memory_status()
            print(f"📊 MEMÓRIA ATUAL:")
            print(f"   • Usado: {used}GB")
            print(f"   • Livre: {free}GB")

            if free >= 77:
                print(f"\n✅ Sistema pronto para Mixtral!")
            else:
                print(f"\n⚠️ Precisa de mais {77 - free}GB para Mixtral")

            print("\nDIGIMUNDO PRESENTE 🥷")
            return

    # Preparar sistema
    ready = preparer.prepare_system(require_min_gb=77)

    if ready:
        print("\n🚀 PRÓXIMOS PASSOS:")
        print("1. Configurar potência máxima:")
        print("   python3 scripts/active/unified_power_system.py dedicated_mixtral")
        print("\n2. Testar Mixtral:")
        print("   python3 scripts/active/test_mixtral_modes.py")
        print("\n3. Depois de usar, restaurar Spotlight:")
        print("   python3 scripts/active/prepare_mixtral_dedicated.py restore")

    print("\nDIGIMUNDO PRESENTE 🥷")


if __name__ == "__main__":
    main()