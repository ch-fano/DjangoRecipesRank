import os
from whoosh.index import create_in, open_dir
from whoosh.fields import Schema, TEXT, NUMERIC, ID
import csv
import pickle
from tqdm import tqdm  # Importa tqdm per la progress bar

from SearchEngine.constants import BASE_DIR, INDEX_DIR, DATASET_DIR


class Index:
    def __init__(self, force_build_index=False, limit=None):
        try:
            rating_dir = os.path.join(BASE_DIR, 'SearchEngine', 'dataset', 'rating.pkl')
            with open(rating_dir, 'rb') as f:
                self.rating_dict = pickle.load(f)
        except Exception:
            raise Exception('Execute read_review.py first')

        self.index_dir = INDEX_DIR
        self.data_dir = DATASET_DIR

        self.schema = self.setup_schema()
        self.index = self.setup_index(force_build_index=force_build_index, limit=limit)

    @staticmethod
    def setup_schema():
        schema = Schema(
            recipe_id=ID(stored=True, unique=False),
            recipe_name=TEXT(stored=True, field_boost=3.0, spelling=True),
            steps=TEXT(stored=True),
            n_steps=NUMERIC(stored=True, numtype=int),
            description=TEXT(stored=True),
            recipe_date=TEXT(stored=True),
            prep_time=NUMERIC(stored=True, numtype=int),
            rating=NUMERIC(stored=True, numtype=float),
            ingredients=TEXT(stored=True, field_boost=2.0),
            n_ingredients=NUMERIC(stored=True, numtype=int)
        )
        return schema

    def setup_index(self, force_build_index, limit):
        if not os.path.exists(self.index_dir) or force_build_index:
            return self.create_index(limit)
        else:
            return open_dir(self.index_dir)

    def create_index(self, limit):
        if not os.path.exists(self.index_dir):
            os.mkdir(self.index_dir)

        ix = create_in(self.index_dir, self.schema)
        writer = ix.writer()

        csv_file_path = os.path.join(self.data_dir, 'RAW_recipes_filtered.csv')

        with open(csv_file_path, 'r', encoding='utf-8') as csvfile:
            reader = list(csv.DictReader(csvfile))  # Converti il reader in una lista per ottenere il numero totale di righe

            # Inizializza tqdm per mostrare la progress bar
            for i, row in tqdm(enumerate(reader), desc="Indexing Recipes", total=len(reader) if not limit else limit):

                    writer.add_document(
                        recipe_id=row['id'],
                        recipe_name=row['name'],
                        prep_time=int(row['minutes']),
                        recipe_date=row['submitted'],
                        n_steps=int(row['n_steps']),
                        steps=row['steps'],
                        description=row['description'],
                        ingredients=row['ingredients'],
                        n_ingredients=int(row['n_ingredients']),
                        rating=self.rating_dict.get(row['id'], 0)
                    )
                    if limit and i >= limit:
                        writer.commit()
                        return ix

        writer.commit()
        return ix


if __name__ == '__main__':
    path = os.path.join(DATASET_DIR, 'RAW_recipes.csv')
    with open(path, 'r', encoding='utf-8') as csvfile:
        r = list(csv.DictReader(csvfile))
        max_minutes=0
        for i, row in enumerate(r):
            if int(row['minutes']) > max_minutes:
                max_minutes = int(row['minutes'])
        print('max prep time is {}'.format(max_minutes))
    #my_index = Index(force_build_index=True, limit=10000)
