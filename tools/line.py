import pandas as pd
import numpy as np

import matplotlib.pyplot as plt
from matplotlib.patches import Circle, RegularPolygon
from matplotlib.path import Path
from matplotlib.projections.polar import PolarAxes
from matplotlib.projections import register_projection
from matplotlib.spines import Spine
from matplotlib.transforms import Affine2D

def line_chart(players, df, title, valid_years=[], restrict=True):
    plt.style.use('dark_background')

    soccer = ['Gls', 'Ast', 'G+A', 'G-PK', 'PK', 'PKatt']

    player_dfs = [df[df['Player']==name] for name in players]

    if restrict:
        if len(valid_years) == 0:
            valid_years = set(player_dfs[0]["Year"].to_list())
            for s in player_dfs[1:]:
                valid_years.intersection_update(s["Year"])
        print(valid_years)

        for i in range(len(players)):
            player_dfs[i] = player_dfs[i][player_dfs[i]["Year"].isin(valid_years)]
    else:
        if len(valid_years) != 0:
            for i in range(len(players)):
                player_dfs[i] = player_dfs[i][player_dfs[i]["Year"].isin(valid_years[i])]

    data = [soccer, (title, [[norm(sum(p_df[col])/len(p_df[col]), max(df[col]), 0) for col in soccer] for p_df in player_dfs])]

    N = len(data[0])
    theta = radar_factory(N, frame='polygon')
    #print(theta)

    spoke_labels = data.pop(0)
    title, case_data = data[0]

    fig, ax = plt.subplots(figsize=(7, 5), subplot_kw=dict(projection='radar'))
    fig.subplots_adjust(top=0.85, bottom=0.05)

    #ax.set_rgrids([0.2, 0.4, 0.6, 0.8])
    ax.set_title(title,  position=(0.5, 1.1), ha='center')

    for i in range(len(case_data)):
        line = ax.plot(theta, case_data[i])
        ax.fill(theta, case_data[i], alpha=0.25, label=players[i])
    ax.set_varlabels(spoke_labels)
    ax.set_yticklabels([])
    #print("bro")
    if len(players) > 1:
        ax.legend()
    #plt.show()
    return fig