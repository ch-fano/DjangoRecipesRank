from django import forms


class SearchForm(forms.Form):
    text_search = forms.CharField(
        label="Words to retrieve",
        widget=forms.TextInput(attrs={'placeholder': 'Search your recipe'}),
        required=False
    )

    n_steps_min = forms.IntegerField(
        label="Minimum Number of Steps",
        required=False,
        widget=forms.NumberInput(attrs={'type': 'range', 'min': '1', 'max': '50', 'value': '1'})
    )

    n_steps_max = forms.IntegerField(
        label="Maximum Number of Steps",
        required=False,
        widget=forms.NumberInput(attrs={'type': 'range', 'min': '1', 'max': '50', 'value': '50'})
    )

    recipe_date = forms.CharField(
        label="Recipe Date",
        max_length=50,
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Recipe Date'})
    )

    prep_time_min = forms.IntegerField(
        label="Minimum Preparation Time (minutes)",
        required=False,
        widget=forms.NumberInput(attrs={'type': 'range', 'min': '1', 'max': '10000', 'value': '1'})
    )

    prep_time_max = forms.IntegerField(
        label="Maximum Preparation Time (minutes)",
        required=False,
        widget=forms.NumberInput(attrs={'type': 'range', 'min': '1', 'max': '10000', 'value': '10000'})
    )

    rating = forms.IntegerField(
        label="Minimum rating",
        required=False,
        widget=forms.RadioSelect(choices=[(i, f"{i} ★") for i in range(0, 6)])
    )

    n_ingredients_min = forms.IntegerField(
        label="Minimum Number of Ingredients",
        required=False,
        widget=forms.NumberInput(attrs={'type': 'range', 'min': '1', 'max': '20', 'value': '1'})
    )

    n_ingredients_max = forms.IntegerField(
        label="Maximum Number of Ingredients",
        required=False,
        widget=forms.NumberInput(attrs={'type': 'range', 'min': '1', 'max': '20', 'value': '20'})
    )
