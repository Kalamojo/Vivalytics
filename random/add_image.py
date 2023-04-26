import pandas as pd
import numpy as np
import bs4
import requests
import time
from selenium import webdriver

df = pd.read_csv("standard_2022_player.csv")

#print(df.head())
driver = webdriver.Chrome()
driver.maximize_window()

def get_img_link(url):
	driver.get(url)
	#time.sleep(3)

	html = bs4.BeautifulSoup(driver.page_source.encode('utf-8').strip(), 'html.parser')
	#print(html)
	title = html.find("div", {"id": "meta"})
	#print(title)
	if title:
		image = title.find("img")
		print(image)
		if image == None:
			return "not_found"
		return image['src']
	return "not_found"

#print(get_img_link("https://fbref.com/en/players/774cf58b/Max-Aarons"))

#"""
links = ["something"]

print(df.iloc[1, 38])
print(type(df.iloc[1, 38]))
print(get_img_link("https://fbref.com/en/players/774cf58b/Max-Aarons"))
print(get_img_link(df.iloc[1, 38]))

print(df.iloc[1, 38])
print(df.shape[0])
for i in range(1, df.shape[0]):
	print(i)
	if i % 50 == 0:
		print(f"{i} done")
	#print(df.iloc[i, 38])
	links.append(get_img_link(df.iloc[i, 38]))

with open("Bruhhhh.txt", "w") as file:
	file.write(str(links))

df['image_link'] = links

df.to_csv("2022_players.csv")
#"""