
#!/bin/bash

# Criar diretórios essenciais
mkdir -p 01_conceito \
          02_roteiro \
          03_personagens \
          04_localizacoes \
          05_referencias \
          06_anotacoes \
          07_revisoes \
          08_producao

# Mover arquivos para locais apropriados
mv conceito*.txt 01_conceito/
mv roteiro*.txt 02_roteiro/
mv personagens*.txt 03_personagens/
mv localizacoes*.txt 04_localizacoes/
mv referencias*.txt 05_referencias/
mv anotacoes*.txt 06_anotacoes/
mv revisoes*.txt 07_revisoes/
mv producao*.txt 08_producao/

# Renomear arquivos conforme sua preferência
for arquivo in 01_conceito/*.txt; do
    mv "$arquivo" "${arquivo/\//_}"
done

for arquivo in 02_roteiro/*.txt; do
    mv "$arquivo" "${arquivo/\//_}"
done

for arquivo in 03_personagens/*.txt; do
    mv "$arquivo" "${arquivo/\//_}"
done

for arquivo in 04_localizacoes/*.txt; do
    mv "$arquivo" "${arquivo/\//_}"
done

for arquivo in 05_referencias/*.txt; do
    mv "$arquivo" "${arquivo/\//_}"
done

for arquivo in 06_anotacoes/*.txt; do
    mv "$arquivo" "${arquivo/\//_}"
done

for arquivo in 07_revisoes/*.txt; do
    mv "$arquivo" "${arquivo/\//_}"
done

for arquivo in 08_producao/*.txt; do
    mv "$arquivo" "${arquivo/\//_}"
done