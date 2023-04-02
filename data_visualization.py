import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

data_file_age_group = r"Esophageal Cancer - age group.csv"
data_file_chronological = r"Esophageal Cancer - all age.csv"


# plot gender difference of incidence


class Visualization(object):
    def __init__(
            self,
            data_file_age_group=r"Esophageal Cancer - age group.csv",
            data_file_chronological=r"Esophageal Cancer - all age.csv"
    ):
        self.data_age_group = pd.read_csv(data_file_age_group)
        self.data_chronological = pd.read_csv(data_file_chronological)

    def plot_0(self):
        fig = make_subplots(
            rows=2,
            cols=2,
            start_cell="top-left",
            subplot_titles=("China", "Taiwan (Province of China)", "Global", "Japan"),
            shared_xaxes=True,
            shared_yaxes=True,
            x_title='age',
            y_title='incidence per 100k, 2019',
        )
        _data = self.data_age_group.loc[(self.data_age_group['measure_name'] == 'Incidence') & (self.data_age_group['metric_name'] == 'Percent') & (self.data_age_group['cause_name'] == 'Esophageal cancer')]

        def _add_sub_trace(location_name, sex_name, col, row, multiplier=100000):
            _tmp = _data.loc[(_data['location_name'] == location_name) & (_data['sex_name'] == sex_name)]
            age_mapping = {
                '20-24 years': 20,
                '25-29 years': 25,
                '30-34 years': 30,
                '35-39 years': 35,
                '40-44 years': 40,
                '45-49 years': 45,
                '50-54 years': 50,
                '55-59 years': 55,
                '60-64 years': 60,
                '65-69 years': 65,
                '70-74 years': 70,
                '75+ years': 75,
            }
            # x = [20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75]
            x = list(age_mapping)
            y = [_tmp.loc[_tmp['age_name'] == name].iloc[0]['val'] * multiplier for name in age_mapping]

            fig.add_trace(go.Scatter(x=x, y=y, mode='lines+markers', name=f'{location_name.split(" ")[0]} {sex_name}'), row=row, col=col)

            fig.add_annotation(x=x[-1], y=y[-1], ax=20, text=f'{location_name.split(" ")[0]} {sex_name}', showarrow=False, row=row, col=col)

        _add_sub_trace(location_name='China', sex_name='Male', col=1, row=1)
        _add_sub_trace(location_name='China', sex_name='Female', col=1, row=1)

        _add_sub_trace(location_name='Global', sex_name='Male', col=1, row=2)
        _add_sub_trace(location_name='Global', sex_name='Female', col=1, row=2)

        _add_sub_trace(location_name='Taiwan (Province of China)', sex_name='Male', col=2, row=1)
        _add_sub_trace(location_name='Taiwan (Province of China)', sex_name='Female', col=2, row=1)

        _add_sub_trace(location_name='Japan', sex_name='Male', col=2, row=2)
        _add_sub_trace(location_name='Japan', sex_name='Female', col=2, row=2)

        fig.update_layout(
            showlegend=False,
            hovermode='x',
            yaxis={'range': [0, 40]},
            yaxis2={'range': [0, 40]},
            yaxis3={'range': [0, 40]},
            yaxis4={'range': [0, 40]},
            xaxis={'spikemode': 'across+toaxis'},
            xaxis2={'spikemode': 'across+toaxis'},
            xaxis3={'spikemode': 'across+toaxis'},
            xaxis4={'spikemode': 'across+toaxis'},
            title_text="Esophageal Cancer Incidence per 100,000",
        )
        fig.show()
        fig.write_html("plot_0.html", full_html=False, include_plotlyjs='cdn')
        fig.write_json('plot_0.json', pretty=True)
        return fig

    def plot_1(self):
        data = pd.read_csv(r"C:\Users\Bolun\Documents\Obsidian\Course Notes\Trimester 2\AE6813 Health Economics\Assignment\Esophageal Cancer - China Daly Chrono.csv")
        _data = data.loc[(data['measure_name'] == 'DALYs (Disability-Adjusted Life Years)') & (data['metric_name'] == 'Percent') & (data['cause_name'] == 'Esophageal cancer')]

        years = list(range(1999, 2020))
        age_mapping = {
            '20-24 years': 20,
            '25-29 years': 25,
            '30-34 years': 30,
            '35-39 years': 35,
            '40-44 years': 40,
            '45-49 years': 45,
            '50-54 years': 50,
            '55-59 years': 55,
            '60-64 years': 60,
            '65-69 years': 65,
            '70-74 years': 70,
            '75+ years': 75,
        }

        def make_figure(location_name):
            male_tmp = _data.loc[(_data['location_name'] == location_name) & (_data['sex_name'] == 'Male')]
            female_tmp = _data.loc[(_data['location_name'] == location_name) & (_data['sex_name'] == 'Female')]

            fig_dict = {
                "data": [],
                "layout": {
                    'title': f'DALY of Esophageal Cancer {location_name}',
                    'xaxis': {"title": "Years"},
                    'yaxis': {"title": "DALY Percentage", 'range': [0, 0.05], 'tickformat': '.2%'},
                    'hovermode': 'x unified',
                    'updatemenus': [{
                        "buttons": [
                            {
                                "args": [None, {"frame": {"duration": 500, "redraw": False}, "fromcurrent": True, "transition": {"duration": 300, "easing": "quadratic-in-out"}}],
                                "label": "Play",
                                "method": "animate"
                            },
                            {
                                "args": [[None], {"frame": {"duration": 0, "redraw": False}, "mode": "immediate", "transition": {"duration": 0}}],
                                "label": "Pause",
                                "method": "animate"
                            }
                        ],
                        "direction": "left",
                        "pad": {"r": 10, "t": 87},
                        "showactive": False,
                        "type": "buttons",
                        "x": 0.1,
                        "xanchor": "right",
                        "y": 0,
                        "yanchor": "top"
                    }],
                    'sliders': [{
                        "active": 0,
                        "yanchor": "top",
                        "xanchor": "left",
                        "currentvalue": {
                            "font": {"size": 20},
                            "prefix": "Year:",
                            "visible": True,
                            "xanchor": "right"
                        },
                        "transition": {"duration": 300, "easing": "cubic-in-out"},
                        "pad": {"b": 10, "t": 50},
                        "len": 0.9,
                        "x": 0.1,
                        "y": 0,
                        "steps": []
                    }]
                },
                "frames": []
            }

            for year in years:
                frame = {"data": [], "name": f'DALY {year}'}

                x = [_.split(" ")[0] for _ in age_mapping]
                male_y = [male_tmp.loc[(male_tmp['age_name'] == name) & (male_tmp['year'] == year)].iloc[0]['val'] for name in age_mapping]
                female_y = [female_tmp.loc[(female_tmp['age_name'] == name) & (female_tmp['year'] == year)].iloc[0]['val'] for name in age_mapping]

                male_data_dict = {
                    "x": x,
                    "y": male_y,
                    "mode": 'lines+markers',
                    "name": f'{location_name.split(" ")[0]} Male'
                }

                female_data_dict = {
                    "x": x,
                    "y": female_y,
                    "mode": 'lines+markers',
                    "name": f'{location_name.split(" ")[0]} Female'
                }

                if year == years[-1]:
                    fig_dict['data'].append(male_data_dict)
                    fig_dict['data'].append(female_data_dict)

                frame["data"].append(male_data_dict)
                frame["data"].append(female_data_dict)
                fig_dict["frames"].append(frame)
                fig_dict['layout']['sliders'][0]["steps"].append(
                    {
                        "args": [
                            [f'DALY {year}'],
                            {"frame": {"duration": 300, "redraw": False},
                             "mode": "immediate",
                             "transition": {"duration": 300}}
                        ],
                        "label": year,
                        "method": "animate"
                    }
                )

            return fig_dict

        fig = go.Figure(make_figure(location_name='China'))

        fig.show()
        fig.write_html("plot_1.html", full_html=False, include_plotlyjs='cdn')
        fig.write_json('plot_1.json', pretty=True)
        return fig

    def plot_2(self):
        years = list(range(1999, 2020))
        age_mapping = {
            '20-24 years': 20,
            '25-29 years': 25,
            '30-34 years': 30,
            '35-39 years': 35,
            '40-44 years': 40,
            '45-49 years': 45,
            '50-54 years': 50,
            '55-59 years': 55,
            '60-64 years': 60,
            '65-69 years': 65,
            '70-74 years': 70,
            '75+ years': 75,
        }

        fig = make_subplots(
            rows=2,
            cols=2,
            subplot_titles=['China DALY', 'China Incidence', 'Global DALY', 'Global Incidence'],
            shared_xaxes=True,
        )

        def make_figure(location_name, measure, row, col):
            data = pd.read_csv(fr"C:\Users\Bolun\Documents\Obsidian\Course Notes\Trimester 2\AE6813 Health Economics\Assignment\Esophageal Cancer - {location_name} Daly Chrono.csv")
            _data = data.loc[(data['measure_name'] == measure) & (data['metric_name'] == 'Percent') & (data['cause_name'] == 'Esophageal cancer')]
            male_tmp = _data.loc[(_data['location_name'] == location_name) & (_data['sex_name'] == 'Male')]
            female_tmp = _data.loc[(_data['location_name'] == location_name) & (_data['sex_name'] == 'Female')]

            frames = list(fig.frames) if fig.frames else []
            have_frame = True if frames else False

            for _ in range(len(years)):
                year = years[_]

                x = [_.split(" ")[0] for _ in age_mapping]
                male_y = [male_tmp.loc[(male_tmp['age_name'] == name) & (male_tmp['year'] == year)].iloc[0]['val'] for name in age_mapping]
                female_y = [female_tmp.loc[(female_tmp['age_name'] == name) & (female_tmp['year'] == year)].iloc[0]['val'] for name in age_mapping]
                diff_y = [male_tmp.loc[(male_tmp['age_name'] == name) & (male_tmp['year'] == year)].iloc[0]['val'] - female_tmp.loc[(female_tmp['age_name'] == name) & (female_tmp['year'] == year)].iloc[0]['val'] for name in age_mapping]

                male_trace = go.Scatter(x=x, y=male_y, mode='lines+markers', name=f'{location_name.split(" ")[0]} Male')
                female_trace = go.Scatter(x=x, y=female_y, mode='lines+markers', name=f'{location_name.split(" ")[0]} Female')
                diff_trace = go.Scatter(x=x, y=diff_y, mode='lines+markers', name=f'{location_name.split(" ")[0]} Diff')

                new_traces = [male_trace, female_trace, diff_trace] if measure == 'Incidence' else [male_trace, female_trace]

                if year == years[-1]:
                    for trace in new_traces:
                        fig.add_trace(trace, row=row, col=col)

                if have_frame:
                    frame = fig.frames[_]
                    data = list(frame.data)
                    traces = list(frame.traces)

                    data.extend(new_traces)
                    traces.extend([traces[-1] + 1 + i for i in range(len(new_traces))])

                    frame.data = data
                    frame.traces = traces
                else:
                    frame = go.Frame(
                        data=new_traces,
                        traces=[i for i in range(len(new_traces))],
                        name=f'{year}'
                    )

                    frames.append(frame)

            fig.frames = frames

            return frames

        make_figure(location_name='China', measure='DALYs (Disability-Adjusted Life Years)', row=1, col=1)
        make_figure(location_name='Global', measure='DALYs (Disability-Adjusted Life Years)', row=2, col=1)
        make_figure(location_name='China', measure='Incidence', row=1, col=2)
        make_figure(location_name='Global', measure='Incidence', row=2, col=2)

        slider = dict(
            active=0,
            yanchor="top",
            xanchor="left",
            currentvalue={
                "visible": True,
                "xanchor": "right"
            },
            # pad={"b": 10, "t": 50},
            steps=[{"args": [[f'{year}'], {"frame": {"duration": 100, "redraw": False}, "mode": "immediate", "transition": {"duration": 0}}], "label": year, "method": "animate"} for year in years]
        )

        fig.update_layout(
            showlegend=False,
            xaxis={"title": "DALY of Esophageal Cancer"},
            xaxis2={"title": "Incidence Rate of Esophageal Cancer"},
            yaxis={"title": "DALY", 'range': [0, 0.05], 'tickformat': '.2%'},
            yaxis2={"title": "Incidence", 'range': [0, 0.0006], 'tickformat': '.3%', 'side': 'right'},
            yaxis3={"title": "DALY", 'range': [0, 0.05], 'tickformat': '.2%'},
            yaxis4={"title": "Incidence", 'range': [0, 0.0006], 'tickformat': '.3%', 'side': 'right'},
            hovermode='x unified',
            # updatemenus=[dict(type='buttons', showactive=False, x=0.1, xanchor="right", y=0, yanchor="top", pad={"b": 10, "t": 50}, buttons=[dict(label='Play', method='animate', args=[None, dict(frame=dict(duration=100, redraw=False), transition=dict(duration=0), fromcurrent=True, mode='immediate')])])],
            sliders=[slider]
        )
        fig.show()
        fig.write_html("plot_2.html", full_html=False, include_plotlyjs='cdn')
        fig.write_json('plot_2.json', pretty=True)
        return fig

    def plot(self):
        # plot gender difference of incidence
        # self.plot_0()
        # self.plot_1()
        self.plot_2()


if __name__ == '__main__':
    _ = Visualization(
        data_file_age_group=r"C:\Users\Bolun\Documents\Obsidian\Course Notes\Trimester 2\AE6813 Health Economics\Assignment\Esophageal Cancer - age group.csv",
        data_file_chronological=r"C:\Users\Bolun\Documents\Obsidian\Course Notes\Trimester 2\AE6813 Health Economics\Assignment\Esophageal Cancer - all age.csv",
    )
    _.plot()
