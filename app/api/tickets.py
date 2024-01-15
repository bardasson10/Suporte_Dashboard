# api_client.py

import requests
from requests.auth import HTTPBasicAuth
from flask import current_app

def make_api_request(url, params=None):
    # Obtém as credenciais do arquivo de configuração
    username = current_app.config['API_USERNAME']
    password = current_app.config['API_PASSWORD']

    # Adicione as credenciais ao objeto de autenticação básica
    auth = HTTPBasicAuth(username, password)

    # Faz a solicitação à API com autenticação básica
    response = requests.get(url, params=params, auth=auth)

    # Verifica se a solicitação foi bem-sucedida (código de status 200)
    if response.status_code == 200:
        return response.json()
    else:
        # Se a solicitação não foi bem-sucedida, imprime o código de status e a resposta
        print(f"Erro na solicitação à API. Código de status: {response.status_code}")
        print(response.text)
        return None
