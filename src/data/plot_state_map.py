import plotly.express as px
import plotly.graph_objs as go
from plotly.subplots import make_subplots
import pandas as pd

#======================================================================================================
# Functions and Class called in us_states_visualisation.ipynb Notebook for Visualizations
# Examples of use can be found there

def barplot_threefav_styles_compare(fav_three, state1_list, state2_list):
    """ 
    Creates a figure with barplot of top 3 favourite beer styles over years for comparison between predefined pairs of states.
    
    Args:
        @fav_three (pd.DataFrame): DataFrame containing three columns - state, year, rating, beer_style. Each state repeats three times for each year - each entry represents one of top 3 favourite styles. 
        @state1_list (list): List containing state names, representing one element of the pair in plot.
        @state2_list (list):  List containing state names, representing other element of the pair in plot.
        
    Return:
        @fig (go.Figure): Figure - 2 subplots containing bar plots of top 3 favourite beer styles over years for 2 states selected by dropdown button.
    """
    # Create a subplot with 1 row and 2 columns, sharing the Y-axis
    fig = make_subplots(rows=1, cols=2, shared_yaxes=True)

    # Keep track of traces and dropdown options
    total_traces = len(state1_list) * 2
    trace_count = 0
    dropdown_buttons = []
    
    initial_visibility = [False] * total_traces  # *2 for two subplots
    initial_visibility[0] = True
    initial_visibility[1] = True

    for state1, state2 in zip(state1_list, state2_list):
        # Create a visibility array to toggle traces
        visibility = [False] * total_traces

        # Filter data for the two states
        state1_data = fav_three[fav_three['state'] == state1]
        state2_data = fav_three[fav_three['state'] == state2]

        # Add trace for the first state
        fig.add_trace(
            go.Bar(
                x=state1_data['year'],
                y=state1_data['rating'],
                name=f"{state1} Top 3 Beers",
                marker=dict(color=state1_data['beer_style'].astype('category').cat.codes),
                text=state1_data['beer_style'],
                hovertemplate='<b>%{text}</b><br>Rating: %{y}<extra></extra>'
            ),
            row=1, col=1
        )
        visibility[trace_count] = True
        trace_count += 1

        # Add trace for the second state
        fig.add_trace(
            go.Bar(
                x=state2_data['year'],
                y=state2_data['rating'],
                name=f"{state2} Top 3 Beers",
                marker=dict(color=state2_data['beer_style'].astype('category').cat.codes),
                text=state2_data['beer_style'],
                hovertemplate='<b>%{text}</b><br>Rating: %{y}<extra></extra>'
            ),
            row=1, col=2
        )
        visibility[trace_count] = True
        trace_count += 1

        # Add a dropdown button for this state pair
        dropdown_buttons.append({
            'label': f"{state1} & {state2}",
            'method': 'update',
            'args': [
                {'visible': visibility},
                {'title': f"Top 3 Favourite Beer Styles by Rankings over Years: {state1} (left) vs {state2} (right)"}
            ]
        })

    # Configure the layout
    fig.update_layout(
        updatemenus=[{
            'buttons': dropdown_buttons,
            'direction': 'down',
            'showactive': True,
            'x': 0.9,
            'y': 1.22,
            'xanchor': 'center',
            'yanchor': 'top'
        }],
        title="Top 3 Favourite Beer Styles by Rankings over by Years: Wisconsin (left) vs Pennsylvania (right)",
        barmode='group',
        xaxis_title="Year",
        xaxis2_title="Year",
        yaxis_title="Rating",
        height=500,
        width=1200,
        showlegend=False
    )

    # Display the figure
    # Set initial visibility for the first two pairs
    for i in range(len(fig.data)):
        fig.data[i].visible = initial_visibility[i]
    fig.show()
    
    return fig

