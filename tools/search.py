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

# Load the spaCy English model
nlp = spacy.load("en_core_web_sm")

lem = WordNetLemmatizer()
punctuations = string.punctuation
stop_words = stopwords.words('english')

def preprocess_text(news):
    """
    This function receives headlines sentence and returns clean sentence
    """
    news = news.lower()
    news = re.sub("\\n", "", news)
    #news = re.sub("\W+", " ", news)
    
    #Split the sentences into words
    words = list(news.split())
    
    words = [lem.lemmatize(word, "v") for word in words]
    words = [w for w in words if w not in punctuations]
    #words = [w for w in words if w not in stop_words]
    #words = [''.join(x for x in w if x.isalpha()) for w in words]
    
    return words

cats_map = {'Goals scored or allowed': 'Gls',
            'Shots on Target': 'SoT',
            "Carries that move the ball towards the opponent's goal line at least 10 yards from its furthest point in the last six passes, or any carry into the penalty area. Excludes carries which end in the defending 50 percent of the pitch": 'PrgC',
            'Number of times the player controlled the ball with their feet': 'Carries',
            'Number of times a player touched the ball. Note: Receiving a pass, then dribbling, then sending a pass counts as one touch': 'Touches',
            'Penalty Kicks Made': 'PK',
            'Passes Completed': 'Cmp',
            'Pass Completion percentage': 'Cmp%',
            'Passes that directly lead to a shot (assisted shots)': 'KP',
            "Completed passes that move the ball towards the opponent's goal line at least 10 yards from its furthest point in the last six passes, or any completed pass into the penalty area.": 'PrgP',
            "Tackles in which the tackler's team won possession of the ball": 'TklW',
            'number of times the goalie saves a ball from being scored': 'Saves',
            'percentage of shots the goalie saves from scoring': 'Save%',
            'number of goals the goalie allows to be scored against them': 'GA',
            'Full matches by goalkeeper where no goals are allowed.': 'CS',
            'Average length of passes, in yards': 'AvgLen',
            'Number of crosses into penalty area which were successfully stopped by the goalkeeper': 'Stp',
            'number of Passes Attempted': 'Att',
            'Total number of shots attempted': 'Sh/90',
            'Shots on Target per 90 minutes': 'SoT/90',
            'Number of players tackled plus number of interceptions': 'Tkl+Int',
            'Number of players tackled': 'Tkl',
            'number of Interceptions': 'Int',
            'Player kicking the ball away from their goal': 'Clr',
            'number of Aerial duels': 'Won',
            "Total distance, in yards, a player moved the ball while controlling it with their feet towards the opponent's goal": 'PrgDist',
            'Number of times blocking a pass by standing in its path': 'Pass',
            'number of Assists': 'Ast'
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
    