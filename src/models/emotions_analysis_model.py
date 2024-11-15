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
        self.emotions: list[str] = ["bitter", "sweet", "sour", "salty", "umami", "spicy", "metallic", "astringent"]
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
    EmotionsAnalysisPipeline().analyse("not sour at all")
        #"Irish oddity brought back by my parents, thanks. It was decent but just OK, like most blonde ales. Beer is blonde and clear with a thin white head of medium bubbles, no lacing, minimal carbonation and retention.Aroma is weak, a little grainy a little sweet. It is OK.Beer is nice in the body, light but not dry, mildly bitter, a decent finish, no aftertaste, I don't think I'd have it again but it is probably good enough to drink more than one.")