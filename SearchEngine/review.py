import os
import yaml
import csv
import pickle


class ReadReview:
    def __init__(self, dump_rating=False):
        with open('./SearchEngine/config.yaml', 'r') as file:
            config_data = yaml.safe_load(file)

        self.data_dir = f"{config_data['DATA']['DATADIR']}"

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
                    'rating': row['rating'],
                    'review': row['review']
                })

        with open(os.path.join(self.data_dir, self.review_file), 'wb') as file:
            pickle.dump(review_dict, file)
        print('Done.')
        return review_dict

    def dump_ratings(self):
        print('Starting ratings evaluation... ', end='')

        rating_dict = dict()

        for recipe_id, review_list in self.review_dict.items():
            for review in review_list:
                rating_dict['recipe_id'] = rating_dict.get('recipe_id', 0) + int(review['rating'])

            rating_dict['recipe_id'] /= len(review_list)

        with open(os.path.join(self.data_dir, self.rating_file), 'wb') as file:
            pickle.dump(rating_dict, file)

        print('Done.')


if __name__ == '__main__':
    rvw = ReadReview(dump_rating=True)
