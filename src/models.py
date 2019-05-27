
from sqlalchemy.sql import expression, func
from src import db
from sqlalchemy import Column, Integer, DateTime
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin
from src import login_manager

class User(UserMixin,db.Model):
  # __tablename__ = 'user'
  id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  email = db.Column(db.String(120), index=True, unique=True)
  firstname= db.Column(db.String(120))
  lastname= db.Column(db.String(120))
  storename= db.Column(db.String(120))
  upgraded= db.Column(db.Boolean, server_default=expression.false())
  password_hash= db.Column(db.String(128), nullable=False)
  tests = db.relationship('Tests', backref='user', lazy=True)
  tokens = db.relationship('Token', backref='user', lazy=True)

  def set_password(self, password):
    self.password_hash = generate_password_hash(password)

  def check_password(self, password):
    return check_password_hash(self.password_hash, password)

  def __repr__(self):
    return f"email:{self.email}, password: {self.password_hash}, firstname: {self.firstname}, upgraded: {self.upgraded}"

class Tests(db.Model):
  # __tablename__='tests'
  id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  user_id= db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
  product_page = db.Column(db.Boolean, server_default=expression.false())
  add_to_cart = db.Column(db.Boolean, server_default=expression.false())
  go_to_checkout= db.Column(db.Boolean, server_default= expression.false())
  personal_info= db.Column(db.Boolean, server_default= expression.false())
  payment_info= db.Column(db.Boolean, server_default=expression.false())
  payment_button= db.Column(db.Boolean, server_default=expression.false())
  time_created = db.Column(DateTime(timezone=True), server_default=func.now())


  def __repr__(self):
    return f"ID: {self.id}, user_id:{self.user_id} product_page:{self.product_page}, add_to_cart: {self.add_to_cart}, go_to_checkout: {self.go_to_checkout},personal_info: {self.personal_info}, payment_info: {self.payment_info}, payment_button: {self.payment_button}, created_at: {self.time_created} \n"



@login_manager.user_loader
def load_user(id):
  return User.query.get(int(id))

class Token(db.Model):
  id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  uuid = db.Column(db.String, unique=True)
  user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

