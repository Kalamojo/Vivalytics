import streamlit as stm
import pandas as pd
from tools.data_filter2 import pos_filt2
from tools.line import line_chart
from tools.api_call import gpt_res3
from tools.stat_search import stat_desc

state = stm.session_state

if "submitted" not in state:
    state.submitted = False

df = pd.read_csv("./resources/persons_all_stats.csv", low_memory=False, memory_map=True)
query_text = stm.text_input("Search sum")

submit_button = stm.button("Let's see", on_click=lambda: state.update(submitted=True))

if state.submitted:
    # Display the output
    filtered_df, pos, worked = pos_filt2(df, query_text)

    stm.write(pos)

    if worked[1]:
	    valid_years = [min(filtered_df["Year"]), max(filtered_df["Year"])]

	    years = stm.slider('Select Year Range', valid_years[0], valid_years[1], value=[valid_years[0], valid_years[1]])

	    print(years)

	    filtered_df = filtered_df[(filtered_df["Year"] >= years[0]) & (filtered_df["Year"] <= years[1])]

	    col1, col2 = stm.columns([1, 1], gap="small")
	    with col1:
	    	config_dict = {
	    		key: stm.column_config.Column(
	    			key,
	    			help=value
	    		) for key, value in stat_desc.items() if key in filtered_df.columns
	    	}
	    	print(config_dict)
	    	stm.write("Hover over a stat in the headers to see a description")
	    	stm.dataframe(
	    	    filtered_df,
	    	    column_config=config_dict
	    	)
	    players = list(set(filtered_df["Player"].to_list()))

	    stats_list = [col for col in filtered_df.columns if col not in ["Year", "League", "Player"]]

	    with col2:
	    	stat = stats_list[0]
	    	if len(stats_list) > 1:
	    	    stat = stm.selectbox("Select a stat", stats_list)
	    	fig = line_chart(players, filtered_df, stat)
	    	stm.plotly_chart(fig, use_container_width=True)
    else:
    	valid_years = [min(filtered_df["Year"]), max(filtered_df["Year"])]

    	years = stm.slider('Select Year Range', valid_years[0], valid_years[1], value=[valid_years[0], valid_years[1]])

    	config_dict = {
    		key: stm.column_config.Column(
    			key,
    			help=value
    		) for key, value in stat_desc.items() if key in filtered_df.columns
    	}
    	print(config_dict)
    	stm.write("Hover over a stat in the headers to see a description")
    	stm.dataframe(
    	    filtered_df,
    	    column_config=config_dict
    	)

    table = filtered_df.head(100).to_string()
    response = gpt_res3(query_text, pos, table)

    stm.write(response)
    