import pathlib
from transformers import pipeline
import torch
from transformers import DistilBertTokenizer, DistilBertForSequenceClassification
from datasets import Dataset
import pandas as pd
from tqdm import tqdm


class SentimentAnalysisPipeline:
    def __init__(self):
        """
        From the generated reviews_df.pkl file (by src/data/load_and_parse_beeradvocate_reviews.py)
        produce the reviews2_df.pkl file with the sentiment scores.
        Efficient code performing batching on GPU
        """
        self.hf_dataset = None

        # Load Tokenizer and Pretrained Sentiment Analysis Model
        self.tokenizer = DistilBertTokenizer.from_pretrained("distilbert-base-uncased-finetuned-sst-2-english")
        self.model = DistilBertForSequenceClassification.from_pretrained("distilbert-base-uncased-finetuned-sst-2-english")

        # Use multiple GPUs
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        if torch.cuda.device_count() > 1:
            print(f"Using {torch.cuda.device_count()} GPUs!")
            model = torch.nn.DataParallel(self.model)

        model.to(device)

    def load_dataset(self, reviews_df_path: str = "data/generated/reviews_df.csv"):
        # remove empty strings
        reviews_df = pd.read_csv(reviews_df_path)
        reviews_df['text'] = reviews_df['text'].dropna()
        reviews_df['text'] = reviews_df['text'].astype(str)
        reviews_df = reviews_df[reviews_df['text'].str.strip() != '']

        # convert DataFrame to Hugging Face Dataset
        self.hf_dataset = Dataset.from_pandas(reviews_df[['text']])
        self.reviews_df = reviews_df

    def produce_sentiment_scores(self, dst_path: str = "data/generated/reviews2_df.pkl"):
        def preprocess_text(batch):
            max_length = 512
            tokenized = self.tokenizer(batch["text"], padding=True, truncation=True, max_length=max_length)
            return {
                "input_ids": tokenized["input_ids"],
                "attention_mask": tokenized["attention_mask"],
            }

        preprocessed_dataset = self.hf_dataset.map(preprocess_text, batched=True, batch_size=32)

        def analyze_sentiment(batch):
            input_ids = torch.tensor(batch["input_ids"], dtype=torch.long, device=self.device)
            attention_mask = torch.tensor(batch["attention_mask"], dtype=torch.long, device=self.device)
            with torch.no_grad():
                outputs = self.model(input_ids=input_ids, attention_mask=attention_mask)
                logits = outputs.logits
                predictions = torch.softmax(logits, dim=1)
            labels = torch.argmax(predictions, dim=1).cpu().numpy()
            scores = torch.max(predictions, dim=1).values.cpu().numpy()
            return {
                "sentiment_label": ["POSITIVE" if label == 1 else "NEGATIVE" for label in labels],
                "sentiment_score": scores,
            }

        # apply sentiment analysis in batches
        scores_results = preprocessed_dataset.map(analyze_sentiment, batched=True, batch_size=32)

        scores_results_df = scores_results.to_pandas()

        self.reviews_df[['sentiment_label', 'sentiment_score']] = scores_results_df[['sentiment_label', 'sentiment_score']]

        # save the results
        self.reviews_df.to_pickle(dst_path)


if __name__ == '__main__':
    sentiment_pipeline = SentimentAnalysisPipeline()
    data_dir_path = pathlib.Path("../../data")

    reviews_df_path = data_dir_path / 'generated' / 'reviews_df.csv'
    dst_path = data_dir_path / 'generated' / 'reviews2_df.pkl'

    sentiment_pipeline.load_dataset(reviews_df_path)
    sentiment_pipeline.produce_sentiment_scores(dst_path)
