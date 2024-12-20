from sklearn.preprocessing import MinMaxScaler
import numpy as np
from matplotlib import pyplot as plt
from torch import Tensor
import pandas as pd
import torch
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity


class BeerCharacteristicsAnalysisPipeline:

    def __init__(self):
        """
        The goal is to measure how much each one of the 8 beer styles we defined from (general_style column in the generated reviews_with_similarities.pkl)
        Running this code is efficient (GPU batching) but still takes a large amount of time because there are 2 million reviews to embed.
        Checkpoint dataframe are saved in the data/generated folder.

        We then define manually 5 beer characteristics that we want to measure and see how much each beer style is close to each of those characteristics (cosine similarity)
        """
        if not torch.cuda.is_available():
            raise SystemError("CUDA is not available :/")
        device = 'cuda'
        self.model = SentenceTransformer('all-mpnet-base-v2', device=device)
        print(f"Model is using device: {self.model.device}")

        self.characteristics = {
            "Hop Intensity": ["bitter", "hoppy", "citrus", "pine", "resinous"],
            "Malt Profile": ["sweet", "caramel", "toffee", "roasted", "chocolate"],
            "Body/Texture": ["light", "medium-bodied", "full-bodied", "creamy", "smooth"],
            "Alcohol Strength": ["boozy", "warming", "strong", "high ABV"],
            "Carbonation": ["crisp", "bubbly", "effervescent", "flat"]
        }

        # Encode keywords and calculate centroids
        self.centroids = {char: self.model.encode(keywords, normalize_embeddings=True).mean(axis=0)
                          for char, keywords in self.characteristics.items()}

    def perform_embedding_on_reviews(self, reviews_categorized_pkl_path, dst_path: str = "reviews_categorized_embedded_fast.pkl"):
        reviews_df = pd.read_pickle(reviews_categorized_pkl_path)

        # preprocessing: remove the empty strings
        reviews_df['text'] = reviews_df['text'].dropna()
        reviews_df['text'] = reviews_df['text'].astype(str)
        reviews_df = reviews_df[reviews_df['text'].str.strip() != '']

        reviews = reviews_df['text'].tolist()

        # change to your batch size
        all_embeddings = self.model.encode(reviews, normalize_embeddings=True, batch_size=128, show_progress_bar=True)

        reviews_df["embedding"] = list(all_embeddings)

        print("saving the updated df")
        reviews_df.to_pickle(dst_path)
        print("saved")

    def compute_similarities(self, embed_df_path, dst_path="reviews_with_similarities.pkl"):
        reviews_df = pd.read_pickle(embed_df_path)

        def compute_characteristics_similarities(reviews_embeddings, centroids):
            similarities = []
            for i, emb in enumerate(reviews_embeddings):
                sim = {char: cosine_similarity([emb], [centroid])[0][0] for char, centroid in centroids.items()}
                if i % 10 == 0:
                    print(i, len(reviews_embeddings), sim)
                similarities.append(sim)
            return similarities

        # we compute similarities for all reviews with the centroids (beer characteristics)
        reviews_df['similarities'] = compute_characteristics_similarities(reviews_df['embedding'], self.centroids)

        reviews_df.to_pickle(dst_path)

    def aggregate_by_style(self, reviews_with_similarities_path):
        df = pd.read_pickle(reviews_with_similarities_path)
        similarities_df = pd.DataFrame(df['similarities'].tolist())
        df = pd.concat([df, similarities_df], axis=1)

        # group by beer style and calculate the median to avoid outliers
        style_characteristics_df = df.groupby("general_style")[list(similarities_df.columns)].median()
        return style_characteristics_df

    def rescale_style_characteristics(self, style_characteristics_df):
        # scale the cosine similarities so that the splotting is readable
        scaler = MinMaxScaler()
        scaled_data = scaler.fit_transform(style_characteristics_df)
        style_characteristics_scaled = pd.DataFrame(
            scaled_data,
            columns=style_characteristics_df.columns,
            index=style_characteristics_df.index
        )
        return style_characteristics_scaled

    def _plot_radar(self, ax, style_name, style_data, characteristics):
        labels = list(characteristics.keys())
        values = style_data.values.flatten().tolist()

        # adding the first value to the end to close the radar chart
        values += values[:1]

        angles = np.linspace(0, 2 * np.pi, len(labels), endpoint=False).tolist()
        angles += angles[:1]  # closing the radar chart too

        ax.plot(angles, values, marker='o', label=style_name)
        ax.fill(angles, values, alpha=0.25)
        ax.set_xticks(angles[:-1])
        ax.set_xticklabels(labels, fontsize=8)
        ax.set_yticks([0.2, 0.4, 0.6, 0.8, 1.0])
        ax.set_yticklabels(['0.2', '0.4', '0.6', '0.8', '1.0'], fontsize=8)
        ax.set_ylim(0, 1)
        ax.set_title(style_name, fontsize=10)

    def plot_grid_radar(self, style_characteristics_scaled):
        """
        Plotting a grid of 8 radar charts
        @param style_characteristics_scaled:
        @param characteristics:
        """
        styles = style_characteristics_scaled.index
        n_styles = len(styles)
        n_cols = 4
        n_rows = 2

        fig, axs = plt.subplots(n_rows, n_cols, figsize=(12, 4 * n_rows), subplot_kw={'polar': True})

        # Plot each beer style in the grid
        for ax, (style_name, style_data) in zip(axs.flat, style_characteristics_scaled.iterrows()):
            self._plot_radar(ax, style_name, style_data, self.characteristics)

        # Hide empty subplots if any
        for ax in axs.flat[n_styles:]:
            ax.axis('off')

        plt.tight_layout()
        plt.show()
