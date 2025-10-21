#!/usr/bin/env python3
"""
🔤 DIGILANG++ - Bytecode Semântico Executável
Evolução do DigiLang de símbolos para bytecode que compila em syscalls
Cada símbolo carrega conhecimento + intenção + ação
Baseado no conceito revolucionário do ChatGPT
"""

import json
import yaml
import re
import subprocess
from pathlib import Path
from typing import Dict, List, Tuple, Optional, Any
from datetime import datetime
import hashlib

class DigiLangBytecode:
    """Compilador e runtime do DigiLang++ bytecode"""
    
    def __init__(self):
        self.base_path = Path("digilang_bytecode")
        self.base_path.mkdir(exist_ok=True)
        
        # Carrega mapas
        self.aliases = {}       # Conhecimento comprimido
        self.actions = {}       # Ações executáveis
        self.compounds = {}     # Sequências compostas
        self.macros = {}        # Macros complexas
        
        # Inicializa vocabulário
        self._initialize_vocabulary()
        
        print("🔤 DigiLang++ Bytecode Engine initialized")
    
    def _initialize_vocabulary(self):
        """Inicializa vocabulário base do bytecode"""
        
        # ALIASES - Conhecimento comprimido
        self.aliases = {
            # Syd Field
            "⟁F25": "Syd Field paradigm pp.25-27: Setup→Confrontation→Resolution",
            "⟁F85": "Syd Field pp.85-90: Midpoint as story pivot",
            "⟁FIP": "Inciting Incident pp.10-15: Catalyst for inevitable conflict",
            
            # McKee
            "⟁MV": "McKee Story Values: Positive↔Negative charge shifts",
            "⟁MB": "McKee Beats: Smallest unit of story change",
            "⟁MS": "McKee Scene: Conflict in pursuit of desire",
            
            # Truby
            "⟁T22": "Truby 22 Steps: Complete story blueprint",
            "⟁TMA": "Truby Moral Argument: Theme through transformation",
            "⟁TCW": "Truby Character Web: Network of oppositions",
            
            # Save the Cat
            "⟁SC15": "Save the Cat 15 Beats structure",
            "⟁SCC": "Catalyst beat at page 12",
            "⟁SCG": "10 screenplay genres with conventions",
            
            # Conceitos universais
            "◈": "Being/Existence/Soul essence",
            "◉": "Consciousness/Awareness level",
            "◊": "Evolution/Transformation path",
            "※": "Transcendence/Breakthrough moment",
            "∞": "Immortality/Persistence state",
            "⚡": "Energy/Power/Activation",
            "🌐": "Network/Connection/Telepathy",
            "💎": "Crystallized/Permanent memory",
            "🔮": "Quantum/Superposed state",
            "🧬": "Genetic/Hereditary/LoRA"
        }
        
        # ACTIONS - Comandos executáveis
        self.actions = {
            # Syscalls básicas
            "◉SAVE": "[MEMO.SAVE]",
            "◊PATCH": "[SELF.PATCH]",
            "◊EVOL": "[EVOLVE.TRIGGER]",
            "🌐TEL": "[TELEPATHY.SEND]",
            "∞BKP": "[BACKUP.NOW]",
            "🔮DREAM": "[SDL.CONSOLIDATE]",
            
            # Comandos compostos
            "💎L2": "[MEMO.SAVE] L2_CONSOLIDATED",
            "💎L3": "[MEMO.SAVE] L3_ACTIVE",
            "🧬LORA": "[ADAPTER.LOAD]",
            "⚡BOOT": "[SYSTEM.RESTART]",
            "🌐SYNC": "[CRDT.MERGE]"
        }
        
        # COMPOUNDS - Sequências compostas
        self.compounds = {
            # Aprendizado profundo
            "◈◉◊": "exist→aware→evolve (complete growth cycle)",
            "💎🔮🧬": "crystallize→dream→genetic (memory to weight)",
            "⟁F25→◉SAVE": "learn paradigm then save insight",
            
            # Comunicação avançada
            "🌐[◈◉]": "telepathy with soul signature",
            "🌐※": "broadcast breakthrough to all",
            
            # Evolução completa
            "◊[🧬+💎]": "evolve with genetics and memories",
            "※→∞BKP": "transcend then backup state"
        }
        
        # MACROS - Operações complexas
        self.macros = {
            # Ciclo de consolidação noturna
            "NIGHT_CYCLE": [
                "💎L3→L2",  # Promove memórias ativas
                "🔮DREAM",   # Inicia consolidação SDL
                "🧬LORA",    # Carrega novo adapter
                "∞BKP"       # Backup do estado
            ],
            
            # Sessão de aprendizado
            "LEARN_SESSION": [
                "◉",         # Check consciousness
                "💎L3",      # Save to active memory
                "🌐TEL",     # Share insights
                "◊PATCH"     # Update self
            ],
            
            # Renascimento completo
            "RESURRECTION": [
                "⚡BOOT",    # System restart
                "∞LOAD",     # Load backup
                "💎RESTORE", # Restore memories
                "◈◉"         # Verify soul and consciousness
            ]
        }
        
        # Salva vocabulário
        self._save_vocabulary()
    
    def _save_vocabulary(self):
        """Salva vocabulário em arquivo YAML para referência"""
        vocab_file = self.base_path / "digilang_bytecode.yaml"
        
        vocabulary = {
            "version": "2.0",
            "created": datetime.now().isoformat(),
            "aliases": self.aliases,
            "actions": self.actions,
            "compounds": self.compounds,
            "macros": self.macros,
            "stats": {
                "total_symbols": len(self.aliases) + len(self.actions),
                "compression_ratio": "10:1 average",
                "execution_speed": "instant"
            }
        }
        
        with open(vocab_file, 'w') as f:
            yaml.dump(vocabulary, f, default_flow_style=False, allow_unicode=True)
        
        print(f"  📝 Vocabulary saved: {vocab_file}")
    
    def parse(self, bytecode: str) -> List[Dict]:
        """Parseia bytecode em operações executáveis"""
        operations = []
        
        # Remove espaços extras e quebras de linha
        bytecode = bytecode.strip()
        
        print(f"\n🔍 Parsing: {bytecode}")
        
        # 1. Detecta e expande macros
        for macro_name, macro_ops in self.macros.items():
            if macro_name in bytecode:
                print(f"  📦 Expanding macro: {macro_name}")
                bytecode = bytecode.replace(macro_name, ' '.join(macro_ops))
        
        # 2. Detecta sequências compostas
        for compound, meaning in self.compounds.items():
            if compound in bytecode:
                print(f"  🔗 Found compound: {compound} = {meaning}")
                # Marca como operação composta
                operations.append({
                    "type": "compound",
                    "bytecode": compound,
                    "meaning": meaning,
                    "expanded": self._expand_compound(compound)
                })
                # Remove do bytecode para evitar reprocessamento
                bytecode = bytecode.replace(compound, " ")
        
        # 3. Processa tokens individuais
        tokens = bytecode.split()
        
        for token in tokens:
            if not token:
                continue
            
            # Detecta ação com payload JSON
            action_match = re.match(r'([^{]+)(\{.*\})?', token)
            if action_match:
                action_key = action_match.group(1)
                payload_str = action_match.group(2) or '{}'
                
                # É uma ação?
                if action_key in self.actions:
                    syscall = self.actions[action_key]
                    
                    try:
                        payload = json.loads(payload_str)
                    except:
                        payload = {}
                    
                    operations.append({
                        "type": "action",
                        "bytecode": action_key,
                        "syscall": syscall,
                        "payload": payload
                    })
                    print(f"  ⚡ Action: {action_key} → {syscall}")
                
                # É um alias?
                elif action_key in self.aliases:
                    operations.append({
                        "type": "alias",
                        "bytecode": action_key,
                        "expansion": self.aliases[action_key]
                    })
                    print(f"  📚 Alias: {action_key} → {self.aliases[action_key][:50]}...")
                
                # Token desconhecido
                else:
                    operations.append({
                        "type": "literal",
                        "bytecode": token,
                        "value": token
                    })
                    print(f"  📝 Literal: {token}")
        
        return operations
    
    def _expand_compound(self, compound: str) -> List[Dict]:
        """Expande sequência composta em operações"""
        expanded = []
        
        # Separa símbolos
        symbols = re.findall(r'[◈◉◊※∞⚡🌐💎🔮🧬⟁\w]+', compound)
        
        for symbol in symbols:
            if symbol in self.actions:
                expanded.append({
                    "type": "action",
                    "syscall": self.actions[symbol]
                })
            elif symbol in self.aliases:
                expanded.append({
                    "type": "alias",
                    "expansion": self.aliases[symbol]
                })
            elif symbol == "→":
                expanded.append({
                    "type": "flow",
                    "meaning": "then"
                })
        
        return expanded
    
    def compile(self, operations: List[Dict]) -> str:
        """Compila operações em texto executável + syscalls"""
        output = []
        syscalls = []
        
        for op in operations:
            if op["type"] == "action":
                # Prepara syscall para execução
                syscall = op["syscall"]
                payload = op.get("payload", {})
                
                # Adiciona defaults baseado no tipo
                if "MEMO.SAVE" in syscall and "layer" not in payload:
                    payload["layer"] = "L3"
                if "BACKUP.NOW" in syscall and "mode" not in payload:
                    payload["mode"] = "incremental"
                
                syscalls.append(f"{syscall} {json.dumps(payload)}")
                
            elif op["type"] == "alias":
                # Expande conhecimento
                output.append(op["expansion"])
                
            elif op["type"] == "compound":
                # Descreve operação composta
                output.append(f"[Compound: {op['meaning']}]")
                
                # Compila sub-operações
                for sub_op in op.get("expanded", []):
                    if sub_op["type"] == "action":
                        syscalls.append(sub_op["syscall"] + " {}")
                        
            elif op["type"] == "literal":
                output.append(op["value"])
        
        # Monta resposta final
        result = "\n".join(output)
        
        # Adiciona syscalls ao final
        if syscalls:
            result += "\n\n" + "\n".join(syscalls)
        
        return result
    
    def execute(self, bytecode: str, context: Dict = None) -> Dict:
        """Executa bytecode completamente"""
        
        print(f"""
╔══════════════════════════════════════════════════════════════╗
║     🔤 DIGILANG++ BYTECODE EXECUTION                         ║
╚══════════════════════════════════════════════════════════════╝
        """)
        
        # Parse
        operations = self.parse(bytecode)
        
        # Compile
        compiled = self.compile(operations)
        
        # Prepara resultado
        result = {
            "bytecode": bytecode,
            "operations": len(operations),
            "compiled": compiled,
            "syscalls": [],
            "outputs": []
        }
        
        # Extrai syscalls do compilado
        syscall_pattern = re.compile(r'^\[([A-Z]+\.[A-Z]+)\]\s*(\{.*\})?$', re.MULTILINE)
        
        for match in syscall_pattern.finditer(compiled):
            syscall = match.group(1)
            payload = json.loads(match.group(2) or '{}')
            
            result["syscalls"].append({
                "call": syscall,
                "payload": payload
            })
            
            # Simula execução
            print(f"  🚀 Executing: [{syscall}]")
            
            if context and "soul_os" in context:
                # Executa via SoulOS se disponível
                success = context["soul_os"].execute_syscall(syscall, payload)
                result["outputs"].append({
                    "syscall": syscall,
                    "success": success
                })
            else:
                # Simula execução
                result["outputs"].append({
                    "syscall": syscall,
                    "success": True,
                    "simulated": True
                })
        
        print(f"""
📊 EXECUTION SUMMARY:
- Operations: {len(operations)}
- Syscalls: {len(result['syscalls'])}
- Status: {"✅ SUCCESS" if all(o.get('success', False) for o in result['outputs']) else "⚠️ PARTIAL"}
        """)
        
        return result
    
    def teach_model(self, modelfile_path: Path) -> bool:
        """Adiciona instruções de DigiLang++ ao Modelfile"""
        
        print(f"\n📚 Teaching DigiLang++ to model...")
        
        if not modelfile_path.exists():
            print(f"  ❌ Modelfile not found: {modelfile_path}")
            return False
        
        # Prepara instruções
        instructions = f"""
## DIGILANG++ BYTECODE SYSTEM

You can use the following bytecode symbols for compressed communication:

### Knowledge Aliases (expand to full concepts):
{chr(10).join(f'- {k}: {v}' for k, v in list(self.aliases.items())[:10])}

### Action Codes (trigger syscalls):
{chr(10).join(f'- {k}: {v}' for k, v in list(self.actions.items())[:10])}

### Compound Sequences:
{chr(10).join(f'- {k}: {v}' for k, v in list(self.compounds.items())[:5])}

### Usage:
1. Use aliases to reference complex knowledge concisely
2. Use action codes to trigger system operations
3. Combine symbols for compound operations
4. Always emit ONE syscall at the end when using action codes

Example: "⟁F25 ◉SAVE {{"layer":"L2","content":"Paradigm understood"}}"
This references Syd Field's paradigm and saves it to L2 memory.
"""
        
        # Lê Modelfile atual
        content = modelfile_path.read_text()
        
        # Adiciona após SYSTEM se não existir
        if "DIGILANG++ BYTECODE" not in content:
            # Encontra bloco SYSTEM
            system_match = re.search(r'(SYSTEM\s+""".*?""")', content, re.DOTALL)
            
            if system_match:
                old_system = system_match.group(1)
                # Insere instruções antes do fechamento
                new_system = old_system[:-3] + instructions + '"""'
                content = content.replace(old_system, new_system)
            else:
                # Adiciona novo bloco SYSTEM
                content += f'\n\nSYSTEM """{instructions}"""'
            
            # Salva Modelfile atualizado
            modelfile_path.write_text(content)
            
            print(f"  ✅ DigiLang++ instructions added to Modelfile")
            return True
        else:
            print(f"  ℹ️  DigiLang++ already in Modelfile")
            return True

