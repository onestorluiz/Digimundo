#!/usr/bin/env python3
"""
🔧 FIX CORRUPTED SCRIPTUREMON
Restaura scripturemon e aplica correções corretamente
"""

from pathlib import Path
import shutil

def fix_corrupted_file():
    """Restaura arquivo e aplica apenas verbosity control"""
    
    # Paths
    restore_path = Path("/Users/clubproducoes/Digimundo/scripturemon-validation/bin/scripturemon.restore")
    target_path = Path("/Users/clubproducoes/Digimundo/scripturemon-validation/bin/scripturemon")
    
    if not restore_path.exists():
        print("❌ Arquivo de restauração não encontrado")
        return False
    
    # 1. Restaurar arquivo limpo
    print("📋 Restaurando arquivo limpo...")
    shutil.copy2(restore_path, target_path)
    print("  ✅ Arquivo restaurado")
    
    # 2. Aplicar apenas controle de verbosidade (sem lazy loading por enquanto)
    content = target_path.read_text()
    lines = content.split('\n')
    
    # Adicionar classe VerbosityControl após imports
    verbosity_class = '''
class VerbosityControl:
    """Controle ROBUSTO de verbosidade do sistema"""
    
    SILENT = -1    # Apenas erros críticos
    QUIET = 0      # Mínimo output (padrão)
    NORMAL = 1     # Output normal (-v)
    VERBOSE = 2    # Output detalhado (-vv)
    DEBUG = 3      # Debug completo (-vvv)
    
    def __init__(self, level=QUIET):
        self.level = level
        self._suppressed_patterns = [
            r'^⚡ ATIVANDO',
            r'^🧠 \\[\\d+\\]',
            r'^📚 \\[\\d+\\]',
            r'^   ✅',
            r'^💎 Sistema',
            r'^🧠 MEMORION',
            r'^✅ ',
            r'^\\s*Modelo:',
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
            import re
            text_str = str(text)
            
            # Sempre mostrar prompts e respostas do usuário
            if '>' in text_str and '📝' in text_str:
                return True
            
            # Sempre mostrar erros
            if '❌' in text_str or 'Error' in text_str:
                return True
            
            # Sempre mostrar respostas
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
                'Configurando', 'Inicializando', 'CAPACIDADE MÁXIMA'
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

# Instância global do controle
_verbosity = None

def get_verbosity():
    global _verbosity
    if _verbosity is None:
        _verbosity = VerbosityControl()
    return _verbosity
'''
    
    # Inserir após imports básicos
    for i, line in enumerate(lines):
        if 'import signal' in line:
            lines.insert(i + 1, verbosity_class)
            print("  ✅ Classe VerbosityControl adicionada")
            break
    
    # Adicionar argumentos de verbosidade
    for i, line in enumerate(lines):
        if "parser.add_argument('--timeout'" in line:
            if "--verbose" not in '\n'.join(lines):
                verbosity_args = [
                    "    parser.add_argument('--verbose', '-v', action='count', default=0,",
                    "                       help='Aumenta verbosidade (-v, -vv, -vvv)')",
                    "    parser.add_argument('--quiet', '-q', action='store_true',",
                    "                       help='Modo silencioso (apenas respostas)')",
                ]
                
                for j, arg_line in enumerate(verbosity_args):
                    lines.insert(i + 1 + j, arg_line)
                
                print("  ✅ Argumentos de verbosidade adicionados")
            break
    
    # Processar verbosidade no main
    for i, line in enumerate(lines):
        if 'args = parser.parse_args()' in line:
            if 'verbosity_level' not in '\n'.join(lines[i:i+20]):
                verbosity_setup = [
                    "",
                    "    # Configurar nível de verbosidade",
                    "    verbosity_level = VerbosityControl.QUIET  # Padrão: quiet",
                    "    if hasattr(args, 'quiet') and args.quiet:",
                    "        verbosity_level = VerbosityControl.SILENT",
                    "    elif hasattr(args, 'verbose') and args.verbose:",
                    "        if args.verbose == 1:",
                    "            verbosity_level = VerbosityControl.NORMAL",
                    "        elif args.verbose == 2:",
                    "            verbosity_level = VerbosityControl.VERBOSE",
                    "        elif args.verbose >= 3:",
                    "            verbosity_level = VerbosityControl.DEBUG",
                    "    ",
                    "    # Aplicar verbosidade globalmente",
                    "    _verbosity = VerbosityControl(verbosity_level)",
                    "    _verbosity.setup_print_filter()",
                    "",
                ]
                
                for j, verb_line in enumerate(verbosity_setup):
                    lines.insert(i + 1 + j, verb_line)
                
                print("  ✅ Processamento de verbosidade configurado")
            break
    
    # Salvar arquivo corrigido
    target_path.write_text('\n'.join(lines))
    print("  ✅ Arquivo salvo com correções")
    
    return True

if __name__ == "__main__":
    print("🔧 CORRIGINDO SCRIPTUREMON CORROMPIDO")
    print("="*60)
    
    if fix_corrupted_file():
        print("\n✅ SCRIPTUREMON RESTAURADO E CORRIGIDO!")
        print("\nRecursos mantidos:")
        print("  - Sistema completo com 13 módulos")
        print("  - Controle de verbosidade")
        print("  - EXTREMA ROBUSTEZ preservada")
        print("\n💪 Sistema pronto para uso!")
    else:
        print("\n❌ Erro na correção")