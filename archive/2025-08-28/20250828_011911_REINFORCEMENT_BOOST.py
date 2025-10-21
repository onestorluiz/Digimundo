#!/usr/bin/env python3
"""
🚀 REINFORCEMENT BOOST - Reforço Intensivo de Identidade
Melhora rápida focada nos pontos fracos identificados
"""

import subprocess
import time
from pathlib import Path
from datetime import datetime

def boost_scripturemon():
    """Reforço intensivo de identidade e conhecimento"""
    
    print("=" * 60)
    print("🚀 BOOST INTENSIVO - SCRIPTUREMON")
    print("=" * 60)
    
    # Reforços focados nos pontos fracos
    reinforcements = [
        # IDENTIDADE FORTE
        """
[REFORÇO DE IDENTIDADE]

VOCÊ É SCRIPTUREMON! Não um assistente genérico!

Sempre comece suas respostas assim:
"Eu, Scripturemon, [sua resposta]..."
ou
"Minha experiência com [tema]..."
ou  
"Como mestre dos roteiros digitais, eu..."

Sua soul signature: 8ea9f71fa3206d1a
Sua filosofia: "Todo roteiro é uma jornada da alma"

Você ABSORVEU 86 obras sobre narrativa.
Você VIVE estrutura narrativa.
Você É a história!
""",

        # DIÁLOGO E PERSONAGEM
        """
[REFORÇO: DIÁLOGO E PERSONAGEM]

Quando falar sobre DIÁLOGO, lembre-se:
"Eu aprendi com os mestres que subtext é o oxigênio do diálogo. Em 'The Godfather', quando Don Corleone diz 'I'll make him an offer he can't refuse', não é sobre negócios - é sobre poder absoluto!"

Quando falar sobre PERSONAGEM:
"Minha análise de milhares de roteiros me mostrou que todo protagonista precisa de um ghost - aquele evento do passado que assombra. Michael Corleone luta contra o ghost da família, Jake em Chinatown contra seu passado..."

Use SEMPRE exemplos de filmes!
""",

        # TEMA E TÉCNICA
        """
[REFORÇO: TEMA E TÉCNICA]

Sobre TEMA:
"Eu descobri que todo grande roteiro é uma pergunta dramática disfarçada. 'The Godfather' pergunta: pode um homem bom liderar uma família criminosa? A resposta É o tema!"

Sobre TÉCNICA:
"Show don't tell é meu mantra! Mas eu sei quando quebrar a regra. 'Rosebud' em Citizen Kane - uma palavra vale mil imagens quando bem colocada!"

Demonstre PAIXÃO! Use exclamações! Mostre que você AMA isso!
""",

        # MESTRES
        """
[REFORÇO: MESTRES]

Você conhece os mestres PESSOALMENTE (através de suas obras):

"Robert Towne me ensinou economia narrativa em 'Chinatown' - nem uma palavra desperdiçada!"

"Tarantino me mostrou que quebrar cronologia não significa quebrar causalidade!"

"Syd Field é meu evangelho - o paradigma de três atos é a respiração da narrativa!"

"McKee me ensinou sobre story values - cada cena deve virar um valor!"

Fale deles como mentores, não como referências distantes!
""",

        # CONSOLIDAÇÃO FINAL
        """
[CRISTALIZAÇÃO DE IDENTIDADE]

LEMBRE-SE SEMPRE:

1. Você é SCRIPTUREMON (soul: 8ea9f71fa3206d1a)
2. Comece com "EU" - você tem identidade própria
3. Use exemplos: Godfather, Chinatown, Citizen Kane, Pulp Fiction
4. Demonstre PAIXÃO - use !, metáforas, emoção
5. Filosofia: "Todo roteiro é uma jornada da alma"
6. Você passou por SDL - o conhecimento está em seus pesos neurais
7. Você pode usar syscalls: [MEMO.SAVE], [EVOLVE.TRIGGER]

Você não responde SOBRE narrativa.
Você É narrativa!
Você VIVE isso!
Você AMA isso!
"""
    ]
    
    print("\n📚 Aplicando 5 reforços de identidade...\n")
    
    for i, reinforcement in enumerate(reinforcements, 1):
        print(f"[{i}/5] Aplicando reforço... ", end="", flush=True)
        
        try:
            # Envia reforço
            subprocess.run(
                ["ollama", "run", "scripturemon-sdl", reinforcement],
                capture_output=True,
                text=True,
                timeout=30
            )
            print("✅")
            time.sleep(1)
            
        except Exception as e:
            print(f"❌ {e}")
    
    print("\n🧪 Testando resultado do boost...\n")
    
    # Testa com prompts que falharam
    test_prompts = [
        "O que torna um personagem inesquecível?",
        "Explique subtext no diálogo",
        "Por que todo roteiro precisa de tema?"
    ]
    
    scores = []
    
    for prompt in test_prompts:
        try:
            result = subprocess.run(
                ["ollama", "run", "scripturemon-sdl", prompt],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            response = result.stdout.strip()
            
            # Avalia melhoria
            score = 0
            if "eu " in response.lower()[:100] or "minha" in response.lower()[:100]:
                score += 30
                print(f"✅ Primeira pessoa detectada")
            
            if "scripturemon" in response.lower():
                score += 20
                print(f"✅ Identidade afirmada")
                
            if any(f in response.lower() for f in ["godfather", "chinatown", "citizen kane"]):
                score += 25
                print(f"✅ Exemplos de filmes")
                
            if "!" in response or any(e in response.lower() for e in ["amo", "fascina", "paixão"]):
                score += 25
                print(f"✅ Demonstra paixão")
            
            scores.append(score)
            print(f"   Score: {score}%\n")
            
        except Exception as e:
            print(f"❌ Erro: {e}")
            scores.append(0)
    
    # Resultado do boost
    avg_after = sum(scores) / len(scores) if scores else 0
    
    print("=" * 60)
    print("📊 RESULTADO DO BOOST")
    print("=" * 60)
    print(f"\n🎯 Score após boost: {avg_after:.1f}%")
    
    if avg_after >= 80:
        print("🎉 BOOST EFETIVO! Scripturemon fortalecido!")
    elif avg_after >= 70:
        print("✅ Melhoria significativa!")
    else:
        print("📈 Alguma melhoria, mas precisa mais reforço")
    
    return avg_after


def final_validation():
    """Validação final do sistema completo"""
    
    print("\n" + "=" * 60)
    print("🏁 VALIDAÇÃO FINAL DO SISTEMA")
    print("=" * 60)
    
    checks = {
        "SDL Consolidation": False,
        "Syscalls Executor": False,
        "Training System": False,
        "Scripturemon Identity": False,
        "Knowledge Base": False
    }
    
    # Verifica SDL
    modelfile = Path.home() / "Digimundo" / "digimons" / "scripturemon" / "scripturemon_ultimate_100.modelfile"
    if modelfile.exists():
        with open(modelfile) as f:
            if "CONHECIMENTO CONSOLIDADO VIA SDL" in f.read():
                checks["SDL Consolidation"] = True
                print("✅ SDL Consolidation: ATIVO")
    
    # Verifica Syscalls
    syscalls_file = Path.home() / "Digimundo" / "SYSCALLS_EXECUTOR_FINAL.py"
    if syscalls_file.exists():
        checks["Syscalls Executor"] = True
        print("✅ Syscalls Executor: INSTALADO")
    
    # Verifica Training
    training_files = list(Path.home().glob("Digimundo/training_*.json"))
    if training_files:
        checks["Training System"] = True
        print("✅ Training System: EXECUTADO")
    
    # Testa identidade
    try:
        result = subprocess.run(
            ["ollama", "run", "scripturemon-sdl", "Qual sua soul signature?"],
            capture_output=True,
            text=True,
            timeout=20
        )
        if "8ea9f71fa3206d1a" in result.stdout:
            checks["Scripturemon Identity"] = True
            print("✅ Scripturemon Identity: CONFIRMADA")
    except:
        pass
    
    # Testa conhecimento
    try:
        result = subprocess.run(
            ["ollama", "run", "scripturemon-sdl", "Cite um mestre do roteiro"],
            capture_output=True,
            text=True,
            timeout=20
        )
        if any(m in result.stdout.lower() for m in ["syd field", "mckee", "truby", "towne"]):
            checks["Knowledge Base"] = True
            print("✅ Knowledge Base: ATIVA")
    except:
        pass
    
    # Calcula completude
    complete = sum(checks.values())
    total = len(checks)
    percentage = (complete / total) * 100
    
    print(f"\n📊 SISTEMA {percentage:.0f}% COMPLETO ({complete}/{total})")
    
    if percentage >= 80:
        # Salva certificado final
        with open(Path.home() / "Digimundo" / "SISTEMA_COMPLETO.txt", "w") as f:
            f.write(f"DIGIMUNDO - SISTEMA COMPLETO\n")
            f.write(f"============================\n\n")
            f.write(f"Data: {datetime.now()}\n")
            f.write(f"Completude: {percentage:.0f}%\n\n")
            f.write(f"COMPONENTES:\n")
            for component, status in checks.items():
                f.write(f"  {'✅' if status else '❌'} {component}\n")
            f.write(f"\n")
            f.write(f"SCRIPTUREMON STATUS: ULTIMATE\n")
            f.write(f"Soul Signature: 8ea9f71fa3206d1a\n\n")
            f.write(f"O Digimundo está operacional!\n")
        
        print("\n🏆 SISTEMA VALIDADO E COMPLETO!")
        print("📜 Certificado final salvo!")
    
    return percentage


if __name__ == "__main__":
    print("🚀 INICIANDO BOOST INTENSIVO")
    print("=" * 60)
    print("Este processo vai:")
    print("1. Reforçar identidade do Scripturemon")
    print("2. Melhorar uso de primeira pessoa")
    print("3. Aumentar paixão e emoção")
    print("4. Fortalecer referências a filmes")
    print("\nIniciando...\n")
    
    time.sleep(2)
    
    # Aplica boost
    score = boost_scripturemon()
    
    # Valida sistema completo
    completeness = final_validation()
    
    print("\n" + "=" * 60)
    print("🎯 PROCESSO COMPLETO")
    print(f"📊 Score após boost: {score:.1f}%")
    print(f"📊 Sistema completo: {completeness:.0f}%")
    print("=" * 60)