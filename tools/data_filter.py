import pandas as pd
import numpy as np
from tools.api_call import gpt_res
from tools.match_name import find_entity
from tools.stat_search import find_stat, search_stat

def league_filt(df, pos, leagues):
	if pos[1][1] != 'null':
		league = pos[1][1]
		closest_leagues = find_entity(league, leagues)
		if len(closest_leagues) == 1:
			league = closest_leagues[0][0]
		else:
			print("Multiple Leagues with similar names")
			return df, False
		print(closest_leagues)
		return df[df["League"] == league], True
	else:
		print("Query did not extract League")
		return df, False

def player_filt(df, pos, names):
	if pos[0][0][:6] == 'Player' and pos[0][1] != 'null':
		player = pos[0][1]
		closest_players = find_entity(player, names)
		if len(closest_players) == 1:
			player = closest_players[0][0]
		else:
			print("Multiple Players with similar names")
			return df, False
		print(closest_players)
		return df[df["Player"] == player], True
	else:
		print("Query did not extract player")
		return df, False

def stat_filt(df, pos, player):
	if pos[3][1] != 'null':
		#stat = find_stat(pos[3][1])
		stat = search_stat(pos[3][1])
		if not player:
			return df[["Year", "League", "Player", stat]].sort_values(stat, ascending=False), True
		else:
			return df[["Year", "League", "Player", stat]], True
	else:
		return df, False

def pos_filt(df, prompt):
	res = gpt_res(prompt)
	names = list(set(df["Player"].to_list()))
	leagues = list(set(df["League"].to_list()))

	print(df.shape)

	df, league_worked = league_filt(df, res, leagues)

	print(df.shape)

	df, player_worked = player_filt(df, res, names)

	print(df.shape, player_worked)

	df, stat_worked = stat_filt(df, res, player_worked)

	print(df.shape, stat_worked)

	if stat_worked:
		print(df.columns)

	if not player_worked and stat_worked:
		print(df.iloc[0])

	return df, res, (league_worked, player_worked, stat_worked)
