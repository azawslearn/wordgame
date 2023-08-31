from flask import Flask, render_template, request, jsonify, session
from models import db, Sentence
import random
from populate import populate_db

app = Flask(__name__)
app.secret_key = 'some_random_string_here'

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://ivansto:EmersonFitipaldi@172.174.76.187/words'
db.init_app(app)

with app.app_context():
    db.create_all()
    populate_db()

@app.route('/')
def index():
    if 'correct' not in session:
        session['correct'] = 0
    if 'incorrect' not in session:
        session['incorrect'] = 0
    return render_template('index.html')

@app.route('/get_sentence')
def get_sentence():
    all_sentences = Sentence.query.all()
    if len(all_sentences) == 0:
        session['correct'] = 0
        session['incorrect'] = 0
        return jsonify({'end': True, 'correct': session['correct'], 'incorrect': session['incorrect']})
    selected_sentence_record = random.choice(all_sentences)
    db.session.delete(selected_sentence_record)
    db.session.commit()
    selected_sentence = {
        'id': selected_sentence_record.id,
        'sentence': selected_sentence_record.sentence,
        'article': selected_sentence_record.article,
        'adj_ending': selected_sentence_record.adj_ending,
        'case': selected_sentence_record.case,
        'declension': selected_sentence_record.declension
    }
    formatted_sentence = selected_sentence['sentence'].replace('{}', '___')
    selected_sentence['sentence'] = formatted_sentence
    return jsonify(selected_sentence)

@app.route('/check_answer', methods=['POST'])
def check_answer():
    user_article = request.form['user_article']
    user_adj_ending = request.form['user_adj_ending']
    correct_article = request.form['correct_article']
    correct_adj_ending = request.form['correct_adj_ending']
    if user_article == correct_article and user_adj_ending == correct_adj_ending:
        session['correct'] += 1
    else:
        session['incorrect'] += 1
    return jsonify({'correct': session['correct'], 'incorrect': session['incorrect']})

if __name__ == '__main__':
    app.run(debug=True)
