import streamlit as stm
import pandas as pd
import bs4
import requests
from tools.spyder import spyder1
from tools.line import line_chart

def get_img_link(url):
	print("why")
	r = requests.get(url)
	print("this")

	html = bs4.BeautifulSoup(r.text, 'html.parser')
	title = html.find("div", {"id": "meta"})
	print("slow")
	if title:
		image = title.find("img")
		print(image)
		if image == None:
			return "not_found"
		return image['src']
	return "not_found"
  
stm.title("Individual Stats")
stm.sidebar.success("You are currently viewing The Stats Searching page")
df = pd.read_csv("./resources/standard_stats_6.csv")

player = stm.selectbox("Enter the name of a player", 
						  [''] + sorted(list(set(df["Player"]))),
						  0)
if player:
	try:
		player_df = df[df["Player"] == player]
		player_df.index = player_df.pop("Year")
		player_df.sort_index(inplace=True)
		#print(player_df)
		col1a, col2a = stm.columns([1, 2])
		with col2a:
			stm.title(player)
			stm.caption(player_df.iloc[0]["Player Link"])
			stm.write("Squad: " + player_df.iloc[-1]['Squad'])
		stat = stm.selectbox("Select a stat", ['Gls', 'Ast', 'G+A', 'G-PK', 'PK', 'PKatt'])
		col1b, col2b = stm.columns([1, 1])
		players = [player]
		with col1b:
			fig = spyder1(players, df, player)
			stm.pyplot(fig)
		with col2b:
			fig = line_chart(players, df, stat)
			stm.plotly_chart(fig)
		player_df_rom = player_df.drop(["Rk", "Player", "Born", "Matches", "Player Link", "Player ID"], 
										  axis=1)
		player_df_rom.index = player_df_rom.index.map(str)
		#print(player_df_rom)
		stm.dataframe(player_df_rom)
		image_link = get_img_link(player_df.iloc[0]["Player Link"])
		with col1a:
			stm.image(image_link)
			
	except:
		stm.error("Player not found")