# This module contains the custom classes for scoring
import os

import yaml
from whoosh.scoring import BM25F
from gensim.models.doc2vec import Doc2Vec, TaggedDocument
from whoosh.analysis import StandardAnalyzer
import json
from sklearn.metrics.pairwise import cosine_similarity

from SearchEngine.constants import BASE_DIR, WORD2VEC_DIR, WORD2VEC_MODEL, WORD2VEC_JSON


def preprocess_query(query, model: Doc2Vec):
    analyzer = StandardAnalyzer()
    processed_query = [token.text for token in analyzer(query)]

    query_vector = model.infer_vector(processed_query)
    return query_vector


def get_doc2vec_score(id, query, docs, model):
    query_vector = preprocess_query(query, model)
    doc_vector = docs[id]
    similarity = cosine_similarity([query_vector], [doc_vector])[0][0]
    return similarity


class Doc2VecModel(BM25F):
    use_final = True

    def __init__(self):
        super().__init__()
        self.model = Doc2Vec.load(WORD2VEC_MODEL)
        with open(WORD2VEC_JSON, "r") as f:
            self.docs = json.load(f)

    def set_query(self, query):
        self.query = query

    def final(self, searcher, docnum, score):
        id = searcher.stored_fields(docnum)['recipe_id'] # maybe recipe_id (or id)
        doc2vec_score = get_doc2vec_score(id, self.query, self.docs, self.model)
        return score * doc2vec_score
