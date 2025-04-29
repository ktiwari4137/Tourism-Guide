from django import forms
from .models import Destination, Attraction, DestinationImage

class DestinationForm(forms.ModelForm):
    class Meta:
        model = Destination
        fields = [
            'name', 'country', 'climate', 'description', 'rating',
            'best_time_to_visit', 'popular_activities', 'local_cuisine',
            'language', 'currency', 'time_zone', 'image'
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'popular_activities': forms.Textarea(attrs={'rows': 3}),
            'local_cuisine': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': 'w-full px-4 py-2 border border-gray-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-emerald-500 focus:border-transparent'
            })

class AttractionForm(forms.ModelForm):
    class Meta:
        model = Attraction
        fields = [
            'name', 'type', 'description', 'image', 'address',
            'opening_hours', 'ticket_price'
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'opening_hours': forms.Textarea(attrs={'rows': 2}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': 'w-full px-4 py-2 border border-gray-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-emerald-500 focus:border-transparent'
            })

class DestinationImageForm(forms.ModelForm):
    class Meta:
        model = DestinationImage
        fields = ['image', 'caption', 'is_featured']
        widgets = {
            'caption': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-emerald-500 focus:border-transparent'
            }),
            'is_featured': forms.CheckboxInput(attrs={
                'class': 'w-4 h-4 text-emerald-600 border-gray-300 rounded focus:ring-emerald-500'
            }),
        } 