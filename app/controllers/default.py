from flask import Flask, render_template, request,flash,redirect,url_for
from app.api.tickets import make_api_request
from flask_login import login_required  # Import your existing function
from app import app
from datetime import datetime
import plotly.express as px
import pandas as pd

def calculate_duration(created_at, updated_at):
    formats = [
        '%Y-%m-%dT%H:%M:%S.%fZ',
        '%Y-%m-%dT%H:%M:%S.%f',
        '%Y-%m-%d %H:%M:%S',
        # Adicione mais formatos conforme necessário
    ]

    for format_str in formats:
        try:
            created_datetime = datetime.strptime(created_at, format_str)
            updated_datetime = datetime.strptime(updated_at, format_str)
            duration = updated_datetime - created_datetime
            return str(duration)
        except ValueError:
            pass

    # Se nenhum formato corresponder, retorna uma mensagem de erro
    return "Formato de data desconhecido"

@app.route("/", methods=['GET', 'POST'])
@login_required
def index():
    ticketNumber = None
    is_closed_option = 'true'

    try:
        if request.method == 'POST':
            start_date = request.form.get('start_date')
            end_date = request.form.get('end_date')
            is_closed_option = request.form.get('is_closed_option', 'true')

            api_url = "https://api.tiflux.com/api/v1/tickets"
            params = {
                'limit': 200,
                'start_date': start_date,
                'end_date': end_date,
                'is_closed': is_closed_option,
            }

            api_data = make_api_request(api_url, params)

            if api_data:
                ticketNumber = api_data[0].get('ticket_number')

            # Crie um gráfico de barras com Plotly
            fig = create_bar_chart(api_data)

            # Crie um gráfico de barras por atendente no intervalo de datas
            fig_responsible_on_date = create_bar_chart_by_responsible_on_date(api_data)

            # Converter os gráficos Plotly para HTML como strings
            plot_html = fig.to_html(full_html=False)
            plot_responsible_on_date_html = fig_responsible_on_date.to_html(full_html=False)

            return render_template('index.html', api_data=api_data, ticketNumber=ticketNumber, plot=plot_html, plot_responsible_on_date=plot_responsible_on_date_html, calculate_duration=calculate_duration)
        else:
           
            api_data = make_api_request("https://api.tiflux.com/api/v1/tickets", {'limit': 200, 'is_closed': is_closed_option})

            if api_data:
                ticketNumber = api_data[0].get('ticket_number')

            # Crie um gráfico de barras com Plotly
            fig = create_bar_chart(api_data)
            fig_responsible_on_date = create_bar_chart_by_responsible_on_date(api_data)

            # Converter os gráficos Plotly para HTML como strings
            plot_html = fig.to_html(full_html=False)
            plot_responsible_on_date_html = fig_responsible_on_date.to_html(full_html=False)
            return render_template('index.html', api_data=api_data, ticketNumber=ticketNumber, plot=plot_html,plot_responsible_on_date=plot_responsible_on_date_html ,calculate_duration=calculate_duration)
    except KeyError as e:
        flash(f"Não existe registro para a data fornecida.")
        return redirect(url_for('index'))



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

def create_bar_chart_by_responsible_on_date(api_data):
    df = pd.DataFrame(api_data)
    # Contar o número de tickets por responsável
    responsible_counts = df['responsible'].apply(lambda x: x['name'] if pd.notnull(x) else 'Unassigned').value_counts().reset_index()
    responsible_counts.columns = ['responsible', 'count']
    responsible_counts = responsible_counts.sort_values(by='responsible')

    # Criar o gráfico de barras
    fig = px.bar(responsible_counts, x='responsible', y='count', title='Tickets por Responsável',
                  labels={'count': 'Número de Tickets', 'responsible': 'Responsável'},
                  template='plotly')

    # Adicionar rótulos nas barras
    fig.update_traces(texttemplate='%{y}', textposition='outside')

    # Ajustes de layout para evitar corte
    fig.update_layout(margin=dict(t=0, b=0, l=0, r=0))

    return fig



