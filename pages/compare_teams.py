import streamlit as stm
import pandas as pd
from tools.spyder import spyder2
from tools.line import line_chart
  
stm.title("Team Stats Comparison")
stm.sidebar.success("You are currently viewing The Squad Comparison page")
df = pd.read_csv("./resources/team_all_stats.csv")

squadList = stm.multiselect("Enter Squad Names", sorted(list(set(df["Squad"]))))
#player2 = stm.text_input("Enter the second player name")
if squadList:
	try:
		if len(squadList) > 2:
			squad_dfs = [df[df['Squad']==name].sort_values('Year') for name in squadList]
			stats_lists = [["Gls", "Att", "Sh/90", "SoT/90", "Poss", "Cmp%", "Tkl+Int"]]
			valid_years = [min(squad_dfs[0]["Year"]), max(squad_dfs[0]["Year"])]
			for s in squad_dfs[1:]:
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
					stm.caption(f"Only {valid_years[0]} is available for a squad")
					years = [valid_years[0], valid_years[0]]
				else:
					years = stm.slider('Select Year Range', valid_years[0], valid_years[1], value=[valid_years[0], valid_years[1]])
				fig = spyder2(squadList, df, "Stats Compare", stats_lists, set([year for year in range(years[0], years[1]+1)]), group="Squad")
				stm.plotly_chart(fig, use_container_width=True)
			except:
				stm.error("Squads have an incompatable time range")
			stats = ["Gls", "Att", "Sh/90", "SoT/90", "Poss", "Cmp%", "Tkl+Int"]
			stat = stm.selectbox("Select a stat", stats)
			fig = line_chart(squadList, df, stat, 700, group="Squad")
			stm.plotly_chart(fig, use_container_width=True)
		else:
			squad_dfs = [df[df['Squad']==name].sort_values('Year') for name in squadList]
			stats_lists = [["Gls", "Att", "Sh/90", "SoT/90", "Poss", "Cmp%", "Tkl+Int"]]
			valid_years = [(min(squad_dfs[i]["Year"]), max(squad_dfs[i]["Year"])) for i in range(len(squadList))]
			if len(squadList) < 2:
				print("Bro")
				if valid_years[0][0] == valid_years[0][1]:
					stm.caption("Cannot Change Year Range for Squad")
					years = [valid_years[0][0], valid_years[0][0]]
				else:
					years = stm.slider('Select Year Range', valid_years[0][0], valid_years[0][1], value=[valid_years[0][0], valid_years[0][1]])
				fig = spyder2(squadList, df, "Stats Compare", stats_lists, [set([year for year in range(years[0], years[1]+1)])], restrict=False, group="Squad")
				stm.plotly_chart(fig, use_container_width=True)
			else:
				col1a, col2a = stm.columns([1, 1], gap="medium")
				with col1a:
					if valid_years[0][0] == valid_years[0][1]:
						stm.caption("Cannot Change Year Range for Squad")
						years1 = [valid_years[0][0], valid_years[0][0]]
					else:
						years1 = stm.slider('Select Year Range for ' + squadList[0], valid_years[0][0], valid_years[0][1], value=[valid_years[0][0], valid_years[0][1]])

				with col2a:
					if valid_years[1][0] == valid_years[1][1]:
						stm.caption("Cannot Change Year Range for Squad")
						years2 = [valid_years[0][0], valid_years[0][0]]
					else:
						years2 = stm.slider('Select Year Range for ' + squadList[1], valid_years[1][0], valid_years[1][1], value=[valid_years[1][0], valid_years[1][1]])
				fig = spyder2(squadList, df, "Stats Compare", stats_lists, [set([year for year in range(years1[0], years1[1]+1)]), set([year for year in range(years2[0], years2[1]+1)])], group="Squad", restrict=False)
				stm.plotly_chart(fig, use_container_width=True)
			stats = ["Gls", "Att", "Sh/90", "SoT/90", "Poss", "Cmp%", "Tkl+Int"]
			stat = stm.selectbox("Select a stat", stats)
			fig = line_chart(squadList, df, stat, 700, group="Squad")
			stm.plotly_chart(fig, use_container_width=True)
			
	except:
		stm.error("Squad not found")