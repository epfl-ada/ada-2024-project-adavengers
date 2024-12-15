import plotly.express as px
import plotly.graph_objs as go
import pandas as pd

#======================================================================================================
# Functions and Classes called in us_states_visualisation.ipynb Notebook
# Examples of use can be found there

def format_data_for_plotting(beer_preferences, year_list):
    """ Format beer ratings in adequate shape for plotting. """
    
    data = None
    states = beer_preferences.index
    styles = ['IPA', 'Lager', 'Other Ale', 'Pale Ale', 'Pilsner', 'Porter', 'Red/Amber Ale', 'Stout']
    
    for year in year_list:
            
        name_style = [f"{style}_{year}" for style in styles]
        style_year = beer_preferences[name_style]
        
        # Handle NaN rows - No Information
        nan_rows = style_year.isna().all(axis=1)
        style_year = style_year.fillna(-1)
        
        # Identify most preferred beer type
        ratings = style_year.max(axis=1)
        favourite_beer = style_year.idxmax(axis=1)
        
        # Reshape it in appropriate form
        beer_style, years = favourite_beer.str.split('_', expand=True).T.values
        new_frame = {"ratings": ratings, "beer_style": beer_style, "years": years}
        new_df = pd.DataFrame(new_frame)
        new_df = new_df.astype('object')
        new_df.loc[nan_rows, ['ratings', 'beer_style']] = "No Information"
        
        if data is None:
            data = new_df
        
        else:
            data = pd.concat([data, new_df], axis=0)
    
    return data

def barplot_fav_styles_per_state(beer_preferences, data_formatted):
    """ 
    Function creates bar plot of counts of favourite beer styles per state (which can be selected from dropdown menu). 
    Faves are counted in range of 2004 to 2016. 
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
                      
class PlotStateMap:
    def __init__(self, data_by_state, hover_data, animation_frame, state_names_already_abbreviated=True, title: str = "Favourite",
                 dataMetric: str = "Population"):
        """
        key is state name, value is what value we want to display for that state
        @type data_by_state: dict
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
        # Plot the map

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

    def plot_hist(self):
        pass

# Outside of the class

def transform_state_abbreviations(df):
    """
    Transforms state names in the index to abbreviations
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

