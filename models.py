from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Sentence(db.Model):
    __tablename__ = 'sentences'
    id = db.Column(db.Integer, primary_key=True)
    sentence = db.Column(db.String(500))
    article = db.Column(db.String(10))
    adj_ending = db.Column(db.String(10))
    case = db.Column(db.String(50))
    declension = db.Column(db.String(50))