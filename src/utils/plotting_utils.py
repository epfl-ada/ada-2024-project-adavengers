import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

import plotly.graph_objects as go 
import plotly.express as px
from dash import Dash, dcc, html 
from dash.dependencies import Input, Output
from scipy.stats import pearsonr, spearmanr
from plotly.subplots import make_subplots

def plot_review_count(total_reviews):
    """ Create plot of total number of reviews from U.S. Users per beer style. """
    
    total_reviews_grouped_by_style = total_reviews.groupby(by='general_style').size().reset_index(name='count')
    total_reviews_grouped_by_style.sort_values(by=['count'], ascending=False, inplace=True)
    
    fig = px.bar(total_reviews_grouped_by_style, x='general_style', y='count', title='Count of Reviews by U.S. Users per Beer Style', labels={'general_style': 'Beer Style', 'counts':'Counts'})
    
    fig.show()
    
    return fig

def plot_clustering(x, y, labels, states):
    """ Plots PCA of states clustered based on time series of voting patterns per age groups. """
    fig = go.Figure()

    # Add scatter points
    fig.add_trace(go.Scatter(
        x=x,
        y=y,
    mode='markers+text',
    text=states,
    marker=dict(
        size=10,
        color=labels, 
        colorscale='Viridis',
        showscale=False
        ),
    textposition="top center",
    textfont=dict(size=8),
    name="States"
    ))

    fig.update_layout(
        title="Clustering of States Based on Voting Patterns",
        xaxis_title="PCA Component 1",
        yaxis_title="PCA Component 2",
        template="plotly_white"
    )
    
    fig.show()

