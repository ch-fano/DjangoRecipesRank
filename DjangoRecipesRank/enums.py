from django.db import models

class Enums:
    class Model(models.TextChoices):
        BM25 = 'BM25', 'BM25'
        SENTIMENT = 'SE', 'Sentiment'
        SENTIMET_AVG = 'RSE', 'Amount Review Sentiment'
        WORD2VEC = 'W2V', 'Word2Vec'