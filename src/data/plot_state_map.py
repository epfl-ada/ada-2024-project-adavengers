import plotly.express as px
import pandas as pd


class PlotStateMap:
    def __init__(self, data_by_state, state_names_already_abbreviated=True, title: str = "US State Populations",
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
            assert list(data_by_state.columns)[0] == "State"
            assert list(data_by_state.columns)[1] == dataMetric
            self.data_by_state_df = data_by_state

        if not state_names_already_abbreviated:
            self.data_by_state_df["State"] = self.data_by_state_df["State"].apply(self._state_name_to_code)

        self.title = title
        self.valueType = dataMetric

    def plot_map(self):
        # Plot the map

        fig = px.choropleth(
            self.data_by_state_df,
            locations="State",
            locationmode="USA-states",
            color=self.valueType,
            scope="usa",
            title=self.title,
            color_continuous_scale="Viridis"
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
    new_index = df.index.map(lambda x: state_abbreviations.get(x, None))

    if new_index.isnull().any():
        invalid_states = df.index[new_index.isnull()].tolist()
        raise ValueError(f"Invalid state names found: {invalid_states}")

    # Assign the new index and return the dataframe
    df.index = new_index
    return df

