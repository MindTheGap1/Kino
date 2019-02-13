from django import forms

class SearchBar(forms.Form):
	phrase = forms.CharField(max_length=30)