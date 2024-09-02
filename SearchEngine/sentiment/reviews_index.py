import pickle
from tqdm import tqdm
from concurrent.futures import ProcessPoolExecutor, as_completed
from SearchEngine.sentiment.sentiment_classifier import SentimentClassifier
import os

from SearchEngine.constants import REVIEWS_PATH, SENTIMENT_INDEX_DIR


def process_reviews(recipe_id, list_reviews, SENTIMENTS, sentiment):
    local_sentiments = {s: 0 for s in SENTIMENTS}
    for review in list_reviews:
        list_sentiment = sentiment.extract(review['review'])[0]
        for s in list_sentiment:
            local_sentiments[s['label']] += s['score']
    for s in SENTIMENTS:
        local_sentiments[s] /= len(list_reviews)
    return recipe_id, local_sentiments


class ReviewsIndex:
    def __init__(self, force_build_index=False):

        with open(REVIEWS_PATH, 'rb') as file:
            self.review_dict = pickle.load(file)

        if not os.path.exists(SENTIMENT_INDEX_DIR) or force_build_index:
            self.setup_review_db()

        with open(SENTIMENT_INDEX_DIR, 'rb') as fp:
            self.index = pickle.load(fp)

    def setup_review_db(self, index_path):
        print("Building reviews pickle file... ")
        SENTIMENTS = ["anger", "disgust", "fear", "joy", "neutral", "sadness", "surprise"]

        sentiment = SentimentClassifier()

        sentiment_dict = dict()
        tot_recipes = len(self.review_dict)

        with ProcessPoolExecutor() as executor:
            futures = {executor.submit(process_reviews, recipe_id, list_reviews, SENTIMENTS, sentiment): recipe_id for
                       recipe_id, list_reviews in self.review_dict.items()}
            for future in tqdm(as_completed(futures), total=tot_recipes, desc="Indexing Recipes"):
                recipe_id, sentiments = future.result()
                sentiment_dict[recipe_id] = sentiments

        with open(index_path, mode='wb') as f:
            pickle.dump(sentiment_dict, f)

        print("Review pickle file created successfully!")

    def get_sentiments(self, recipe_id):
        return self.index.get(recipe_id)

    def get_number_of_reviews(self, recipe_id):
        return len(self.review_dict[recipe_id])


if __name__ == "__main__":
    rev = ReviewsIndex(force_build_index=True)
