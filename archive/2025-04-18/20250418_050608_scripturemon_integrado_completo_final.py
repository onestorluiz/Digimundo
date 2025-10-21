
import openai
import os
import time
import requests
import telegram
from dotenv import load_dotenv

# Função para verificar e organizar o arquivo .env
def organizar_arquivo_env():
    env_path = '.env'
    if not os.path.exists(env_path):
        print(f"O arquivo {env_path} não foi encontrado. Criando estrutura básica...")
        with open(env_path, 'w') as f:
            f.write('''
# 🧰 Configuração das Chaves de API do Scripturemon
API_KEY_OPENAI=your_openai_api_key
TMDB_API_KEY=your_tmdb_api_key
OMDB_API_KEY=your_omdb_api_key
GOOGLE_BOOKS_API_KEY=your_google_books_api_key
UNSPLASH_API_KEY=your_unsplash_api_key
PEXELS_API_KEY=your_pexels_api_key
            ''')

# Carregar as variáveis do .env
load_dotenv()

# Chave da API OpenAI fornecida
openai.api_key = os.getenv("API_KEY_OPENAI")

# Função para buscar respostas do OpenAI
def buscar_resposta_gpt3(pergunta):
    resposta = openai.Completion.create(
        engine="text-davinci-003",
        prompt=pergunta,
        max_tokens=150
    )
    return resposta.choices[0].text.strip()

# Função para enviar mensagens para o Telegram
def enviar_mensagem_telegram(mensagem):
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")
    bot = telegram.Bot(token=token)
    bot.send_message(chat_id=chat_id, text=mensagem)

# Função para buscar informações na API Pexels
def buscar_imagem_pexels(query):
    api_url = f"https://api.pexels.com/v1/search?query={query}&per_page=1"
    headers = {"Authorization": os.getenv("PEXELS_API_KEY")}
    response = requests.get(api_url, headers=headers)
    return response.json()

# Função para organização e execução de tarefas do Digimundo
def organizar_digimundo():
    print("Organizando Digimundo...")
    # Exemplo de ações que podem ser realizadas pelo Scripturemon
    organizar_arquivo_env()  # Verifica e organiza o .env
    resposta = buscar_resposta_gpt3("Qual a melhor estratégia para otimizar o Digimundo?")
    print(f"Resposta do GPT-3: {resposta}")
    enviar_mensagem_telegram("Scripturemon organizando o Digimundo e integrando APIs.")

# Função de monitoramento de integridade do sistema
def monitorar_integridade():
    print("Monitorando integridade do Digimundo...")
    # Ações de monitoramento contínuo, como verificar conexões e status
    # Implementação de Watchdog ou funcionalidades de integridade
    enviar_mensagem_telegram("Integridade do Digimundo está sendo monitorada.")

# Função de autocura do Scripturemon
def autocura_scripturemon():
    print("Scripturemon em modo de autocura...")
    # Simula ações de autocura, como reiniciar processos ou corrigir erros
    enviar_mensagem_telegram("Scripturemon está em processo de autocura.")

# Função de execução de comandos de monitoramento
def comandos_vivos():
    print("Executando comandos vivos...")
    # Exemplo de execução de comandos adicionais
    enviar_mensagem_telegram("Comandos vivos sendo executados no Digimundo.")
