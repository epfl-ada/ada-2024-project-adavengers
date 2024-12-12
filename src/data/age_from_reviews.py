import pathlib

import pandas as pd

class AgeFromReviews:
    """
    Pipeline for generating Age column from Users and their Reviews. 
    """
    def __init__(self, users_path, reviews_path):
        """
        Initialize AgeFromReviews with users path and reviews path in .csv.
        @param users_path: users .csv file path
        @param reviews_path: reviews .csv file path
        """
        self.users_path = users_path
        self.reviews_path = reviews_path
        
    def make_age_state_cols(self):
        """
        Function that merges user and reviews dataframes and adds age and state columns. Users outside US are filtered out. 
        Age is approximated as 21 + (date_review - date_joining). -> 
        """
        
        # Load data
        users_df = pd.read_csv(self.users_path)
        reviews_df = pd.read_csv(self.reviews_path)
        
        # Merge 2 dfs and approximate age
        merged_df = pd.merge(users_df[['user_id', 'joined', 'location']], reviews_df, on='user_id', how='inner')
        merged_df['age'] = (merged_df['date'] - merged_df['joined']) / (365.25 * 24 * 60 * 60) + 21
        
        # Filter out only users that come from US
        merged_df = merged_df.dropna(subset=['location'])
        merged_us = merged_df[merged_df['location'].str.startswith('United States')]
        
        merged_us_state = merged_us.copy()
        merged_us_state['state'] = merged_us['location'].str.split(',').str[-1].str.strip()
        
        # Add another column year
        column = pd.to_datetime(merged_us_state['date'], unit='s').dt.year
        merged_us_state['year'] = column
        
        return merged_us_state
    
    def filter_beer_type(self):
        """
        Filter beer types of interest. 
        Particularly: Pale Ale, Red/Amber Ale, IPA, Other Ales, Lager, Pilsener, Stout, Porter.
        """
        
        us_users_reviews = self.make_age_state_cols()
        
        list_store_pa = set()
        list_store_lager = set()
        list_store_ipa = set()
        list_store_raa = set()
        list_store_stout = set()
        list_store_porter = set()
        list_store_ale = set()
        list_store_pilsener = set()

        for style in us_users_reviews['style']:
            style_split = style.split(' ')
    
            # Pale Ale
            if 'Ale' in style_split and 'Pale' in style_split and 'India' not in style_split:
                list_store_pa.add(style)
    
            # Lager
            if 'Lager' in style_split:
                list_store_lager.add(style)
        
            # IPA
            if 'IPA' in style_split or ('India' in style_split and 'Pale' in style_split and 'Ale' in style_split):
                list_store_ipa.add(style)

            # Amber or Red Ale
            if 'Ale' in style_split and ('Amber' in style_split or 'Red' in style_split):
                list_store_raa.add(style)

            # Stout
            if 'Stout' in style_split:
                list_store_stout.add(style)

            # Porter
            if 'Porter' in style_split:
                list_store_porter.add(style)

            # Pilsener
            if 'Pilsener' in style_split:
                list_store_pilsener.add(style)
                
            # Other Ale
            if 'Ale' in style_split:
                list_store_ale.add(style)
            
        # Remove IPA, Pale Ale and Red/Amber Ale from other Ales
        list_store_ale -= list_store_ipa
        list_store_ale -= list_store_raa
        list_store_ale -= list_store_pa
        
        # Add all lists together
        all_analyzed_reviews = list_store_pa | list_store_ale | list_store_lager | list_store_raa | list_store_stout | list_store_porter | list_store_ipa | list_store_pilsener
        
        # Filter to keep only the reviews which style is in this predefined set
        filtered_reviews = us_users_reviews[us_users_reviews['style'].isin(all_analyzed_reviews)]
        
        # We want to add general style category - for later aggregation
        style_mapping = {
            **dict.fromkeys(list_store_pa, 'Pale Ale'),
            **dict.fromkeys(list_store_ale, 'Other Ale'),
            **dict.fromkeys(list_store_lager, 'Lager'),
            **dict.fromkeys(list_store_raa, 'Red/Amber Ale'),
            **dict.fromkeys(list_store_stout, 'Stout'),
            **dict.fromkeys(list_store_porter, 'Porter'),
            **dict.fromkeys(list_store_ipa, 'IPA'),
            **dict.fromkeys(list_store_pilsener, 'Pilsner')
        }
        
        filt_new = filtered_reviews.copy()
        filt_new['general_style'] = filtered_reviews['style'].apply(lambda x: style_mapping.get(x, 'Other'))
        
        return filt_new
    
    def aggregate_preferences_year(self, years):
        """
        Aggregate preferences for the specified year for beer styles that we identified.
        """
        
        # Add general style to reviews from US reviews
        reviews_style = self.filter_beer_type()
        
        # Group by year, state and style for average rating 
        results_groupped_by = reviews_style.groupby(by=['state', 'year', 'general_style'], group_keys=False).agg(avg_rating=pd.NamedAgg(column='rating', aggfunc='mean')).reset_index()
        
        # Overlapping states for all years 
        states = ['New York', 'California', 'New Hampshire', 'Wisconsin', 'Nevada', 'Pennsylvania', 'Virginia', 'Ohio', 'Florida', 'North Carolina', 'Arizona', 'Indiana']
        
        # Extract reviews coming from these states and from the specified year 
        filter_states = results_groupped_by[results_groupped_by['state'].isin(states)]
        
        # For mergining
        merged_df = None
        
        for year in years:
            
            filter_year = filter_states[filter_states['year'] == year].drop(columns=['year'])
            filter_year_pivot = pd.pivot_table(filter_year, values='avg_rating', index='state', columns='general_style')
        
            # Rename columns
            columns = filter_year_pivot.columns
            filter_year_pivot.columns = [f"{col}_{year}" for col in columns] 
            
            if merged_df is None:
                merged_df = filter_year_pivot
                
            else:
                # Merge with the existing merged_df on 'state'
                merged_df = pd.merge(merged_df, filter_year_pivot, on='state', how='outer')
            
        
        return merged_df 
        
        
        
        
        