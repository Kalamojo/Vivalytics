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
		if len(playerList) > 2:
			player_dfs = [df[df['Player']==name] for name in playerList]
			valid_years = [min(player_dfs[0]["Year"]), max(player_dfs[0]["Year"])]
			for s in player_dfs[1:]:
				smol = min(s["Year"])
				big = max(s["Year"])
				if smol > valid_years[0]:
					valid_years[0] = smol
				if big < valid_years[1]:
					valid_years[1] = big
			try:
				if valid_years[0] > valid_years[1]:
					raise ValueError('Smallest Valid year is larger than Largest Valid year')
				years = stm.slider('Select Year Range', valid_years[0], valid_years[1], value=[valid_years[0], valid_years[1]])
				fig = spyder(playerList, df, "Stats Compare", set([year for year in range(years[0], years[1]+1)]))
				stm.pyplot(fig)
			except:
				stm.error("Players have an incompatable time range")
		else:
			player_dfs = [df[df['Player']==name] for name in playerList]
			valid_years = [(min(player_dfs[i]["Year"]), max(player_dfs[i]["Year"])) for i in range(len(playerList))]
			if len(playerList) < 2:
				years = stm.slider('Select Year Range', valid_years[0][0], valid_years[0][1], value=[valid_years[0][0], valid_years[0][1]])
				fig = spyder(playerList, df, "Stats Compare", [set([year for year in range(years[0], years[1]+1)])], restrict=False)
				stm.pyplot(fig)
			else:
				col1a, col2a = stm.columns([1, 1], gap="medium")
				with col1a:
					years1 = stm.slider('Select Year Range for ' + playerList[0], valid_years[0][0], valid_years[0][1], value=[valid_years[0][0], valid_years[0][1]])
				with col2a:
					years2 = stm.slider('Select Year Range for ' + playerList[1], valid_years[1][0], valid_years[1][1], value=[valid_years[1][0], valid_years[1][1]])
				fig = spyder(playerList, df, "Stats Compare", [set([year for year in range(years1[0], years1[1]+1)]), set([year for year in range(years2[0], years2[1]+1)])], restrict=False)
				stm.pyplot(fig)
			
	except:
		stm.error("Player not found")