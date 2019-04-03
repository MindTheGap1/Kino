from django import forms
from account import models

class RatingForm(forms.ModelForm):
    ratings_choice = [
        ("1","Didn't like it at all"),
        ("2","It wasn't great"),
        ("3","It's ok"),
        ("4","It was good"),
        ("5","I loved it"),
    ]
    rating = forms.ChoiceField(label = "", choices = ratings_choice, widget=forms.RadioSelect(attrs={'class' : 'ratingbutton'}))

    class Meta:
        model = models.UserMovieStats
        fields = ('rating',)