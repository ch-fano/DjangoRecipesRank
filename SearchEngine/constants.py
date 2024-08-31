# constants.py
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
SEARCH_ENGINE_DIR = os.path.join(BASE_DIR, 'SearchEngine')
DATASET_DIR = os.path.join(SEARCH_ENGINE_DIR, 'dataset')
REVIEWS_PATH = os.path.join(DATASET_DIR, 'review.pkl')
INDEX_DIR = os.path.join(SEARCH_ENGINE_DIR, 'indexdir')
SENTIMENT_INDEX_DIR = os.path.join(INDEX_DIR ,'sentimentIndex')
WORD2VEC_DIR = os.path.join(SEARCH_ENGINE_DIR, 'word2vec')
WORD2VEC_MODEL = os.path.join(WORD2VEC_DIR, 'word2vec.model')
WORD2VEC_JSON = os.path.join(WORD2VEC_DIR, 'word_vectors.json')