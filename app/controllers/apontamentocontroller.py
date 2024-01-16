from flask import render_template
from app.api.tickets import make_api_request
from app import app

@app.route('/apontamentos/<int:ticketNumber>')
def apontamentos(ticketNumber):
    try:
        # Constrói a URL da API com o número do ticket
        url = f'https://api.tiflux.com/api/v1/tickets/{ticketNumber}/appointments?limit=20'

        # Realiza a chamada à API usando a função make_api_request
        data = make_api_request(url)

        if data:
            # Ordena os apontamentos do mais antigo para o mais recente
            data.sort(key=lambda x: x.get('created_at', ''))

            # Renderiza a página de visualização com os dados da API ordenados
            return render_template('apontamentos.html', data=data)
        else:
            # Lida com erros de chamada à API
            return render_template('apontamentos.html', error="Erro na chamada à API")
    except Exception as e:
        # Lida com exceções
        return render_template('apontamentos.html', error=str(e))
