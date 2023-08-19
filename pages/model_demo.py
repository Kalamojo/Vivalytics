import streamlit as stm
import pandas as pd
from tools.data_filter import pos_filt
from tools.line import line_chart

state = stm.session_state

if "submitted" not in state:
    state.submitted = False

df = pd.read_csv("./resources/persons_all_stats.csv")
query_text = stm.text_input("Search sum")

submit_button = stm.button("Let's see", on_click=lambda: state.update(submitted=True))

if state.submitted:
    # Display the output
    filtered_df, pos, worked = pos_filt(df, query_text)
    stm.write(pos)

    if worked[1]:
	    valid_years = [min(filtered_df["Year"]), max(filtered_df["Year"])]

	    years = stm.slider('Select Year Range', valid_years[0], valid_years[1], value=[valid_years[0], valid_years[1]])

	    print(years)

	    filtered_df = filtered_df[(filtered_df["Year"] >= years[0]) & (filtered_df["Year"] <= years[1])]

	    col1, col2 = stm.columns([1, 1], gap="small")
	    with col1:
	    	stm.dataframe(filtered_df)
	    players = list(set(filtered_df["Player"].to_list()))

	    stats_list = [col for col in filtered_df.columns if col not in ["Year", "League", "Player"]]

	    with col2:
	    	stat = stats_list[0]
	    	if len(sta) > 1:
	    	    stat = stm.selectbox("Select a stat", stats_list)
	    	fig = line_chart(players, filtered_df, stat)
	    	stm.plotly_chart(fig, use_container_width=True)
    else:
    	valid_years = [min(filtered_df["Year"]), max(filtered_df["Year"])]

    	years = stm.slider('Select Year Range', valid_years[0], valid_years[1], value=[valid_years[0], valid_years[1]])

    	stm.dataframe(filtered_df)
    