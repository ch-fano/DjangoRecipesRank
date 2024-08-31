import pickle
from tqdm import tqdm
from concurrent.futures import ProcessPoolExecutor, as_completed
from SearchEngine.sentiment.extract_emotions import ExtractEmotions
import yaml
import os

from SearchEngine.constants import BASE_DIR


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
        config_path = os.path.join(BASE_DIR, 'SearchEngine' ,'config.yaml')
        with open(config_path, 'r') as file:
            self.config_data = yaml.safe_load(file)

        review_path = os.path.join(BASE_DIR, 'SearchEngine' ,'dataset', 'review.pkl')

        with open(review_path, 'rb') as file:
            self.review_dict = pickle.load(file)

        index_path =os.path.join(BASE_DIR, self.config_data['INDEX']['SENTIMENT'])
        if not os.path.exists(index_path) or force_build_index:
            self.setupReviewDB()

        with open(index_path, 'rb') as fp:
            self.index = pickle.load(fp)

    def setupReviewDB(self, index_path):
        print("Building reviews pickle file... ")
        SENTIMENTS = ["anger", "disgust", "fear", "joy", "neutral", "sadness", "surprise"]

        sentiment = ExtractEmotions()

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

    def get_sentiment_len_for(self, recipe_id):
        return len(self.review_dict[recipe_id])


if __name__ == "__main__":
    rev = ReviewsIndex(force_build_index=True)
