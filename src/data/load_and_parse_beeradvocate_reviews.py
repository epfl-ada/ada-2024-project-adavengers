import pathlib

import pandas as pd


class BeerAdvocateParser:
    """
    Class for parsing the beer advocate txt file with reviews into pandas DF (saved as .csv)
    """

    def _parse_reviews(self, content):
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
            # print(review)
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

        dictionary = {'beer_name': beer_name,
                      'beer_id': beer_id,
                      'brewery_name': brewery_name,
                      'brewery_id': brewery_id,
                      'style': style,
                      'abv': abv,
                      'date': date,
                      'user_name': user_name,
                      'user_id': user_id,
                      'appearance': appearance,
                      'aroma': aroma,
                      'palate': palate,
                      'taste': taste,
                      'overall': overall,
                      'rating': rating,
                      'text': text}

        return dictionary

    def generate_result(self, src_path, dst_path):
        """
        Generate the result of parsing the reviews into a pandas DF and save it as a .csv file.
        @param src_path: path of the file with reviews to parse
        @param dst_path: path where to save the .csv file with the parsed reviews
        """

        # Read the entire file as a string
        with open(src_path, 'r') as file:
            content = file.read()

        # parse reviews
        dictionary = self._parse_reviews(content)
        review_df = pd.DataFrame(dictionary)

        # date of the review is in unix time, we have to convert it
        column_date = pd.to_datetime(review_df['date'], unit='s').dt.date
        review_df['readable_date'] = column_date

        # save to csv (file is around 1.7GB)
        review_df.to_csv(dst_path)


if __name__ == '__main__':
    parser = BeerAdvocateParser()
    data_dir_path = pathlib.Path("../../data")

    src_path = '/Users/david/Beers/BeerAdvocate/reviews.txt' # data_dir_path / "reviews.txt"
    dst_path = data_dir_path / 'generated' / "reviews_df.csv"

    parser.generate_result(src_path, dst_path)
