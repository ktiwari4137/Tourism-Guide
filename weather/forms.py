from django import forms

class WeatherSearchForm(forms.Form):
    location = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter location (e.g., city, country)',
            'aria-label': 'Location'
        })
    ) 