def barplot_fav_styles_per_state(beer_preferences, data_formatted):
    """ 
    Function creates bar plot of counts of favourite beer styles per state (which can be selected from dropdown menu). 
    Faves are counted in range of 2004 to 2016. 
    
    Args:
        @beer_preferences (pd.DataFrame): DataFrame where each row represents one state and columns are e.g. IPA_2004, IPA_2005, IPA_2006, ... (like this for each one of 8 general beer styles that we selected).
        @data_formatted (pd.DataFrame): DataFrame of [state, rating, beer_style, year] - every row contains top rated beer style for that state and that year.
        
    Returns:
        @fig (go.Figure): Figure displaying counts of how many times beer style was favourite per state (selected through dropdown button) in range 2004-2016.
    """
    
    # Create a list of unique states
    states = beer_preferences.index

    # For each state create a bar plot
    traces = []
    for state in states:
        beer_style_counts = data_formatted[data_formatted.index == state]['beer_style'].value_counts()
        
        trace = go.Bar(x=beer_style_counts.index, y=beer_style_counts.values, name=state, visible=False)
        
        traces.append(trace)
        
    traces[0].visible = True

    layout = go.Layout(
        title="Beer Style Counts by State",
        updatemenus=[{
            'buttons': [
                {
                    'args': [{'visible': [True if i == j else False for i in range(len(states))]}, 
                            {'title': f"Beer Style Counts for {states[j]}"}],
                    'label': state,
                    'method': 'update'
                } for j, state in enumerate(states)
            ],
            'direction': 'down',
            'showactive': True,
        }]
    )

    # Create the figure
    fig = go.Figure(data=traces, layout=layout)

    # Show the figure
    fig.show()
    
    return fig
                      
class PlotStateMap:
    def __init__(self, data_by_state, hover_data, animation_frame, state_names_already_abbreviated=True, title: str = "Favourite",
                 dataMetric: str = "Population"):
        """
        Creates a instance of PlotStateMap class.
        
        Args:
            @ data_by_state (pd.DataFrame): DataFrame where each row represents one state and columns are e.g. IPA_2004, IPA_2005, IPA_2006, ... (like this for each one of 8 general beer styles that we selected).
            @ hover_data (dict): Specifies which columns of DataFrame are going to be displayed as hover data over state.
            @ animation_frame (string): Column along which slider is created. 'years' in this case.
            @ state_names_already_abbreviated (bool): Whether state names are already abbreviated to 2 letter codes.
            @ title (str): Title for the plot.
            @ dataMetric (str): Specifies which column of the DataFrame will be discriminator for colors between states.
        """
        if type(data_by_state) == dict:
            print("dict")
            self.data_by_state_df = pd.DataFrame(list(data_by_state.items()), columns=["State", dataMetric])
        elif type(data_by_state) == pd.DataFrame:
            print("dataframe")
            assert list(data_by_state.columns)[0] == "state"
            #assert list(data_by_state.columns)[1] == dataMetric
            self.data_by_state_df = data_by_state

        if not state_names_already_abbreviated:
            self.data_by_state_df["state"] = self.data_by_state_df["state"].apply(self._state_name_to_code)

        self.title = title
        self.valueType = dataMetric
        self.categ =  self.data_by_state_df[self.valueType].value_counts().index
        
        color_map = ["#EF553B", "#636EFA", "#00CC96", "#AB63FA", "#FFA15A", "#19D3F3", "#B6E880", "#696969"]
        
        self.color_map = {categ: color for categ, color in zip(self.categ, color_map[:len(self.categ)])}
        
        self.category_orders = {self.valueType: self.categ}
        
        self.hover_data = hover_data
        
        self.animation_frame = animation_frame
        
    def plot_map(self):
        """ 
        Plots map of U.S. states where each state is colored differently depending on favourite beer style (the one with highest average rating). Includes the slider for selecting different years. 
        
        Returns:
            @ fig (go.Figure): Figure that displayes what is described above.
            
        """

        fig = px.choropleth(
            self.data_by_state_df,
            locations="state",
            locationmode="USA-states",
            animation_frame=self.animation_frame,
            category_orders = self.category_orders,
            color_discrete_map=self.color_map,
            hover_name="state",                 
            hover_data=self.hover_data, 
            color=self.valueType,
            scope="usa",
            title=self.title,
        )

        fig.update_layout(
            legend=dict(
            title=self.valueType,
            yanchor="top",
            y=1,
            xanchor="left",
            x=1.02
        )
)
        # Show the plot
        fig.show()
        
        return fig
    
    def plot_swing_pattern(self):
        """ 
        Function that does plotting of swing pattern. DataFrame is manually created within the function since there is not many states. Countries with the same swing pattern are colored same way.
        
        Returns:
            @ fig (go.Figure): Described figure.
        """
        
        data = pd.DataFrame({
            'state': ['IN', 'IA', 'FL', 'NV', 'NC', 'OH', 'PA', 'VA', 'WI'],
            'Swing Pattern': ['Democrat only in 2008', 'Republican in 2004 and 2016 // Democrat in 2008 and 2012', 'Republican in 2004 and 2016 // Democrat in 2008 and 2012', 'Republican only in 2004', 'Democrat only in 2008', 'Republican in 2004 and 2016 // Democrat in 2008 and 2012', 'Republican only in 2016', 'Republican only in 2004', 'Republican only in 2016'],
            'state_full': ['Indiana', 'Iowa', 'Florida', 'Nevada', 'North Carolina', 'Ohio', 'Pennsylvania', 'Virginia', 'Wisconsin']})

        # Create the choropleth plot
        fig = px.choropleth(
            data,
            locations='state',
            locationmode='USA-states',
            color='Swing Pattern', 
            hover_name='state_full',
            hover_data=['Swing Pattern'], 
            scope='usa',
            title="Swing States and their Respective Swing Patterns",
        )

        fig.update_layout(width=1000, height=500)

        # Show the plot
        fig.show()
    
        return fig

    def plot_hist(self):
        pass

