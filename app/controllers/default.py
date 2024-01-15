from flask import render_template, Response
from app import app
from flask_login import login_required
from app.api.tickets import make_api_request
from flask_paginate import Pagination, get_page_args
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from io import BytesIO
import base64

@app.route("/")
@login_required
def index():
    # URL da API e parâmetros da solicitação
    api_url = "https://api.tiflux.com/api/v1/tickets"
    params = {
        'limit': 200,
        'start_date': '2023-01-01',
        'end_date': '2023-12-03',
        'is_closed': 'true',
    }

    api_data = make_api_request(api_url, params)

    # Cria um DataFrame a partir dos dados da API
    df = pd.DataFrame(api_data)

    # Verifica se a coluna 'created_at' está presente
    if 'created_at' not in df.columns:
        return "Erro: A coluna 'created_at' não está presente nos dados da API."

    # Certifique-se de ajustar o nome da coluna 'created_at' de acordo com os dados reais
    df['created_at'] = pd.to_datetime(df['created_at'])

    # Configuração da paginação
    page, per_page, offset = get_page_args(page_parameter='page', per_page_parameter='per_page')
    total = len(df)

    data_for_current_page = df.iloc[offset: offset + per_page]

    pagination = Pagination(page=page, per_page=10, total=total, css_framework='bootstrap4')


    # Ajusta o tamanho da figura proporcionalmente ao tamanho da tela
    fig, ax = plt.subplots(figsize=(13, 7))
    fig.autofmt_xdate()

    # Cria o gráfico de barras com o total geral de tickets por dia
    tickets_per_day_all = df['created_at'].dt.date.value_counts().sort_index()
    ax.bar(tickets_per_day_all.index.astype(str), tickets_per_day_all.values, label='Total Geral')

    ax.set_xlabel('Data de Criação')
    ax.set_ylabel('Número de Tickets')
    ax.set_title(f'Número de Tickets Criados por Dia entre 2024-01-01 e 2024-01-15')
    ax.legend()

    # Adiciona rótulos nas barras
    for i, value in enumerate(tickets_per_day_all.values):
        ax.text(i, value + 0.1, str(value), ha='center', va='bottom')

    # Salva o gráfico em uma imagem BytesIO
    img_buf = BytesIO()
    plt.savefig(img_buf, format='png')
    img_buf.seek(0)

    # Converta a imagem para base64
    img_base64 = base64.b64encode(img_buf.read()).decode('utf-8')

    # Limpa a figura para evitar problemas
    plt.close()

    # Adicione os dados da API e da paginação ao contexto do template
    # ...

# Adicione os dados da API e da paginação ao contexto do template
    return render_template('index.html', tickets=data_for_current_page.to_dict(orient='records'), img_base64=img_base64, pagination=pagination)





