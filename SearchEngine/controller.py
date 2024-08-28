from whoosh.scoring import BM25F

from SearchEngine.index import Index
from SearchEngine.model import IRModel


class Controller:

    def __init__(self, index:Index):
        self.index = index
        self.search_model = None
        self.data = None

    def search(self):
        print(f"model in use is: {(self.search_model.model)}")
        if not self.data['use_sentiment'] and isinstance(self.search_model.model, BM25F):
            # indexing model
            recipes = self.search_model.search(query=self.get_query, res_limit=int(self.data['number_of_results']))
        else:
            # sentiment model
            recipes = self.search_model.search(query=self.get_query, res_limit=int(self.data['number_of_results']), sentiments=self.data['chosen_sentiments'])

        return recipes

    @property
    def get_query(self):
        if not self.search_model or not self.data:
            return ''

        query = ''
        if self.data.get('text_search', ''):
            query += self.data.get('text_search')
        if self.data.get('n_steps_min', 0) and self.data.get('n_steps_max', 50):
            query += f" AND n_steps:[{int(self.data.get('n_steps_min'))} TO {int(self.data.get('n_steps_max'))}]"
        if self.data.get('prep_time_min', 0) and self.data.get('prep_time_max', 10000):
            query += f" AND prep_time:[{int(self.data.get('prep_time_min'))} TO {int(self.data.get('prep_time_max'))}]"
        if self.data.get('rating', ''):
            query += f" AND rating:[{int(self.data.get('rating'))} TO 5]"
        if self.data.get('n_ingredients_min', 0) and self.data.get('n_ingredients_max', 20):
            query += f" AND n_ingredients:[{int(self.data.get('n_ingredients_min'))} TO {int(self.data.get('n_ingredients_max'))}]"
        if self.data.get('recipe_date_min', 2000) and self.data.get('recipe_date_max', 2024):
            query += f" AND recipe_date:[{self.data.get('recipe_date_min')}-01-01 TO {self.data.get('recipe_date_max')}-12-31]"
        return query

    def set_model(self, model: IRModel):
        self.search_model = model

    def set_data(self, clean_data:dict):
        self.data = clean_data