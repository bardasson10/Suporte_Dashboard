from flask import Flask,jsonify

app = Flask(__name__, template_folder='../templates')

from app.routes.routes import *


