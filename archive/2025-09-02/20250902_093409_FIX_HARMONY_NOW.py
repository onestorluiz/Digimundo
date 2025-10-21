#!/usr/bin/env python3
"""
🔧 CORRETOR DE HARMONIA - Faz todos os componentes funcionarem juntos
================================================================
Este script corrige os problemas identificados para fazer o Scripturemon
funcionar em harmonia total.
"""

import os
import sys
import subprocess
from pathlib import Path

print("=" * 80)
print("🔧 CORRETOR DE HARMONIA DO SCRIPTUREMON")
print("=" * 80)

# Base path
BASE = Path("/Users/clubproducoes/Digimundo/scripturemon-validation")
os.chdir(BASE)

fixes_applied = []
fixes_failed = []

# 1. Corrigir SoulOS
print("\n1️⃣ Corrigindo SoulOS...")
try:
    soulos_file = BASE / "apps/scripturemon/soulos.py"
    if soulos_file.exists():
        content = soulos_file.read_text()
        
        # Adiciona método process_syscalls que estava faltando
        if "def process_syscalls" not in content and "def process(" in content:
            # Adiciona alias para o método
            fix = """
    def process_syscalls(self, text: str) -> Dict:
        \"\"\"Alias para process() - compatibilidade\"\"\"
        return self.process(text)
"""
            # Encontra onde inserir (após process())
            lines = content.split('\n')
            for i, line in enumerate(lines):
                if "def process(self" in line:
                    # Encontra o fim do método
                    indent_count = len(line) - len(line.lstrip())
                    j = i + 1
                    while j < len(lines):
                        if lines[j].strip() and not lines[j].startswith(' ' * (indent_count + 4)):
                            # Inserir aqui
                            lines.insert(j, fix)
                            break
                        j += 1
                    break
            
            content = '\n'.join(lines)
            soulos_file.write_text(content)
            print("   ✅ SoulOS corrigido - adicionado process_syscalls()")
            fixes_applied.append("SoulOS")
    else:
        print("   ⚠️ soulos.py não encontrado")
except Exception as e:
    print(f"   ❌ Erro: {e}")
    fixes_failed.append("SoulOS")

# 2. Corrigir Genetic Evolution
print("\n2️⃣ Corrigindo Genetic Evolution...")
try:
    evolution_file = BASE / "apps/scripturemon/genetic_evolution.py"
    if evolution_file.exists():
        content = evolution_file.read_text()
        
        # Adiciona método create_dna que estava faltando
        if "def create_dna" not in content:
            fix = """
    def create_dna(self, name: str = "default") -> DNA:
        \"\"\"Cria novo DNA
        
        Args:
            name: Nome do DNA
            
        Returns:
            Instância de DNA
        \"\"\"
        return DNA(name=name)
"""
            # Adiciona antes do final da classe
            if "class GeneticEvolution" in content:
                lines = content.split('\n')
                # Encontra o fim da classe
                class_found = False
                for i, line in enumerate(lines):
                    if "class GeneticEvolution" in line:
                        class_found = True
                    elif class_found and line and not line.startswith(' '):
                        # Fim da classe, inserir antes
                        lines.insert(i-1, fix)
                        break
                
                content = '\n'.join(lines)
                evolution_file.write_text(content)
                print("   ✅ Evolution corrigido - adicionado create_dna()")
                fixes_applied.append("Evolution")
        else:
            print("   ✅ create_dna já existe")
            fixes_applied.append("Evolution")
    else:
        print("   ⚠️ genetic_evolution.py não encontrado")
except Exception as e:
    print(f"   ❌ Erro: {e}")
    fixes_failed.append("Evolution")

# 3. Corrigir Telepathy Network
print("\n3️⃣ Corrigindo Telepathy Network...")
try:
    telepathy_file = BASE / "apps/scripturemon/telepathy_network.py"
    if telepathy_file.exists():
        content = telepathy_file.read_text()
        
        # Adiciona propriedade messages_sent
        if "self.messages_sent" not in content:
            # Encontra __init__ e adiciona
            lines = content.split('\n')
            for i, line in enumerate(lines):
                if "def __init__" in line:
                    # Encontra onde adicionar
                    j = i + 1
                    while j < len(lines) and lines[j].strip().startswith('self.'):
                        j += 1
                    lines.insert(j, "        self.messages_sent = 0")
                    break
            
            # Atualiza broadcast para incrementar contador
            for i, line in enumerate(lines):
                if "def broadcast" in line:
                    # Encontra return True
                    j = i + 1
                    while j < len(lines):
                        if "return True" in lines[j]:
                            lines.insert(j, "            self.messages_sent += 1")
                            break
                        j += 1
                    break
            
            content = '\n'.join(lines)
            telepathy_file.write_text(content)
            print("   ✅ Telepathy corrigido - adicionado messages_sent")
            fixes_applied.append("Telepathy")
    else:
        print("   ⚠️ telepathy_network.py não encontrado")
except Exception as e:
    print(f"   ❌ Erro: {e}")
    fixes_failed.append("Telepathy")

