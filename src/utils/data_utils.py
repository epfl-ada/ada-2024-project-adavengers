import os
import pandas as pd
import pathlib

# ================================================================================================

# This is utils script for parsing reviews data into pandas DF and saving it as .csv
# Also, it contains processing pipeline for generating .csv for presidental data

# ================================================================================================

# Specify file path where the reviews are located
FILE_PATH = "/content/BeerReviews/BeerAdvocate/reviews_beers_adv.txt"
NAME = "reviews_df.csv"

# Specify file path where the original presidental data will be stored
FILE_PATH_PRESIDENT = pathlib.Path("data") / "1976-2020-president.csv"

def sum_the_votes(parties, data):
    """
    Sum all the votes from the candidates coming from the same party. 
    
    Args:
        parties (array): Array of containing all the parties. 
        data (dataframe): President data.
        
    
    """ 
    pr_df_filt = data.copy()
    
    for party in parties:
        
        # Group by state and year and then aggregate by summing all the votes for the same party
        pr_df_filt_party = pr_df_filt[pr_df_filt['party_simplified'] == party].groupby(['state', 'year']).agg({'candidatevotes' : 'sum', 'totalvotes' : 'first'}).reset_index()
        pr_df_filt_party['party_simplified'] = party
        
        pr_df_non_party = pr_df_filt[pr_df_filt['party_simplified'] != party]
        pr_df_filt = pd.concat([pr_df_non_party, pr_df_filt_party])  
        
    return pr_df_filt      
        
def extract_president_data(file_path):
    """
    Extract president data in the adequate format, i.e. to have which party won each year in every state (from number of votes per each candidate per state every election year). 
    
    The function will generate two .csv file.
    1. With information of percentage per each party per state per year and a column winner corresponding to that years winner (2001-2017) - party_winners_over_years.csv.
    2. State with status DEMOCRAT, REPUBLICAN, SWING - party_winners.csv.
    
    Args:
        file_path (pathlib Path): Path to the president data file.
    """
    
    # Load president data
    president_data = pd.read_csv(file_path)
    
    # Our beer reviews data contains data from 2001 to 2017 - we need to filter out those election years
    # We are keeping columns: year, state, party_simplified, candidate votes and total votes
    pr_df_filt = president_data[(president_data['year'] >= 2001) & (president_data['year'] <= 2017)]
    relevant_columns = ['year', 'state', 'party_simplified', 'candidatevotes', 'totalvotes']
    pr_df_filt = pr_df_filt[relevant_columns]
    
    parties = pr_df_filt['party_simplified'].unique()
    
    # Sum all the votes
    pr_df_combined = sum_the_votes(parties, pr_df_filt)  
    
    # Create a column percentage which will have percentage of votes each candidate got
    pr_df_combined['percentage'] = (pr_df_combined['candidatevotes'] / pr_df_combined['totalvotes']) * 100
    pr_df_percentage = pr_df_combined.drop(['candidatevotes', 'totalvotes'], axis=1, inplace=False)
    
    # We want to create another column - winner - which identifies what party won in that specifc year
    pr_df = pd.pivot_table(pr_df_percentage, columns=['party_simplified'], values='percentage', index=['state', 'year']).reset_index()
    winner = pr_df[['DEMOCRAT', 'OTHER', 'LIBERTARIAN', 'REPUBLICAN']].idxmax(axis=1)
    pr_df['winner'] = winner
    
    # Save this df with winners and percentages
    pr_df.to_csv('party_winners_over_years.csv')
    
    # Based on winners classify states in 3 categories - SWING, DEMOCRAT, REPUBLICAN
    # We consider a party swing if it changed from one party to another (over our period of interest)
    states = list(pr_df['state'].unique())
    party = []
    
    for state in states:
        winners = pr_df[pr_df['state'] == state]['winner']
        if len(winners.unique()) > 1:
            party.append('SWING')
        else:
            party.append(winners.unique()[0])
    
    # Create dictionary for new df with state and status (DEMOCRAT, REPUBLICAN, SWING)
    data_dictionary = {'state' : states, 'party' : party}
    df_status = pd.DataFrame(data_dictionary)
    
    # To have Upperlower-letters format
    df_status['state'] = df_status['state'].str.title()
    
    # Save this one to csv
    df_status.to_csv('party_winners.csv')
    

