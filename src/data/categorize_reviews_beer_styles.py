import numpy as np
import pathlib
from src.data import reviews_processing, load_and_find_party_winners


class CategorizeReviewsBeerStyles:
    def __init__(self, data_dir_path):
        """
        Script go generate the reviews_categorized.pkl file.
        It represents the same dataframe as the generated reviews_df.csv file (which was generated in load_and_parse_beeradvocate_reviews.py) but with an extra column "general_style" which represents one of the 8 beer styles.

        @param data_dir_path: path where the input files that are needed are stored.
        """
        self.users_path = data_dir_path / "BeerAdvocate" / "users.csv"
        self.reviews_path = data_dir_path / "generated" / "reviews_df.csv"
        self.winners_path = data_dir_path / "generated" / "party_winners_over_years.csv"

    def generate_pickle(self, dst_path):
        """
        @param dst_path: location where to save the pickle file
        """
        users_reviews = reviews_processing.Reviews(self.users_path, self.reviews_path)
        year_list = list(np.arange(2004, 2017, 1, dtype=int))
        results = users_reviews.aggregate_preferences_year(year_list, all_states=True)
        winners = load_and_find_party_winners.state_winner_years(self.winners_path)

        total_reviews = users_reviews.filter_beer_type()
        total_reviews.to_pickle(dst_path)


if __name__ == "__main__":
    data_dir_path = pathlib.Path("../../data")
    dst_path = data_dir_path / "generated" / "reviews_categorized.pkl"
    CategorizeReviewsBeerStyles(data_dir_path).generate_pickle(dst_path)
