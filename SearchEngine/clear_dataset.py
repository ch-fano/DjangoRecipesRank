import csv
import os
import pickle
from SearchEngine.constants import BASE_DIR, DATASET_DIR


def read_pickles():
    try:
        rating_dir = os.path.join(BASE_DIR, 'SearchEngine', 'dataset', 'rating.pkl')
        with open(rating_dir, 'rb') as f:
            rating_dict = pickle.load(f)
    except Exception:
        raise Exception('Execute read_review.py first')

    try:
        review_dir = os.path.join(BASE_DIR, 'SearchEngine', 'dataset', 'review.pkl')
        with open(review_dir, 'rb') as f:
            review_dict = pickle.load(f)
    except Exception:
        raise Exception('Execute read_review.py first')

    return rating_dict, review_dict


def write_pickles(rating_dict, review_dict):

    rating_dir = os.path.join(BASE_DIR, 'SearchEngine', 'dataset', 'rating.pkl')
    with open(rating_dir, 'wb') as f:
        pickle.dump(rating_dict, f)

    review_dir = os.path.join(BASE_DIR, 'SearchEngine', 'dataset', 'review.pkl')
    with open(review_dir, 'wb') as f:
        pickle.dump(review_dict, f)


def clear_dataset(min_num_review, max_num_review):
    rating_dict, review_dict = read_pickles()

    print('Starting to clear the dataset, actual number of recipes: ', len(review_dict))

    delete_recipes = list()
    for recipe_id, list_review in review_dict.items():
        length = len(list_review)

        if not (min_num_review <= length <= max_num_review):
            delete_recipes.append(recipe_id)

    tot_deleted = len(delete_recipes)
    for recipe_id in delete_recipes:
        del review_dict[recipe_id]
        del rating_dict[recipe_id]

    write_pickles(rating_dict, review_dict)
    filter_csv_files(review_dict.keys())


    print('Finished to clear the dataset, remaining recipes: ', len(review_dict), '\nDeleted ', tot_deleted, ' recipes')

def filter_csv_files(valid_ids):

    # Filter RAW_interactions.csv
    interactions_path = os.path.join(DATASET_DIR, 'RAW_interactions.csv')
    filter_csv(interactions_path, valid_ids, 'recipe_id')

    # Filter RAW_recipes.csv
    recipes_path = os.path.join(DATASET_DIR, 'RAW_recipes.csv')
    filter_csv(recipes_path, valid_ids, 'id')


def filter_csv(file_path, valid_ids, id_field):
    temp_file_path = file_path.replace('.csv', '_filtered.csv')

    with open(file_path, 'r', newline='', encoding='utf-8') as infile, open(temp_file_path, 'w', newline='', encoding='utf-8') as outfile:
        reader = csv.DictReader(infile)
        writer = csv.DictWriter(outfile, fieldnames=reader.fieldnames)

        writer.writeheader()

        for row in reader:
            if row[id_field] in valid_ids:
                # Convert the row to a dictionary (already in dictionary form)
                filtered_row = {key: row[key] for key in reader.fieldnames}
                writer.writerow(filtered_row)

    # Replace the original file with the filtered one
    #os.replace(temp_file_path, file_path)

if __name__ == '__main__':
    clear_dataset(min_num_review=7, max_num_review=70)
