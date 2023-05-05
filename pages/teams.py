import streamlit as stm
import pandas as pd
from tools.spyder import spyder1
from tools.line import line_chart

stm.title("Team Stats")
stm.sidebar.success("You are currently viewing The Stats Searching page")
df = pd.read_csv("./resources/team_all_stats.csv")

team = stm.selectbox("Enter the name of a Squad", 
						  [''] + sorted(list(set(df["Squad"]))),
						  0)
if team:
	try:
		team_df = df[df["Squad"] == team]
		team_df.index = team_df.pop("Year")
		team_df.sort_index(inplace=True)
		#print(player_df)
		stm.title(team)
		#stm.caption(player_df.iloc[0]["player_link"])
		stm.write("League: " + team_df.iloc[-1]['League'])

		stats_list = ["Gls", "Att", "Sh/90", "SoT/90", "Poss", "Cmp%", "Tkl+Int"]
		stat = stm.selectbox("Select a stat", stats_list)
		col1b, col2b = stm.columns([1, 1])
		teams = [team]
		with col1b:
			fig = spyder1(teams, df, team, [stats_list], group="Squad")
			stm.pyplot(fig)
		with col2b:
			fig = line_chart(teams, df, stat, group="Squad")
			stm.plotly_chart(fig)
		team_df_rom = team_df.drop(["Unnamed: 0", "Unnamed: 109", "Squad", "team_id", "League"], 
										  axis=1)
		team_df_rom.dropna(axis=1, how='all', inplace=True)
		team_df_rom.index = team_df_rom.index.map(str)
		to_front = ["Age"]
		for col in reversed(to_front):
			team_df_rom.insert(0, col, team_df_rom.pop(col))
		#print(player_df_rom)
		stm.dataframe(team_df_rom)
			
	except:
		stm.error("Squad not found")