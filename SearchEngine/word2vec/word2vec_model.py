# This module contains the custom classes for scoring

from whoosh.scoring import BM25F
from gensim.models.doc2vec import Doc2Vec
from whoosh.analysis import StandardAnalyzer
import json
from sklearn.metrics.pairwise import cosine_similarity

from SearchEngine.constants import WORD2VEC_MODEL, WORD2VEC_JSON


def preprocess_query(query, model: Doc2Vec):
    analyzer = StandardAnalyzer()
    processed_query = [token.text for token in analyzer(query)]

    query_vector = model.infer_vector(processed_query)
    return query_vector


def get_word2vec_score(recipe_id, query, docs, model):
    query_vector = preprocess_query(query, model)
    doc_vector = docs[recipe_id]
    similarity = cosine_similarity([query_vector], [doc_vector])[0][0]
    return similarity


class Word2VecModel(BM25F):
    use_final = True

    def __init__(self):
        super().__init__()
        self.model = Doc2Vec.load(WORD2VEC_MODEL)
        self.query=None
        with open(WORD2VEC_JSON, "r") as f:
            self.docs = json.load(f)

    def set_query(self, query):
        self.query = query

    def final(self, searcher, docnum, score):
        if self.query is None:
            raise Exception('Query undefined. Call set_query first')

        recipe_id = searcher.stored_fields(docnum)['recipe_id']
        doc2vec_score = get_word2vec_score(recipe_id, self.query, self.docs, self.model)
        return score * doc2vec_score
