from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, JSON
from app import db

class Postos(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(255))
    cnpj = db.Column(db.String(20))
    stid = db.Column(db.String(50))
    bsid = db.Column(db.String(50))
    ec = db.Column(db.String(50))
    rede = db.Column(db.String(255))
    fabricante = db.Column(db.String(50))
    serial_number = db.Column(db.String(50))
    modelo_automacao = db.Column(db.String(50))
    bandeira = db.Column(db.String(50))
    provider = db.Column(db.String(50))
    resultado_ativacao = db.Column(db.String(50))
