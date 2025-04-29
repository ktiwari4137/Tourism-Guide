from django import forms
from .models import Booking
from packages.models import Package
from hotels.models import Hotel

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['package', 'hotel', 'check_in_date', 'check_out_date', 'number_of_guests', 'special_requests']
        widgets = {
            'check_in_date': forms.DateInput(attrs={'type': 'date'}),
            'check_out_date': forms.DateInput(attrs={'type': 'date'}),
            'special_requests': forms.Textarea(attrs={'rows': 4}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['package'].queryset = Package.objects.filter(is_available=True)
        self.fields['hotel'].queryset = Hotel.objects.filter(is_available=True) 