import os
import csv
import pickle

from SearchEngine.constants import DATASET_DIR


class ReadReview:
    def __init__(self, dump_rating=False):
        self.data_dir = DATASET_DIR

        self.review_file = 'review.pkl'
        self.rating_file = 'rating.pkl'

        self.review_dict = self.dump_reviews()

        if dump_rating:
            self.dump_ratings()

    def dump_reviews(self):
        if not os.path.exists(self.data_dir):
            raise Exception('Execute setup first')

        print('Starting reviews dump... ', end='')

        csv_file_path = os.path.join(self.data_dir, 'RAW_interactions.csv')

        with open(csv_file_path, 'r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            review_dict = dict()
            for row in reader:
                if not review_dict.get(row['recipe_id'], None):
                    review_dict[row['recipe_id']] = list()

                review_dict[row['recipe_id']].append({
                    'user_id': row['user_id'],
                    'date': row['date'],
                    'rating': int(row['rating']),
                    'review': row['review']
                })

                review_dict[row['recipe_id']].sort(key=lambda x: x['date'], reverse=True)

        with open(os.path.join(self.data_dir, self.review_file), 'wb') as file:
            pickle.dump(review_dict, file)
        print('Done.')
        return review_dict

    def dump_ratings(self):
        print('Starting ratings evaluation... ', end='')

        rating_dict = dict()

        for recipe_id, review_list in self.review_dict.items():
            for review in review_list:
                if recipe_id not in rating_dict:
                    rating_dict[recipe_id] = 0

                rating_dict[recipe_id] += int(review['rating'])

            rating_dict[recipe_id] /= len(review_list)

        with open(os.path.join(self.data_dir, self.rating_file), 'wb') as file:
            pickle.dump(rating_dict, file)

        print('Done.')


if __name__ == '__main__':
    rvw = ReadReview(dump_rating=True)
