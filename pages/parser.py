import streamlit as stm
import numpy as np
from tools.search import query

text_embeddings = np.loadtxt('./resources/embeds3.txt')

query_text = stm.text_input("Search sum")

# Add a button to trigger the prediction
if stm.button("Let's see"):
    # Display the output
    persons, dates, orgs, closest_texts = query(query_text, text_embeddings)
    stm.write("Entities: ", persons, dates, orgs)
    stm.write("Matches:")
    for text in closest_texts:
    	stm.write(text)