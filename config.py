from app import app
import os
from dotenv import load_dotenv
load_dotenv()
DEBUG = True

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True  # Desativa o rastreamento de modificações
# config.py

API_USERNAME = "wellington.ramos@eztech.ind.br"
API_PASSWORD = "17cd4fbc36cf0729a77a4a413dc31ae7"