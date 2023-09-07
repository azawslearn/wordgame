from flask import current_app
from models import db, Sentence

def populate_db():
    # Check if the database is already populated
    if Sentence.query.first():
        print("Database already populated. Skipping.")
        return

    try:
        print("Populating DB: Starting")

        data = [
            {'sentence': '{} gut{} Mann hilft seinen Nachbarn.', 'article': 'Der', 'adj_ending': 'e', 'case': 'Nominative', 'declension': 'Weak'},
            {'sentence': '{} gut{} Frau liest ein interessantes Buch.', 'article': 'Die', 'adj_ending': 'e', 'case': 'Nominative', 'declension': 'Weak'}
        ]

        print(f"Data to populate: {data}")

        for record in data:
            entry = Sentence(**record)
            print(f"Adding entry: {entry}")
            db.session.add(entry)

        print("Committing to database")
        db.session.commit()
        print("Database populated successfully")

    except Exception as e:
        print("An error occurred:", e)
        db.session.rollback()
