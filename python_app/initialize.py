
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_pyfile('config.py')
db = SQLAlchemy(app)

def create_app():
    from models import Sentence
    with app.app_context():
        # Check if the 'sentences' table already exists
        if db.engine.has_table('sentences'):
            # Drop it if you want to override
            Sentence.__table__.drop(db.engine)
        # Create the table
        db.create_all()
    return app
