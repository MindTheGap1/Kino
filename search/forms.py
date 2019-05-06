from django import forms
from movies.models import Genre

class SearchForm(forms.Form):
	phrase = forms.CharField(max_length=30,label='', required=False)
	total_genre_list = Genre.objects.order_by('genreName')
	genre_select = forms.ModelChoiceField(queryset=total_genre_list, empty_label='Any Genre',label='', required=False)
	sorting_choices = [(0, 'Search Relevance'),
						(1, 'Name Ascending'),
						(2, 'Name Descending'),
						(3, 'Cost Ascending'),
						(4, 'Cost Descending'),
						(5, 'Overall Rating Ascending'),
						(6, 'Overall Rating Descending'),
						(7, 'Length Ascending'),
						(8, 'Length Descending'),
						(9, 'Release Date Ascending'),
						(10, 'Release Date Descending')]
	sort_select = forms.ChoiceField(choices=sorting_choices,label='', required=False)

class SortForm(forms.Form):
	sorting_choices = [(0, 'Name Ascending'),
						(1, 'Name Descending'),
						(2, 'Cost Ascending'),
						(3, 'Cost Descending'),
						(4, 'Overall Rating Ascending'),
						(5, 'Overall Rating Descending'),
						(6, 'Length Ascending'),
						(7, 'Length Descending'),
						(8, 'Release Date Ascending'),
						(9, 'Release Date Descending')]
	sort_select = forms.ChoiceField(choices=sorting_choices,label='', required=False)