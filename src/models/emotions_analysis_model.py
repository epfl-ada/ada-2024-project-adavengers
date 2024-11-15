from torch import Tensor
from sentence_transformers import SentenceTransformer


class EmotionsAnalysisPipeline:
    def __init__(self):
        """
        Initialize the pipeline with the emotions and the model

        Emotions beers can evoke: surprise, disgust, happiness, sadness, anger, fear, neutral
        we can embed those emotions and compare with the embeddings of the beers text.
        if the embeddings are similar the beer evokes that emotion otherwise they don't.
        """

        # hardcoded list of emotions
        self.emotions: list[str] = ["surprise", "disgust", "happiness", "sadness", "anger", "fear", "neutral"]
        self.model: SentenceTransformer = SentenceTransformer('all-mpnet-base-v2')

        self.emotions_emb: Tensor = self.model.encode(self.emotions, normalize_embeddings=True)

    def analyse(self, text: str):
        """
        Analyse the text and print the emotions it evokes
        @param text:
        """
        text_emb: Tensor = self.model.encode(text, normalize_embeddings=True)
        similarity: Tensor = self.model.similarity(text_emb, self.emotions_emb)  # 1x8

        for i, emotion in enumerate(self.emotions):
            print(f"{emotion.ljust(30)}: {similarity[0, i]}")


if __name__ == '__main__':
    EmotionsAnalysisPipeline().analyse("This beer is very surprising, I didn't expect it to be so good.")