from gensim import corpora
from gensim.models import LdaModel
from nltk.corpus import stopwords
from nltk.stem.wordnet import WordNetLemmatizer
from collections import defaultdict
from pprint import pprint
import nltk

from src.data.text_reviews_dataloader import TextReviews

nltk.download('stopwords')
nltk.download('wordnet')


class LDAAnalysis:
    def __init__(self, reviews: list[str]):
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

    def load_dataset(self):
        """Load the dataset using the TextReviews class."""
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


if __name__ == "__main__":
    # Sample reviews with two main categories: technology and health
    reviews = ["The computer network relies on secure software for data protection.",
               "A balanced diet and regular exercise are key to good health.",
               "Programming AI systems requires a deep understanding of data.",
               "Medicine and treatment plans are developed by the doctor for wellness.",
               "Internet connectivity is essential for accessing modern software tools.",
               "Exercise improves overall wellness and complements a healthy diet."
               ]
    # Need to use TextReviews instead of this sample and study the topics in the reviews that come out
    # TODO see what chunk size parameters to use and should we use n-grams as well during preprocessing?
    lda_analysis = LDAAnalysis(reviews)
    lda_analysis.load_dataset()
    lda_analysis.preprocess()
    lda_analysis.train_lda()
    lda_analysis.print_topics(num_words=10)

"""
[nltk_data] Downloading package stopwords to /Users/david/nltk_data...
[nltk_data]   Package stopwords is already up-to-date!
[nltk_data] Downloading package wordnet to /Users/david/nltk_data...
Loaded dataset with 6 reviews.
starting preprocess
[nltk_data]   Package wordnet is already up-to-date!
preprocessing completed
LDA model training completed.
[(0, '0.822*"software" + 0.178*"exercise"'),
 (1, '0.822*"exercise" + 0.178*"software"')]
 
 """

# as we can see the output makes sense we have a first topic about software and a second topic about exercise
