import pandas as pd
import numpy as np
from tools.api_call import gpt_res, gpt_res2, gpt_res3
from tools.match_name import find_entity
from tools.stat_search import find_stat, search_stat
import re

def league_filt(df, league, leagues):
	try:
		if league != None:
			closest_leagues = find_entity(league, leagues)
			if len(closest_leagues) == 1:
				league = closest_leagues[0][0]
			else:
				print("Multiple Leagues with similar names")
				return df, False
			print("CLosest league:", league)
			return df[df["League"] == league], True
		else:
			print("Query did not extract League")
			return df, False
	except:
		print("Query did not extract League")
		return df, False

def player_filt(df, players, names):
	try:
		if players != None:
			matched_players = []
			for i in range(len(players)):
				closest_players = find_entity(players[i], names)
				if len(closest_players) == 1:
					matched_players.append(closest_players[0][0])
			if len(matched_players) == 0:
				print("Multiple Players with similar names")
				return df, False
			return df[df["Player"].isin(matched_players)], True
		else:
			print("Query did not extract player")
			return df, False
	except:
		print("Query did not extract player")
		return df, False

def stat_filt(df, stat, player):
	if stat != None:
		#stat = find_stat(pos[3][1])
		print("abouta find stats")
		stat = search_stat(stat)
		print("statty:", stat)
		if not player:
			return df[["Year", "League", "Player", stat]][df[stat].notnull()].sort_values(stat, ascending=False), True
		else:
			return df[["Year", "League", "Player", stat]], True
	else:
		print("Query did not extract stat")
		return df[["Year", "League", "Player"] + ['Gls', 'SoT', 'PrgC', 'Carries', 'Touches', 'PK', 'Cmp', 'Cmp%', 'KP', 'PrgP', 'TklW', 'Saves', 'Save%', 'GA', 'CS', 'AvgLen', 'Stp', 'Att', 'Sh/90', 'Tkl+Int', 'Tkl', 'Int', 'Clr', 'Won', 'PrgDist', 'Pass', 'Ast']], False

def pos_filt2(df, prompt):
	res = gpt_res2(prompt)
	print("response:", res)

	pattern = r'```python\n(.*?)```'
	parsed_res = re.findall(pattern, res, re.DOTALL)
	if parsed_res:
		res = parsed_res[0]
	
	variables = {}
	try:
	    exec(res, variables)
	except Exception as e:
	    print(f"Error executing code: {e}")

	print("league:", variables.get('league'))
	print("players:", variables.get('players'))
	print("stats:", variables.get('stat'))

	names = list(set(df["Player"].to_list()))
	leagues = list(set(df["League"].to_list()))

	#print(df.shape)

	df, league_worked = league_filt(df, variables.get('league'), leagues)

	#print(df.shape)

	df, player_worked = player_filt(df, variables.get('players'), names)

	#print(df.shape, player_worked)

	df, stat_worked = stat_filt(df, variables.get('stat'), player_worked)

	#print(df.shape, stat_worked)

	#if stat_worked:
		#print(df.columns)

	#if not player_worked and stat_worked:
		#print(df.iloc[0])

	return df, res, (league_worked, player_worked, stat_worked)