def parse_review(content):
    """
    Parses all the reviews to dictionary.
    
    Args:
        content (list): List containing each review as a string entry.
    
    Return:
        dictionary (dict): All the reviews stored in the dictionary (each component of the the review is one key). 
    """
    
    # By looking at the data we can observe that each review is separated by double newline \n\n
    rows = content.strip().split('\n\n')

    # Create dictionary out of these reviews that will be turned into pandas DF
    # Each lists stores one component of the review, for each reviewer
    beer_name = []
    beer_id = []
    brewery_name = []
    brewery_id = []
    style = []
    abv = []
    date = []
    user_name = []
    user_id = []
    appearance = []
    aroma = []
    palate = []
    taste = []
    overall = []
    rating = []
    text = []

    for row in rows:
      
        review = row.split('\n')
        #print(review)
        for element in review:
            # Append beer name
            if element.startswith('beer_name'):
                beer_name.append(element.split(': ')[1])
            # Append beer_id
            elif element.startswith('beer_id'):
                beer_id.append(element.split(': ')[1])
            # Append brewery_name
            elif element.startswith('brewery_name'):
                brewery_name.append(element.split(': ')[1])
            # Append brewery_id
            elif element.startswith('brewery_id'):
                brewery_id.append(element.split(': ')[1])
            # Append style
            elif element.startswith('style'):
                style.append(element.split(': ')[1])
            # Append abv
            elif element.startswith('abv'):
                abv.append(element.split(': ')[1])
            # Append date
            elif element.startswith('date'):
                date.append(element.split(': ')[1])
            # Append user_name
            elif element.startswith('user_name'):
                user_name.append(element.split(': ')[1])
            # Append user_id
            elif element.startswith('user_id'):
                user_id.append(element.split(': ')[1])
            # Append appearance
            elif element.startswith('appearance'):
                appearance.append(element.split(': ')[1])
            # Append aroma
            elif element.startswith('aroma'):
                aroma.append(element.split(': ')[1])
            # Append palate
            elif element.startswith('palate'):
                palate.append(element.split(': ')[1])
            # Append taste
            elif element.startswith('taste'):
                taste.append(element.split(': ')[1])
            # Append overall
            elif element.startswith('overall'):
                overall.append(element.split(': ')[1])
            # Append rating
            elif element.startswith('rating'):
                rating.append(element.split(': ')[1])
            # Append text
            elif element.startswith('text'):
                text.append(element.split(': ')[1])

    dictionary = {'beer_name' : beer_name,
            'beer_id' : beer_id,
            'brewery_name': brewery_name,
            'brewery_id': brewery_id,
            'style': style,
            'abv' : abv,
            'date': date,
            'user_name' : user_name,
            'user_id' : user_id,
            'appearance' : appearance,
            'aroma' : aroma,
            'palate' : palate,
            'taste' : taste,
            'overall' : overall,
            'rating' : rating,
            'text' : text}


    return dictionary

if __name__ == "main":
    
    # Read the entire file as a string
    with open(FILE_PATH, 'r') as file:
        content = file.read()
    
    # Parse reviews
    dictionary = parse_review(content)
    review_df = pd.DataFrame(dictionary)
    
    # Date of the review is in unix time, we have to convert it 
    column_date = pd.to_datetime(review_df['date'], unit='s').dt.date
    review_df['readable_date'] = column_date
    
    # Save to csv - file is around 1.7GB
    review_df.to_csv(NAME)   