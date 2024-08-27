'''import pickle

from tqdm import tqdm

from SearchEngine.sentiment.extract_emotions import ExtractEmotions
import yaml
import os


class ReviewsIndex:
    def __init__(self, force_build_index=False):
        with open('./SearchEngine/config.yaml', 'r') as file:
            self.config_data = yaml.safe_load(file)

        path = f"./{self.config_data['INDEX']['SENTIMENT']}"
        if not os.path.exists(path) or force_build_index:
            self.setupReviewDB()

        with open(path, "rb") as fp:
            self.index = pickle.load(fp)

    def get_sentiments(self, id):
        return self.index.get(id)[0]

    """ 
	Stores in a pickle file a dict containing, for each apartment (id), the reviews sentiments vectors and the amount of reviews, 
 	i.e. a dict with that structure:
		id: ({"anger":x_1, "disgust":x_2, "fear":x_3, "joy":x_4, "neutral":x_5, "sadness":x_6, "surprise":x_7}, int),
		..., 
  
	Actually each sentiment score (x_n) is an overall (mean) value of that sentiment based on all reviews of that apartment.
 	"""

    def setupReviewDB(self):
        print("Building reviews pickle file... ")
        SENTIMENTS = ["anger", "disgust", "fear", "joy", "neutral", "sadness", "surprise"]

        sentiment = ExtractEmotions()

        with open('./SearchEngine/dataset/review.pkl', 'rb') as file:
            review_dict = pickle.load(file)

        sentiment_dict = dict()
        tot_recipes = len(review_dict)
        for i, (recipe_id, list_reviews) in enumerate(review_dict.items()):
            print('Recipe ', i+1, '/', tot_recipes)

            sentiment_dict[recipe_id] = {s: 0 for s in SENTIMENTS}

            for review in tqdm(list_reviews, total=len(list_reviews), desc=f"Indexing Reviews for recipe {recipe_id}"):
                list_sentiment = sentiment.extract(review['review'])[0]
                for s in list_sentiment:
                    sentiment_dict[recipe_id][s['label']] += s['score']

            for s in SENTIMENTS:
                sentiment_dict[recipe_id][s] /= len(list_reviews)

        for k, v in sentiment_dict.items():
            print(k, '->', v, end='\n\n')

        with open(f"./{self.config_data['INDEX']['SENTIMENT']}", mode='wb') as f:
            pickle.dump(sentiment_dict, f)

        print("Review pickle file created successfully! ")

    def get_sentiment_len_for(self, key):
        return self.index.get(int(key))[1]


if __name__ == "__main__":
    rev = ReviewsIndex(force_build_index=True)
'''

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

    def get_sentiments(self, id):
        return self.index.get(id)[0]

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

    def get_sentiment_len_for(self, key):
        return self.index.get(int(key))[1]


if __name__ == "__main__":
    rev = ReviewsIndex(force_build_index=True)
