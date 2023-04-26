from nerodia.browser import Browser
import pandas as pd
import numpy as np
from selenium.webdriver.chrome.options import Options
import time
from functools import reduce

# Using Selenium Chrome Options, set headless so the physical GUI of Chrome doesn't have to be used, and no sandbox to avoid crashes
options = Options()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
browser = Browser('chrome', options=options) # Create Browser element

#The analysis focuses on goal scoring
# Each of the metrics has an associated data table
# A list of table tags is created to allow appending to the url string
tags=['goals','total_pass','touches','total_scoring_att','big_chance_missed','appearances','total_offside','dispossessed','total_cross','total_through_ball']
#se='?se=418'
se = ''
#Base url string
urls=['https://www.premierleague.com/stats/top/players/'+str(i)+se for i in tags]

goals=urls[0]
total_pass=urls[1]
touches=urls[2]
total_shots=urls[3]
big_chance_missed=urls[4]
appearances=urls[5]
offsides=urls[6]
disposessions=urls[7]
total_cross=urls[8]
total_through_ball=urls[9]

#create a function to read in the various tables into dataframes
def create_df(df,url,statcol):
	browser.goto(url) 
	time.sleep(4) # time delay for data reload 
	#Create dataframe by reading from html table 
	df = pd.read_html(browser.html)[0]
	#table is paginated. At the last page, the "next" button becomes inactive
	# the while not loop below allows reading of data from each page until the inactive button is found 
	# https://deepnote.com/@danielstpaul/EPL-Web-Scraper-GfUde655TFGQbN7gE42hRA
	while not browser.div(class_name=['paginationBtn',   'paginationNextContainer', 'inactive']).exists:
		# fire onClick event on page next element.  
		browser.div(class_name=['paginationBtn', 'paginationNextContainer']).fire_event('onClick') 
		# append the table from this page with the existing dataframe.

		df2 = pd.read_html(browser.html)[0]

		#print(df2)
		#for i in range(5): print("V")
		#print(df)

		df = pd.concat([df, df2], axis=0).drop_duplicates().reset_index(drop=True)

	#Some data preprocessing 
	df=df.rename(columns={"Stat": statcol}) 
	df = df.iloc[: , :-1] # Drop last "nan" column 
	df=df.drop(columns='Rank') # Drop "rank" column
	return df

#Apply function to create dataframes
goal_df=create_df('goals_df',goals,'Goals')
#print(goal_df)
#goal_df.to_csv("bruh.csv")

#"""
total_pass_df=create_df('total_pass',total_pass,'TotalPasses')
touches_df=create_df('touches',touches,'Touches')
total_shots_df=create_df('total_shots',total_shots,'TotalShots')
big_chance_missed_df=create_df('big_chance_missed',big_chance_missed,'BigChancesMissed')
appearances_df=create_df('appearances',appearances,'Appearances')
offsides_df=create_df('offsides',offsides,'Offsides')
disposessions_df=create_df('disposessions',disposessions,'Disposessions')
total_cross_df=create_df('total_cross',total_cross,'TotalCrosses')
total_through_ball_df=create_df('total_through_ball',total_through_ball,'ThroughBalls')

#Creating list of dataframes
dfs=[goal_df, total_pass_df, touches_df,total_shots_df,big_chance_missed_df,appearances_df,offsides_df,disposessions_df,total_cross_df,total_through_ball_df]
#Use reduce function to merge all the dataframes all at once
df = reduce(lambda  left,right: pd.merge(left,right,on=['Player','Nationality','Club'],how='outer'), dfs).drop_duplicates()
#Create First Name and Last Name Features, in order to enhance the optics during vizualization
df.loc[df['Player'].str.split().str.len() == 2, 'FirstName'] = df['Player'].str.split().str[0]
df['FirstName']=df['FirstName'].str[0]
df.loc[df['Player'].str.split().str.len() == 2, 'LastName'] = df['Player'].str.split().str[-1]
df['PlayerName']=df['FirstName']+str(".")+df['LastName']
#Drop Player column
df.drop(columns=['FirstName','LastName'],inplace=True)
df.to_csv("whole.csv")

print(df.head())
#"""