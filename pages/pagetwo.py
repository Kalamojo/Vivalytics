import streamlit as stm
import pandas as pd
from tools.spyder import spyder
  
stm.title("Stats Comparison")
stm.sidebar.success("You are currently viewing The Player Comparison page")

df = pd.read_csv("./resources/standard_stats_5.csv")

playerList = stm.multiselect("Enter Player Names", list(set(df["Player"])))
#player2 = stm.text_input("Enter the second player name")
if playerList:
	try:
		fig = spyder(playerList, df, "Stats Compare")
		stm.pyplot(fig)
			
	except:
		stm.error("Player not found")