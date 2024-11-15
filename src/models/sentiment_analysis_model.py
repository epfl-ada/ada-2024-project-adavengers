from transformers import pipeline


class SentimentAnalysisPipeline:
    def __init__(self):
        self.sentiment_pipeline = pipeline("sentiment-analysis", model="finiteautomata/bertweet-base-sentiment-analysis")

    def predict(self, text):
        return self.sentiment_pipeline(text)


if __name__ == '__main__':
    sentiment_pipeline = SentimentAnalysisPipeline()
    result = sentiment_pipeline.predict(
        "500ml bottlePours with a light, slightly hazy golden body, light amber in colour. Slight tan head formsSmell, slight hop aromas, some sweetness coming offTaste, well balanced hoppy, nice herby floral hop flavour, nice malt finishA good little brew, this one suprised me"
    )
    print(result)
