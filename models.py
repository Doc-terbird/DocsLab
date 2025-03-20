from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class AllowList(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    from_allowed_ending = db.Column(db.Boolean, nullable=True)
    role = db.Column(db.String(50), nullable=False, default='Admin')
    last_login = db.Column(db.DateTime, nullable=True)

class BlockList(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)

class AllowedEmailEndings(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email_ending = db.Column(db.String(120), unique=True, nullable=False)

# TODO: Add more models as needed