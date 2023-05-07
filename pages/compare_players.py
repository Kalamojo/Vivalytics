import streamlit as stm
import pandas as pd
from tools.spyder import spyder2
from tools.line import line_chart
  
stm.title("Player Stats Comparison")
stm.sidebar.success("You are currently viewing The Player Comparison page")
df = pd.read_csv("./resources/persons_all_stats.csv")

stat_spread = {"FW": ["Gls", "SoT", "PrgC", "Carries", "Touches", "PK"],
			   "MF": ["Cmp", "Cmp%", "KP", "PrgP", "Carries", "TklW"],
			   "DF": ["Tkl", "Int", "Clr", "Won", "PrgDist", "Pass"],
			   "GK": ["Saves", "Save%", "PrgDist", "CS", "AvgLen", "Stp"]}

playerList = stm.multiselect("Enter Player Names", sorted(list(set(df["Player"]))))
#player2 = stm.text_input("Enter the second player name")
if playerList:
	try:
		if len(playerList) > 2:
			player_dfs = [df[df['Player']==name].sort_values('Year') for name in playerList]
			stats_lists = [stat_spread[p_df.iloc[-1]["Pos"].split(",")[0]] for p_df in player_dfs]
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
				if valid_years[0] == valid_years[1]:
					stm.caption(f"Only {valid_years[0]} is available for a player")
					years = [valid_years[0], valid_years[0]]
				else:
					years = stm.slider('Select Year Range', valid_years[0], valid_years[1], value=[valid_years[0], valid_years[1]])
				fig = spyder2(playerList, df, "Stats Compare", stats_lists, set([year for year in range(years[0], years[1]+1)]))
				stm.plotly_chart(fig, use_container_width=True)
			except:
				stm.error("Players have an incompatable time range")
			stats = list(set(sum(stats_lists, [])))
			stat = stm.selectbox("Select a stat", stats)
			fig = line_chart(playerList, df, stat, 700)
			stm.plotly_chart(fig)
		else:
			player_dfs = [df[df['Player']==name].sort_values('Year') for name in playerList]
			stats_lists = [stat_spread[p_df.iloc[-1]["Pos"].split(",")[0]] for p_df in player_dfs]
			valid_years = [(min(player_dfs[i]["Year"]), max(player_dfs[i]["Year"])) for i in range(len(playerList))]
			if len(playerList) < 2:
				print("Bro")
				if valid_years[0][0] == valid_years[0][1]:
					stm.caption("Cannot Change Year Range for Player")
					years = [valid_years[0][0], valid_years[0][0]]
				else:
					years = stm.slider('Select Year Range', valid_years[0][0], valid_years[0][1], value=[valid_years[0][0], valid_years[0][1]])
				fig = spyder2(playerList, df, "Stats Compare", stats_lists, [set([year for year in range(years[0], years[1]+1)])], restrict=False)
				stm.plotly_chart(fig, use_container_width=True)
			else:
				col1a, col2a = stm.columns([1, 1], gap="medium")
				with col1a:
					if valid_years[0][0] == valid_years[0][1]:
						stm.caption("Cannot Change Year Range for Player")
						years1 = [valid_years[0][0], valid_years[0][0]]
					else:
						years1 = stm.slider('Select Year Range for ' + playerList[0], valid_years[0][0], valid_years[0][1], value=[valid_years[0][0], valid_years[0][1]])

				with col2a:
					if valid_years[1][0] == valid_years[1][1]:
						stm.caption("Cannot Change Year Range for Player")
						years2 = [valid_years[0][0], valid_years[0][0]]
					else:
						years2 = stm.slider('Select Year Range for ' + playerList[1], valid_years[1][0], valid_years[1][1], value=[valid_years[1][0], valid_years[1][1]])
				fig = spyder2(playerList, df, "Stats Compare", stats_lists, [set([year for year in range(years1[0], years1[1]+1)]), set([year for year in range(years2[0], years2[1]+1)])], margin=False, restrict=False)
				stm.plotly_chart(fig, use_container_width=True)
			stats = list(set(sum(stats_lists, [])))
			stat = stm.selectbox("Select a stat", stats)
			fig = line_chart(playerList, df, stat, 700)
			stm.plotly_chart(fig)
			
	except:
		stm.error("Player not found")