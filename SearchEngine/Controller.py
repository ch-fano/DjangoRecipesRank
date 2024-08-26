from SearchEngine.index import Index
from SearchEngine.model import IRModel


class Controller:

    def __init__(self, index:Index, model:IRModel, cleaned_data:dict):
        self.index = index
        self.model = model
        self.cleaned_data = cleaned_data

    def search(self):
        #TODO: implementare uno switch tra sentiment e no

        recepies = self.model.search(query=self.get_query) #TODO: Aggiungere un campo per prendere il limite della ricerca
        return recepies

    @property
    def get_query(self):
        query = ''
        if self.cleaned_data.get('text_search', ''):
            query += self.cleaned_data.get('text_search')
        if self.cleaned_data.get('n_steps_min', 0) and self.cleaned_data.get('n_steps_max', ''):
            query += f' AND n_steps:[{int(self.cleaned_data.get('n_steps_min'))} TO {int(self.cleaned_data.get('n_steps_max'))}]'
        if self.cleaned_data.get('prep_time_min', 0) and self.cleaned_data.get('prep_time_max', ''):
            query += f' AND prep_time:[{int(self.cleaned_data.get('prep_time_min'))} TO {int(self.cleaned_data.get('prep_time_max'))}]'
        if self.cleaned_data.get('rating', ''):
            query += f' AND rating:[{int(self.cleaned_data.get('rating'))} TO]'
        if self.cleaned_data.get('n_ingredients_min', 0) and self.cleaned_data.get('n_ingredients_max', ''):
            query += f' AND prep_time:[{int(self.cleaned_data.get('n_ingredients_min'))} TO {int(self.cleaned_data.get('n_ingredients_max'))}]'
        return query