import pathlib

import pandas as pd


class PopulationInformationDataLoader:

    def __init__(self, src_path):
        """

        @param src_path: population data source path
        """
        self.src_path = src_path

        self.age_groups = []
        self.populations_dataframe = None

    def get_population_infos_by_states(self):

        df = pd.read_csv(self.src_path, low_memory=False)

        df = df[['year', 'state', 'pop_annual','pop25to44', 'pop45to64', 'popover65','pctpop25to44', 'pctpop45to64', 'pctpopover65']]

        # So we could map with the beer dataset later, we only focus on those election years:
        election_years = [2004, 2008, 2012, 2016]
        df = df[df['year'].isin(election_years)]

        # We prefer to work with percentages going from 0 to 1
        df.loc[df['year'].isin([2016]), 'pctpop25to44'] = df['pctpop25to44'] / 100
        df.loc[df['year'].isin([2016]), 'pctpop45to64'] = df['pctpop45to64'] / 100
        df.loc[df['year'].isin([2016]), 'pctpopover65'] = df['pctpopover65'] / 100

        # Since variables for percentage of population (namely pctpop...) are only available for years 2013-2017 (from which we only take 2016 as election year),
        # we still have to add the % for years 2004, 2008 and 2012.
        # For 2004 and 2008 we can compute the percentage with popXtoY / pop_annual
        # We can't do the same for 2012 since variables for population number are available only for year 2002-2010
        df.loc[df['year'].isin([2004, 2008]), 'pctpop25to44'] = df['pop25to44'] / df['pop_annual']
        df.loc[df['year'].isin([2004, 2008]), 'pctpop45to64'] = df['pop45to64'] / df['pop_annual']
        df.loc[df['year'].isin([2004, 2008]), 'pctpopover65'] = df['popover65'] / df['pop_annual']

        self.populations_dataframe = df[['year', 'state', 'pctpop25to44', 'pctpop45to64', 'pctpopover65', 'pop_annual']]

        return self.populations_dataframe

    # def plot_evolution(self):
    #     pass
    #
    # def plot_population_evolution(self, state_in_evidence):
    #     pass
    #
    # def _population_of_age_group_in_state(self, age_group):
    #     pass
    #
    # def wealth_by_state(self, state):
    #     pass

if __name__ == '__main__':
    data_dir_path = pathlib.Path("../../data")

    src_path = data_dir_path / 'correlates2-6.csv'

    PopulationInformationDataLoader(src_path).get_population_infos_by_states().head()

