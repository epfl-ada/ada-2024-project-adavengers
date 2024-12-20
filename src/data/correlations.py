import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import StandardScaler
import numpy as np
import plotly.express as px

def preprocess_data(data_path, path_winners, year):
    """ 
    Preprocess voting data per age bracket for democrats and republicans - calculate to sum to one. Remove columns that are not in our interest. 
    
    Args:
        @data_path (pathlib.Path): Path to one of files of type year_per_age_region.csv.
        @path_winners (pathlib.Path): Path to party_winners_over_years.csv.
        @year (int): Specific year from which we are extracting data.
        
    Returns:
        @age_range_ohe_drop (pd.DataFrame): DataFrame of described properties. 
        @age_winners (pd.DataFrame): Initial DataFrame with all dropped columns. 
    """
    # Load data
    age = pd.read_csv(data_path, delimiter=';')
    
    # Merge with winners 
    party_winners = pd.read_csv(path_winners)
    party_winners['state'] = party_winners['state'].str.title()
    party_winners = party_winners[party_winners['year'] == year]
    
    age_winners = pd.merge(age, party_winners[['state', 'winner']], how='inner', left_on='state', right_on='state')

    # Drop ages that are out of age range of interest, also division and region 
    age_range = age_winners.drop(columns=['division', 'winner', 'region', 'pop65_democrat', 'pop65_republican'])

    # Normalize percents
    for col_ind in range(1,4): # we have 3 different age groups
        column_name_democrat = age_range.columns[col_ind]
        column_name_republican = age_range.columns[(3 + col_ind)]
        
        age_range[column_name_democrat] = age_range[column_name_democrat] / (age_range[column_name_democrat] + age_range[column_name_republican])
        age_range[column_name_republican] = 1- age_range[column_name_democrat]
    
    # Standard scaling
    age_range = age_range.set_index('state')
    # scaler = StandardScaler()
    # age_range_scaled = scaler.fit_transform(age_range)
    # age_range_scaled_df = pd.DataFrame(age_range_scaled, index=age_range.index, columns=age_range.columns)

    # One hot encode categorical columns
    #age_range_ohe = pd.get_dummies(age_range, columns=['region'])

    # Drop states that have NaN and state column
    age_range_ohe_drop = age_range.dropna(axis=0)
    # age_range_ohe_drop = age_range_ohe_drop.set_index('state', drop=True)
    
    # Adding a year as suffix to all column names
    age_range_ohe_drop.columns = [f"{col}_{year}" for col in age_range_ohe_drop.columns]
    return age_range_ohe_drop, age_winners

def compute_correlation(data):
    """ 
    *This function was part of initial idea, now not used in the code anywhere. *
    Computes correlation on preprocessed data. Extracts pairs of states that had positive/negative correlations.
    
    """
    
    correlation_matrix = data.T.corr()
    
    # Extract upper triangle of correlation matrix 
    upper_triangle = correlation_matrix.where(np.triu(np.ones(correlation_matrix.shape), k=1).astype(bool))
    upper_triangle.index.names = ['State_1']
    upper_triangle.columns.names = ['State_2']
    correlations = upper_triangle.stack().reset_index()
    correlations.columns = ['State_1', 'State_2', 'Corr']
    
    # Filter on positive and negative correlations
    positive_correlations = correlations[correlations['Corr'] > 0]
    positive_correlations_sorted = positive_correlations.sort_values(by='Corr', ascending=False).reset_index(drop=True)
    
    negative_correlations = correlations[correlations['Corr'] < 0]
    negative_correlations_sorted = negative_correlations.sort_values(by='Corr', ascending=True).reset_index(drop=True)
    
    return correlations, positive_correlations_sorted, negative_correlations_sorted

def merge_winners_and_compare(path_winners, year, correlations):
    """ 
    *This function was part of initial idea, now not used in the code anywhere. *
    Merge correlations with winners. 
    """
    
    # Load winners
    party_winners = pd.read_csv(path_winners)
    party_winners['state'] = party_winners['state'].str.title()
    party_winners = party_winners[party_winners['year'] == year]
    
    # Merge winners
    merge_winners_state_1 = pd.merge(correlations, party_winners[['state', 'winner']], how='inner', left_on='State_1', right_on='state')
    merge_winners_state_2 = pd.merge(merge_winners_state_1, party_winners[['state', 'winner']], how='inner', left_on='State_2', right_on='state')
    
    # Drop unnecessary columns and rename some
    merge_winners = merge_winners_state_2.drop(columns=['state_x', 'state_y'])
    merge_winners_rename = merge_winners.rename(columns = {"winner_x" : "Winner_1", "winner_y" : "Winner_2"})
    
    # Compare whether winners are the same
    comparison = (merge_winners_rename['Winner_1'] == merge_winners_rename['Winner_2'])
    
    # Return same and different pairs
    same = merge_winners_rename[comparison].reset_index(drop=True)
    different = merge_winners_rename[~comparison].reset_index(drop=True)
    
    return merge_winners_rename, same, different

