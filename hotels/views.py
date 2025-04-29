from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from django.db.models import Q
from .models import Hotel
from destinations.models import Destination

# Create your views here.

class HotelListView(ListView):
    model = Hotel
    template_name = 'hotels/hotel_list.html'
    context_object_name = 'hotels'
    paginate_by = 9

    def get_queryset(self):
        queryset = super().get_queryset()
        destination_id = self.request.GET.get('destination')
        room_type = self.request.GET.get('room_type')
        min_price = self.request.GET.get('min_price')
        max_price = self.request.GET.get('max_price')

        if destination_id:
            queryset = queryset.filter(destination_id=destination_id)
        if room_type:
            queryset = queryset.filter(room_type=room_type)
        if min_price:
            queryset = queryset.filter(price_per_night__gte=min_price)
        if max_price:
            queryset = queryset.filter(price_per_night__lte=max_price)

        return queryset.filter(is_available=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['destinations'] = Destination.objects.all()
        return context

class HotelDetailView(DetailView):
    model = Hotel
    template_name = 'hotels/hotel_detail.html'
    context_object_name = 'hotel'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['packages'] = self.object.packages.all()
        return context
