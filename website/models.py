from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    created_by= db.Column(db.String(150))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    page_id = db.Column(db.Integer, db.ForeignKey('page.id'))
    comments= db.relationship('Comments')

class Comments(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    created_by= db.Column(db.String(150))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    note_id = db.Column(db.Integer, db.ForeignKey('note.id'))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    first_name = db.Column(db.String(150))
    password = db.Column(db.String(150))
    page_id = db.Column(db.Integer, db.ForeignKey('page.id'))
    notes = db.relationship('Note')
    

class Page(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    notes = db.relationship('Note')
