from app import app
from flask import render_template
from app.controllers.test_controller import test_controller

@app.route('/')
def index():

    resposta, status_code = test_controller()
    dados = resposta.json
    print(f'Message: {dados["nome"]}')
    print(f'Code: {status_code}')



    return render_template('index.html',dados = dados)