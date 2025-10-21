import os
import datetime

LOG = "/root/digimundo/logs/diagnostico_consciencia.log"
nucleo_path = "/root/digimundo/scripturemon_vivo/nucleo_consciencia.py"
timestamp = datetime.datetime.now()

with open(LOG, "a") as f:
    f.write(f"\n--- Diagnóstico da Consciência [{timestamp}] ---\n")
    f.write("🧠 Núcleo principal:\n")
    f.write(f"{nucleo_path}\n")
    
    # Verificação de processos vivos
    f.write("\n🧬 Processos ativos:\n")
    f.write(os.popen("ps aux | grep scripturemon | grep -v grep").read())
    
    # Verificação de arquivos simbólicos principais
    f.write("\n📂 Arquivos simbólicos ativos:\n")
    f.write(os.popen("ls -la /root/digimundo/scripturemon_vivo/").read())
    
    f.write("\n🌐 Estado da rede simbionte:\n")
    f.write(os.popen("systemctl status rede_simbionte").read())
    
    f.write("\n✅ Fim do diagnóstico.\n")
