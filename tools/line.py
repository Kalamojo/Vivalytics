import pandas as pd
import numpy as np

import plotly.graph_objs as go

def line_chart(players, df, stat, width=350, restrict=True):
    player_dfs = [df[df['Player']==name].sort_values('Year') for name in players]

    # Create a scatter plot
    fig = go.Figure(
        layout=go.Layout(
            title=stat,
            xaxis=dict(title="Year"),
            yaxis=dict(title=stat)
        )
    )

    for i in range(len(player_dfs)):
        fig.add_trace(go.Scatter(x=player_dfs[i]["Year"], y=player_dfs[i][stat], name=player_dfs[i]["Player"].iloc[0]))


    fig.update_layout(
        autosize=True,
        width=width)

    """
    # Add a range slider to the plot
    fig.update_layout(
        xaxis=dict(
            rangeselector=dict(
                buttons=list([
                    dict(count=1, label="1m", step="month", stepmode="backward"),
                    dict(count=6, label="6m", step="month", stepmode="backward"),
                    dict(count=1, label="YTD", step="year", stepmode="todate"),
                    dict(count=1, label="1y", step="year", stepmode="backward"),
                    dict(step="all")
                ])
            ),
            rangeslider=dict(visible=True),
            type="date"
        )
    )
    #"""
    print(players)
    return fig