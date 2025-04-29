from django import forms
from .models import Booking
from packages.models import TourPackage

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['package', 'number_of_guests', 'total_price']
        widgets = {
            'package': forms.HiddenInput(),
            'total_price': forms.HiddenInput(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['package'].queryset = TourPackage.objects.filter(is_available=True)
        self.fields['number_of_guests'].widget.attrs.update({
            'class': 'w-full px-4 py-2 border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-emerald-500 focus:border-transparent',
            'min': '1',
            'max': '10'
        }) 