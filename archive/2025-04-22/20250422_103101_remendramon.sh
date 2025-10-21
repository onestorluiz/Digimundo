#!/bin/bash
echo "Remendramon vasculhando por arquivos corrompidos..."
find /core_oraculo -type f -empty -name "*.sh" | while read -r f; do
  echo "#!/bin/bash" > "$f"
  echo "echo 'Arquivo remendado por Remendramon.'" >> "$f"
  chmod +x "$f"
  echo ">> Remendado: $f"
done
