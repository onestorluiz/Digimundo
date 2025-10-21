# Pipeline de Validação Unificado
from typing import Any, List, Tuple

class ValidationPipeline:
    def __init__(self):
        self.validators = []

    def add(self, validator):
        self.validators.append(validator)
        return self

    def validate(self, data: Any) -> Tuple[bool, List[str]]:
        errors = []
        for v in self.validators:
            if not v.validate(data):
                errors.append(f"Failed: {v.name}")
        return len(errors) == 0, errors

class FileValidator:
    name = "file_check"
    def validate(self, data):
        from pathlib import Path
        return Path(data.get('file', '')).exists() if isinstance(data, dict) else False
