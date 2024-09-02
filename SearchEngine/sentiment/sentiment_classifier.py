from transformers import RobertaTokenizer, AutoModelForSequenceClassification, pipeline
import torch


class SentimentClassifier:
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    def __init__(self):
        self.tokenizer = RobertaTokenizer.from_pretrained(f"j-hartmann/emotion-english-distilroberta-base")
        self.model = AutoModelForSequenceClassification.from_pretrained(f"j-hartmann/emotion-english-distilroberta-base")



    def extract(self, document):
        return pipeline(
            model=self.model.to(SentimentClassifier.device),  # Sposta il modello sulla GPU se disponibile
            tokenizer=self.tokenizer,
            task="text-classification",
            top_k=7,
            max_length=512,
            truncation=True,
            device=SentimentClassifier.device  # Passa il dispositivo di calcolo al metodo pipeline
        )(document)


if __name__ == "__main__":
    classifier = SentimentClassifier()
    text = "What a wonderful accomodation! I loved staying there. Although people outside were a little bit scary, the stay was pleasant."
    text2 = "i made this carrot cake because it seemed a simple recipe, i have to say the result is delicious! with few ingredients the cake is really tasty, but i found it a little bitter for my personal taste. Everyone liked it."
    text3 = "i tried this salmon in crust recipe that i found online and i was pretty disappointed! the fish was overcooked and had a horrible taste"
    results = classifier.extract([text, text2, text3])
    print(results)
