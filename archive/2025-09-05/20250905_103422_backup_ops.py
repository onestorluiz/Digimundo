import os
import zipfile
from pathlib import Path
from typing import List, Dict
import fnmatch


def safe_snapshot(source_dir: str, zip_path: str, exclude_globs: List[str]) -> Dict:
    """
    Compacta source_dir em zip_path (ZIP).
    
    Args:
        source_dir: Diretório fonte para compactar
        zip_path: Caminho do arquivo ZIP de destino
        exclude_globs: Lista de padrões glob para exclusão
        
    Returns:
        Dict com metadados do backup
    """
    # Adicionar exclusões obrigatórias
    mandatory_excludes = [
        '*backup*', '*backups*', '*.venv*', '*__pycache__*', 
        '*.mypy_cache*', '*.ruff_cache*', '*.pytest_cache*'
    ]
    
    all_excludes = list(exclude_globs) + mandatory_excludes
    
    source_path = Path(source_dir).resolve()
    zip_path = Path(zip_path).resolve()
    
    # Criar diretório do zip se não existir
    zip_path.parent.mkdir(parents=True, exist_ok=True)
    
    files_included = 0
    excluded_paths = []
    
    def should_exclude(file_path: Path) -> bool:
        """Verifica se o arquivo deve ser excluído."""
        relative = str(file_path.relative_to(source_path))
        
        # Verificar cada padrão de exclusão
        for pattern in all_excludes:
            # Verificar o caminho completo e cada parte do caminho
            path_parts = relative.split(os.sep)
            for part in path_parts:
                if fnmatch.fnmatch(part, pattern):
                    return True
            if fnmatch.fnmatch(relative, pattern):
                return True
                
        # Verificação adicional para 'backup' ou 'backups' em qualquer parte do caminho
        if 'backup' in relative.lower() or 'backups' in relative.lower():
            return True
            
        return False
    
    # Criar arquivo ZIP
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(source_path):
            root_path = Path(root)
            
            # Filtrar diretórios que devem ser excluídos
            dirs[:] = [d for d in dirs if not should_exclude(root_path / d)]
            
            for file in files:
                file_path = root_path / file
                
                if should_exclude(file_path):
                    excluded_paths.append(str(file_path.relative_to(source_path)))
                    continue
                
                # Adicionar arquivo ao ZIP
                arcname = str(file_path.relative_to(source_path))
                zipf.write(file_path, arcname)
                files_included += 1
    
    return {
        'zip_path': str(zip_path),
        'files_included': files_included,
        'excluded': excluded_paths[:50]  # Limitar lista de exclusões para não ficar muito grande
    }