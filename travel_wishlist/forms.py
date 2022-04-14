from tkinter import Widget
from django import forms
from .models import Place
from django.forms import FileInput, DateInput

class NewPlaceForm(forms.ModelForm):
    class Meta:
        model = Place
        fields = ('name', 'visited')


class DateInput(forms.DateInput):  # usues django input format
    input_type = 'date'

     
class TripReviewForm(forms.ModelForm):  # information about the object and it belongs to Place.
    class Meta:
        model = Place
        fields = ('note', 'date_visited', 'photo')
        Widgets = {
            'date_visited': DateInput()
        }
