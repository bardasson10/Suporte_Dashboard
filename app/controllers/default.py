from flask import render_template
from app import app
from flask_login import login_required

@app.route("/index/<user>")
@app.route("/", defaults={"user":None})
@login_required
def index(user):
    return render_template('index.html',user=user)

