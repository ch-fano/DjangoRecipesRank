# Recipes Search-Engine

## Brief description

This project aims to create a simple search engine operating on a large dataset
of recipes, obtained from a database-scrape of [food.com]().  

Front-end is implemented through `Django Framework`, back-end uses Whoosh and various IR models to search the results.

 
## Installation

Firstly, clone the repository on your local machine:  
```
git clone https://github.com/ch-fano/DjangoRecipesRank
```

Prepare your Python environment (using a `venv` is highly recommended), installing all the necessary packages from the `requirements.txt` file:
```
pip install -r requirements.txt
```  
 
## Setup
Setup all necessary data structures using:
```
python -m SearchEngine.setup
```
Please make sure to be in the root folder of your project when executing this from terminal.  
This will:
- automatically download the dataset from [kaggle.com]()
- clean the dataset to reduce entries a little
- generate Whoosh index
- generate Sentiment Analyses' scores from reviews' texts
- train Doc2Vec model for later usage
 

## Usage
Run the search engine and the relative web interface starting Django's server:
```
python manage.py runserver
```
Please make sure to run **setup.py** file (see previous section) before starting the application for the first time.  

Not doing this will result in a lot of issues and program will probably **not start at all**.

 

## Project Structure

* ***dataset***: this directory contains dataset files downloaded from the web and then cleared. 
* ***word2vec***: this package contains the implementation of ```Doc2VecModel```.
* ***benchmark***: this package contains functions and queries for *benchmarks.ipynb*. 
* ***indexdir***: directory containing the index files. 
* ***sentiment***: this package contains the implementation of ```SentimentModelARWA``` and ```SentimentModelWA```, two slightly different Sentiment Analyses models.
* ***benchmarks.ipynb***: notebook to run benchmarks
* ***controller\.py***: file serves as the central hub for interacting with and orchestrating the functionalities of various other files within this software project. 
* ***index\.py***: this file builds Whoosh's own *schema* and then generates the *index*, which is stored in the *indexdir* directory.
* ***model\.py***: carry out the actual search function after having appropriately selected the model.
* ***config\.yaml***: stores configuration settings and parameters for the search-engine. 

 
## Query Language

The project supports **Natural Query Language**. In addition, when ```SentimentModelARWA``` or ```SentimentModelWA``` are selected, a list of convenient *Sentiments* checkboxes will appear, which allows to rank the retrived documents based on *Sentiments* selected first. 

The documents are retrieved based on the options selected by these filters:
* **Number of results**: to select the number of documents to retrieve.  
* **Number of steps**: to select the minimum and maximum number of steps. 
* **Preparation time**: to select the minimum and maximum minutes needed to complete the recipe.
* **Number of ingredients**: to select the minimum and maximum number of the recipe's ingredients.
* **Year range**: to select the minimum and maximum year in which the recipe was inserted into the database.
* **Minimum rating**: to select the minimum rating the recipe has to have (this is computed using an average of all its reviews).
 

### RAW_recipes.csv
- **id**: The unique identifier for the recipe.
- **name**: The recipe name.
- **minutes**: The estimated time to make the recipe expressed in minutes.
- **contributor_id**: The id of the user that inserted the recipe in the dataset (_unused_).
- **submitted**: The date on which the recipe has been inserted in the dataset.
- **tags**: The tags for the indexing (_unused_).
- **nutrition**: The recipe's nutritional values (_unused_).
- **n_steps**: The number of steps to follow to complete the recipe.
- **steps**: The steps to follow to complete the recipe.
- **description**: The description of the recipe.
- **ingredients**: The list of ingredients to buy.
- **n_ingredients**: The number of ingredients.

 
### RAW_interactions.csv
- **user_id**: The id of the user which has written the review (_unused_).
- **recipe_id**: The id of the recipe on which the review was written.
- **date**: The date on which the review was written.
- **rating**: The rating associated with the recipe.
- **review**: The text of the review.

## Benchmarking
The benchmarking suite is located in `SearchEngine/benchmark`.  
This folder contains a Python file with all the necessary benchmarking functions, and a Jupyter Notebook that allows to run the tests while showing the results.  
To run this, just use your favourite IDE with a Jupyter Notebook plugin installed.
 
## Authors
* Christofer Fanò
* Emanuele Reggiani
* Lorenzo Taccini