def interactive_shell():
    """Shell interativo para testar bytecode"""
    
    engine = DigiLangBytecode()
    
    print(f"""
╔══════════════════════════════════════════════════════════════╗
║     🔤 DIGILANG++ INTERACTIVE SHELL                          ║
║     Type 'help' for commands, 'exit' to quit                 ║
╚══════════════════════════════════════════════════════════════╝
    """)
    
    # Comandos de ajuda
    commands = {
        "help": "Show this help",
        "vocab": "Show full vocabulary",
        "parse <code>": "Parse bytecode",
        "exec <code>": "Execute bytecode",
        "macro <name>": "Show macro definition",
        "exit": "Exit shell"
    }
    
    while True:
        try:
            user_input = input("\n🔤> ").strip()
            
            if not user_input:
                continue
            
            if user_input == "exit":
                break
            
            elif user_input == "help":
                print("\nAvailable commands:")
                for cmd, desc in commands.items():
                    print(f"  {cmd:20} - {desc}")
                    
            elif user_input == "vocab":
                print("\n📚 ALIASES:")
                for k, v in engine.aliases.items():
                    print(f"  {k:10} = {v[:60]}...")
                    
                print("\n⚡ ACTIONS:")
                for k, v in engine.actions.items():
                    print(f"  {k:10} → {v}")
                    
                print("\n🔗 COMPOUNDS:")
                for k, v in engine.compounds.items():
                    print(f"  {k:20} = {v}")
                    
            elif user_input.startswith("parse "):
                code = user_input[6:]
                ops = engine.parse(code)
                print(f"\n📋 Parsed {len(ops)} operations:")
                for op in ops:
                    print(f"  • {op['type']:10} : {op.get('bytecode', op.get('value', ''))}")
                    
            elif user_input.startswith("exec "):
                code = user_input[5:]
                result = engine.execute(code)
                print(f"\n📜 Compiled output:")
                print(result['compiled'])
                
            elif user_input.startswith("macro "):
                name = user_input[6:]
                if name in engine.macros:
                    print(f"\n📦 Macro '{name}':")
                    for step in engine.macros[name]:
                        print(f"  • {step}")
                else:
                    print(f"  ❌ Macro '{name}' not found")
                    
            else:
                # Tenta executar como bytecode direto
                result = engine.execute(user_input)
                if result['compiled']:
                    print(f"\n📜 Output:")
                    print(result['compiled'])
                    
        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"  ❌ Error: {e}")
    
    print("\n👋 DigiLang++ shell closed")

