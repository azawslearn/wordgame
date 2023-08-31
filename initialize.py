from flask import Flask
from models import db
from populate import populate_db

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://ivansto:EmersonFitipaldi@172.174.76.187/words'

db.init_app(app)

with app.app_context():
    db.create_all()
    populate_db()