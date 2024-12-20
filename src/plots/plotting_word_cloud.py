import pathlib
import numpy as np
from PIL import Image
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import pickle


def plot_word_cloud():
    data_dir_path = pathlib.Path("../../data")
    frequencies = None

    with open(data_dir_path / 'generated' / 'frequencies.pkl', 'wb') as f:
        pickle.dump(frequencies, f)

    images_dir_path = pathlib.Path("../../images")
    fonts_dir_path = pathlib.Path("../../fonts")
    beer_mask = np.array(Image.open(images_dir_path / "bubble_mask.png"))

    wordcloud: WordCloud = WordCloud(
        background_color="white",
        mask=beer_mask,
        contour_width=3,
        contour_color="black",
        font_path=fonts_dir_path / 'Kavoon' / 'Kavoon-Regular.ttf',
        prefer_horizontal=1,
        min_font_size=20,
        colormap="copper_r").generate_from_frequencies(frequencies)

    plt.figure(figsize=(30, 30))
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")
    plt.title("Beer Word Cloud", fontsize=20, color="brown")
    plt.show()
