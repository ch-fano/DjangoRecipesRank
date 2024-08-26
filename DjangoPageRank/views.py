from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST
from .forms import SearchForm
import pickle

# download the dataset only one time

try:
    with open('./SearchEngine/dataset/review.pkl', 'rb') as f:
        review_dict = pickle.load(f)
except Exception:
    review_dict = None
    raise Exception('Execute review.py first')


def get_home(request):
    form = SearchForm()
    return render(request, 'homepage.html', {'form': form})

@require_POST
def get_result(request):
    form = SearchForm(request.POST)
    if form.is_valid():
        cleaned_data = form.cleaned_data

        ctx = {
            'text_search': cleaned_data.get('text_search', ''),
            'n_steps_min': cleaned_data.get('n_steps_min', ''),
            'n_steps_max': cleaned_data.get('n_steps_max', ''),
            'recipe_date_min': cleaned_data.get('recipe_date_min', ''),
            'prep_time_min': cleaned_data.get('prep_time_min', ''),
            'prep_time_max': cleaned_data.get('prep_time_max', ''),
            'rating': cleaned_data.get('rating', ''),
            'n_ingredients_min': cleaned_data.get('n_ingredients_min', ''),
            'n_ingredients_max': cleaned_data.get('n_ingredients_max', ''),
        }

        # Render the result template with the context
        return render(request, 'result.html', ctx)

    return redirect(get_home)

def get_recipe(request):
    pass
