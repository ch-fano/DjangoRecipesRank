from django.shortcuts import render
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
    pass


def get_recipe(request):
    pass
