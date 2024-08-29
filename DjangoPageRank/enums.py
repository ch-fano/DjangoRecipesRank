from django.db import models

class Enums:
    class Model(models.TextChoices):
        BM25 = 'BM25', 'BM25'
        SENTIMENT = 'SE', 'Sentiment'
        SENTIMET_AVG = 'RSE', 'Amounted Review Sentiment'