from flask import render_template
from app import app
#from app import db
#from sqlalchemy import text
@app.route("/index/<user>")
@app.route("/", defaults={"user":None})
def index(user):
    return render_template('index.html',user=user)
    #try:
        # Tenta conectar ao banco de dados
       # db.session.execute(text('SELECT 1'))
       # return 'Conexão com o banco de dados bem-sucedida!'
   # except Exception as e:
       # return f'Erro ao conectar ao banco de dados: {str(e)}'
@app.route("/login")
def login ():
    return render_template('Login.html')