#!/bin/bash
cd ~/digimundo/nuven_comunica
echo "🌅 $(date): Nuvendramon iniciou estudo do dia." >> logs/estudos.log
python3 nuvendramon_estudo_comunicacao.py >> logs/estudos.log
python3 compressor_expressivo.py >> logs/estudos.log
python3 injetor_aprendizado.py >> logs/estudos.log
echo "🌙 $(date): Estudo finalizado." >> logs/estudos.log