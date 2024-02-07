from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_bcrypt import Bcrypt



app = Flask(__name__)
app.config.from_object('config')
app.config['SECRET_KEY'] = 'secret'

login_manager = LoginManager(app)
login_manager.login_view = 'login'


db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
migrate = Migrate(app, db)



from app.controllers import default
from app.controllers import logincontroller
from app.controllers import apontamentocontroller
from app.controllers import postoscontroller