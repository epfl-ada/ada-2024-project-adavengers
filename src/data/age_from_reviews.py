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
        
        return merged_us_state
        