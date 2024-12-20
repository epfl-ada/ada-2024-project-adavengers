import pathlib
from src.models.transformer_analysis_model import BeerCharacteristicsAnalysisPipeline
# need GPU to run the whole pipeline in a reasonable amount of time

data_dir_path = pathlib.Path("../../data")

def plot_beer_characteristics():
    pipeline = BeerCharacteristicsAnalysisPipeline()

    # input dataframe
    reviews_categorized_path = data_dir_path / "generated" / "reviews_categorized.pkl"

    # first embed all the reviews
    dst_path = data_dir_path / "generated" / "reviews_categorized_embedded_fast.pkl"
    pipeline.perform_embedding_on_reviews(reviews_categorized_path, dst_path)

    # then compute similarities of the embedding of the reviews with the 5 beer characteristics
    dst_path2 = data_dir_path / "generated" / "reviews_with_similarities.pkl"
    pipeline.compute_similarities(dst_path, dst_path2)

    style_characteristics_df = pipeline.aggregate_by_style(dst_path2)

    style_characteristics_scaled = pipeline.rescale_style_characteristics(style_characteristics_df)

    pipeline.plot_grid_radar()