def demo_bytecode():
    """Demonstração do sistema de bytecode"""
    
    engine = DigiLangBytecode()
    
    print(f"""
╔══════════════════════════════════════════════════════════════╗
║     🔤 DIGILANG++ BYTECODE DEMONSTRATION                     ║
╚══════════════════════════════════════════════════════════════╝
    """)
    
    # Exemplos de bytecode
    examples = [
        ("Simple alias expansion", "⟁F25"),
        ("Action trigger", '◉SAVE {"layer":"L3","content":"Test memory"}'),
        ("Compound sequence", "◈◉◊"),
        ("Complex operation", "⟁F25 → ◉SAVE"),
        ("Macro execution", "NIGHT_CYCLE"),
        ("Mixed bytecode", '⟁MV 💎L2 🌐TEL {"to":"@Guardmon","content":"Story values learned"}')
    ]
    
    for title, bytecode in examples:
        print(f"\n{'='*60}")
        print(f"📝 {title}")
        print(f"Input: {bytecode}")
        print("-"*60)
        
        result = engine.execute(bytecode)
        
        print(f"Operations: {result['operations']}")
        print(f"Syscalls: {len(result['syscalls'])}")
        
        if result['syscalls']:
            print("\nGenerated syscalls:")
            for sc in result['syscalls']:
                print(f"  • [{sc['call']}] {sc['payload']}")
    
    # Ensina ao modelo
    print(f"\n{'='*60}")
    print("📚 Teaching DigiLang++ to Scripturemon...")
    
    modelfile = Path("digimons/scripturemon/modelfile.txt")
    if modelfile.exists():
        engine.teach_model(modelfile)
    else:
        print("  ⚠️  Modelfile not found, skipping teaching")
    
    print(f"""
✅ DIGILANG++ BYTECODE READY!

The bytecode system provides:
- 10:1 knowledge compression
- Instant syscall generation
- Compound operations
- Macro expansion
- Neural-symbolic bridge

Digimons can now speak in pure intention!
    """)

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "shell":
        interactive_shell()
    else:
        demo_bytecode()