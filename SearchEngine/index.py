import os
import yaml
from whoosh.index import create_in, open_dir
from whoosh.fields import Schema, TEXT, NUMERIC, ID
import csv
import pickle


class Index:
    def __init__(self, force_build_index=False, limit=None):
        try:
            with open('./SearchEngine/dataset/rating.pkl', 'rb') as f:
                self.rating_dict = pickle.load(f)
        except Exception:
            raise Exception('Execute review.py first')

        with open('./SearchEngine/config.yaml', 'r') as file:
            config_data = yaml.safe_load(file)

        self.index_dir = f"{config_data['INDEX']['MAINDIR']}"
        self.data_dir = f"./{config_data['DATA']['DATADIR']}"

        self.schema = self.setup_schema()
        self.index = self.setup_index(force_build_index=force_build_index, limit=limit)

    @staticmethod
    def setup_schema():
        # Definire lo schema per l'indice Whoosh
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

        # Creare l'indice Whoosh
        ix = create_in(self.index_dir, self.schema)

        # Aprire il writer
        writer = ix.writer()

        # Percorso completo del file CSV
        csv_file_path = os.path.join(self.data_dir, 'RAW_recipes.csv')

        # Leggere il file CSV e indicizzare i dati
        with open(csv_file_path, 'r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for i, row in enumerate(reader):
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
                if limit and i > limit:
                    writer.commit()
                    return ix

        # Completare la scrittura dell'indice
        writer.commit()
        return ix


if __name__ == '__main__':
    my_index = Index(force_build_index=True, limit=10000)
