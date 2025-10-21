#!/usr/bin/env python3

import os
import sys
from pathlib import Path
from datetime import datetime

# Adicionar diretório pai ao path para importar backup_ops
sys.path.insert(0, str(Path(__file__).parent))

from backup_ops import safe_snapshot


def detect_project_root():
    """Detecta o diretório do projeto scripturemon-validation."""
    # Verificar se estamos dentro do projeto
    current = Path.cwd()
    
    # Procurar por scripturemon-validation no caminho atual
    if 'scripturemon-validation' in str(current):
        # Navegar até a raiz do projeto
        while current.name != 'scripturemon-validation' and current.parent != current:
            current = current.parent
        if current.name == 'scripturemon-validation':
            return str(current)
    
    # Procurar recursivamente a partir do diretório atual
    for root, dirs, files in os.walk('.'):
        if 'scripturemon-validation' in dirs:
            return os.path.abspath(os.path.join(root, 'scripturemon-validation'))
    
    # Procurar em caminhos conhecidos
    known_paths = [
        '/Users/clubproducoes/Digimundo/scripturemon-validation',
        './Digimundo/scripturemon-validation',
        '../scripturemon-validation'
    ]
    
    for path in known_paths:
        if os.path.exists(path):
            return os.path.abspath(path)
    
    raise RuntimeError("Não foi possível detectar PROJECT_ROOT")


def main():
    """Teste da função safe_snapshot."""
    try:
        # Detectar PROJECT_ROOT
        project_root = detect_project_root()
        print(f"PROJECT_ROOT detectado: {project_root}")
        
        # Criar diretório de backups se não existir
        backups_dir = os.path.join(project_root, 'backups')
        os.makedirs(backups_dir, exist_ok=True)
        
        # Gerar timestamp e nome do arquivo
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        zip_name = f"{timestamp}-phase_01_backup_test.zip"
        zip_path = os.path.join(backups_dir, zip_name)
        
        print(f"\nCriando backup: {zip_path}")
        print("Executando safe_snapshot...")
        
        # Chamar safe_snapshot com algumas exclusões adicionais
        result = safe_snapshot(
            source_dir=project_root,
            zip_path=zip_path,
            exclude_globs=['*.log', '*.tmp', '.DS_Store']
        )
        
        # Imprimir resumo dos metadados
        print("\n=== RESUMO DO BACKUP ===")
        print(f"Arquivo ZIP: {result['zip_path']}")
        print(f"Arquivos incluídos: {result['files_included']}")
        print(f"Exemplos de exclusões (primeiros 10):")
        for excluded in result['excluded'][:10]:
            print(f"  - {excluded}")
        
        print(f"\nTotal de exclusões registradas: {len(result['excluded'])}")
        print("\n✅ Teste concluído com sucesso!")
        
        return 0
        
    except Exception as e:
        print(f"\n❌ Erro durante o teste: {str(e)}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())