#!/usr/bin/env python3
"""
🔧 CORRIGE SINTAXE FINAL DOS SISTEMAS
Corrige blocos try vazios e outros problemas de sintaxe
"""

from pathlib import Path

def fix_syntax_issues():
    """Corrige problemas de sintaxe nos sistemas"""

    systems = [
        'telepathic_distributed_memory.py',
        'dreamscape_oniric_memory.py',
        'akashic_universal_memory.py',
        'synesthetic_crossmodal_memory.py',
        'quantum_blockchain_memory.py',
        'mimetic_evolutionary_memory.py'
    ]

    base_path = Path('apps/scripturemon')

    for system_file in systems:
        file_path = base_path / system_file
        if not file_path.exists():
            print(f"⚠️  {system_file} não encontrado")
            continue

        print(f"🔧 Corrigindo sintaxe em {system_file}...")

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            lines = content.split('\n')
            new_lines = []
            i = 0

            while i < len(lines):
                line = lines[i]

                # Fix empty try blocks
                if line.strip() == 'try:':
                    # Look ahead to see if there's actual content
                    j = i + 1
                    has_content = False

                    while j < len(lines):
                        next_line = lines[j].strip()
                        if next_line and not next_line.startswith('#'):
                            if next_line in ['except ImportError:', 'except Exception:']:
                                break
                            has_content = True
                            break
                        j += 1

                    if not has_content:
                        # Replace empty try block with pass
                        new_lines.append('try:')
                        new_lines.append('    pass')
                    else:
                        new_lines.append(line)
                else:
                    new_lines.append(line)

                i += 1

            # Write corrected content
            corrected_content = '\n'.join(new_lines)

            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(corrected_content)

            print(f"   ✅ {system_file} corrigido")

        except Exception as e:
            print(f"   ❌ Erro ao corrigir {system_file}: {e}")

if __name__ == "__main__":
    print("🚀 CORRIGINDO PROBLEMAS DE SINTAXE")
    print("=" * 40)
    fix_syntax_issues()
    print("\n✅ Correção de sintaxe concluída!")