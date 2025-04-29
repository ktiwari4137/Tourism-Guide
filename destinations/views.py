from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from .models import Destination

# Create your views here.

class DestinationListView(ListView):
    model = Destination
    template_name = 'destinations/destination_list.html'
    context_object_name = 'destinations'
    paginate_by = 9

    def get_queryset(self):
        queryset = super().get_queryset()
        country = self.request.GET.get('country')
        if country:
            queryset = queryset.filter(country__icontains=country)
        return queryset

class DestinationDetailView(DetailView):
    model = Destination
    template_name = 'destinations/destination_detail.html'
    context_object_name = 'destination'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['hotels'] = self.object.hotels.all()
        context['packages'] = self.object.packages.all()
        return context
