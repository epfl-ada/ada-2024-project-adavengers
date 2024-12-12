import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import StandardScaler
import numpy as np

def preprocess_data(data_path, path_winners, year):
    """ Preprocess data - calculate to sum to one. Remove columns that are not in our interest. """
    # Load data
    age = pd.read_csv(data_path, delimiter=';')
    
    # Merge with winners 
    party_winners = pd.read_csv(path_winners)
    party_winners['state'] = party_winners['state'].str.title()
    party_winners = party_winners[party_winners['year'] == year]
    
    age_winners = pd.merge(age, party_winners[['state', 'winner']], how='inner', left_on='state', right_on='state')

    # Drop ages that are out of range of interest, also division and region 
    age_range = age_winners.drop(columns=['division', 'winner', 'region'])

    # Normalize percents
    age_range['pop18_29_democrat'] = age_range['pop18_29_democrat'] / (age_range['pop18_29_democrat'] + age_range['pop18_29_republican'])
    age_range['pop30_44_democrat'] = age_range['pop30_44_democrat'] / (age_range['pop30_44_democrat'] + age_range['pop30_44_republican'])
    age_range['pop45_64_democrat'] = age_range['pop45_64_democrat'] / (age_range['pop45_64_democrat'] + age_range['pop45_64_republican'])
    age_range['pop65_democrat'] = age_range['pop65_democrat'] / (age_range['pop65_democrat'] + age_range['pop65_republican'])

    age_range['pop18_29_republican'] = 1 - age_range['pop18_29_democrat']
    age_range['pop30_44_republican'] = 1 - age_range['pop30_44_democrat']
    age_range['pop45_64_republican'] = 1 - age_range['pop45_64_democrat']
    age_range['pop65_republican'] = 1 - age_range['pop65_democrat']
    
    # Standard scaling
    scaler = StandardScaler()
    age_range_scaled = scaler.fit_transform(age_range)

    # One hot encode categorical columns
    #age_range_ohe = pd.get_dummies(age_range, columns=['region'])

    # Drop states that have NaN and state column
    age_range_ohe_drop = age_range_scaled.dropna(axis=0)
    age_range_ohe_drop = age_range_ohe_drop.set_index('state', drop=True)
    
    return age_range_ohe_drop, age_winners

def compute_correlation(data):
    """ Computes correlation on preprocessed data. """
    
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
    """ Merge correlations with winners. """
    
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
