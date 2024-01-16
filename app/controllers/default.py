from flask import Flask, render_template, request
from app.api.tickets import make_api_request  # Import your existing function
from app import app
import plotly.express as px
import pandas as pd


@app.route("/", methods=['GET', 'POST'])
def index():
    ticketNumber = None

    if request.method == 'POST':
        start_date = request.form.get('start_date')
        end_date = request.form.get('end_date')
        api_url = "https://api.tiflux.com/api/v1/tickets"
        params = {
            'limit': 200,
            'start_date': start_date,
            'end_date': end_date,
            'is_closed': 'true',
        }
        api_data = make_api_request(api_url, params)

        if api_data:
            ticketNumber = api_data[0].get('ticket_number')

        # Crie um gráfico de barras com Plotly
        fig = create_bar_chart(api_data)

        # Converter o gráfico Plotly para HTML como uma string
        plot_html = fig.to_html(full_html=False)

        return render_template('index.html', api_data=api_data, ticketNumber=ticketNumber, plot=plot_html)
    else:
        api_data = make_api_request("https://api.tiflux.com/api/v1/tickets", {'limit': 200, 'is_closed': 'true'})

        if api_data:
            ticketNumber = api_data[0].get('ticket_number')

        # Crie um gráfico de barras com Plotly
        fig = create_bar_chart(api_data)

        # Converter o gráfico Plotly para HTML como uma string
        plot_html = fig.to_html(full_html=False)

        return render_template('index.html', api_data=api_data, ticketNumber=ticketNumber, plot=plot_html)

def create_bar_chart(api_data):
    df = pd.DataFrame(api_data)
    df['created_at'] = pd.to_datetime(df['created_at'])
    df['date'] = df['created_at'].dt.date

    data_counts = df['date'].value_counts().reset_index()
    data_counts.columns = ['date', 'count']
    data_counts = data_counts.sort_values(by='date')

    fig = px.bar(data_counts, x='date', y='count', title='Tickets por Dia',
                 labels={'count': 'Número de Tickets', 'date': 'Data'},
                 template='plotly')

    # Adicionar rótulos nas barras
    fig.update_traces(texttemplate='%{y}', textposition='outside')

    # Mostrar todos os dias definidos
    fig.update_xaxes(type='category')

    # Ajustes de layout para evitar corte
    fig.update_layout(margin=dict(t=0, b=0, l=0, r=0))

    return fig


