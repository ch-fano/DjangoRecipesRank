
from gensim.models.doc2vec import Doc2Vec, TaggedDocument

from whoosh.analysis import StandardAnalyzer
import json, yaml, os, csv

# define a list of documents.

def word2vec_creation():
    print('Creating the model...')
    docs=[]
    with open('./SearchEngine/config.yaml','r') as file:
        config_data = yaml.safe_load(file)

    csv_file_path = os.path.join(f'./{config_data["DATA"]["DATADIR"]}', 'RAW_recipes_filtered.csv')

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
    
    model.build_vocab(tagged_docs)
    
    model.train(tagged_docs,
                total_examples=model.corpus_count,
                epochs=model.epochs)

    model.save(f'./{config_data["WORD2VEC"]["DATADIR"]}/word2vec.model')
    print("Model created and stored succesfully!")


def to_json():
    print("Creating the json...")
    with open('./SearchEngine/config.yaml', 'r') as file:
        config_data = yaml.safe_load(file)
        
    model = Doc2Vec.load(f'./{config_data["WORD2VEC"]["DATADIR"]}/word2vec.model')  # load the model
    docs_vector = {}

    csv_file_path = os.path.join(f'./{config_data["DATA"]["DATADIR"]}', 'RAW_recipes_filtered.csv')
    with open(csv_file_path, 'r', encoding='utf-8') as csvfile:
        reader = list(csv.DictReader(csvfile))
        for i, row in enumerate(reader):
            docs_vector[row['id']]= model.dv[i]
    
    serializable_docs_vector = {key: value.tolist() for key, value in docs_vector.items()}
    json_path = f'./{config_data["WORD2VEC"]["DATADIR"]}/word_vectors.json'  # json file path
    with open(json_path, 'w') as json_file:
        json.dump(serializable_docs_vector, json_file)  
    print("Json created and stored successfully!")
    
    
if __name__ == "__main__":
    with open('./SearchEngine/config.yaml','r') as file:
        config_data = yaml.safe_load(file)
        
    try:
        if not os.path.exists(f'./{config_data["WORD2VEC"]["DATADIR"]}/word2vec.model'):
            word2vec_creation()
    except FileExistsError:
        pass 
    try:
        if not os.path.exists(f'./{config_data["WORD2VEC"]["DATADIR"]}/word_vectors.json'):
            to_json()
    except FileExistsError:
        pass