def interpolate_votes(voting_data_merged):
    """ 
    Interpolate voting percentages beyond election years. 
    
    Args:
        @voting_data_merged (pd.DataFrame): Voting data in wide format, i.e. columns include year information, e.g. pop18_29_republican_2004.
    
    Returns:
        @final_data (pd.DataFrame): DataFrame containing interpolated columns for years beyond election ones.
    """
    
    # We need these two None because for one state we are going over columns and interpolating them to contain more years
    # data_columns will interpolate for one state and then data_rows will contatenate for all the states together
    data_columns = None
    data_rows = None
    categories = ['pop18_29', 'pop30_44', 'pop45_64']
    list_years = [2004, 2008, 2012, 2016]
    states = voting_data_merged.index
    
    for state in states:
        for category in categories:
            
            # Extract state and cateogry (age bracket for interpolating)
            state_data = voting_data_merged.loc[state]
            categ_year = [f"{category}_democrat_{year}" for year in list_years]
            
            timepoints = state_data.loc[categ_year]
            series = pd.Series(data=timepoints.values, index=list_years)
            
            all_years = range(min(list_years), max(list_years) + 1)
            interpolated = series.reindex(all_years).interpolate(method='linear')
            
            # Republican are 1-Democrat
            rnm_indexes_democr = [f"{category}_democrat_{year}" for year in interpolated.index]
            rnm_indexes_repub = [f"{category}_republican_{year}" for year in interpolated.index]
            interpolated.index = rnm_indexes_democr
            
            republican = 1 - interpolated
            republican.index = rnm_indexes_repub
            
            df_democr = interpolated.to_frame().T
            df_repub = republican.to_frame().T
            
            # Concatenates inteprolated Republican and Democrat columns for one state
            if data_columns is None:
                data_columns = df_democr
            
            else:
                data_columns = pd.concat([data_columns, df_democr], axis=1)
            
            data_columns = pd.concat([data_columns, df_repub], axis=1)
        
        # Concatenating them to all other states
        if data_rows is None:
            data_rows = data_columns
        else:
            data_rows = pd.concat([data_rows, data_columns], axis=0)
        data_columns = None
        
    data_rows['state'] = states
    final_data = data_rows.set_index('state')

    return final_data
    

def merge_voting_by_years(path_to_data=""):
    """ 
    Calls preprocess_data() to merge .csv files corresponding to each election year. Subset of states we're left with are only ones common to all .csv files (only ones that have exit polls results in every election year).
    """
    election_years = [2004, 2008, 2012, 2016]
    path_winners = path_to_data / "data/generated/party_winners_over_years.csv"
    voting_data_merged = []

    for ind_year, year in enumerate(election_years):

        data_path = path_to_data / f"data/{year}_per_age_region.csv"

        processed_data, _ = preprocess_data(data_path, path_winners, year)
        
        if(ind_year==0):
            voting_data_merged = processed_data
        else:
            # Merging is inner - only the subset of states that exist in each year will be taken
            voting_data_merged = pd.merge(voting_data_merged, processed_data, left_on='state', right_on='state')

    return voting_data_merged

# Visualizations

def reshape_data(df, years, age_groups):
    """
    Reshape the data into long format for plotting when State is the index.
    
    Args:
        df (pd.DataFrame): Voting data in long format where year is appended to column name.
        years (list): List of years of interest.
        age_groups (list): ["18_29", "30_44", "45_64"]
        
    Returns:
        pd.DataFrame: In long format.
    """
    
    records = []
    for year in years:
        for age_group in age_groups:
            
            dem_col = f"pop{age_group}_democrat_{year}"
            rep_col = f"pop{age_group}_republican_{year}"
            
            for state in df.index: 
                
                records.append({
                    "State": state,
                    "Age_Group": age_group.replace('_', '-'),
                    "Year": year,
                    "Party": "Democrat",
                    "Value": df.loc[state, dem_col],
                })
                
                records.append({
                    "State": state,
                    "Age_Group": age_group.replace('_', '-'),
                    "Year": year,
                    "Party": "Republican",
                    "Value": df.loc[state, rep_col],
                })
    
    return pd.DataFrame(records)

    
