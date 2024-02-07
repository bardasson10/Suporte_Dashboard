from flask import Flask, render_template, request, flash, redirect, url_for
from app.api.tickets import make_api_request
from flask_login import login_required
from app import app

@app.route('/pag-dashboard', methods=['GET', 'POST'])
@login_required
def index_dashboard():
    lista_de_postos_url = "https://api.tiflux.com/api/v1/tickets"
    params = {
        'limit': 200,
        'desk_id': 34189,
        'include_entity': 'true',
        'is_closed': 'true',
    }

    data_postos = make_api_request(lista_de_postos_url, params)
            
            
    print(data_postos)
    return render_template('dash_cadastro.html', api_data=data_postos)


    

