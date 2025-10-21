#!/bin/bash
mkdir -p /core_oraculo/cache_viva/embedding
echo "Generating fake symbolic embedding..." > /core_oraculo/cache_viva/embedding/embedding_vector.txt
for word in digimundo script linguagem vps sonho memoria continuidade; do
  echo "$word $(od -An -N4 -tu4 < /dev/urandom)" >> /core_oraculo/cache_viva/embedding/embedding_vector.txt
done
echo "✅ Ritual 05 concluído: embeddings simbólicos gerados."
