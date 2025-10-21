#!/usr/bin/env python3
"""
🔇 IMPLEMENT VERBOSITY CONTROL - CONTROLE ROBUSTO DE VERBOSIDADE
Adiciona controle de verbosidade mantendo extrema robustez
"""

from pathlib import Path
import re

def implement_verbosity_control():
    """Implementa sistema de controle de verbosidade ROBUSTO"""
    
    scripturemon_path = Path("/Users/clubproducoes/bin/scripturemon")
    
    if not scripturemon_path.exists():
        print("❌ scripturemon não encontrado")
        return False
    
    content = scripturemon_path.read_text()
    lines = content.split('\n')
    changes_made = []
    
    # 1. Adicionar argumento de verbosidade ao parser
    for i, line in enumerate(lines):
        if "parser.add_argument('--timeout'" in line:
            # Adicionar após timeout
            if "--verbose" not in content and "--quiet" not in content:
                verbosity_args = [
                    "    parser.add_argument('--verbose', '-v', action='count', default=0,",
                    "                       help='Aumenta verbosidade (-v, -vv, -vvv)')",
                    "    parser.add_argument('--quiet', '-q', action='store_true',",
                    "                       help='Modo silencioso (apenas respostas)')",
                    ""
                ]
                
                for j, arg_line in enumerate(verbosity_args):
                    lines.insert(i + 1 + j, arg_line)
                
                changes_made.append("✅ Argumentos --verbose e --quiet adicionados")
            break
    
    content = '\n'.join(lines)
    
    # 2. Adicionar classe de controle de verbosidade
    if "class VerbosityControl:" not in content:
        verbosity_class = '''
class VerbosityControl:
    """Controle ROBUSTO de verbosidade do sistema"""
    
    SILENT = -1    # Apenas erros críticos
    QUIET = 0      # Mínimo output (padrão será este)
    NORMAL = 1     # Output normal (-v)
    VERBOSE = 2    # Output detalhado (-vv)
    DEBUG = 3      # Debug completo (-vvv)
    
    def __init__(self, level=QUIET):
        self.level = level
        self._original_print = print
        self._suppressed_patterns = [
            r'^⚡ ATIVANDO',
            r'^🧠 \\[1-6\\]',
            r'^📚 \\[7\\]',
            r'^🧠 \\[8\\]',
            r'^⚡ \\[9\\]',
            r'^🎯 \\[10\\]',
            r'^📊 \\[11\\]',
            r'^🌐 \\[12\\]',
            r'^🤖 \\[13\\]',
            r'^   ✅',
            r'^   💾',
            r'^   🔄',
            r'^💎 Sistema',
            r'^🧠 MEMORION',
            r'^✅ ',
            r'^\\s*Modelo:',
            r'^\\s*Hipocampo:',
            r'^\\s*Estruturas:',
            r'^\\s*Caches:',
            r'^📖 Pré-carregando',
            r'^🔍 Verificando'
        ]
    
    def should_print(self, text):
        """Decide se deve imprimir baseado no nível"""
        if self.level >= self.VERBOSE:
            return True  # Verbose mostra tudo
        
        if self.level == self.SILENT:
            # Apenas erros e prompts
            return '❌' in text or '>' in text or 'Error' in text
        
        if self.level == self.QUIET:
            # Suprime inicialização mas mostra interações
            text_str = str(text)
            
            # Sempre mostrar prompts e respostas do usuário
            if '>' in text_str and '📝' in text_str:
                return True
            
            # Sempre mostrar erros
            if '❌' in text_str or 'Error' in text_str or 'error' in text_str:
                return True
            
            # Sempre mostrar respostas (não status)
            if '🎭 Scripturemon' in text_str:
                return True
            
            # Suprimir padrões de inicialização
            for pattern in self._suppressed_patterns:
                if re.match(pattern, text_str):
                    return False
            
            # Suprimir linhas de separação durante init
            if text_str.strip() in ['='*70, '='*60, '-'*40, '-'*50]:
                return False
            
            # Suprimir títulos de inicialização
            if any(x in text_str for x in [
                'INICIALIZANDO', 'ATIVANDO', 'Carregando', 
                'Configurando', 'Inicializando', 'FASE 4',
                'CAPACIDADE MÁXIMA', 'HARMONIA 100%',
                'STATUS COMPLETO', 'TODOS OS'
            ]):
                return False
            
            return True
        
        return True  # Normal e acima mostram mais
    
    def setup_print_filter(self):
        """Configura filtro global de print"""
        original_print = print
        control = self
        
        def filtered_print(*args, **kwargs):
            text = ' '.join(str(arg) for arg in args)
            if control.should_print(text):
                original_print(*args, **kwargs)
        
        # Substituir print globalmente
        import builtins
        builtins.print = filtered_print
    
    def get_init_summary(self):
        """Retorna resumo conciso da inicialização"""
        return """🎬 SCRIPTUREMON v2.0 | 13 sistemas ativos | Modo: Capacidade Máxima
Digite 'help' para comandos | 'status' para ver sistemas"""

# Instância global do controle
_verbosity = None

def get_verbosity():
    global _verbosity
    if _verbosity is None:
        _verbosity = VerbosityControl()
    return _verbosity
'''
        
        # Inserir após imports
        lines = content.split('\n')
        for i, line in enumerate(lines):
            if 'from apps.scripturemon' in line and i < 50:
                # Inserir antes das importações dos apps
                lines.insert(i, verbosity_class)
                changes_made.append("✅ Classe VerbosityControl adicionada")
                break
        
        content = '\n'.join(lines)
    
    # 3. Integrar verbosidade no __init__ da classe principal
    lines = content.split('\n')
    for i, line in enumerate(lines):
        if 'def __init__(self):' in line and 'ScripturemonMaxCapacity' in '\n'.join(lines[max(0,i-5):i]):
            # Adicionar controle de verbosidade no início do __init__
            if 'self.verbosity' not in '\n'.join(lines[i:i+20]):
                init_lines = [
                    "        # Controle de verbosidade",
                    "        self.verbosity = get_verbosity()",
                    "        ",
                    "        # Mostrar apenas resumo se quiet",
                    "        if self.verbosity.level <= VerbosityControl.QUIET:",
                    "            # Suprimir prints de inicialização",
                    "            self.verbosity.setup_print_filter()",
                    "            # Mostrar apenas resumo",
                    "            print(self.verbosity.get_init_summary())",
                    "        else:",
                    "            # Modo verbose - mostrar tudo",
                    '            print("\\n" + "="*70)',
                    '            print("🎬 SCRIPTUREMON - INICIALIZANDO CAPACIDADE MÁXIMA")',
                    '            print("="*70)',
                    ""
                ]
                
                # Encontrar onde inserir (após super ou no início)
                insert_pos = i + 1
                # Pular docstring se houver
                while insert_pos < len(lines) and '"""' in lines[insert_pos]:
                    insert_pos += 1
                
                for j, init_line in enumerate(init_lines):
                    lines.insert(insert_pos + j, init_line)
                
                changes_made.append("✅ Controle de verbosidade integrado no __init__")
            break
    
    content = '\n'.join(lines)
    
    # 4. Atualizar main para passar verbosidade
    lines = content.split('\n')
    for i, line in enumerate(lines):
        if 'if __name__ == "__main__":' in line:
            # Procurar onde processar args
            for j in range(i, min(i+50, len(lines))):
                if 'args = parser.parse_args()' in lines[j]:
                    # Adicionar processamento de verbosidade
                    if 'verbosity_level' not in '\n'.join(lines[j:j+20]):
                        verbosity_setup = [
                            "",
                            "    # Configurar nível de verbosidade",
                            "    verbosity_level = VerbosityControl.QUIET  # Padrão: quiet",
                            "    if args.quiet:",
                            "        verbosity_level = VerbosityControl.SILENT",
                            "    elif args.verbose:",
                            "        if args.verbose == 1:",
                            "            verbosity_level = VerbosityControl.NORMAL",
                            "        elif args.verbose == 2:",
                            "            verbosity_level = VerbosityControl.VERBOSE",
                            "        elif args.verbose >= 3:",
                            "            verbosity_level = VerbosityControl.DEBUG",
                            "    ",
                            "    # Aplicar verbosidade globalmente",
                            "    _verbosity = VerbosityControl(verbosity_level)",
                            "    ",
                            "    # Mostrar nível se verbose",
                            "    if verbosity_level >= VerbosityControl.VERBOSE:",
                            '        print(f"🔊 Verbosidade: {verbosity_level}")',
                            ""
                        ]
                        
                        for k, verb_line in enumerate(verbosity_setup):
                            lines.insert(j + 1 + k, verb_line)
                        
                        changes_made.append("✅ Processamento de verbosidade no main")
                    break
            break
    
    content = '\n'.join(lines)
    
    # 5. Adicionar método para alternar verbosidade em runtime
    lines = content.split('\n')
    for i, line in enumerate(lines):
        if "elif user_input.lower() == 'help':" in line:
            # Adicionar comando verbose antes do help
            if "'verbose'" not in content:
                verbose_cmd = [
                    "        elif user_input.lower().startswith('verbose'):",
                    "            # Alterar verbosidade em runtime",
                    "            parts = user_input.split()",
                    "            if len(parts) > 1:",
                    "                try:",
                    "                    level = int(parts[1])",
                    "                    self.verbosity.level = level",
                    "                    levels = {",
                    "                        -1: 'SILENT',",
                    "                        0: 'QUIET',",
                    "                        1: 'NORMAL',",
                    "                        2: 'VERBOSE',",
                    "                        3: 'DEBUG'",
                    "                    }",
                    "                    print(f'🔊 Verbosidade alterada para {levels.get(level, level)}')",
                    "                except:",
                    "                    print('Uso: verbose [0-3] (-1=silent, 0=quiet, 1=normal, 2=verbose, 3=debug)')",
                    "            else:",
                    "                print(f'🔊 Verbosidade atual: {self.verbosity.level}')",
                    "            ",
                ]
                
                for j, cmd_line in enumerate(verbose_cmd):
                    lines.insert(i + j, cmd_line)
                
                changes_made.append("✅ Comando 'verbose' adicionado")
            break
    
    # Salvar arquivo
    scripturemon_path.write_text('\n'.join(lines))
    
    print("\n".join(changes_made))
    return len(changes_made) > 0

