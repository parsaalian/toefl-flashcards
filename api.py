import json
import nltk
import numpy as np
from nltk.corpus import wordnet
from googletrans import Translator
from flask import Flask, request, render_template


app = Flask(__name__)
translator = Translator()


@app.route("/")
def random():
    global translator
    res = {}
    words = []

    with open("words.json", "r") as f:
        words = json.load(f)

    word = np.random.choice(words, 1)[0]

    translation = translator.translate(word, dest="fa").text

    synonyms = []
    try:
        for syn in wordnet.synsets(word):
            for lm in syn.lemmas():
                synonyms.append(lm.name())

        synonyms = list(set(synonyms))
    except:
        pass

    antonyms = []
    try:
        for syn in wordnet.synsets(word):
            for lm in syn.lemmas():
                if lm.antonyms():
                    antonyms.append(lm.antonyms()[0].name())

        antonyms = list(set(antonyms))
    except:
        pass

    return render_template(
        "index.html",
        word=word,
        translation=translation,
        synonyms=synonyms,
        antonyms=antonyms,
    )


if __name__ == "__main__":
    from waitress import serve

    nltk.download("wordnet")
    serve(app, listen="0.0.0.0:5000")
