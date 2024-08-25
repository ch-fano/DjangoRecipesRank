import pickle
from SearchEngine.sentiment.extract_emotions import ExtractEmotions
import yaml
import os
import json


class ReviewsIndex:
    def __init__(self):
        with open('./SearchEngine/config.yaml', 'r') as file:
            self.config_data = yaml.safe_load(file)

        path = f"./{self.config_data['DATA']['SENTIMENT']}"
        if not os.path.exists(path):
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

        for recipe_id, list_reviews in review_dict.items():
            sentiment_dict[recipe_id] = {s: 0 for s in SENTIMENTS}

            for review in list_reviews:
                list_sentiment = sentiment.extract(review)[0]
                for s in list_sentiment:
                    sentiment_dict[recipe_id][s['label']] += s['score']

            for s in SENTIMENTS:
                sentiment_dict[recipe_id][s] /= len(list_reviews)

        print(sentiment_dict)
        with open(f"./{self.config_data['DATA']['SENTIMENT']}", mode='wb') as f:
            pickle.dump(sentiment_dict, f)

        print("Review pickle file created successfully! ")

    def get_sentiment_len_for(self, key):
        return self.index.get(int(key))[1]


if __name__ == "__main__":
    rev = ReviewsIndex()
