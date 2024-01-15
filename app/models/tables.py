from app import db,login_manager,bcrypt
from flask_login import UserMixin


@login_manager.user_loader
def get_user (user_id):
    return User.query.filter_by(id =user_id).first()

class User(db.Model, UserMixin):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True)
    password = db.Column(db.String)
    name = db.Column(db.String)

    def __init__(self, username, password, name):
        self.username = username
        self.password = self._generate_password_hash(password)
        self.name = name

    def _generate_password_hash(self, password):
        # Gera um salt usando bcrypt.gensalt()
        salt = bcrypt.gensalt()
        if not salt:
            raise ValueError("Failed to generate salt")

        # Verifica se a senha fornecida é igual à senha de confirmação
        if password != self.confirm_password:
            raise ValueError("Passwords do not match")

        # Faz o hash da senha com o salt gerado
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        
        if not hashed_password:
            raise ValueError("Failed to generate hashed password")

        return hashed_password
    def verify_password(self, pwd):
        # Verifica se a senha fornecida coincide com a senha armazenada
        return bcrypt.check_password_hash(self.password, pwd)
    def __repr__(self):
        return "<User %r>"% self.username