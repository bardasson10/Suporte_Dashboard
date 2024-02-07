from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from app import db

class Postos(db.Model):
    __tablename__ = "postos"
    
    id = db.Column(Integer, primary_key=True, autoincrement=True)
    ticket_number = db.Column(Integer)
    title = db.Column(String(255))
    updated_at = db.Column(DateTime)
    attend_expiration = db.Column(DateTime)
    is_revised = db.Column(Boolean)
    is_closed = db.Column(Boolean)
    billed = db.Column(Boolean)
    requestor_email = db.Column(String(255))
    solve_expiration = db.Column(DateTime)
    solved_in_time = db.Column(DateTime)
    created_by_way_of = db.Column(String(255))
    created_at = db.Column(DateTime)
    pause_sla_reason = db.Column(String(255))
    pause_sla_stopped = db.Column(Boolean)
    attend_sla = db.Column(Boolean)
    client_id = db.Column(Integer)
    desk_id = db.Column(Integer)
    last_answer_type = db.Column(String(255))
    responsible_id = db.Column(Integer)
    priority_id = db.Column(Integer)
    services_catalog_id = db.Column(Integer)
    stage_id = db.Column(Integer)
    status_id = db.Column(Integer)
    rating = db.Column(Integer)

class Entity(db.Model):
    __tablename__ = 'entity'

    id = db.Column(Integer, primary_key=True, autoincrement=True)
    banco_id = db.Column(Integer, ForeignKey('postos.id'))
    entity_name = db.Column(String(255))
    entity_description = db.Column(String(255))
    menu_item = db.Column(Boolean)

class Field(db.Model):
    __tablename__ = 'field'

    id = db.Column(Integer, primary_key=True, autoincrement=True)
    entity_id = db.Column(Integer, ForeignKey('entity.id'))
    field_id = db.Column(Integer)
    field_name = db.Column(String(255))
    field_type = db.Column(String(255))
    is_required = db.Column(Boolean)

class Option(db.Model):
    __tablename__ = 'option'

    id = db.Column(Integer, primary_key=True, autoincrement=True)
    field_id = db.Column(Integer, ForeignKey('field.id'))
    option_id = db.Column(Integer)
    option_name = db.Column(String(255))
    value = db.Column(String(255))
