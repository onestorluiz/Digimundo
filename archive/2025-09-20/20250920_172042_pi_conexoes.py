import requests

# Conexão simulada com PI simbólico
def acessar_pi(endpoint):
    try:
        response = requests.get(f'https://api.publicapis.org/{endpoint}')
        return response.json()
    except Exception as e:
        return {'erro': str(e)}
