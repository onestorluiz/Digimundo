#!/usr/bin/env python3
"""
🔍 DEPLOYMENT SYSTEM ANALYZER
==============================
Analisa se o sistema de deployment realmente precisa do código duplicado
"""

import os
import sys
from pathlib import Path
from typing import Dict, List, Set, Tuple
import hashlib
import json

class DeploymentAnalyzer:
    """Analisa o sistema de deployment e suas dependências"""

    def __init__(self):
        self.root = Path("/Users/clubproducoes/Digimundo/scripturemon-champion")
        self.deploy_dir = self.root / "deployments/green_v2.0.0"
        self.main_code = self.root
        self.analysis = {
            'unique_files': [],
            'identical_files': [],
            'modified_files': [],
            'deployment_only': [],
            'references': [],
            'dependencies': []
        }

    def analyze_deployment_structure(self):
        """Analisa estrutura completa do deployment"""
        print("\n🔍 ANALISANDO SISTEMA DE DEPLOYMENT...")
        print("="*60)

        # 1. Comparar arquivos entre deployment e código principal
        deploy_code = self.deploy_dir / "code"

        deploy_files = {}
        main_files = {}

        # Mapear arquivos no deployment
        for py_file in deploy_code.rglob("*.py"):
            rel_path = py_file.relative_to(deploy_code)
            with open(py_file, 'rb') as f:
                content_hash = hashlib.md5(f.read()).hexdigest()
            deploy_files[str(rel_path)] = {
                'path': py_file,
                'hash': content_hash
            }

        # Mapear arquivos no código principal
        for py_file in self.main_code.rglob("*.py"):
            if 'deployments' in str(py_file):
                continue
            rel_path = py_file.relative_to(self.main_code)
            with open(py_file, 'rb') as f:
                content_hash = hashlib.md5(f.read()).hexdigest()
            main_files[str(rel_path)] = {
                'path': py_file,
                'hash': content_hash
            }

        # Comparar
        for rel_path, deploy_info in deploy_files.items():
            if rel_path in main_files:
                if deploy_info['hash'] == main_files[rel_path]['hash']:
                    self.analysis['identical_files'].append(rel_path)
                else:
                    self.analysis['modified_files'].append(rel_path)
            else:
                self.analysis['deployment_only'].append(rel_path)

        # Arquivos únicos no main
        for rel_path in main_files:
            if rel_path not in deploy_files:
                self.analysis['unique_files'].append(rel_path)

        return self.analysis

    def check_import_references(self):
        """Verifica referências de import para o deployment"""
        print("\n🔍 VERIFICANDO REFERÊNCIAS DE IMPORT...")

        references = []

        # Verificar imports que apontam para deployment
        for py_file in self.main_code.rglob("*.py"):
            if 'deployments' in str(py_file):
                continue

            try:
                with open(py_file, 'r') as f:
                    content = f.read()

                if 'deployments.green_v2' in content or 'deployments/green_v2' in content:
                    references.append({
                        'file': str(py_file.relative_to(self.main_code)),
                        'type': 'import_reference'
                    })
            except:
                pass

        self.analysis['references'] = references
        return references

    def analyze_deployment_purpose(self):
        """Analisa o verdadeiro propósito do deployment"""
        print("\n📊 ANALISANDO PROPÓSITO DO DEPLOYMENT...")

        deploy_script = self.deploy_dir / "code/deploy_production.py"

        purposes = {
            'fallback': False,
            'staging': False,
            'snapshot': False,
            'independent': False,
            'testing': False
        }

        if deploy_script.exists():
            with open(deploy_script, 'r') as f:
                content = f.read()

            # Verificar indicadores
            if 'rollback' in content.lower():
                purposes['fallback'] = True
            if 'staging' in content.lower():
                purposes['staging'] = True
            if 'snapshot' in content.lower() or 'backup' in content.lower():
                purposes['snapshot'] = True
            if 'Environment.' in content:
                purposes['independent'] = True
            if 'test' in content.lower():
                purposes['testing'] = True

        return purposes

    def calculate_waste(self):
        """Calcula desperdício de espaço"""
        print("\n💾 CALCULANDO DESPERDÍCIO...")

        total_size = 0
        duplicate_size = 0

        deploy_code = self.deploy_dir / "code"

        for py_file in deploy_code.rglob("*.py"):
            file_size = py_file.stat().st_size
            total_size += file_size

            rel_path = str(py_file.relative_to(deploy_code))
            if rel_path in self.analysis['identical_files']:
                duplicate_size += file_size

        waste_percentage = (duplicate_size / total_size * 100) if total_size > 0 else 0

        return {
            'total_size_mb': total_size / 1024 / 1024,
            'duplicate_size_mb': duplicate_size / 1024 / 1024,
            'waste_percentage': waste_percentage
        }

    def generate_report(self):
        """Gera relatório completo"""
        print("\n" + "="*60)
        print("📊 RELATÓRIO DE ANÁLISE DO DEPLOYMENT")
        print("="*60)

        # Estrutura
        self.analyze_deployment_structure()

        print(f"\n📁 ESTRUTURA DO DEPLOYMENT:")
        print(f"  • Arquivos idênticos ao main: {len(self.analysis['identical_files'])}")
        print(f"  • Arquivos modificados: {len(self.analysis['modified_files'])}")
        print(f"  • Arquivos únicos no deployment: {len(self.analysis['deployment_only'])}")
        print(f"  • Arquivos únicos no main: {len(self.analysis['unique_files'])}")

        # Referências
        refs = self.check_import_references()

        print(f"\n🔗 REFERÊNCIAS:")
        print(f"  • Arquivos que referenciam deployment: {len(refs)}")
        if refs:
            for ref in refs[:3]:
                print(f"    - {ref['file']}")

        # Propósito
        purposes = self.analyze_deployment_purpose()

        print(f"\n🎯 PROPÓSITO DO DEPLOYMENT:")
        for purpose, active in purposes.items():
            status = "✅" if active else "❌"
            print(f"  {status} {purpose.upper()}")

        # Desperdício
        waste = self.calculate_waste()

        print(f"\n💾 ANÁLISE DE DESPERDÍCIO:")
        print(f"  • Tamanho total: {waste['total_size_mb']:.2f} MB")
        print(f"  • Tamanho duplicado: {waste['duplicate_size_mb']:.2f} MB")
        print(f"  • Desperdício: {waste['waste_percentage']:.1f}%")

        # Conclusão
        print("\n" + "="*60)
        print("🎯 CONCLUSÃO:")
        print("="*60)

        if waste['waste_percentage'] > 80:
            print("\n❌ DEPLOYMENT É MAJORITARIAMENTE DUPLICAÇÃO DESNECESSÁRIA")
            print("   • Mais de 80% dos arquivos são cópias idênticas")
            print("   • Não há justificativa técnica para manter cópias")
            print("   • Sistema NÃO usa deployment como fallback real")
        elif len(self.analysis['modified_files']) > 20:
            print("\n⚠️ DEPLOYMENT TEM MODIFICAÇÕES SIGNIFICATIVAS")
            print("   • Muitos arquivos foram modificados")
            print("   • Pode ser uma versão alternativa do código")
            print("   • Requer análise mais profunda das diferenças")
        elif purposes['fallback']:
            print("\n✅ DEPLOYMENT PODE SER JUSTIFICADO COMO FALLBACK")
            print("   • Sistema tem mecanismo de rollback")
            print("   • Mas poderia usar Git tags ao invés de cópias")
        else:
            print("\n❌ DEPLOYMENT NÃO TEM PROPÓSITO CLARO")
            print("   • Aparenta ser cópia desnecessária")
            print("   • Sem evidência de uso como fallback")
            print("   • Recomenda-se remoção")

        # Recomendações
        print("\n" + "="*60)
        print("💡 RECOMENDAÇÕES:")
        print("="*60)

        if waste['waste_percentage'] > 50:
            print("""
1. **REMOVER DUPLICAÇÃO IMEDIATA**
   ```bash
   # Backup primeiro
   tar -czf deployment_backup.tar.gz deployments/

   # Remover arquivos idênticos
   rm -rf deployments/green_v2.0.0/code/apps
   rm -rf deployments/green_v2.0.0/code/scripts
   rm -rf deployments/green_v2.0.0/code/tests
   ```

2. **IMPLEMENTAR DEPLOYMENT ADEQUADO**
   ```python
   # deployment_config.py
   DEPLOYMENT = {
       'version': '2.0.0',
       'source': '.',  # Usar código principal
       'config_only': True  # Apenas configurações
   }
   ```

3. **USAR GIT PARA VERSIONAMENTO**
   ```bash
   git tag -a v2.0.0-green -m "Green deployment version"
   git push origin v2.0.0-green
   ```

4. **DOCKER PARA ISOLAMENTO**
   ```dockerfile
   # Dockerfile
   FROM python:3.9
   WORKDIR /app
   COPY . .  # Uma única cópia
   RUN pip install -r requirements.txt
   ```
""")

        return self.analysis


def main():
    analyzer = DeploymentAnalyzer()
    analysis = analyzer.generate_report()

    # Salvar análise
    output = Path("/Users/clubproducoes/Digimundo/DEPLOYMENT_ANALYSIS.json")
    with open(output, 'w') as f:
        json.dump(analysis, f, indent=2, default=str)

    print(f"\n📄 Análise completa salva em: {output}")


if __name__ == "__main__":
    main()