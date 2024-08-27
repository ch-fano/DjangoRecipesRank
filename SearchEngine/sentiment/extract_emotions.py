from transformers import RobertaTokenizer, AutoModelForSequenceClassification, pipeline


class ExtractEmotions:

    def __init__(self):
        self.tokenizer = RobertaTokenizer.from_pretrained(f"j-hartmann/emotion-english-distilroberta-base")
        self.model = AutoModelForSequenceClassification.from_pretrained(f"j-hartmann/emotion-english-distilroberta-base")

    def extract(self, document):
        return pipeline(
            model=self.model,
            tokenizer=self.tokenizer,
            task="text-classification",
            top_k=7,
            max_length=512,
            truncation=True,
            #device=0
        )(document)


if __name__ == "__main__":
    classifier = ExtractEmotions()
    text = "What a wonderful accomodation! I loved staying there. Although people outside were a little bit scary, the stay was pleasant."
    text2 = "i made this carrot cake because it seemed a simple recipe, i have to say the result is delicious! with few ingredients the cake is really tasty, but i found it a little bitter for my personal taste. Everyone liked it."
    text3 = "i tried this salmon in crust recipe that i found online and i was pretty disappointed! the fish was overcooked and had a horrible taste"
    results = classifier.extract([text, text2, text3])
    print(results)
