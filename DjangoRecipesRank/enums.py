from django.db import models

class Enums:
    class Model(models.TextChoices):
        BM25F = 'BM25F', 'BM25F'
        SENTIMENT = 'SE', 'Sentiment'
        REVIEW_SENTIMENT = 'RSE', 'Review Sentiment'
        WORD2VEC = 'W2V', 'Word2Vec'