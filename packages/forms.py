from django import forms
from .models import TourPackage

class TourPackageForm(forms.ModelForm):
    class Meta:
        model = TourPackage
        fields = [
            'name', 'destination', 'description', 'duration', 'price',
            'max_participants', 'start_date', 'end_date', 'inclusions',
            'exclusions', 'image'
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'inclusions': forms.Textarea(attrs={'rows': 3}),
            'exclusions': forms.Textarea(attrs={'rows': 3}),
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': 'w-full px-4 py-2 border border-gray-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-emerald-500 focus:border-transparent'
            })
