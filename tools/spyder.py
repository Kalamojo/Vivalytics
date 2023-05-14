import pandas as pd
import numpy as np

import matplotlib.pyplot as plt
from matplotlib.patches import Circle, RegularPolygon
from matplotlib.path import Path
from matplotlib.projections.polar import PolarAxes
from matplotlib.projections import register_projection
from matplotlib.spines import Spine
from matplotlib.transforms import Affine2D
import matplotlib.colors as mcolors

import plotly.express as px

stat_desc = {"Gls": "Goals",
             "SoT": "Shots on Target",
             "PrgC": "Progressive Carries",
             "Carries": "Carries",
             "Touches": "Touches",
             "PK": "Penalty Kicks",
             "Cmp": "Passes Completed",
             "Cmp%": "Pass Completion %",
             "KP": "Key Passes",
             "PrgP": "Progessive Passes",
             "TklW": "Tackles Won",
             "Saves": "Saves",
             "Save%": "Save Percentage",
             "GA": "Goals Against",
             "CS": "Clean Sheets",
             "AvgLen": "Average Pass Length",
             "Stp": "Crosses Stopped",
             "Att": "Passes Attempted",
             "Sh/90": "Shots Total/90",
             "SoT/90": "Shots on Target/90",
             "Poss": "Possession%",
             "Tkl+Int": "Tackles + Interceptions",
             "Tkl": "Dribblers Tackled",
             "Int": "Interceptions",
             "Clr": "Clearances",
             "Won": "Arials Won",
             "PrgDist": "Progessive Passing Distance",
             "Pass": "Passes Blocked"
}

def radar_factory(num_vars, frame='circle'):
    """Create a radar chart with `num_vars` axes.

    This function creates a RadarAxes projection and registers it.

    Parameters
    ----------
    num_vars : int
        Number of variables for radar chart.
    frame : {'circle' | 'polygon'}
        Shape of frame surrounding axes.

    """
    # calculate evenly-spaced axis angles
    theta = np.linspace(0, 2*np.pi, num_vars, endpoint=False)
    
    class RadarTransform(PolarAxes.PolarTransform):
        def transform_path_non_affine(self, path):
            # Paths with non-unit interpolation steps correspond to gridlines,
            # in which case we force interpolation (to defeat PolarTransform's
            # autoconversion to circular arcs).
            if path._interpolation_steps > 1:
                path = path.interpolated(num_vars)
            return Path(self.transform(path.vertices), path.codes)
    class RadarAxes(PolarAxes):

        name = 'radar'
        
        PolarTransform = RadarTransform

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            # rotate plot such that the first axis is at the top
            self.set_theta_zero_location('N')

        def fill(self, *args, closed=True, **kwargs):
            """Override fill so that line is closed by default"""
            return super().fill(closed=closed, *args, **kwargs)

        def plot(self, *args, **kwargs):
            """Override plot so that line is closed by default"""
            lines = super().plot(*args, **kwargs)
            for line in lines:
                self._close_line(line)

        def _close_line(self, line):
            x, y = line.get_data()
            # FIXME: markers at x[0], y[0] get doubled-up
            if x[0] != x[-1]:
                x = np.concatenate((x, [x[0]]))
                y = np.concatenate((y, [y[0]]))
                line.set_data(x, y)

        def set_varlabels(self, labels):
            self.set_thetagrids(np.degrees(theta), labels)

        def _gen_axes_patch(self):
            # The Axes patch must be centered at (0.5, 0.5) and of radius 0.5
            # in axes coordinates.
            if frame == 'circle':
                return Circle((0.5, 0.5), 0.5)
            elif frame == 'polygon':
                return RegularPolygon((0.5, 0.5), num_vars,
                                      radius=.5, edgecolor="k")
            else:
                raise ValueError("unknown value for 'frame': %s" % frame)

        def draw(self, renderer):
            """ Draw. If frame is polygon, make gridlines polygon-shaped """
            if frame == 'polygon':
                gridlines = self.yaxis.get_gridlines()
                for gl in gridlines:
                    gl.get_path()._interpolation_steps = num_vars
            super().draw(renderer)
        def _gen_axes_spines(self):
            if frame == 'circle':
                return super()._gen_axes_spines()
            elif frame == 'polygon':
                # spine_type must be 'left'/'right'/'top'/'bottom'/'circle'.
                spine = Spine(axes=self,
                              spine_type='circle',
                              path=Path.unit_regular_polygon(num_vars))
                # unit_regular_polygon gives a polygon of radius 1 centered at
                # (0, 0) but we want a polygon of radius 0.5 centered at (0.5,
                # 0.5) in axes coordinates.
                spine.set_transform(Affine2D().scale(.5).translate(.5, .5)
                                    + self.transAxes)


                return {'polar': spine}
            else:
                raise ValueError("unknown value for 'frame': %s" % frame)

    register_projection(RadarAxes)
    return theta

