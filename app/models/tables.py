from app import db,login_manager,bcrypt
from flask_login import UserMixin


@login_manager.user_loader
def get_user (user_id):
    return User.query.filter_by(id =user_id).first()

class User(db.Model, UserMixin):
    __tablename__ = "users"

    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String,unique=True)
    password = db.Column(db.String)
    name = db.Column(db.String)

    def __init__(self,username,password,name) :
        self.username = username
        self.password= bcrypt.generate_password_hash(password).decode('utf-8')
        self.name = name

    def verify_password(self,pwd) :
       return bcrypt.check_password_hash(self.password, pwd)
        
    def __repr__(self):
        return "<User %r>"% self.username