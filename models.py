from flask import Flask

import os
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager, UserMixin, login_manager
from werkzeug.security import generate_password_hash, check_password_hash

app=Flask(__name__)

app.config['SECRET_KEY']='mysecret'
# SQLDATABASE SECTION
basedir=os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///'+os.path.join(basedir,'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False

db=SQLAlchemy(app)
Migrate(app,db)

###########login configurations######################

login_manager=LoginManager()
login_manager.init_app(app)
login_manager.login_view= 'login'


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)



class User(db.Model,UserMixin):
     __tablename__ = 'users'
     id = db.Column(db.Integer,primary_key=True)

     username = db.Column(db.String(64),unique=True,index=True)
     password_hash = db.Column(db.String(128))

     categorys = db.relationship('Entry',backref='owner',lazy=True)

     def __init__(self,email,username,password):
        self.email = email
        self.username = username
        self.password_hash = generate_password_hash(password)

     def check_password(self,password):
        return check_password_hash(self.password_hash,password)

     def __repr__(self):
        return f"Username {self.username}"

class Entry(db.Model):

    users = db.relationship(User)

    id = db.Column(db.Integer,primary_key=True)
    user_id = db.Column(db.Integer,db.ForeignKey('users.id'),nullable=False)
    category=db.Column(db.String(140),nullable=False)
    site_name = db.Column(db.String(140), nullable=False)
    s_uname= db.Column(db.String(140), nullable=False)
    s_pwd=db.Column(db.String(140),nullable=False)

    def __init__(self,category,site_name,s_uname,s_pwd,user_id):
        self.category=category
        self.site_name=site_name
        self.s_uname=s_uname
        self.s_pwd=s_pwd
        self.user_id = user_id

    def __repr__(self):
        return f"Entry ID: {self.id} -- Category {self.category}--- {self.site_name} --- {self.s_uname}-----{self.s_pwd}"


