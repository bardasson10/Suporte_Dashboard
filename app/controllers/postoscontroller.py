from flask import render_template
from flask_login import login_required
import requests
from app import app, db
from app.models.postos import Postos
from app.api.tickets import make_api_request

def get_option_name_by_value(options, target_value):
    for option in options:
        if option.get('value') == target_value:
            return option.get('name')
    return None

@app.route('/postos', methods=['GET', 'POST'])
@login_required
def postos():
    lista_de_postos_url = "https://api.tiflux.com/api/v1/tickets"
    params = {
        'limit': 1,
        'desk_id': 34189,
        'include_entity': 'true',
        'is_closed': 'true',
    }
    response = requests.get(lista_de_postos_url, params=params)
    response.encoding = 'utf-8'

    try:
        data_postos = response.json()
    except UnicodeDecodeError as e:
        print(f"Error decoding JSON: {e}")
        data_postos = {}

    # Extrair dados da resposta da API e salvar no banco
    for ticket in data_postos:
        posto = Postos(
            nome=ticket.get('title', '').split('"')[1].split('-')[0].strip(),
            cnpj=ticket.get('entities', [])[7].get('options', [])[0].get('value', ''),
            stid=ticket.get('entities', [])[6].get('options', [])[0].get('value', ''),
            bsid=ticket.get('entities', [])[8].get('options', [])[0].get('value', ''),
            ec=ticket.get('entities', [])[5].get('options', [])[0].get('value', ''),
            rede=ticket.get('entities', [])[9].get('options', [])[0].get('value', ''),
            fabricante=get_option_name_by_value(ticket.get('entities', [])[0].get('fields', [])[0].get('options', []), 'true'),
            serial_number=get_option_name_by_value(ticket.get('entities', [])[0].get('fields', [])[2].get('options', []), 'true'),
            modelo_automacao=get_option_name_by_value(ticket.get('entities', [])[0].get('fields', [])[1].get('options', []), 'true'),
            bandeira=get_option_name_by_value(ticket.get('entities', [])[11].get('fields', [])[0].get('options', []), 'true'),
            provider=get_option_name_by_value(ticket.get('entities', [])[10].get('fields', [])[0].get('options', []), 'true'),
            resultado_ativacao=get_option_name_by_value(ticket.get('entities', [])[0].get('fields', [])[0].get('options', []), 'true')
        )

        db.session.add(posto)

    db.session.commit()

    return render_template('postos.html', api_data=data_postos)
