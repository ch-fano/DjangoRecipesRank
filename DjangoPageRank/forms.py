from django import forms


class SearchForm(forms.Form):
    text_search = forms.CharField(
        label="Words to retrieve",
        widget=forms.TextInput(attrs={'placeholder': 'Search your recipe'}),
        required=True
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

    recipe_date_min = forms.IntegerField(
        label="Minimum Recipe Date",
        required=False,
        widget=forms.NumberInput(attrs={'type': 'range', 'min': '2000', 'max': '2024', 'value': '2000'})
    )

    recipe_date_max = forms.IntegerField(
        label="Maximum Recipe Date",
        required=False,
        widget=forms.NumberInput(attrs={'type': 'range', 'min': '2000', 'max': '2024', 'value': '2024'})
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

    use_sentiment = forms.BooleanField(
        label="Sentiment",
        required=False,
        widget=forms.CheckboxInput()
    )

    chosen_sentiments = forms.MultipleChoiceField(
        label="Chosen Sentiments",
        required=False,
        widget=forms.CheckboxSelectMultiple,
        choices= [
            ('anger', 'Anger'),
            ('disgust', 'Disgust'),
            ('fear', 'Fear'),
            ('joy', 'Joy'),
            ('neutral', 'Neutral'),
            ('sadness', 'Sadness'),
            ('surprise', 'Surprise'),
        ]
    )

    number_of_results = forms.ChoiceField(
        label="Number of Results",
        choices=[(5, "5"), (10, "10"), (15, "15"), (20, "20"), (25, "25")],
        required=False
    )
