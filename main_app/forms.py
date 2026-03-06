from django import forms
from .models import Listening

class ListeningForm(forms.ModelForm):
    class Meta:
        model = Listening
        fields = ['date', 'listen_type']
        widgets = {
            'date': forms.DateInput(
                format=('%Y-%m-%d'),
                attrs={'type': 'date'}
            ),
        }