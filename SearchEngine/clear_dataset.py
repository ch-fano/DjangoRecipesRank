import pickle


# TODO: Creare il file csv con il dataset già pulito in base alle recensioni

def read_pickles():
    try:
        with open('./SearchEngine/dataset/rating.pkl', 'rb') as f:
            rating_dict = pickle.load(f)
    except Exception:
        raise Exception('Execute review.py first')

    try:
        with open('./SearchEngine/dataset/review.pkl', 'rb') as f:
            review_dict = pickle.load(f)
    except Exception:
        raise Exception('Execute review.py first')

    return rating_dict, review_dict


def write_pickles(rating_dict, review_dict):
    with open('./SearchEngine/dataset/rating.pkl', 'wb') as f:
        pickle.dump(rating_dict, f)

    with open('./SearchEngine/dataset/review.pkl', 'wb') as f:
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

    print('Finished to clear the dataset, remaining recipes: ', len(review_dict), '\nDeleted ', tot_deleted, ' recipes')


if __name__ == '__main__':
    clear_dataset(min_num_review=7, max_num_review=70)
