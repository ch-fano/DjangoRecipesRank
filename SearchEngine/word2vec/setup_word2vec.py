
from gensim.models.doc2vec import Doc2Vec, TaggedDocument

from whoosh.analysis import StandardAnalyzer
import json, os, csv

from SearchEngine.constants import DATASET_DIR, WORD2VEC_MODEL, WORD2VEC_JSON


# define a list of documents.

def word2vec_creation():
    print('Creating the model...')
    docs=[]

    csv_file_path = os.path.join(DATASET_DIR, 'RAW_recipes_filtered.csv')

    with open(csv_file_path, 'r', encoding='utf-8') as csvfile:
        reader = list(csv.DictReader(csvfile))
        for row in reader:
            docs.append(f'{row["name"]} {row["description"]} {row["ingredients"]}')

    print('Added all the documents')

    # preproces the documents, and create TaggedDocuments
    analyzer = StandardAnalyzer()
    tagged_docs = [TaggedDocument(words=[token.text for token in analyzer(doc)],tags=[str(i)]) for i, doc in enumerate(docs)]

    # train the Doc2vec model
    model = Doc2Vec(vector_size=50,
                    min_count=1, epochs=100, workers=8)
    print('building vocab')
    model.build_vocab(tagged_docs)
    print('training')
    model.train(tagged_docs,
                total_examples=model.corpus_count,
                epochs=model.epochs)
    print('training done, now saving')
    with open(WORD2VEC_MODEL,'wb') as model_file:
        model.save(model_file)
        print("Model created and stored successfully!")


def to_json():
    print("Creating the json...")

    model = Doc2Vec.load(WORD2VEC_MODEL)  # load the model
    docs_vector = {}

    csv_file_path = os.path.join(DATASET_DIR, 'RAW_recipes_filtered.csv')
    with open(csv_file_path, 'r', encoding='utf-8') as csvfile:
        reader = list(csv.DictReader(csvfile))
        for i, row in enumerate(reader):
            docs_vector[row['id']]= model.dv[i]
    
    serializable_docs_vector = {key: value.tolist() for key, value in docs_vector.items()}
    with open(WORD2VEC_JSON, 'w') as json_file:
        json.dump(serializable_docs_vector, json_file)  
    print("Json created and stored successfully!")
    
def setup_word2vec():

    try:
        if not os.path.exists(WORD2VEC_MODEL):
            word2vec_creation()
    except FileExistsError:
        pass
    try:
        if not os.path.exists(WORD2VEC_JSON):
            to_json()
    except FileExistsError:
        pass

if __name__ == "__main__":
    setup_word2vec()
