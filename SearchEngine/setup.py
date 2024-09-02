import json
import os
from kaggle.api.kaggle_api_extended import KaggleApi

from SearchEngine.constants import DATASET_DIR
from SearchEngine.index import Index
from SearchEngine.read_review import ReadReview
from SearchEngine.clear_dataset import clear_dataset
from SearchEngine.sentiment.reviews_index import ReviewsIndex
from SearchEngine.word2vec.setup_word2vec import setup_word2vec


def load_api_key(api_key_file):
    with open(api_key_file, 'r') as f:
        api_key_data = json.load(f)
    return api_key_data


# Scarica il dataset specificato dall'URL Kaggle
def download_dataset(dataset_url, output_path):
    # Crea la cartella output_path se non esiste
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    if len(os.listdir(output_path)):
        print("Dataset already exists, or directory is not empty. Skipping download.")
        return

    api = KaggleApi()
    try:
        api.authenticate()
    except Exception as e:
        print(f"Authentication Failed: {e}")
        return

    api.dataset_download_files(dataset_url, path=output_path, unzip=True)

    if len(os.listdir(output_path)):
        print("Dataset scaricato con successo.")
        remove_files(output_path)
    else:
        print("Errore durante il download del dataset.")


def remove_files(output_path):
    for file_name in os.listdir(output_path):
        if file_name not in ['RAW_interactions.csv', 'RAW_recipes.csv']:
            file_path = os.path.join(output_path, file_name)
            if os.path.isfile(file_path):
                os.remove(file_path)

    print(f"Tutti i file superflui sono stati eliminati.")


def create_db():
    dataset_url = "shuyangli94/food-com-recipes-and-user-interactions"



    download_dataset(dataset_url, DATASET_DIR)


if __name__ == "__main__":
    create_db()
    ReadReview(dump_rating=True)
    clear_dataset(min_num_review=7, max_num_review=70)  # delete the recipes with less than min_num_review and more than max_num_review
    Index(force_build_index=True)
    ReviewsIndex(force_build_index=False)
    setup_word2vec()

