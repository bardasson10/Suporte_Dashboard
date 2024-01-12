from app import app
import os
from dotenv import load_dotenv
load_dotenv()
DEBUG = True

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True  # Desativa o rastreamento de modificações