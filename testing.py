from tools.spyder import spyder
import pandas as pd

df = pd.read_csv("./resources/standard_stats_5.csv")

player = 'Lionel Messi'
if player:
	players = [player]
	fig = spyder(players, df, player)
	fig.show()