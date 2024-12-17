import pandas as pd
import numpy as np

class FavouriteBeers():
    """ Class that does various processings of beer style preferences to prepare data for plotting. """
    def __init__(self, beer_preferences):
        """
        @param beer_preferences: pd.DataFrame containing average rating of selected beer styles per year per US state. 
        Format created by aggregate_preferences_years method from Reviews class in reviews_processing.py.
        """
        self.beer_preferences = beer_preferences
        self.year_list = list(np.arange(2004, 2017, 1, dtype=int))
        
    def favbeer_process_for_mapplotting(self):
        """ Format beer ratings in adequate shape for plotting favourite beer of state for each year. """
    
        data = None
        styles = ['IPA', 'Lager', 'Other Ale', 'Pale Ale', 'Pilsner', 'Porter', 'Red/Amber Ale', 'Stout']
        
        # Iterate over all years
        for year in self.year_list:
                
            name_style = [f"{style}_{year}" for style in styles]
            style_year = self.beer_preferences[name_style]
            
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
            
            # Concatenate data for the specific year to the already formed subset
            if data is None:
                data = new_df
            
            else:
                data = pd.concat([data, new_df], axis=0)
        
        return data
    
    def threefavbeer_for_barplotting(self):
        """ Format beer ratings in adequate shape for bar plotting 3 favourite beers of state for each year. """ 
        
        beer_preferences = self.beer_preferences.reset_index()
        
        # Extract columns related to beer styles - all except state
        beer_columns = [col for col in beer_preferences.columns if col != "state"]
        
        
        # Convert from wide to long format
        bp_long = pd.melt(beer_preferences, id_vars=['state'], value_vars=beer_columns, var_name="beer_year", value_name="rating")
        
        # Break beer_year column into columns beer_style and year
        beer_style, year = bp_long['beer_year'].str.split('_', expand=True).T.values
        bp_long['beer_style'] = beer_style
        bp_long['year'] = year
        
        # Find three top ranked styles
        bp_ranked = bp_long.groupby(['state', 'year']).apply(lambda x: x.nlargest(3, 'rating'), include_groups=False).reset_index()
        
        # Extract only columns of interest 
        bp_columns_interest = bp_ranked[['state', 'year', 'rating', 'beer_style']]
        
        return bp_columns_interest
        
        
        
        