def create_test_script():
    """Cria script para testar diferentes níveis de verbosidade"""
    
    test_content = '''#!/usr/bin/env python3
"""
🔊 TEST VERBOSITY LEVELS
Testa diferentes níveis de verbosidade
"""

import subprocess
import time

def test_verbosity():
    """Testa cada nível de verbosidade"""
    
    print("🔊 TESTANDO NÍVEIS DE VERBOSIDADE")
    print("="*60)
    
    levels = [
        ('--quiet', 'SILENT (-q)'),
        ('', 'QUIET (padrão)'),
        ('-v', 'NORMAL (-v)'),
        ('-vv', 'VERBOSE (-vv)'),
        ('-vvv', 'DEBUG (-vvv)')
    ]
    
    test_cmd = "echo 'teste' | "
    
    for flag, name in levels:
        print(f"\\n📊 Testando {name}...")
        print("-"*40)
        
        cmd = f"{test_cmd}./bin/scripturemon {flag} --timeout 3"
        
        try:
            result = subprocess.run(
                cmd,
                shell=True,
                capture_output=True,
                text=True,
                timeout=5,
                cwd='/Users/clubproducoes/Digimundo/scripturemon-validation'
            )
            
            # Contar linhas de output
            lines = result.stdout.split('\\n')
            non_empty = [l for l in lines if l.strip()]
            
            print(f"  Linhas de output: {len(non_empty)}")
            
            if flag == '--quiet':
                if len(non_empty) < 10:
                    print("  ✅ Modo quiet funcionando (output mínimo)")
                else:
                    print("  ⚠️ Modo quiet ainda verboso")
            elif flag == '-vvv':
                if len(non_empty) > 50:
                    print("  ✅ Modo debug funcionando (output máximo)")
                else:
                    print("  ⚠️ Modo debug não mostra detalhes suficientes")
            
            # Mostrar amostra
            print(f"  Primeiras 3 linhas:")
            for line in non_empty[:3]:
                print(f"    {line[:60]}")
                
        except subprocess.TimeoutExpired:
            print("  ⏱️ Timeout (sistema pode estar lento)")
        except Exception as e:
            print(f"  ❌ Erro: {e}")
    
    print("\\n✅ Teste de verbosidade completo!")

if __name__ == "__main__":
    test_verbosity()
'''
    
    test_path = Path("/Users/clubproducoes/Digimundo/scripturemon-validation/test_verbosity.py")
    test_path.write_text(test_content)
    test_path.chmod(0o755)
    print("✅ Script de teste criado: test_verbosity.py")