# Outside of the class
def transform_state_abbreviations(df):
    """
    Transforms state names in the index to abbreviations.
    
    Args:
        @ df (pd.DataFrame): DataFrame which as index column has full U.S. state's names.
       
    Returns:
        @ data (pd.DataFrame): New DataFrame where index column is modified such that there are no full state names but two letter abbreviations. 
    """
    # State abbreviation dictionary
    state_abbreviations = {
        "Alabama": "AL", "Alaska": "AK", "Arizona": "AZ", "Arkansas": "AR",
        "California": "CA", "Colorado": "CO", "Connecticut": "CT", "Delaware": "DE",
        "Florida": "FL", "Georgia": "GA", "Hawaii": "HI", "Idaho": "ID",
        "Illinois": "IL", "Indiana": "IN", "Iowa": "IA", "Kansas": "KS",
        "Kentucky": "KY", "Louisiana": "LA", "Maine": "ME", "Maryland": "MD",
        "Massachusetts": "MA", "Michigan": "MI", "Minnesota": "MN", "Mississippi": "MS",
        "Missouri": "MO", "Montana": "MT", "Nebraska": "NE", "Nevada": "NV",
        "New Hampshire": "NH", "New Jersey": "NJ", "New Mexico": "NM",
        "New York": "NY", "North Carolina": "NC", "North Dakota": "ND",
        "Ohio": "OH", "Oklahoma": "OK", "Oregon": "OR", "Pennsylvania": "PA",
        "Rhode Island": "RI", "South Carolina": "SC", "South Dakota": "SD",
        "Tennessee": "TN", "Texas": "TX", "Utah": "UT", "Vermont": "VT",
        "Virginia": "VA", "Washington": "WA", "West Virginia": "WV",
        "Wisconsin": "WI", "Wyoming": "WY"
    }

    # Replace index with abbreviations
    data = df.copy()
    new_index = data.index.map(lambda x: state_abbreviations.get(x, None))

    if new_index.isnull().any():
        invalid_states = data.index[new_index.isnull()].tolist()
        raise ValueError(f"Invalid state names found: {invalid_states}")

    # Assign the new index and return the dataframe
    data.index = new_index
    return data

