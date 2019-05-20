from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os
from flask_login import LoginManager
from flask_cors import CORS

app= Flask(__name__)
CORS(app)
login_manager = LoginManager()
login_manager.init_app(app)
app.config['SECRET_KEY']= "shh"
#WHERE DB IS LOCATED
app.config['SQLALCHEMY_DATABASE_URI']='postgresql://postgres:something123@localhost/shophealthcheck'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


# POSTGRES = {
#     'user': 'postgres',
#     'pw': 'something123',
#     'db': 'shophealthcheck',
#     'host': 'localhost',
#     'port': '5432',
# }

# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://%(user)s:%(pw)s@%(host)s:\
# %(port)s/%(db)s' % POSTGRES
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


# convention = {
#     "ix": 'ix_%(column_0_label)s',
#     "uq": "uq_%(table_name)s_%(column_0_name)s",
#     "ck": "ck_%(table_name)s_%(constraint_name)s",
#     "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
#     "pk": "pk_%(table_name)s"
# }
# metadata = MetaData(naming_convention=convention)
db=SQLAlchemy(app)
Migrate(app,db)