def plot_sentiment_posneg_years(df):
    """Plotting the fraction of positive/negative sentiment for each beer style and state over the years 2004-2016"""
    years = sorted(df['year'].unique())
    beer_styles = df['general_style'].unique()

    # Create a subplot layout: 4x2 grid
    fig = make_subplots(
        rows=4, cols=2, 
        subplot_titles=beer_styles,
        #shared_xaxes=True
        vertical_spacing=0.1
    )

    # Create traces for each year and beer style
    traces = []

    for year in years:
        filtered_df = df[df['year'] == year]
        for row_idx, style in enumerate(beer_styles):
            style_df = filtered_df[filtered_df['general_style'] == style]
            row = (row_idx // 2) + 1
            col = (row_idx % 2) + 1
            
            # Add POSITIVE bar
            traces.append(go.Bar(
                x=style_df['state'],
                y=style_df['POSITIVE'],
                name=f'POSITIVE {year}',
                marker_color='green',
                showlegend=(row_idx == 0),  
                visible=(year == years[0])
            ))
            
            # Add NEGATIVE bar
            traces.append(go.Bar(
                x=style_df['state'],
                y=style_df['NEGATIVE'],
                name=f'NEGATIVE {year}',
                marker_color='red',
                showlegend=False,  
                visible=(year == years[0])
            ))

            # Add the traces to the subplot
            fig.add_trace(traces[-2], row=row, col=col)
            fig.add_trace(traces[-1], row=row, col=col)

    # Create slider steps for each year
    steps = []
    for year_idx, year in enumerate(years):
        step = dict(
            method="update",
            label=str(year),  
            args=[
                {"visible": [False] * len(traces)},  
                {"title": f"Sentiment Analysis by Beer Style for {year}"}
            ],
        )
        # Make current year's traces visible
        for trace_idx in range(len(beer_styles) * 2):
            step["args"][0]["visible"][trace_idx + (year_idx * len(beer_styles) * 2)] = True
        steps.append(step)

    # Create slider
    sliders = [dict(
        active=0,  
        currentvalue={"prefix": "Year: "},
        steps=steps
    )]

    # Update layout
    fig.update_layout(
        sliders=sliders,
        barmode='stack',
        height=1200,  
        template="plotly_white",
        title=f"Sentiment Analysis by Beer Style for {years[0]}",
        xaxis_tickangle=-45
        #margin=dict(t=50,b=200,l=50,r=50)
    )
    fig.update_xaxes(tickangle=-45)

    fig.show()

def plot_sentiment_posneg_states(df):
    """Plotting the fraction of positive/negative sentiment for each beer style and state over the years 2004-2016"""
    states = sorted(df['state'].unique())  
    beer_styles = df['general_style'].unique()
    years = sorted(df['year'].unique())

    # Create a subplot layout: 4x2 grid
    fig = make_subplots(
        rows=4, cols=2,
        subplot_titles=beer_styles,
        vertical_spacing=0.1
    )

    # Create traces for each state and beer style
    traces = []

    for state in states:
        filtered_df = df[df['state'] == state]
        for row_idx, style in enumerate(beer_styles):
            style_df = filtered_df[filtered_df['general_style'] == style]
            row = (row_idx // 2) + 1
            col = (row_idx % 2) + 1

            # Add POSITIVE bar
            traces.append(go.Bar(
                x=style_df['year'],
                y=style_df['POSITIVE'],
                name=f'POSITIVE {state}',
                marker_color='green',
                showlegend=(row_idx == 0), 
                visible=(state == states[0]) 
            ))

            # Add NEGATIVE bar
            traces.append(go.Bar(
                x=style_df['year'],
                y=style_df['NEGATIVE'],
                name=f'NEGATIVE {state}',
                marker_color='red',
                showlegend=False,  
                visible=(state == states[0])  
            ))

            # Add the traces to the subplot
            fig.add_trace(traces[-2], row=row, col=col)
            fig.add_trace(traces[-1], row=row, col=col)

    # Create slider steps for each state
    steps = []
    for state_idx, state in enumerate(states):
        step = dict(
            method="update",
            label=state,  
            args=[
                {"visible": [False] * len(traces)},  
                {"title": f"Sentiment Analysis by Beer Style for {state}"}
            ],
        )
        # Make current state's traces visible
        for trace_idx in range(len(beer_styles) * 2):
            step["args"][0]["visible"][trace_idx + (state_idx * len(beer_styles) * 2)] = True
        steps.append(step)

    # Create slider
    sliders = [dict(
        active=0,  
        currentvalue={"prefix": "State: "},
        steps=steps
    )]

    # Update layout
    fig.update_layout(
        sliders=sliders,
        barmode='stack',
        height=1200, 
        template="plotly_white",
        title=f"Sentiment Analysis by Beer Style for {states[0]}",
        xaxis_tickangle=-45,  
    )
    fig.update_xaxes(tickangle=-45)
    fig.show()


def get_beer_styles_data(results, state, beer_style, year_list):
        
        style_names = [f"{beer_style}_{year}" for year in year_list]
        return results.loc[state, style_names]

class BeerStyleTrendsDashApp:
    def __init__(self, beer_preferences, winners, get_beer_styles_data, kind):
        
        # Initialize the App
        self.app = Dash(__name__)
        self.beer_preferences = beer_preferences
        self.styles = ['IPA', 'Lager', 'Other Ale', 'Pale Ale', 'Pilsner', 'Porter', 'Red/Amber Ale', 'Stout']
        self.election_winners_by_state = winners.groupby('state').apply(lambda group: dict(zip(group['year'], group['winner']))).to_dict()
        self.year_list = list(np.arange(2004, 2017, 1, dtype=int))
        self.election_years = [2004, 2008, 2012, 2016]
        self.get_beer_styles_data = get_beer_styles_data
        self.kind = kind
        
        self.setup_layout()
        
        
        
    def setup_layout(self):
        
        # Build the layout for the app
        pre_def_pearson, _ = pearsonr(self.get_beer_styles_data(self.beer_preferences, 'New York', 'IPA', self.year_list), self.get_beer_styles_data(self.beer_preferences, 'California', 'IPA', self.year_list))
        pre_def_spearman, _ = spearmanr(self.get_beer_styles_data(self.beer_preferences, 'New York', 'IPA', self.year_list), self.get_beer_styles_data(self.beer_preferences, 'California', 'IPA', self.year_list))
        
        self.app.layout = html.Div([
            html.H1(f"Beer Style {self.kind} by State", style={"color": "white"}),

            html.Div([
                html.Div([
                    html.Div("State 1:", style={"color": "white"}),
                    dcc.Dropdown(id='state1-dropdown',
                         options=[{'label': state, 'value': state} for state in self.beer_preferences.index],
                         value='New York',
                         style={'width': '100%'})
                        ], style={'width': '30%'}),  

            html.Div([
                html.Div("State 2:", style={"color": "white"}),
                dcc.Dropdown(id='state2-dropdown',
                         options=[{'label': state, 'value': state} for state in self.beer_preferences.index],
                         value='California',
                         style={'width': '100%'})
                        ], style={'width': '30%'}),  

            html.Div([
                html.Div("Beer style:", style={"color": "white"}),
                dcc.Dropdown(id='style-dropdown',
                    options=[{'label': style, 'value': style} for style in self.styles],
                    value='IPA',  
                    style={'width': '100%'})
                    ], style={'width': '30%'}),  
            ], style={'display': 'flex', 'flexDirection': 'row', 'justifyContent': 'space-between', 'marginBottom': '20px'}),

            html.Div([
                html.Div([
                    html.Div(f"Pearson Correlation: {pre_def_pearson:.2f}", id='pearson-output',
                     style={'margin': '10px', 'fontWeight': 'bold', "color": "white"})
                    ], style={'width': '48%'}),  

                html.Div([
                    html.Div(f"Spearman Correlation: {pre_def_spearman:.2f}", id='spearman-output',
                     style={'margin': '10px', 'fontWeight': 'bold', "color": "white"})
                    ], style={'width': '48%'}),  
            ], style={'display': 'flex', 'flexDirection': 'row', 'justifyContent': 'space-between'}),
    
            dcc.Graph(id='beer-ratings-graph')
            ])
        
        self.setup_callbacks()
    
    def setup_callbacks(self):
        
        @self.app.callback(
        [
            Output('beer-ratings-graph', 'figure'),
            Output('pearson-output', 'children'),
            Output('spearman-output', 'children')
        ],
        [
            Input('state1-dropdown', 'value'),
            Input('state2-dropdown', 'value'),
            Input('style-dropdown', 'value')
        ]
        )
        def update_graph_and_correlation(state1, state2, style):
            # Beer ratings
            trace_state1 = go.Scatter(x=self.year_list, y=self.get_beer_styles_data(self.beer_preferences, state1, style, self.year_list), mode='lines', name=f"{state1}_{style}")
            trace_state2 = go.Scatter(x=self.year_list, y=self.get_beer_styles_data(self.beer_preferences, state2, style, self.year_list), mode='lines', name=f"{state2}_{style}")

            # Election traces
            election_results_state_1 = go.Scatter(
                x=self.election_years,
                y=self.get_beer_styles_data(self.beer_preferences, state1, style, self.election_years),
                mode='markers',
                marker=dict(size=10, color=['blue' if self.election_winners_by_state[state1][year] == 'Democrat' else 'red' for year in self.election_years]),
                hovertext=[self.election_winners_by_state[state1][year] for year in self.election_years], hoverinfo='text',
                showlegend=False)
    
            election_results_state_2 = go.Scatter(
                x=self.election_years,
                y=self.get_beer_styles_data(self.beer_preferences, state2, style, self.election_years),
                mode='markers',
                marker=dict(size=10, color=['blue' if self.election_winners_by_state[state2][year] == 'Democrat' else 'red' for year in self.election_years]),
                hovertext=[self.election_winners_by_state[state2][year] for year in self.election_years], 
                hoverinfo='text',
                showlegend=False)
    
    
            pearsoncorr, _ = pearsonr(self.get_beer_styles_data(self.beer_preferences, state1, style, self.year_list), self.get_beer_styles_data(self.beer_preferences, state2, style, self.year_list))
            spearmancorr, _ = spearmanr(self.get_beer_styles_data(self.beer_preferences, state1, style, self.year_list), self.get_beer_styles_data(self.beer_preferences, state2, style, self.year_list))
    
            pearson_text = f"Pearson Correlation: {pearsoncorr:.2f}"
            spearman_text = f"Spearman Correlation: {spearmancorr:.2f}"
    
            figure = {
                'data': [trace_state1, trace_state2, election_results_state_1, election_results_state_2],
                'layout': go.Layout(
                    title=f"Beer Style {self.kind}: {style}",
                    xaxis={'title': 'Year'},
                    yaxis={'title': self.kind},
                    showlegend=True
                )
            }
    
            return figure, pearson_text, spearman_text
    
    def run(self):
        # Run App
        self.app.run_server(mode='inline')


def plot_beer_pref_trends(beer_ratings, winners, states):
    """ For the specified states plot beer trends for each beer styles. """
    styles = ['IPA', 'Lager', 'Other Ale', 'Pale Ale', 'Pilsner', 'Porter', 'Red/Amber Ale', 'Stout']
    year_list = list(np.arange(2004, 2017, 1, dtype=int))

    # Identify the states of interest
    states_interest = beer_ratings.loc[states]
    
    # Modify winners to be in adequate form for plotting
    winners_interest = winners.loc[states]
    election_winners_by_state = winners_interest.groupby('state').apply(lambda group: dict(zip(group['year'], group['winner']))).to_dict()
    election_colors = {'Republican': 'red', 'Democrat': 'blue'}
    election_years = [2004, 2008, 2012, 2016]

    # Create grid for plotting 
    _, axes = plt.subplots(4, 2, figsize=(12, 16))
    axes = axes.flatten()

    for i, style in enumerate(styles):
        
        # Set the ax where we are plotting
        ax = axes[i]
        
        # Identify the styles
        style_names = [f"{style}_{year}" for year in year_list]
        beer_styles = states_interest[style_names]
        
        for index, row in beer_styles.iterrows():
            ax.plot(year_list, row, label=f"{index}")
            
            # Add winners for election years
            for election_year in election_years:
                winner = election_winners_by_state[index].get(election_year)
                ax.scatter(election_year, row.iloc[year_list.index(election_year)], color=election_colors[winner], s=50)
                ax.text(election_year, row.iloc[year_list.index(election_year)] + 0.005, winner,
                    color=election_colors[winner], fontsize=8, ha='center')         
            
        ax.set_title(f"Trend in average ratings of {style} beer preferences")
        ax.set_xlabel('Years')
        ax.set_ylabel('Average ratings')
        ax.legend(title='States', fontsize=8, loc='best')
        ax.grid(True)
        
    # Adjust layout
    plt.tight_layout()
    plt.show()