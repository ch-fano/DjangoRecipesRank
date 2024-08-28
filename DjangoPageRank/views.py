import ast

from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST
from django.conf import settings
from whoosh.qparser import QueryParser

from SearchEngine.controller import Controller
from SearchEngine.model import IRModel
from SearchEngine.sentiment.sentiment_model import SentimentModelWA
from .forms import SearchForm

# download the dataset only one time


def get_home(request):
    form = SearchForm()
    return render(request, 'homepage.html', {'form': form})


@require_POST
def get_result(request):
    form = SearchForm(request.POST)
    if form.is_valid():
        cleaned_data = form.cleaned_data
        ctx = {}
        ctx = {
             'text_search': cleaned_data.get('text_search', ''),
             'n_steps_min': cleaned_data.get('n_steps_min', ''),
             'n_steps_max': cleaned_data.get('n_steps_max', ''),
             'recipe_date_min': cleaned_data.get('recipe_date_min', ''),
             'recipe_date_max': cleaned_data.get('recipe_date_max', ''),
             'prep_time_min': cleaned_data.get('prep_time_min', ''),
             'prep_time_max': cleaned_data.get('prep_time_max', ''),
             'rating': cleaned_data.get('rating', ''),
             'n_ingredients_min': cleaned_data.get('n_ingredients_min', ''),
             'n_ingredients_max': cleaned_data.get('n_ingredients_max', ''),
        }
        print(ctx)
        controller = getattr(settings,'CONTROLLER', None)
        if cleaned_data['use_sentiment']:
            model = getattr(settings, 'SENTIMENT_MODEL', None)
        else:
            model = getattr(settings, 'BASE_MODEL', None)

        print(cleaned_data.get('chosen_sentiments'))
        controller.set_model(model)
        controller.set_data(cleaned_data)
        ctx['recipes'] = controller.search()

        # Render the result template with the context
        return render(request, 'result.html', ctx)

    return redirect(get_home)

def recipe_detail(request, recipe_id):
    ctx = {}
    index = getattr(settings, 'INDEX', None)

    with index.index.searcher() as searcher:
        document = searcher.document(recipe_id=recipe_id)
        if document:
            document['ingredients'] = ast.literal_eval(document.get("ingredients", '[]'))
            document['steps'] = ast.literal_eval(document.get("steps", '[]'))
            ctx['recipe'] = document
    # with index.searcher() as searcher:
    #     query_parser = QueryParser("recipe_id", schema=index.schema)
    #     query = query_parser.parse(recipe_id)
    #
    #     results = searcher.search(query, limit=1)
    #
    #     if len(results) > 0:
    #         doc = results[0]
    #         ctx['recipe'] = doc

    return render(request, 'detail.html', ctx)
