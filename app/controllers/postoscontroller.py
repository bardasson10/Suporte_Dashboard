from flask import Flask, render_template, request, flash, redirect, url_for
from app.api.tickets import make_api_request
from flask_login import login_required
from app import app, db
from app.models.postos import Postos, Entity, Field, Option  # Importe seus modelos aqui

@app.route('/postos', methods=['GET', 'POST'])
@login_required
def postos():
    if request.method == 'POST':
        try:
            synchronize_data()  # Chame a função de sincronização quando o formulário for enviado
            flash('Dados sincronizados com sucesso.', 'success')
        except Exception as e:
            flash(f'Erro ao sincronizar dados: {str(e)}', 'error')

    lista_de_postos_url = "https://api.tiflux.com/api/v1/tickets"
    params = {
        'limit': 1,
        'desk_id': 34189,
        'include_entity': 'true',
        'is_closed': 'true',
    }

    data_postos = make_api_request(lista_de_postos_url, params)

    print(data_postos)
    return render_template('postos.html', api_data=data_postos)


def synchronize_data():
    # Obtenha dados da API
    lista_de_postos_url = "https://api.tiflux.com/api/v1/tickets"
    params = {
        'limit': 1,
        'desk_id': 34189,
        'include_entity': 'true',
        'is_closed': 'true',
    }
    api_data = make_api_request(lista_de_postos_url, params)

    # Salve dados no banco de dados
    for post_data in api_data:
        try:
            # Salve dados de Postos
            post = Postos(
                ticket_number=post_data.get('ticket_number'),
                title=post_data.get('title'),
                updated_at=post_data.get('updated_at'),
                attend_expiration=post_data.get('attend_expiration'),
                is_revised=post_data.get('is_revised'),
                is_closed=post_data.get('is_closed'),
                billed=post_data.get('billed'),
                requestor_email=post_data.get('requestor_email'),
                solve_expiration=post_data.get('solve_expiration'),
                solved_in_time=post_data.get('solved_in_time'),
                created_by_way_of=post_data.get('created_by_way_of'),
                created_at=post_data.get('created_at'),
                pause_sla_reason=post_data.get('pause_sla_reason'),
                pause_sla_stopped=post_data.get('pause_sla_stopped'),
                attend_sla=post_data.get('attend_sla'),
                client_id=post_data.get('client_id'),
                desk_id=post_data.get('desk_id'),
                last_answer_type=post_data.get('last_answer_type'),
                responsible_id=post_data.get('responsible_id'),
                priority_id=post_data.get('priority_id'),
                services_catalog_id=post_data.get('services_catalog_id'),
                stage_id=post_data.get('stage').get('id') if post_data.get('stage') else None,
                status_id=post_data.get('status').get('id') if post_data.get('status') else None,
                rating=post_data.get('rating'),
            )
            db.session.add(post)
            db.session.commit()  # Commit para garantir que o ID seja gerado

            # Obtenha e salve dados de Entity associados
            entity_data_list = post_data.get('entities')
            if entity_data_list:
                for entity_data in entity_data_list:
                    entity = Entity(
                        banco_id=post.id,  # Use o ID recém-gerado de Postos como chave estrangeira
                        entity_name=entity_data.get('entity_name'),
                        entity_description=entity_data.get('entity_description'),
                        menu_item=entity_data.get('menu_item')
                    )
                    db.session.add(entity)
                    db.session.commit()

                    # Obtenha e salve dados de Field associados
                    field_data_list = entity_data.get('fields')
                    if field_data_list:
                        for field_data in field_data_list:
                            field = Field(
                                entity_id=entity.id,  # Use o ID recém-gerado de Entity como chave estrangeira
                                field_id=field_data.get('field_id'),
                                field_name=field_data.get('field_name'),
                                field_type=field_data.get('field_type'),
                                is_required=field_data.get('is_required')
                            )
                            db.session.add(field)
                            db.session.commit()

                            # Obtenha e salve dados de Option associados
                            option_data_list = field_data.get('options')
                            if option_data_list:
                                for option_data in option_data_list:
                                    if option_data.get('value') == 'true':
                                        option_name = option_data.get('option_name') or option_data.get('value')
                                        option = Option(
                                            field_id=field.id,  # Use o ID recém-gerado de Field como chave estrangeira
                                            option_id=option_data.get('option_id'),
                                            option_name=option_name,
                                            value=option_data.get('value')
                                        )
                                        db.session.add(option)
                                        db.session.commit()
        except Exception as e:
            db.session.rollback()  # Desfaça qualquer alteração em caso de erro
            raise e  # Propague a exceção para sinalizar o erro
