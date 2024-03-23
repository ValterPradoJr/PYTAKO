from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func


class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class Aposta(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    aposta_json = db.Column(db.String(10000))
    data_confirmacao = db.Column(db.DateTime(timezone=True), default=func.now())

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    cpf = db.Column(db.String(150))
    nome_completo = db.Column(db.String(150))
    pagou_aposta = db.Column(db.Boolean)
    has_admin = db.Column(db.Boolean)
    data_inicioti = db.Column(db.Date)
    foto_perfil = db.Column(db.String(200))
    notes = db.relationship('Note')

class Time(db.Model):
    nome = db.Column(db.String(150), primary_key=True)
    img_url = db.Column(db.String(300))
