from transformers import pipeline


class SentimentAnalysisPipeline:
    def __init__(self):
        self.sentiment_pipeline = pipeline("sentiment-analysis", model="finiteautomata/bertweet-base-sentiment-analysis")

    def predict(self, text):
        return self.sentiment_pipeline(text)


if __name__ == '__main__':
    sentiment_pipeline = SentimentAnalysisPipeline()
    result = sentiment_pipeline.predict(
        # "Pours pale copper with a thin head that quickly goes. Caramel, golden syrup nose. Taste is big toasty, grassy hops backed by dark fruit, candy corn and brack malts. Clingy. Dries out at the end with more hops. Brave, more going on that usual for this type."
        # "500ml Bottle bought from The Vintage, Antrim...Poured a golden yellow / orange colour... White head poured quite thick and foamy and faded to thin layer...Aroma - Fruity (burnt orange, some apple hints), light maltiness, spicy hops, vanilla, some sea saltiness...Taste - Spicy / peppery hop notes, citrusy, light sweetness, grassy, slight creaminess, some bready notes...Feel - Quite sharp and pretty dry. Light body.... Pretty drinkable...Overall - A pretty good beer.... worth a try..."
        #     "500ml bottlePours with a light, slightly hazy golden body, light amber in colour. Slight tan head formsSmell, slight hop aromas, some sweetness coming offTaste, well balanced hoppy, nice herby floral hop flavour, nice malt finishA good little brew, this one suprised me"
        #         "Bottle at The Black Sheep, Dublin, IrelandA: The beer is hazy yellow in color and has a high amount of visible carbonation. It poured into a weizen glass with a finger and a half high bright white head that has good retention properties and consistently left a short head covering the surface.S: Moderate aromas of wheat are present in the nose along with hints of bananas from the yeast.T: Like the smell, the taste has flavors of wheat with slight bits of bananas from the yeast.M: It feels light- to medium-bodied on the palate and has a moderate amount of carbonation.O: This isn't a bad Irish representation of a German wheat beer. It is very easy to drink."
        "Irish oddity brought back by my parents, thanks. It was decent but just OK, like most blonde ales. Beer is blonde and clear with a thin white head of medium bubbles, no lacing, minimal carbonation and retention.Aroma is weak, a little grainy a little sweet. It is OK.Beer is nice in the body, light but not dry, mildly bitter, a decent finish, no aftertaste, I don't think I'd have it again but it is probably good enough to drink more than one. I dont recommend at all this beer, its disgusrting"
    )
    print(result)
