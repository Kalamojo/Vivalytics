import streamlit as stm
import pandas as pd
from tools.spyder import spyder
  
stm.title("Stats Comparison")
stm.sidebar.success("You are currently viewing The Player Comparison page")

df = pd.read_csv("./resources/standard_stats_6.csv")

playerList = stm.multiselect("Enter Player Names", sorted(list(set(df["Player"]))))
#player2 = stm.text_input("Enter the second player name")
if playerList:
	try:
		player_dfs = [df[df['Player']==name] for name in playerList]
		valid_years = set(player_dfs[0]["Year"].to_list())
		for s in player_dfs[1:]:
			valid_years.intersection_update(s["Year"])
		try:
			years = stm.slider('Select Year Range', min(valid_years), max(valid_years), value=[min(valid_years), max(valid_years)])
			fig = spyder(playerList, df, "Stats Compare", set([year for year in range(years[0], years[1]+1)]))
			stm.pyplot(fig)
		except:
			stm.error("Players have an incompatable time range")
			
	except:
		stm.error("Player not found")