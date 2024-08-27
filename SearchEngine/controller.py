from whoosh.scoring import BM25F

from SearchEngine.index import Index
from SearchEngine.model import IRModel


class Controller:

    def __init__(self, index:Index, model:IRModel, cleaned_data:dict):
        self.index = index
        self.model = model
        self.data = cleaned_data

    def search(self):

        if not self.data['sentiment'] and isinstance(self.model.model, BM25F):
            # indexing model
            recipes = self.model.search(query=self.get_query, res_limit=int(self.data['number_of_results']))
        else:
            # sentiment model
            recipes = self.model.search(query=self.get_query, res_limit=int(self.data['number_of_results']), sentiments=[])

        return recipes

    @property
    def get_query(self):
        query = ''
        if self.data.get('text_search', ''):
            query += self.data.get('text_search')
        if self.data.get('n_steps_min', 0) and self.data.get('n_steps_max', 50):
            query += f" AND n_steps:[{int(self.data.get('n_steps_min'))} TO {int(self.data.get('n_steps_max'))}]"
        if self.data.get('prep_time_min', 0) and self.data.get('prep_time_max', 10000):
            query += f" AND prep_time:[{int(self.data.get('prep_time_min'))} TO {int(self.data.get('prep_time_max'))}]"
        if self.data.get('rating', ''):
            query += f" AND rating:[{int(self.data.get('rating'))} TO]"
        if self.data.get('n_ingredients_min', 0) and self.data.get('n_ingredients_max', 20):
            query += f" AND n_ingredients:[{int(self.data.get('n_ingredients_min'))} TO {int(self.data.get('n_ingredients_max'))}]"
        return query