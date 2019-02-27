from django import forms
from movies.models import Genre

class SearchForm(forms.Form):
	phrase = forms.CharField(max_length=30,label='Search', required=False)
	total_genre_list = Genre.objects.order_by('genreName')
	genre_select = forms.ModelChoiceField(queryset=total_genre_list, empty_label='Any Genre',label='', required=False)
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