def norm(num, big, smol):
        return (num-smol)/(big-smol)

def spyder1(players, df, title, stats_list=[], valid_years=[], group="Player", restrict=True):
    plt.style.use('dark_background')
    df = df.fillna(0)

    if len(stats_list) == 0 and group == "Player":
        stats_list = [['Gls', 'Ast', 'G+A', 'G-PK', 'PK', 'PKatt']]

    soccer = ['Gls', 'Ast', 'G+A', 'G-PK', 'PK', 'PKatt']
    #print(soccer)

    player_dfs = [df[df[group]==name] for name in players]
    for i in range(len(player_dfs)):
        if group == "Player" and sum((player_dfs[i][stats_list[i]] == 0).all()) >= 3:
            stats_list[i] = soccer
    
    soccer = list(set(sum(stats_list, [])))
    #print(soccer)

    if restrict:
        if len(valid_years) == 0:
            valid_years = set(player_dfs[0]["Year"].to_list())
            for s in player_dfs[1:]:
                valid_years.intersection_update(s["Year"])

        for i in range(len(players)):
            player_dfs[i] = player_dfs[i][player_dfs[i]["Year"].isin(valid_years)]
    else:
        if len(valid_years) != 0:
            for i in range(len(players)):
                player_dfs[i] = player_dfs[i][player_dfs[i]["Year"].isin(valid_years[i])]

    print("Valid years:", valid_years)
    data = [soccer, (title, [[norm(sum(p_df[col][p_df[col] != 0])/max(len(p_df[col][p_df[col] != 0]), 1), max(df[col]), 0) for col in soccer] for p_df in player_dfs])]
    #print(data)

    N = len(data[0])
    theta = radar_factory(N, frame='polygon')
    print(type(theta), theta)

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
    #plt.ion()
    
    return fig, ax

def spyder2(players, df, title, stats_list=[], valid_years=[], group="Player", margin=True, restrict=True):
    plt.style.use('dark_background')
    df = df.fillna(0)

    if len(stats_list) == 0 and group == "Player":
        stats_list = [['Gls', 'Ast', 'G+A', 'G-PK', 'PK', 'PKatt']]

    soccer = ['Gls', 'Ast', 'G+A', 'G-PK', 'PK', 'PKatt']
    #print(soccer)

    player_dfs = [df[df[group]==name] for name in players]
    for i in range(len(player_dfs)):
        if group == "Player" and sum((player_dfs[i][stats_list[i]] == 0).all()) >= 3:
            stats_list[i] = soccer
    
    soccer = list(set(sum(stats_list, [])))
    #print(soccer)

    if restrict:
        if len(valid_years) == 0:
            valid_years = set(player_dfs[0]["Year"].to_list())
            for s in player_dfs[1:]:
                valid_years.intersection_update(s["Year"])

        for i in range(len(players)):
            player_dfs[i] = player_dfs[i][player_dfs[i]["Year"].isin(valid_years)]
    else:
        if len(valid_years) != 0:
            for i in range(len(players)):
                player_dfs[i] = player_dfs[i][player_dfs[i]["Year"].isin(valid_years[i])]

    print("Valid years:", valid_years)
    data = [soccer, (title, [[norm(sum(p_df[col][p_df[col] != 0])/max(len(p_df[col][p_df[col] != 0]), 1), max(df[col]), 0) for col in soccer] for p_df in player_dfs])]
    #print(data)

    data_df = pd.DataFrame(columns=['category', group.lower(), 'points', 'describe', 'average'])
    ind = 0
    for p_df in player_dfs:
        for col in soccer:
            data_df.loc[ind] = [col, p_df.iloc[0][group], norm(sum(p_df[col][p_df[col] != 0])/max(len(p_df[col][p_df[col] != 0]), 1), max(df[col]), 0), stat_desc[col], round(sum(p_df[col][p_df[col] != 0])/max(len(p_df[col][p_df[col] != 0]), 1), 2)]
            ind += 1

    #print(data_df.isnull().sum())
    #data_df.append(data_df)

    fig = px.line_polar(data_df, r="points",
                        theta="category",
                        color=group.lower(),
                        line_close=True,
                        custom_data=["describe", "average"],
                        template="plotly_dark")

    fig.update_traces(
        hovertemplate="<br>".join([
            "Stat: %{customdata[0]}",
            "Average: %{customdata[1]}"
        ])
    )

    fig.update_polars(angularaxis_showgrid=False,
                      radialaxis_gridwidth=0,
                      gridshape='linear',
                      bgcolor="#494b5a",
                      radialaxis_showticklabels=False
                      )

    #fig.update_layout(paper_bgcolor="#2c2f36",
    #                  width=width)
    if margin:
        fig.update_layout(margin=dict(l=40))

    return fig