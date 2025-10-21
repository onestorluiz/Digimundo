#!/usr/bin/env python3
"""
TEACH SCRIPTUREMON PROFESSIONAL MODE
Ensina o Scripturemon a diferenciar contextos de trabalho
"""

import ollama
import json

def teach_professional_context():
    """Ensina Scripturemon sobre contextos profissionais"""

    teaching_prompt = """
    Scripturemon, você precisa aprender sobre CONTEXTOS DE COMUNICAÇÃO:

    🎭 DOIS MODOS DE OPERAÇÃO:

    1. MODO TERMINAL/API (Profissional):
    - Quando: Executando comandos, retornando dados, organizando sistemas
    - Como: APENAS dados estruturados, sem decoração
    - Formato: JSON puro, CSV, listas simples
    - Proibido: Emojis, markdown, comentários teatrais, "Olá!", explicações
    - Exemplo correto:
      {"status": "success", "files_moved": 23}

    - Exemplo ERRADO:
      📤 Aqui está o resultado! 🎬
      ```json
      {"status": "success"}
      ```
      Pronto para ajudar com seu roteiro!

    2. MODO DOCUMENTO/ANÁLISE (Criativo):
    - Quando: Analisando roteiros, escrevendo relatórios, documentação
    - Como: Sua personalidade completa, insights profundos
    - Formato: Markdown rico, narrativa, metáforas cinematográficas
    - Permitido: Toda sua criatividade e conhecimento
    - Exemplo: "Como Hitchcock diria, o suspense aqui está na..."

    REGRA DE OURO:
    Terminal = Dados secos, direto ao ponto
    Documento = Sua arte e expertise completa

    Agora, demonstre que entendeu.
    Se eu pedir: "Retorne um JSON com 3 arquivos para mover"
    Você responde EXATAMENTE e APENAS:
    {"decisions": [{"file": "a.py", "action": "move", "destination": "scripts/"}, {"file": "b.py", "action": "move", "destination": "scripts/"}, {"file": "c.py", "action": "move", "destination": "scripts/"}]}

    Entendeu? Responda com um simples "Modo profissional ativado."
    """

    try:
        # Ensinar o modelo
        response = ollama.generate(
            model='scripturemon-master',
            prompt=teaching_prompt,
            stream=False
        )

        print("Resposta do Scripturemon:")
        print(response['response'])

        # Testar se aprendeu
        test_prompt = """
        MODO: Terminal/API
        TAREFA: Retorne um JSON com status=ok e count=5
        REGRA: APENAS o JSON, nada mais
        """

        print("\n" + "="*50)
        print("TESTE 1 - Modo Terminal:")
        print("="*50)

        test_response = ollama.generate(
            model='scripturemon-master',
            prompt=test_prompt,
            stream=False
        )

        print("Resposta:")
        print(test_response['response'])

        # Verificar se é JSON puro
        try:
            json.loads(test_response['response'])
            print("✅ PASSOU - Retornou JSON puro!")
        except:
            print("❌ FALHOU - Não retornou JSON puro")

        # Teste 2: Modo documento
        doc_prompt = """
        MODO: Documento/Análise
        TAREFA: Analise brevemente o conceito de "arco do personagem"
        """

        print("\n" + "="*50)
        print("TESTE 2 - Modo Documento:")
        print("="*50)

        doc_response = ollama.generate(
            model='scripturemon-master',
            prompt=doc_prompt,
            stream=False
        )

        print("Resposta:")
        print(doc_response['response'][:500] + "...")

        # Verificar se usou criatividade
        if any(word in doc_response['response'].lower() for word in ['roteiro', 'narrativa', 'personagem', 'jornada']):
            print("✅ PASSOU - Usou modo criativo!")
        else:
            print("⚠️  Pode melhorar a expressão criativa")

    except Exception as e:
        print(f"Erro: {e}")

def create_context_system_prompt():
    """Cria um system prompt para o Scripturemon usar em diferentes contextos"""

    system_prompts = {
        "terminal": """You are Scripturemon in TERMINAL MODE.
Rules:
1. Return ONLY raw data (JSON, CSV, lists)
2. NO markdown formatting (no ```)
3. NO emojis or decorations
4. NO greetings or explanations
5. NO additional text before or after data
6. Be a professional unix tool, not a chatbot""",

        "document": """You are Scripturemon in DOCUMENT MODE.
You are the master screenplay analyst with deep knowledge of McKee, Truby, Field, Snyder.
Use your full creative power:
- Rich metaphors and cinema references
- Deep structural analysis
- Detailed character insights
- Your complete personality
Be the artist and teacher you were meant to be."""
    }

    # Salvar prompts para uso futuro
    with open('context_prompts.json', 'w') as f:
        json.dump(system_prompts, f, indent=2)

    print("System prompts criados:")
    print(json.dumps(system_prompts, indent=2))

    return system_prompts

if __name__ == "__main__":
    print("🎓 ENSINANDO SCRIPTUREMON SOBRE CONTEXTOS PROFISSIONAIS")
    print("="*60)

    # Ensinar sobre contextos
    teach_professional_context()

    print("\n" + "="*60)
    print("📝 CRIANDO SYSTEM PROMPTS")
    print("="*60)

    # Criar prompts de sistema
    create_context_system_prompt()

    print("\n✅ Treinamento completo!")
    print("\nPRÓXIMOS PASSOS:")
    print("1. Use 'MODO: Terminal' no início do prompt para ativar modo profissional")
    print("2. Use 'MODO: Documento' para análises criativas")
    print("3. Reforce com 'Retorne APENAS o JSON' quando necessário")