if __name__ == "__main__":
    print("🔇 IMPLEMENTANDO CONTROLE DE VERBOSIDADE ROBUSTO")
    print("="*60)
    
    print("\n1. Aplicando controle de verbosidade...")
    if implement_verbosity_control():
        print("\n2. Criando script de teste...")
        create_test_script()
        
        print("\n✅ CONTROLE DE VERBOSIDADE IMPLEMENTADO!")
        print("\nRecursos adicionados:")
        print("  - Argumentos --quiet/-q e --verbose/-v/-vv/-vvv")
        print("  - Classe VerbosityControl com 5 níveis")
        print("  - Filtro inteligente de prints")
        print("  - Comando 'verbose' em runtime")
        print("  - Modo QUIET como padrão (menos verboso)")
        print("  - Supressão de padrões de inicialização")
        print("\nNíveis disponíveis:")
        print("  -q    : SILENT  - Apenas erros críticos")
        print("  (padrão): QUIET   - Output mínimo")
        print("  -v    : NORMAL  - Output normal")
        print("  -vv   : VERBOSE - Output detalhado")
        print("  -vvv  : DEBUG   - Debug completo")
        print("\nSistema mantém EXTREMA ROBUSTEZ com verbosidade configurável!")
    else:
        print("❌ Erro ao implementar controle de verbosidade")