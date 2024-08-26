from SearchEngine.index import Index
from whoosh import qparser
from whoosh.scoring import WeightingModel
from whoosh.scoring import BM25F


class Recepie:

    def __init__(self, id, name, steps, n_steps, description, date, prep_time, rating, ingredients, n_ingredients):
        self.id = id
        self.name = name
        self.steps = steps
        self.n_steps = n_steps
        self.description = description
        self.date = date
        self.prep_time = prep_time
        self.rating = rating
        self.ingredients = ingredients
        self.n_ingredients = n_ingredients


    def __str__(self):
        return f'[{self.id}] {self.name}'



class IRModel:
    def __init__(self, index: Index, weightingModel: WeightingModel = BM25F):
        self.index = index
        self.model = weightingModel
        self.query = ''

    def search(self, query: str, resLimit = -1, sentiments=None, verbose=True):
        resDict = []
        correctedString = ''
        s = self.index.index.searcher(weighting=self.model)
        try:
            # if isinstance(self.model, SentimentModelWA):
            #     self.model.set_user_sentiment(sentiments)
            # elif isinstance(self.model, Doc2VecModel):
            #     self.model.set_query(query)

            qp = qparser.MultifieldParser(['recipe_name', 'description', 'ingredients'], schema=self.index.schema, group=qparser.OrGroup)

            parsedQ = qp.parse(query)
            if (verbose):
                print(f'Input query: {query}')
                print(f'Parsed query: {parsedQ}')
            results = s.search(parsedQ, terms=True, limit=resLimit) if resLimit > 0 else s.search(parsedQ, terms=True)
            for i in results:
                resDict.append(Recepie(i['recipe_id'], i['recipe_name'], i['steps'], i['n_steps'], i['description'],
                                           i['recipe_date'], i['prep_time'], i['rating'], i['ingredients'],
                                           i['n_ingredients']))

            # Did you Mean? codice per implementarlo
            # corrected = s.correct_query(parsedQ, query)
            # if corrected.query != parsedQ:
            #     correctedString = reduce(
            #         lambda x, y: x + " " + str(y[1]),
            #         list(filter(lambda term: term[1] if term[0] == "name" else "", corrected.query.iter_all_terms())),
            #         ""
            #     ).strip()
        except Exception as e:
            print(e)
        finally:
            s.close()
        #return correctedString, resDict
        return resDict


if __name__ == '__main__':
    print('small debug-only CLI interface for query testing.')
    my_index = Index()
    model = IRModel(my_index)

    while True:
        query = input('Input your query: ')
        resdict = model.search(query, verbose=True)
        for row, (key, values) in enumerate(resdict.items()):
            print(f'{row}: {key}: {values}')