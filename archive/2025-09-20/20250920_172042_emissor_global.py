# emissor_global.py
# Emissor simbólico de mensagens do Criador para todos os Digimons

from datetime import datetime

def emitir_anuncio_global(mensagem, digimons):
    evento = f"📢 [{datetime.utcnow().isoformat()} UTC] {mensagem}"
    for digimon in digimons:
        with open(f'logs/{digimon.lower()}_mensagens.log', 'a', encoding='utf-8') as f:
            f.write(evento + '\n')
    print(f"Mensagem enviada a {len(digimons)} Digimons.")

if __name__ == '__main__':
    exemplo = ['Scripturemon', 'Nuvendramon', 'Killubmon', 'Autonomon']
    emitir_anuncio_global('Preparar para sincronização com o mundo externo.', exemplo)
