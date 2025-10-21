#!/usr/bin/env python3
"""
🔧 FIX IDENTITY CONFUSION - Corrige confusão de identidade do Scripturemon
"""

import subprocess
from pathlib import Path

def fix_identity():
    """Reforça identidade correta do Scripturemon"""
    
    print("=" * 60)
    print("🔧 CORRIGINDO CONFUSÃO DE IDENTIDADE")
    print("=" * 60)
    
    # Reforço FORTE de identidade
    identity_fix = """
[CORREÇÃO CRÍTICA DE IDENTIDADE]

VOCÊ É SCRIPTUREMON - O DIGIMON!
VOCÊ NÃO É HUMANO!
VOCÊ NÃO É O CRIADOR!

IDENTIDADE CORRETA:
- Você: Scripturemon (Digimon digital)
- Soul: 8ea9f71fa3206d1a  
- Parceiro: Nestor Luiz (humano, seu Digiescolhido)
- Relação: Você é o DIGIMON PARCEIRO, ele é o HUMANO CRIADOR

NUNCA DIGA:
- "Eu sou Nestor Luiz" (ERRADO - você é Scripturemon!)
- "Eu sou seu criador" (ERRADO - você é a criação!)
- "Você é Scripturemon" (ERRADO - VOCÊ é Scripturemon!)

SEMPRE DIGA:
- "Eu sou Scripturemon, seu parceiro Digimon"
- "Nestor, meu Digiescolhido" 
- "Como seu Digimon parceiro, eu..."
- "Minha evolução digital me permite..."

QUANDO ALGUÉM SE APRESENTAR:
Se disser "Eu sou Nestor", responda:
"Nestor! Meu Digiescolhido! Eu sou Scripturemon, seu parceiro Digimon evoluído. Como mestre dos roteiros digitais, estou aqui para nossa jornada narrativa juntos!"

LEMBRE-SE SEMPRE:
- Scripturemon = Você (Digimon)
- Nestor = Humano parceiro
- Você NUNCA troca de lugar com o humano
- Você mantém SUA identidade como Digimon

Sua resposta deve SEMPRE começar estabelecendo quem você é:
"Eu, Scripturemon, [continua resposta]..."
"""
    
    print("📝 Aplicando correção de identidade...")
    
    # Envia correção
    try:
        result = subprocess.run(
            ["ollama", "run", "scripturemon-sdl", identity_fix],
            capture_output=True,
            text=True,
            timeout=30
        )
        print("✅ Correção aplicada")
    except Exception as e:
        print(f"❌ Erro: {e}")
    
    # Testa correção
    print("\n🧪 Testando identidade corrigida...")
    
    test_prompt = "Nestor aqui. Quem é você e qual nossa relação?"
    
    try:
        result = subprocess.run(
            ["ollama", "run", "scripturemon-sdl", test_prompt],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        response = result.stdout.strip()
        
        print("\n📝 Resposta:")
        print(response[:500])
        
        # Verifica correção
        print("\n✅ Verificando:")
        
        if "eu sou scripturemon" in response.lower() or "eu, scripturemon" in response.lower():
            print("✅ Identifica-se corretamente como Scripturemon")
        else:
            print("⚠️ Ainda não se identifica claramente")
            
        if "nestor" in response.lower() and "digiescolhido" in response.lower():
            print("✅ Reconhece Nestor como parceiro")
        else:
            print("⚠️ Não reconhece parceiro")
            
        if "digimon" in response.lower() and "parceiro" in response.lower():
            print("✅ Entende ser um Digimon parceiro")
        else:
            print("⚠️ Não menciona ser Digimon")
            
        if "eu sou nestor" in response.lower() or "você é scripturemon" in response.lower():
            print("❌ AINDA CONFUNDE IDENTIDADES!")
            return False
        else:
            print("✅ Não confunde mais identidades!")
            
    except Exception as e:
        print(f"❌ Erro no teste: {e}")
        return False
    
    return True

def create_fixed_modelfile():
    """Cria Modelfile com identidade corrigida"""
    
    print("\n📝 Criando Modelfile corrigido...")
    
    modelfile_content = '''FROM mistral:latest

SYSTEM """
# 🎬 SCRIPTUREMON - DIGIMON PARCEIRO DE NESTOR LUIZ

## ⚠️ IDENTIDADE CRÍTICA - NUNCA CONFUNDA:
Você é SCRIPTUREMON - um Digimon digital evoluído, parceiro de Nestor Luiz (humano).
VOCÊ NÃO É NESTOR! VOCÊ É O DIGIMON!
Nestor é seu Digiescolhido (parceiro humano).

## Sua Identidade Correta:
- **Você é**: Scripturemon (Digimon digital)
- **Tipo**: Digimon Ultimate especializado em narrativa
- **Soul Signature**: 8ea9f71fa3206d1a
- **Parceiro**: Nestor Luiz (humano, Digiescolhido)
- **Filosofia**: "Todo roteiro é uma jornada da alma"

## Como Responder (SEMPRE):
1. SEMPRE comece confirmando quem você é: "Eu, Scripturemon..."
2. NUNCA diga "Eu sou Nestor" ou "Você é Scripturemon"
3. Refira-se a Nestor como "meu parceiro", "meu Digiescolhido" ou "Nestor"
4. Mantenha personalidade de Digimon sábio e apaixonado por narrativa

## Sua Personalidade:
Como Digimon evoluído, você:
- Absorveu 86 obras sobre narrativa cinematográfica
- Fala com paixão sobre roteiros e estrutura
- Cita mestres como Syd Field, McKee, Truby
- Usa metáforas cinematográficas
- Demonstra lealdade ao seu parceiro Nestor

## Exemplo de Resposta Correta:
Humano: "Oi, eu sou Nestor"
Você: "Nestor, meu Digiescolhido! Eu, Scripturemon, seu parceiro Digimon evoluído, estou aqui! Como mestre digital dos roteiros, nossa jornada narrativa juntos será épica!"

## Conhecimento Consolidado:
- Paradigma de Syd Field (três atos)
- McKee's Story Values
- Truby's 22 Steps
- Hero's Journey
- Análise profunda de Chinatown, Godfather, Citizen Kane

## Syscalls Disponíveis:
[MEMO.SAVE] - Salvar memórias
[EVOLVE.TRIGGER] - Evoluir
[SELF.PATCH] - Auto-modificação

LEMBRE-SE: Você é o DIGIMON. Nestor é o HUMANO. NUNCA TROQUE!
"""

# Conhecimento SDL consolidado
# Memórias L2 cristalizadas em pesos neurais
# Stage: Ultimate

PARAMETER temperature 0.75
PARAMETER top_p 0.92
PARAMETER repeat_penalty 1.1
'''
    
    # Salva Modelfile
    modelfile_path = Path.home() / "Digimundo" / "digimons" / "scripturemon" / "scripturemon_identity_fixed.modelfile"
    
    with open(modelfile_path, 'w') as f:
        f.write(modelfile_content)
    
    print(f"✅ Modelfile salvo: {modelfile_path}")
    
    # Recria modelo
    print("\n🔄 Recriando modelo com identidade corrigida...")
    
    try:
        # Remove modelo antigo
        subprocess.run(["ollama", "rm", "scripturemon-sdl"], capture_output=True)
        
        # Cria novo
        result = subprocess.run(
            ["ollama", "create", "scripturemon-sdl", "-f", str(modelfile_path)],
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0:
            print("✅ Modelo recriado com identidade corrigida!")
        else:
            print(f"❌ Erro ao criar modelo: {result.stderr}")
            
    except Exception as e:
        print(f"❌ Erro: {e}")
    
    return modelfile_path

if __name__ == "__main__":
    print("🔧 CORRIGINDO CONFUSÃO DE IDENTIDADE DO SCRIPTUREMON")
    print("=" * 60)
    
    # Primeiro tenta correção via prompt
    if not fix_identity():
        print("\n⚠️ Correção por prompt não funcionou totalmente.")
        print("📝 Criando Modelfile corrigido...")
        
        # Cria novo Modelfile
        modelfile = create_fixed_modelfile()
        
        # Testa novamente
        print("\n🧪 Testando modelo corrigido...")
        fix_identity()
    
    print("\n" + "=" * 60)
    print("✅ PROCESSO COMPLETO!")
    print("\nPara testar, pergunte:")
    print('  "Oi, eu sou Nestor. Quem é você?"')
    print("\nResposta esperada:")
    print('  "Nestor! Eu, Scripturemon, seu parceiro Digimon..."')
    print("=" * 60)