import streamlit as stm
import pandas as pd
import bs4
import requests
from tools.spyder import spyder

def get_img_link(url):
	r = requests.get(url)

	html = bs4.BeautifulSoup(r.text, 'html.parser')
	title = html.find("div", {"id": "meta"})
	if title:
		image = title.find("img")
		print(image)
		if image == None:
			return "not_found"
		return image['src']
	return "not_found"
  
stm.title("This is PageOne Geeks.")
stm.sidebar.success("You are currently viewing Page One Geek")
df = pd.read_csv("./resources/standard_stats_5.csv")

player = stm.selectbox("Enter the name of a player", 
						  [''] + list(set(df["Player"])),
						  0)
if player:
	#try:
	player_df = df[df["Player"] == player]
	print(player_df)
	col1a, col2a = stm.columns([1, 2])
	with col2a:
		stm.title(player)
		stm.caption(player_df.iloc[0]["Player Link"])
		stm.write("Squad: " + player_df.iloc[0]['Squad'])
	players = [player]
	fig = spyder(players, df, player)
	stm.pyplot(fig)
	#col1b, col2b = stm.columns([1, 2])
	#with col1b:
		
	#with col2b:
	player_df_rom = player_df.drop(["Rk", "Player", "Born", "Matches", "Player Link", "Player ID"], 
									  axis=1)
	player_df_rom.index = player_df_rom.pop("Year")
	player_df_rom.sort_index(inplace=True)
	player_df_rom.index = player_df_rom.index.map(str)
	print(player_df_rom)
	stm.dataframe(player_df_rom)
	image_link = get_img_link(player_df.iloc[0]["Player Link"])
	with col1a:
		stm.image(image_link)
			
	#except:
	#	stm.error("Player not found")