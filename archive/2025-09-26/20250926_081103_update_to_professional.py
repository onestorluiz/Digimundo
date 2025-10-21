#!/usr/bin/env python3
"""
UPDATE TO PROFESSIONAL MODE
Atualiza scripts para usar scripturemon-professional onde apropriado
"""

import os
import re

def should_use_professional(filepath):
    """Determina se o arquivo deve usar o modelo professional"""

    # Scripts que devem usar professional (para respostas estruturadas)
    professional_scripts = [
        'self_organize',
        'git_aware_organization',
        'master_organization_plan',
        'execute_reorganization',
        'command_bridge',
        'system_autonomous',
        'system_diagnostic'
    ]

    filename = os.path.basename(filepath)

    # Verificar se é um script de organização/sistema
    for script in professional_scripts:
        if script in filename:
            return True

    # Scripts de análise criativa devem manter o master
    if 'deep_analysis' in filename or 'ultimate_analysis' in filename:
        return False

    # Testes devem manter o modelo original (exceto teste do professional)
    if '/tests/' in filepath and 'professional' not in filename:
        return False

    return False

def update_file(filepath):
    """Atualiza um arquivo para usar o modelo correto"""

    with open(filepath, 'r') as f:
        content = f.read()

    original_content = content
    changes = []

    if should_use_professional(filepath):
        # Atualizar para professional
        patterns = [
            (r'model\s*=\s*["\']scripturemon-master["\']',
             'model = "scripturemon-professional"'),
            (r'model\s*=\s*["\']scripturemon-ultimate["\']',
             'model = "scripturemon-professional"'),
            (r'"model":\s*"scripturemon-master"',
             '"model": "scripturemon-professional"'),
            (r'"model":\s*"scripturemon-ultimate"',
             '"model": "scripturemon-professional"')
        ]

        for pattern, replacement in patterns:
            if re.search(pattern, content):
                content = re.sub(pattern, replacement, content)
                changes.append(f"  • {pattern} → {replacement}")

    if content != original_content:
        with open(filepath, 'w') as f:
            f.write(content)
        return changes

    return None

def main():
    print("🔄 ATUALIZANDO SCRIPTS PARA USAR MODELO PROFESSIONAL")
    print("=" * 50)

    base_path = "/Users/clubproducoes/Digimundo/scripturemon-ultimate"
    updated_files = []

    # Buscar arquivos Python
    for root, dirs, files in os.walk(base_path):
        # Pular diretórios desnecessários
        if 'archive' in root or '__pycache__' in root or '.git' in root:
            continue

        for file in files:
            if file.endswith('.py'):
                filepath = os.path.join(root, file)

                # Verificar se contém referências aos modelos
                try:
                    with open(filepath, 'r') as f:
                        content = f.read()

                    if 'scripturemon-master' in content or 'scripturemon-ultimate' in content:
                        changes = update_file(filepath)

                        if changes:
                            relative_path = filepath.replace(base_path + '/', '')
                            updated_files.append((relative_path, changes))
                            print(f"✅ Atualizado: {relative_path}")
                            for change in changes:
                                print(change)

                except Exception as e:
                    print(f"⚠️ Erro ao processar {filepath}: {e}")

    # Resumo
    print("\n" + "=" * 50)
    print("📊 RESUMO DAS ATUALIZAÇÕES")
    print("=" * 50)

    if updated_files:
        print(f"\n✅ {len(updated_files)} arquivos atualizados para usar scripturemon-professional:")
        for file, _ in updated_files:
            print(f"   • {file}")

        print("\n💡 Estes scripts agora usarão o modo professional para:")
        print("   • Respostas em JSON estruturado")
        print("   • Organização de arquivos")
        print("   • Comandos do sistema")
        print("   • Diagnósticos")
    else:
        print("\n✅ Nenhuma atualização necessária!")

    print("\n📝 NOTA: Scripts de análise criativa mantêm scripturemon-master")
    print("         Testes mantêm os modelos originais para consistência")

if __name__ == "__main__":
    main()