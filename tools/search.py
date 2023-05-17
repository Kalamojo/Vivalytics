import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords
nltk.download('wordnet')
from nltk.stem.wordnet import WordNetLemmatizer
import string
import re
import spacy
import en_core_web_sm

# Load the spaCy English model
nlp = en_core_web_sm.load()

lem = WordNetLemmatizer()
punctuations = string.punctuation
stop_words = stopwords.words('english')

def preprocess_text(news, stop=True):
    """
    This function receives headlines sentence and returns clean sentence
    """
    news = news.lower()
    news = re.sub("\\n", "", news)
    #news = re.sub("\W+", " ", news)
    
    #Split the sentences into words
    words = list(news.split())

    if stop:
        words = [w for w in words if w not in stop_words]
    words = [''.join(x for x in w if x.isalpha()) for w in words]
    words = [lem.lemmatize(word, "v") for word in words]
    words = [w for w in words if w not in punctuations]
    if stop:
        print(words)
    return words

cats_map = {'Goals scored': 'Gls',
         'Shoots ball on Target': 'SoT',
         'Progressive Balls Carries': 'PrgC',
         'Ball Carries': 'Carries',
         'Ball touches': 'Touches',
         'Penalty Kicks': 'PK',
         'Passes Completed': 'Cmp',
         'Pass Completion percentage': 'Cmp%',
         'Key passes': 'KP',
         'Progressive completed passes': 'PrgP',
         'Tackles won': 'TklW',
         'Goalie saves': 'Saves',
         'Goalie save percentage': 'Save%',
         'Goalie misses': 'GA',
         'No goals allowed': 'CS',
         'Average pass length': 'AvgLen',
         'Goalie stops crosses': 'Stp',
         'Passes Attempted': 'Att',
         'Attempt shoot ball': 'Sh/90',
         'Tackles and ball interceptions': 'Tkl+Int',
         'Tackles': 'Tkl',
         'Intercept ball': 'Int',
         'Cleared ball away': 'Clr',
         'Aerial duels': 'Won',
         'Moved ball toward': 'PrgDist',
         'Blocked pass': 'Pass',
         'Assists': 'Ast'
}

pages = [k for k in cats_map.keys()]

def query(q, emb):
    # Process the text with spaCy
    doc = nlp(q)

    # Extract person names
    persons = []
    dates = []
    orgs = []
    for entity in doc.ents:
        print(entity.text, entity.label_)
        if entity.label_ in ["PERSON", "ORG"]:
            persons.append(entity.text)
        elif entity.label_ == "DATE":
            dates.append(entity.text)
        elif entity.label_ in ["GPE", "FAC"]:
            orgs.append(entity.text)
    
    # Tokenize the search query
    query_embedding = np.mean([nlp(token).vector for token in preprocess_text(q)], axis=0)
    query_embedding = query_embedding.reshape(1, -1)
    #print(query_embedding)

    similarities = cosine_similarity(query_embedding, emb).flatten()

    # Find the index of the text with the highest similarity
    #closest_index = np.argmax(similarities)
    #closest_text = pages[closest_index]
    closest_indices = similarities.argsort()[-3:][::-1]
    closest_texts = [[similarities[ind], pages[ind]] for ind in closest_indices]
    return persons, dates, orgs, closest_texts
    