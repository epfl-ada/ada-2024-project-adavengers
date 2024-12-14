import pathlib

import pandas as pd

def state_winner_years(path_winners):
    """ From party_winners_over_years.csv extract state, year and winner. """
    
    # Load the data
    winners = pd.read_csv(path_winners)
    
    winners['state'] = winners['state'].str.title()
    winners['winner'] = winners['winner'].str.title()
    
    winners_columns = winners[['state', 'winner', 'year']]
    winners_idx = winners_columns.set_index('state')
    
    return winners_idx

class PartyWinnersParser:
    """
    Processing pipeline for generating .csv for presidental data
    """

    def __init__(self, src_path, dst_path_party_winnders_and_percentages, dst_path_party_winners):
        """
        Initialize the PartyWinnersParser with the source and destination paths.
        @param src_path: presidential data file path
        @param dst_path_party_winnders_and_percentages: result 1 path
        @param dst_path_party_winners: result 2 path
        """
        self.src_path = src_path
        self.dst_path_party_winners_and_percentages = dst_path_party_winnders_and_percentages
        self.dst_path_party_winners = dst_path_party_winners

    def _sum_the_votes(self, parties, data):
        """
        Sum all the votes from the candidates coming from the same party.

        Args:
            parties (array): Array of containing all the parties.
            data (dataframe): President data.
        """
        pr_df_filt = data.copy()

        for party in parties:
            # Group by state and year and then aggregate by summing all the votes for the same party
            pr_df_filt_party = pr_df_filt[pr_df_filt['party_simplified'] == party].groupby(['state', 'year']).agg(
                {'candidatevotes': 'sum', 'totalvotes': 'first'}).reset_index()
            pr_df_filt_party['party_simplified'] = party

            pr_df_non_party = pr_df_filt[pr_df_filt['party_simplified'] != party]
            pr_df_filt = pd.concat([pr_df_non_party, pr_df_filt_party])

        return pr_df_filt

    def extract_president_data(self):
        """
        Extract president data in the adequate format, i.e. to have which party won each year in every state (from number of votes per each candidate per state every election year).

        The function will generate two .csv file.
        1. With information of percentage per each party per state per year and a column winner corresponding to that years winner (2001-2017) - party_winners_over_years.csv.
        2. State with status DEMOCRAT, REPUBLICAN, SWING - party_winners.csv.

        Args:
            src_path (pathlib Path): Path to the president data file.
            dst_path_party_winnders_and_percentages (pathlib Path): Path to the file where to save the data with winners and percentages.
            dst_path_party_winners (pathlib Path): Path to the file where to save the data with states and their status.
        """

        # Load president data
        president_data = pd.read_csv(self.src_path)

        # Our beer reviews data contains data from 2001 to 2017 - we need to filter out those election years
        # We are keeping columns: year, state, party_simplified, candidate votes and total votes
        pr_df_filt = president_data[(president_data['year'] >= 2001) & (president_data['year'] <= 2017)]
        relevant_columns = ['year', 'state', 'party_simplified', 'candidatevotes', 'totalvotes']
        pr_df_filt = pr_df_filt[relevant_columns]

        parties = pr_df_filt['party_simplified'].unique()

        # Sum all the votes
        pr_df_combined = self._sum_the_votes(parties, pr_df_filt)

        # Create a column percentage which will have percentage of votes each candidate got
        pr_df_combined['percentage'] = (pr_df_combined['candidatevotes'] / pr_df_combined['totalvotes']) * 100
        pr_df_percentage = pr_df_combined.drop(['candidatevotes', 'totalvotes'], axis=1, inplace=False)

        # We want to create another column - winner - which identifies what party won in that specifc year
        pr_df = pd.pivot_table(pr_df_percentage, columns=['party_simplified'], values='percentage',
                               index=['state', 'year']).reset_index()
        winner = pr_df[['DEMOCRAT', 'OTHER', 'LIBERTARIAN', 'REPUBLICAN']].idxmax(axis=1)
        pr_df['winner'] = winner

        # Save this df with winners and percentages
        pr_df.to_csv(self.dst_path_party_winners_and_percentages)

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
        data_dictionary = {'state': states, 'party': party}
        df_status = pd.DataFrame(data_dictionary)

        # To have Upperlower-letters format
        df_status['state'] = df_status['state'].str.title()

        # Save this one to csv
        df_status.to_csv(self.dst_path_party_winners)
        print("Data processing for presidents dataset completed.")


if __name__ == '__main__':
    data_dir_path = pathlib.Path("../../data")

    src_path = data_dir_path / '1976-2020-president.csv'
    dst_path_party_winners_and_percentages = data_dir_path / 'generated' / 'party_winners_over_years.csv'
    dst_path_party_winners = data_dir_path / 'generated' / 'party_winners.csv'

    PartyWinnersParser(src_path,
                       dst_path_party_winners_and_percentages,
                       dst_path_party_winners).extract_president_data()
