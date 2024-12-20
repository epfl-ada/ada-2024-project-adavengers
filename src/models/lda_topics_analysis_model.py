import pandas as pd
import pathlib
from gensim import corpora
from gensim.models import LdaModel
from nltk.corpus import stopwords
from nltk.stem.wordnet import WordNetLemmatizer
from collections import defaultdict
from pprint import pprint
import nltk
from wordcloud import WordCloud
import matplotlib.pyplot as plt

nltk.download('stopwords')
nltk.download('wordnet')


class LDAAnalysis:
    def __init__(self, reviews: list[str] = []):
        """
        Initialize the LDA Analysis pipeline with the dataset
        The goal is to find the general topics in the reviews
        @param reviews: dataset of string reviews
        """
        self.dataset = reviews

        self.stop_words = set(stopwords.words('english'))
        self.lemmatizer = WordNetLemmatizer()
        self.dictionary = None
        self.corpus = None
        self.lda_model = None

    def load_dataset(self, reviews_df_path):
        """Load the dataset """
        reviews_df = pd.read_csv(reviews_df_path)

        # remove empty strings
        reviews_df['text'] = reviews_df['text'].dropna()
        reviews_df['text'] = reviews_df['text'].astype(str)
        reviews_df = reviews_df[reviews_df['text'].str.strip() != '']

        reviews = reviews_df['text'].tolist()
        self.dataset = reviews
        print(f"Loaded dataset with {len(self.dataset)} reviews.")

    def preprocess(self):
        """
        Preprocess the document text by tokenizing, removing stop words, and lemmatizing
        """
        print("starting preprocess")
        documents = [self.dataset[i] for i in range(len(self.dataset))]
        documents = self._keep_valid_string_docs(documents)

        tokenized_docs = [doc.lower().split() for doc in documents]
        tokenized_docs = self._filter_out_stop_words(tokenized_docs)
        tokenized_docs = self._lematize(tokenized_docs)

        processed_docs = self._remove_word_that_occur_once(tokenized_docs)
        self.dictionary = corpora.Dictionary(processed_docs)
        self.corpus = [self.dictionary.doc2bow(doc) for doc in processed_docs]
        print("preprocessing completed")

    def _lematize(self, tokenized_docs):
        docs = [[self.lemmatizer.lemmatize(token) for token in doc] for doc in tokenized_docs]
        return docs

    def _filter_out_stop_words(self, tokenized_docs):
        docs = [[token for token in doc if token not in self.stop_words] for doc in tokenized_docs]
        return docs

    def _keep_valid_string_docs(self, documents):
        documents = [doc for doc in documents if isinstance(doc, str)]
        return documents

    def _remove_word_that_occur_once(self, docs):
        frequency = defaultdict(int)
        for doc in docs:
            for token in doc:
                frequency[token] += 1
        docs = [[token for token in doc if frequency[token] > 1] for doc in docs]
        return docs

    def train_lda(self):
        """
        Fit the LDA to the preprocessed data
        """
        self.lda_model = LdaModel(self.corpus, num_topics=2, id2word=self.dictionary, passes=10, per_word_topics=True)

        print("LDA model training completed.")

    def print_topics(self, num_words=10):
        """Print the topics discovered by the LDA model."""
        if not self.lda_model:
            raise ValueError("please train the LDA model first")
        pprint(self.lda_model.print_topics(num_words=num_words))

    def save_model(self, model_path: str):
        """Save the trained LDA model"""
        self.lda_model.save(model_path)

    def load_saved_model(self, model_path: str):
        """Load a saved LDA model"""
        self.lda_model = LdaModel.load(model_path)

    def show_plot(self):
        for i in range(6):  # Assuming 6 topics
            plt.figure()
            word_freq = dict(lda_analysis.lda_model.show_topic(i, 30))
            wordcloud = WordCloud(background_color='white').generate_from_frequencies(word_freq)
            plt.imshow(wordcloud, interpolation='bilinear')
            plt.axis('off')
            plt.title(f"Topic {i}")
            plt.show()


if __name__ == "__main__":
    data_dir_path = pathlib.Path("../../data")
    reviews_df_path = data_dir_path / "generated" / "reviews_df.csv"

    lda_analysis = LDAAnalysis()
    lda_analysis.load_dataset(reviews_df_path)
    lda_analysis.preprocess()
    lda_analysis.train_lda()
    lda_analysis.print_topics(num_words=10)

    dst_model_path = data_dir_path / "generated" / "biglda"
    lda_analysis.save_model(dst_model_path) # save the model for later use
