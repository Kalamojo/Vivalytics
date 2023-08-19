#import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity as dist
import cohere
from fuzzywuzzy import process
import difflib
#import spacy

# Load the spaCy English model
#nlp = spacy.load("en_core_web_sm")

# Load the cohere model
co = cohere.Client('0Qp52FnTMwc3dhwWafuGWw8yOqdyy1bKK0usvqxD') # This is your trial API key

stat_desc = {"Gls": "Goals scored",
             "SoT": "Shoots ball on Target",
             "PrgC": "Progressive Balls Carries",
             "Carries": "Ball Carries",
             "Touches": "Ball touches",
             "PK": "Penalty Kicks",
             "Cmp": "Passes Completed",
             "Cmp%": "Pass Completion percentage",
             "KP": "Key passes",
             "PrgP": "Progressive completed passes",
             "TklW": "Tackles won",
             "Saves": "Goalie saves",
             "Save%": "Goalie save percentage",
             "GA": "Goalie misses",
             "CS": "No goals allowed",
             "AvgLen": "Average pass length",
             "Stp": "Goalie stops crosses",
             "Att": "Passes Attempted",
             "Sh/90": "Attempt shoot ball",
             "Tkl+Int": "Tackles and ball interceptions",
             "Tkl": "Tackles",
             "Int": "Intercept ball",
             "Clr": "Cleared ball away",
             "Won": "Aerial duels",
             "PrgDist": "Moved ball toward",
             "Pass": "Blocked pass",
             "Ast": "Assists"
}

desc_stat = {val: key for key, val in stat_desc.items()}

pages = [v for v in stat_desc.values()]

def search_stat(q, embeddings_location='./resources/embeds4.txt'):
    if not q[-1].isalpha():
        q = q[:-1]
    emb = np.loadtxt(embeddings_location)
    # Tokenize the search query
    response = co.embed(
        model='embed-english-v2.0',
        texts=[q])

    query_embedding = np.array(response.embeddings[0])
    query_embedding = query_embedding.reshape(1, -1)
    #print(query_embedding)

    similarities = dist(query_embedding, emb).flatten()

    # Find the index of the text with the highest similarity
    #closest_index = np.argmax(similarities)
    #closest_text = pages[closest_index]
    closest_indices = similarities.argsort()[-3:][::-1]
    #closest_indices = similarities.argsort()[:3]
    closest_texts = [[similarities[ind], pages[ind], desc_stat[pages[ind]]] for ind in closest_indices]
    print(closest_texts)
    return desc_stat[closest_texts[0][1]]
    
def find_stat(search_query):
    if not search_query[-1].isalpha():
        search_query = search_query[:-1]
    closest_matches = process.extract(search_query, pages)
    #return [(match, desc_stat[match[0]]) for match in closest_matches]
    print(closest_matches)
    return desc_stat[closest_matches[0][0]]

def reg_stat(search_query):
    if not search_query[-1].isalpha():
        search_query = search_query[:-1]
    closest_matches = difflib.get_close_matches(search_query, pages)
    print(closest_matches)
    return desc_stat[closest_matches[0]]