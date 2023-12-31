from flask import Flask, render_template, request, jsonify, session
import random

application = Flask(__name__)
application.secret_key = 'some_random_string_here'

sentences = [
    #weak
    {'sentence': '{} gut{} Mann hilft seinen Nachbarn.', 'article': 'Der', 'adj_ending': 'e', 'case': 'Nominative', 'declension': 'Weak'},
    {'sentence': '{} gut{} Frau liest ein interessantes Buch.', 'article': 'Die', 'adj_ending': 'e', 'case': 'Nominative', 'declension': 'Weak'},
    {'sentence': '{} gut{} Kind spielt im Garten.', 'article': 'Das', 'adj_ending': 'e', 'case': 'Nominative', 'declension': 'Weak'},
    {'sentence': '{} klug{} gut{} Männer haben das Problem gelöst.', 'article': 'Die', 'adj_ending': 'en', 'case': 'Nominative', 'declension': 'Weak'},
    {'sentence': '{} freundlich{} gut{} Frauen helfen gerne in der Gemeinschaft.', 'article': 'Die', 'adj_ending': 'en', 'case': 'Nominative', 'declension': 'Weak'},
    {'sentence': '{} aufgeweckt{} gut{} Kinder stellen viele Fragen.', 'article': 'Die', 'adj_ending': 'en', 'case': 'Nominative', 'declension': 'Weak'},
    {'sentence': '{} klug{} gut{} Mann habe ich gestern getroffen.', 'article': 'Den', 'adj_ending': 'en', 'case': 'Accusative', 'declension': 'Weak'},
    {'sentence': '{} freundlich{} gut{} Frau kenne ich schon lange.', 'article': 'Die', 'adj_ending': 'e', 'case': 'Accusative', 'declension': 'Weak'},
    {'sentence': '{} aufgeweckt{} gut{} Kind hat einen Preis gewonnen.', 'article': 'Das', 'adj_ending': 'e', 'case': 'Accusative', 'declension': 'Weak'},
    {'sentence': '{} klug{} gut{} Männer haben das Projekt erfolgreich abgeschlossen.', 'article': 'Die', 'adj_ending': 'en', 'case': 'Accusative', 'declension': 'Weak'},
    {'sentence': '{} freundlich{} gut{} Frauen unterstützen die Wohltätigkeitsorganisation.', 'article': 'Die', 'adj_ending': 'en', 'case': 'Accusative', 'declension': 'Weak'},
    {'sentence': '{} aufgeweckt{} gut{} Kinder besuchen den Zoo am Wochenende.', 'article': 'Die', 'adj_ending': 'en', 'case': 'Accusative', 'declension': 'Weak'},
    {'sentence': '{} klug{} gut{} Mann habe ich gestern geholfen.', 'article': 'Dem', 'adj_ending': 'en', 'case': 'Dative', 'declension': 'Weak'},
    {'sentence': '{} freundlich{} gut{} Frau habe ich das Buch geliehen.', 'article': 'Der', 'adj_ending': 'en', 'case': 'Dative', 'declension': 'Weak'},
    {'sentence': '{} aufgeweckt{} gut{} Kind habe ich eine Geschichte erzählt.', 'article': 'Dem', 'adj_ending': 'en', 'case': 'Dative', 'declension': 'Weak'},
    {'sentence': '{} klug{} gut{} Männern habe ich bei ihrer Arbeit geholfen.', 'article': 'Den', 'adj_ending': 'en', 'case': 'Dative', 'declension': 'Weak'},
    {'sentence': '{} freundlich{} gut{} Frauen habe ich bei der Organisation geholfen.', 'article': 'Den', 'adj_ending': 'en', 'case': 'Dative', 'declension': 'Weak'},
    {'sentence': '{} aufgeweckt{} gut{} Kindern habe ich Spielzeug geschenkt.', 'article': 'Den', 'adj_ending': 'en', 'case': 'Dative', 'declension': 'Weak'},
    {'sentence': '{} klug{} gut{} Mannes kenne ich die Geschichte.', 'article': 'Des', 'adj_ending': 'en', 'case': 'Genitive', 'declension': 'Weak'},
    {'sentence': '{} freundlich{} gut{} Frau habe ich den Rat gefolgt.', 'article': 'Der', 'adj_ending': 'en', 'case': 'Genitive', 'declension': 'Weak'},
    {'sentence': '{} aufgeweckt{} gut{} Kindes Spielzeug liegt im Zimmer.', 'article': 'Des', 'adj_ending': 'en', 'case': 'Genitive', 'declension': 'Weak'},
    {'sentence': '{} klug{} gut{} Männer Leistungen sind beeindruckend.', 'article': 'Der', 'adj_ending': 'en', 'case': 'Genitive', 'declension': 'Weak'},
    {'sentence': '{} freundlich{} gut{} Frauen Anstrengungen sind lobenswert.', 'article': 'Der', 'adj_ending': 'en', 'case': 'Genitive', 'declension': 'Weak'},
    {'sentence': '{} aufgeweckt{} gut{} Kinder Neugierde ist bewundernswert.', 'article': 'Der', 'adj_ending': 'en', 'case': 'Genitive', 'declension': 'Weak'},
    #Mixed
    {'sentence': '{} klug{} gut{} Mann hat viel Wissen.', 'article': 'Ein', 'adj_ending': 'er', 'case': 'Nominative', 'declension': 'Mixed'},
    {'sentence': '{} freundlich{} gut{} Frau ist immer hilfsbereit.', 'article': 'Eine', 'adj_ending': 'e', 'case': 'Nominative', 'declension': 'Mixed'},
    {'sentence': '{} aufgeweckt{} gut{} Kind lernt schnell.', 'article': 'Ein', 'adj_ending': 'es', 'case': 'Nominative', 'declension': 'Mixed'},
    {'sentence': '{} klug{} gut{} Männer sind gekommen.', 'article': 'Keine', 'adj_ending': 'en', 'case': 'Nominative', 'declension': 'Mixed'},
    {'sentence': '{} freundlich{} gut{} Frauen haben teilgenommen.', 'article': 'Keine', 'adj_ending': 'en', 'case': 'Nominative', 'declension': 'Mixed'},
    {'sentence': '{} aufgeweckt{} gut{} Kinder waren da.', 'article': 'Keine', 'adj_ending': 'en', 'case': 'Nominative', 'declension': 'Mixed'},
    {'sentence': '{} klug{} gut{} Mann habe ich getroffen.', 'article': 'Einen', 'adj_ending': 'en', 'case': 'Accusative', 'declension': 'Mixed'},
    {'sentence': '{} freundlich{} gut{} Frau habe ich begrüßt.', 'article': 'Eine', 'adj_ending': 'e', 'case': 'Accusative', 'declension': 'Mixed'},
    {'sentence': '{} aufgeweckt{} gut{} Kind habe ich unterstützt.', 'article': 'Ein', 'adj_ending': 'es', 'case': 'Accusative', 'declension': 'Mixed'},
    {'sentence': '{} klug{} gut{} Männer habe ich gesehen.', 'article': 'Keine', 'adj_ending': 'en', 'case': 'Accusative', 'declension': 'Mixed'},
    {'sentence': '{} freundlich{} gut{} Frauen habe ich getroffen.', 'article': 'Keine', 'adj_ending': 'en', 'case': 'Accusative', 'declension': 'Mixed'},
    {'sentence': '{} aufgeweckt{} gut{} Kinder habe ich beobachtet.', 'article': 'Keine', 'adj_ending': 'en', 'case': 'Accusative', 'declension': 'Mixed'},
    {'sentence': '{} klug{} gut{} Mann habe ich geholfen.', 'article': 'Einem', 'adj_ending': 'en', 'case': 'Dative', 'declension': 'Mixed'},
    {'sentence': '{} freundlich{} gut{} Frau habe ich zugehört.', 'article': 'Einer', 'adj_ending': 'en', 'case': 'Dative', 'declension': 'Mixed'},
    {'sentence': '{} aufgeweckt{} gut{} Kind habe ich eine Geschichte erzählt.', 'article': 'Einem', 'adj_ending': 'en', 'case': 'Dative', 'declension': 'Mixed'},
    {'sentence': '{} klug{} gut{} Männern habe ich vertraut.', 'article': 'Keinen', 'adj_ending': 'en', 'case': 'Dative', 'declension': 'Mixed'},
    {'sentence': '{} freundlich{} gut{} Frauen habe ich meine Pläne erzählt.', 'article': 'Keinen', 'adj_ending': 'en', 'case': 'Dative', 'declension': 'Mixed'},
    {'sentence': '{} aufgeweckt{} gut{} Kindern habe ich Spielzeug gegeben.', 'article': 'Keinen', 'adj_ending': 'en', 'case': 'Dative', 'declension': 'Mixed'},
    {'sentence': '{} klug{} gut{} Mannes kenne ich die Pläne.', 'article': 'Eines', 'adj_ending': 'en', 'case': 'Genitive', 'declension': 'Mixed'},
    {'sentence': '{} freundlich{} gut{} Frau habe ich den Rat befolgt.', 'article': 'Einer', 'adj_ending': 'en', 'case': 'Genitive', 'declension': 'Mixed'},
    {'sentence': '{} aufgeweckt{} gut{} Kindes bin ich mir bewusst.', 'article': 'Eines', 'adj_ending': 'en', 'case': 'Genitive', 'declension': 'Mixed'},
    {'sentence': '{} klug{} gut{} Männer habe ich Respekt gezollt.', 'article': 'Keiner', 'adj_ending': 'en', 'case': 'Genitive', 'declension': 'Mixed'},
    {'sentence': '{} freundlich{} gut{} Frauen habe ich das Vertrauen geschenkt.', 'article': 'Keiner', 'adj_ending': 'en', 'case': 'Genitive', 'declension': 'Mixed'},
    {'sentence': '{} aufgeweckt{} gut{} Kinder habe ich meine Aufmerksamkeit geschenkt.', 'article': 'Keiner', 'adj_ending': 'en', 'case': 'Genitive', 'declension': 'Mixed'},
    #Strong
    {'sentence': '{} gut{} klug{} Mann arbeitet hart.', 'article': 'None', 'adj_ending': 'er', 'case': 'Nominative', 'declension': 'Strong'},
    {'sentence': '{} gut{} freundlich{} Frau hilft gerne.', 'article': 'None', 'adj_ending': 'e', 'case': 'Nominative', 'declension': 'Strong'},
    {'sentence': '{} gut{} aufgeweckt{} Kind lernt schnell.', 'article': 'None', 'adj_ending': 'es', 'case': 'Nominative', 'declension': 'Strong'},
    {'sentence': '{} gut{} klug{} Männer sind talentiert.', 'article': 'None', 'adj_ending': 'e', 'case': 'Nominative', 'declension': 'Strong'},
    {'sentence': '{} gut{} freundlich{} Frauen engagieren sich in der Gemeinschaft.', 'article': 'None', 'adj_ending': 'e', 'case': 'Nominative', 'declension': 'Strong'},
    {'sentence': '{} gut{} aufgeweckt{} Kinder haben viel Energie.', 'article': 'None', 'adj_ending': 'e', 'case': 'Nominative', 'declension': 'Strong'},
    {'sentence': '{} gut{} klug{} Mann habe ich getroffen.', 'article': 'None', 'adj_ending': 'en', 'case': 'Accusative', 'declension': 'Strong'},
    {'sentence': '{} gut{} freundlich{} Frau habe ich begrüßt.', 'article': 'None', 'adj_ending': 'e', 'case': 'Accusative', 'declension': 'Strong'},
    {'sentence': '{} gut{} aufgeweckt{} Kind habe ich unterstützt.', 'article': 'None', 'adj_ending': 'es', 'case': 'Accusative', 'declension': 'Strong'},
    {'sentence': '{} gut{} klug{} Männern habe ich geholfen.', 'article': 'None', 'adj_ending': 'en', 'case': 'Dative', 'declension': 'Strong'},
    {'sentence': '{} gut{} freundlich{} Frauen habe ich meine Pläne erzählt.', 'article': 'None', 'adj_ending': 'en', 'case': 'Dative', 'declension': 'Strong'},
    {'sentence': '{} gut{} aufgeweckt{} Kindern habe ich Spielzeug gegeben.', 'article': 'None', 'adj_ending': 'en', 'case': 'Dative', 'declension': 'Strong'},
    {'sentence': '{} gut{} klug{} Mannes kenne ich die Pläne.', 'article': 'None', 'adj_ending': 'en', 'case': 'Genitive', 'declension': 'Strong'},
    {'sentence': '{} gut{} freundlich{} Frau habe ich den Rat befolgt.', 'article': 'None', 'adj_ending': 'er', 'case': 'Genitive', 'declension': 'Strong'},
    {'sentence': '{} gut{} aufgeweckt{} Kindes bin ich mir bewusst.', 'article': 'None', 'adj_ending': 'en', 'case': 'Genitive', 'declension': 'Strong'},
    {'sentence': '{} gut{} klug{} Männer Leistungen sind beeindruckend.', 'article': 'None', 'adj_ending': 'er', 'case': 'Genitive', 'declension': 'Strong'},
    {'sentence': '{} gut{} freundlich{} Frauen Anstrengungen sind lobenswert.', 'article': 'None', 'adj_ending': 'er', 'case': 'Genitive', 'declension': 'Strong'},
    {'sentence': '{} gut{} aufgeweckt{} Kinder Neugierde ist bewundernswert.', 'article': 'None', 'adj_ending': 'er', 'case': 'Genitive', 'declension': 'Strong'}
]

@application.route('/')
def index():
    if 'correct' not in session:
        session['correct'] = 0
    if 'incorrect' not in session:
        session['incorrect'] = 0
    return render_template('index.html')

@application.route('/get_sentence')
def get_sentence():
    if len(sentences) == 0:
        return jsonify({'end': True, 'correct': session['correct'], 'incorrect': session['incorrect']})

    selected_sentence = random.choice(sentences)
    sentences.remove(selected_sentence)
    
    # Replace curly braces {} with underscores ___
    formatted_sentence = selected_sentence['sentence'].replace('{}', '___')
    selected_sentence['sentence'] = formatted_sentence
    
    return jsonify(selected_sentence)

@application.route('/check_answer', methods=['POST'])
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
    application.run(debug=True)