# 4. Corrigir Quadruple Pipeline
print("\n4️⃣ Corrigindo Quadruple Pipeline...")
try:
    quadruple_file = BASE / "apps/scripturemon/quadruple_pipeline.py"
    if quadruple_file.exists():
        content = quadruple_file.read_text()
        
        # Adiciona propriedade config
        if "self.config" not in content:
            lines = content.split('\n')
            for i, line in enumerate(lines):
                if "def __init__" in line:
                    j = i + 1
                    while j < len(lines) and (lines[j].strip().startswith('self.') or not lines[j].strip()):
                        j += 1
                    # Adiciona config
                    lines.insert(j-1, """        self.config = {
            "extractor": {"model": "llama3.2:3b", "role": "Extração"},
            "analyzer": {"model": "mistral:instruct", "role": "Análise"},
            "evaluator": {"model": "scripturemon-maestro", "role": "Avaliação"},
            "synthesizer": {"model": "scripturemon-soulos", "role": "Síntese"}
        }""")
                    break
            
            content = '\n'.join(lines)
            quadruple_file.write_text(content)
            print("   ✅ Quadruple corrigido - adicionado config")
            fixes_applied.append("Quadruple")
    else:
        print("   ⚠️ quadruple_pipeline.py não encontrado")
except Exception as e:
    print(f"   ❌ Erro: {e}")
    fixes_failed.append("Quadruple")

# 5. Instalar dependências
print("\n5️⃣ Verificando dependências...")
deps_to_install = []

# Verifica tiktoken
try:
    import tiktoken
    print("   ✅ tiktoken já instalado")
except:
    print("   ⚠️ tiktoken não encontrado")
    deps_to_install.append("tiktoken")

# Verifica PyPDF2
try:
    import PyPDF2
    print("   ✅ PyPDF2 já instalado")
except:
    print("   ⚠️ PyPDF2 não encontrado")
    deps_to_install.append("PyPDF2")

# Verifica pdfplumber
try:
    import pdfplumber
    print("   ✅ pdfplumber já instalado")
except:
    print("   ⚠️ pdfplumber não encontrado")
    deps_to_install.append("pdfplumber")

if deps_to_install:
    print(f"\n   📦 Instalando: {', '.join(deps_to_install)}")
    for dep in deps_to_install:
        try:
            subprocess.run([sys.executable, "-m", "pip", "install", dep], 
                         capture_output=True, check=True)
            print(f"   ✅ {dep} instalado")
            fixes_applied.append(f"Dep: {dep}")
        except:
            print(f"   ❌ Falha ao instalar {dep}")
            fixes_failed.append(f"Dep: {dep}")

# 6. Verificar Ollama
print("\n6️⃣ Verificando Ollama...")
try:
    result = subprocess.run(["ollama", "list"], capture_output=True, text=True)
    if result.returncode == 0:
        print("   ✅ Ollama disponível")
        # Verifica modelos
        output = result.stdout
        if "mistral" in output:
            print("   ✅ Modelo mistral disponível")
        else:
            print("   ⚠️ Modelo mistral não encontrado")
            print("   💡 Instale com: ollama pull mistral:instruct")
    else:
        print("   ❌ Ollama com problema")
except FileNotFoundError:
    print("   ❌ Ollama não instalado")
    print("   💡 Instale de: https://ollama.ai")

# 7. Criar link simbólico para CINEMA_KNOWLEDGE
print("\n7️⃣ Conectando CINEMA_KNOWLEDGE ao RAG...")
try:
    cinema_source = BASE / "CINEMA_KNOWLEDGE"
    rag_target = BASE / "data/cinema_knowledge"
    
    if cinema_source.exists() and not rag_target.exists():
        rag_target.parent.mkdir(parents=True, exist_ok=True)
        os.symlink(cinema_source, rag_target)
        print("   ✅ CINEMA_KNOWLEDGE conectado ao sistema RAG")
        fixes_applied.append("Cinema-RAG")
    elif rag_target.exists():
        print("   ✅ Link já existe")
    else:
        print("   ⚠️ CINEMA_KNOWLEDGE não encontrado")
except Exception as e:
    print(f"   ❌ Erro: {e}")
    fixes_failed.append("Cinema-RAG")

# Relatório final
print("\n" + "=" * 80)
print("📊 RELATÓRIO DE CORREÇÕES")
print("=" * 80)

if fixes_applied:
    print(f"\n✅ Correções aplicadas ({len(fixes_applied)}):")
    for fix in fixes_applied:
        print(f"   • {fix}")

if fixes_failed:
    print(f"\n❌ Correções falhadas ({len(fixes_failed)}):")
    for fix in fixes_failed:
        print(f"   • {fix}")

success_rate = len(fixes_applied) / (len(fixes_applied) + len(fixes_failed)) * 100 if (fixes_applied or fixes_failed) else 0

print(f"\n📈 Taxa de sucesso: {success_rate:.0f}%")

if success_rate >= 80:
    print("\n🎉 HARMONIA RESTAURADA!")
    print("O Scripturemon agora deve funcionar com todos os componentes integrados.")
elif success_rate >= 50:
    print("\n✅ HARMONIA PARCIAL")
    print("Maioria dos componentes corrigidos. Sistema funcional.")
else:
    print("\n⚠️ HARMONIA INCOMPLETA")
    print("Muitas correções falharam. Verifique manualmente.")

print("\n💡 PRÓXIMOS PASSOS:")
print("1. Teste o chat: python3 -m apps.scripturemon.chat")
print("2. Verifique status: python3 -m apps.scripturemon.cli validate once")
print("3. Teste harmonia: python3 FINAL_HARMONY_TEST.py")

print("=" * 80)