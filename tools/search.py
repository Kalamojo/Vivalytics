import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity as dist
import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords
nltk.download('wordnet')
from nltk.stem.wordnet import WordNetLemmatizer
import string
import re
import cohere
import spacy

# Load the spaCy English model
nlp = spacy.load("en_core_web_sm")

# Load the cohere model
co = cohere.Client('0Qp52FnTMwc3dhwWafuGWw8yOqdyy1bKK0usvqxD') # This is your trial API key

lem = WordNetLemmatizer()
punctuations = string.punctuation
stop_words = stopwords.words('english')
new_stop = ["stat", "stats", "statistic", "statistics"]
stop_words.extend(new_stop)

def preprocess_text(news, filters=[], stop=True):
    """
    This function receives headlines sentence and returns clean sentence
    """
    for filt in filters:
        news = news.replace(filt, "")
    news = news.lower()
    news = re.sub("\\n", "", news)
    #news = re.sub("\W+", " ", news)
    
    #Split the sentences into words
    words = list(news.split())

    if stop:
        words = [w for w in words if w not in stop_words]
    words = [''.join(x for x in w if x.isalpha()) for w in words]
    words = [lem.lemmatize(word) for word in words]
    words = [w for w in words if w not in punctuations]
    if stop:
        print(words)
    return " ".join(words)

stat_desc = {
    "Gls": "Goals scored. Shot conversion. Shooting & Attacking stats. Attacker, Midfielder.",
    "SoT": "Shots on Target. Target goal. Shooting & Attacking stats. Attacker, Midfielder.",
    "PrgC": "Progressive Balls Carries. Player moves ball across field to opposition. Playmaking and attacking stat. Creates scoring opportunties. Dribbling stat.",
    "Carries": "Ball Carries. Dribbling stat. Distance Covered. Attack.",
    "Touches": "Ball touches. Maintains possession. Attacker, Midfielder.",
    "PK": "Penalty Kicks. Shooting stat.",
    "Cmp": "Passes Completed. Midfielder stat. Passing Stat. Possession Stat. Progresses play. Possession Control.",
    "Cmp%": "Pass Completion percentage. Midfielder stat. Passing stat. Accuracy stat. Possession stat. Progresses play. Puts pressure. Build-up Play.",
    "KP": "Key passes. Build-up play. Progresses play. Chances created. Playmaking stat. Passing stat. Creating stat. Pressure play. Midfielder, Winger. ",
    "PrgP": "Progressive completed passes. Build-up play. Pressure increased. Progresses play. Playmaking stat. Passing stat. Creating stat. Midfielder, Winger.",
    "TklW": "Tackles won. Defensive stat. Defender. Disruption. Regain possession.",
    "Saves": "Goalie saves. Goalie stat.",
    "Save%": "Goalie save percentage. Goalie stat. Goalie/Goalkeeper ",
    "GA": "Goalie misses. Goalie stat. Goalie/Goalkeeper",
    "CS": "No goals allowed. Defensive stat.",
    "AvgLen": "Average pass length. Midfielder stat. Progression. Passing stat.",
    "Stp": "Goalie stops crosses. Goalie stat. Prevent goal scoring opportunties and chances.",
    "Att": "Passes Attempted. Passing stat. Playmaking stat. Midfielder, Attacker, Winger, Defender.",
    "Sh/90": "Shots per game. Attacker/Attacking. Shooting stat. Pressure stat. Offensive efforts. Chance creation.",
    "Tkl+Int": "Tackles and ball interceptions. Defense/Defender stat. Chance prevention stat. Defensive contribution. Positioning. Defender/Central Defensive Midfielder", 
    "Tkl": "Tackles. Defense/Defender stat. Chance prevention. Defensive contribution. Positioning. Defender/Central Defensive Midfielder",
    "Int": "Intercepts ball. Defense/Defender stat. Chance prevention stat. Defensive contribution. Positioning",
    "Clr": "Cleared ball away. Defense/Defender stat. Chance prevention stat. Defensive contribution. Positioning. Defender/Central Defensive Midfielder",
    "Won": "Aerial duels. Defense/Defender stat. Chance prevention stat. Defensive contribution. Positioning. ",
    "PrgDist": "Moved ball toward. Attacking stat. Progresses ball. Playmaking stat. Puts pressure. Dribbling stat. Midfielder.",
    "Pass": "Blocked pass. Defense/Defender stat. Chance prevention stat. Defensive contribution. Positioning. Defender/Central Defensive Midfielder",
    "Ast": "Assists. Pass into goal. Playmaking play. Scoring opportunity. Chance creation. Goal created. Midfielder, Attacker, Winger. Key pass."
}

pages = [v for v in stat_desc.values()]

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
    response = co.embed(
        model='embed-english-v2.0',
        texts=[preprocess_text(q, filters=persons + dates + orgs)])

    query_embedding = np.array(response.embeddings[0])
    query_embedding = query_embedding.reshape(1, -1)
    #print(query_embedding)

    similarities = dist(query_embedding, emb).flatten()

    # Find the index of the text with the highest similarity
    #closest_index = np.argmax(similarities)
    #closest_text = pages[closest_index]
    closest_indices = similarities.argsort()[-3:][::-1]
    #closest_indices = similarities.argsort()[:3]
    closest_texts = [[similarities[ind], pages[ind]] for ind in closest_indices]
    return persons, dates, orgs, closest_texts
    