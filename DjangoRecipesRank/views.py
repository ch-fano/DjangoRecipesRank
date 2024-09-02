import ast

from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST, require_http_methods
from django.conf import settings

from .enums import Enums
from .forms import SearchForm

# download the dataset only one time


def get_home(request):
    form = SearchForm()
    return render(request, 'homepage.html', {'form': form})



@require_http_methods(["GET", "POST"])
def get_result(request):
    if request.method == "POST":
        form = SearchForm(request.POST)
        if form.is_valid():
            cleaned_data = form.cleaned_data
            request.session['search_data'] = cleaned_data  # Salva i dati di ricerca nella sessione
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
            controller = getattr(settings, 'CONTROLLER', None)

            if cleaned_data['selected_model'] == Enums.Model.SENTIMENT:
                model = getattr(settings, 'SENTIMENT_MODEL', None)
            elif cleaned_data['selected_model'] == Enums.Model.REVIEW_SENTIMENT:
                model = getattr(settings, 'SENTIMENT_REVIEW_MODEL', None)
            elif cleaned_data['selected_model'] == Enums.Model.WORD2VEC:
                model = getattr(settings, 'WORD2VEC_MODEL', None)
            else:
                model = getattr(settings, 'BASE_MODEL', None)

            controller.set_model(model)
            controller.set_data(cleaned_data)
            recipes = controller.search()
            print([int(recipe.id) for recipe in recipes])
            paginator = Paginator(recipes, 21)  # 21 ricette per pagina
            page_number = request.GET.get('page')
            page_obj = paginator.get_page(page_number)

            ctx['page_obj'] = page_obj

            return render(request, 'result.html', ctx)
    else:  # Handle GET requests for pagination
        cleaned_data = request.session.get('search_data')
        if cleaned_data:
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
            controller = getattr(settings, 'CONTROLLER', None)

            if cleaned_data['selected_model'] == Enums.Model.SENTIMENT:
                model = getattr(settings, 'SENTIMENT_MODEL', None)
            elif cleaned_data['selected_model'] == Enums.Model.REVIEW_SENTIMENT:
                model = getattr(settings, 'SENTIMENT_REVIEW_MODEL', None)
            elif cleaned_data['selected_model'] == Enums.Model.WORD2VEC:
                model = getattr(settings, 'WORD2VEC_MODEL', None)
            else:
                model = getattr(settings, 'BASE_MODEL', None)

            controller.set_model(model)
            controller.set_data(cleaned_data)
            recipes = controller.search()
            print([int(recipe.id) for recipe in recipes])
            paginator = Paginator(recipes, 21)  # 20 ricette per pagina
            page_number = request.GET.get('page')
            page_obj = paginator.get_page(page_number)

            ctx['page_obj'] = page_obj

            return render(request, 'result.html', ctx)
        else:
            return redirect(get_home)  # Reindirizza alla home se non ci sono dati di ricerca in sessione
def recipe_detail(request, recipe_id):
    ctx = {}
    index = getattr(settings, 'INDEX', None)
    review_dict = getattr(settings, 'REVIEW_DICT', None)
    sentiment_index = getattr(settings, 'SENTIMENT_INDEX', None)

    with index.index.searcher() as searcher:
        document = searcher.document(recipe_id=recipe_id)
        if document:
            document['ingredients'] = ast.literal_eval(document.get("ingredients", '[]'))
            document['steps'] = ast.literal_eval(document.get("steps", '[]'))
            ctx['recipe'] = document
            ctx['reviews'] = review_dict[recipe_id] if review_dict else []
            if sentiment_index:
                ctx['sentiment_list'] = sorted(sentiment_index.index[recipe_id].keys())
                ctx['sentiment_vector'] = [sentiment_index.index[recipe_id][sentiment] for sentiment in ctx['sentiment_list']]
            else:
                ctx['sentiment_list'] = None
                ctx['sentiment_vector'] = []

    return render(request, 'detail.html', ctx)
