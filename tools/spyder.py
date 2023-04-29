import pandas as pd
import numpy as np

import matplotlib.pyplot as plt
from matplotlib.patches import Circle, RegularPolygon
from matplotlib.path import Path
from matplotlib.projections.polar import PolarAxes
from matplotlib.projections import register_projection
from matplotlib.spines import Spine
from matplotlib.transforms import Affine2D

import plotly.graph_objs as go

def norm(num, big, smol):
        return (num-smol)/(big-smol)

def spyder1(players, df, title, valid_years=[], restrict=True):
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

    plt.style.use('dark_background')

    soccer = ['Gls', 'Ast', 'G+A', 'G-PK', 'PK', 'PKatt']

    player_dfs = [df[df['Player']==name] for name in players]

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
    #plt.ion()
    
    return fig

def spyder2(players, df, title, valid_years=[], restrict=True):
    soccer = ['Gls', 'Ast', 'G+A', 'G-PK', 'PK', 'PKatt']
    player_dfs = [df[df['Player']==name] for name in players]

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

    fig = go.Figure()

    for i, player_df in enumerate(player_dfs):
        data = [norm(sum(player_df[col])/len(player_df[col]), max(df[col]), 0) for col in soccer]
        fig.add_trace(go.Scatterpolar(
            r=data,
            theta=soccer,
            fill='toself',
            name=players[i]
        ))

    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 1]
            )),
        showlegend=True,
        title=title
    )

    return fig