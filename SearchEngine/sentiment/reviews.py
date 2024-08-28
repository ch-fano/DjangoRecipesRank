import pickle
from tqdm import tqdm
from concurrent.futures import ProcessPoolExecutor, as_completed
from SearchEngine.sentiment.extract_emotions import ExtractEmotions
import yaml
import os


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
        with open('./SearchEngine/config.yaml', 'r') as file:
            self.config_data = yaml.safe_load(file)

        path = f"./{self.config_data['INDEX']['SENTIMENT']}"
        if not os.path.exists(path) or force_build_index:
            self.setupReviewDB()

        with open(path, "rb") as fp:
            self.index = pickle.load(fp)


    def setupReviewDB(self):
        print("Building reviews pickle file... ")
        SENTIMENTS = ["anger", "disgust", "fear", "joy", "neutral", "sadness", "surprise"]

        sentiment = ExtractEmotions()

        with open('./SearchEngine/dataset/review.pkl', 'rb') as file:
            review_dict = pickle.load(file)

        sentiment_dict = dict()
        tot_recipes = len(review_dict)

        with ProcessPoolExecutor() as executor:
            futures = {executor.submit(process_reviews, recipe_id, list_reviews, SENTIMENTS, sentiment): recipe_id for recipe_id, list_reviews in review_dict.items()}
            for future in tqdm(as_completed(futures), total=tot_recipes, desc="Indexing Recipes"):
                recipe_id, sentiments = future.result()
                sentiment_dict[recipe_id] = sentiments

        with open(f"./{self.config_data['INDEX']['SENTIMENT']}", mode='wb') as f:
            pickle.dump(sentiment_dict, f)

        print("Review pickle file created successfully! ")

    def get_sentiments(self, recipe_id):
        return self.index.get(recipe_id)

    def get_sentiment_len_for(self, key):
        with open('./SearchEngine/dataset/review.pkl', 'rb') as file:
            review_dict = pickle.load(file)

        return len(review_dict[int(key)])
        #return self.index.get(int(key))[1]


if __name__ == "__main__":
    rev = ReviewsIndex(force_build_index=True)
