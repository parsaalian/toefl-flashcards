import json
import nltk
import numpy as np
from nltk.corpus import wordnet
from googletrans import Translator
from flask import Flask, request, jsonify, render_template


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

    tranlation = translator.translate(word, dest="fa").text

    synonyms = []
    for syn in wordnet.synsets(word):
        for lm in syn.lemmas():
            synonyms.append(lm.name())

    synonyms = list(set(synonyms))

    antonyms = []
    for syn in wordnet.synsets(word):
        for lm in syn.lemmas():
            if lm.antonyms():
                antonyms.append(lm.antonyms()[0].name())

    antonyms = list(set(antonyms))

    return render_template("index.html", word=word)


if __name__ == "__main__":
    nltk.download("wordnet")
    app.run(port=5000)
