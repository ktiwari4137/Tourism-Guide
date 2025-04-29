from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from .models import Weather
from destinations.models import Destination
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import WeatherSearchForm

# Create your views here.

class WeatherListView(ListView):
    model = Weather
    template_name = 'weather/list.html'
    context_object_name = 'weather_list'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        destination_id = self.request.GET.get('destination')
        date = self.request.GET.get('date')
        
        if destination_id:
            queryset = queryset.filter(destination_id=destination_id)
        if date:
            queryset = queryset.filter(forecast_date=date)
        
        return queryset.order_by('-forecast_date')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['destinations'] = Destination.objects.all()
        return context

class WeatherDetailView(DetailView):
    model = Weather
    template_name = 'weather/forecast_detail.html'
    context_object_name = 'forecast'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.object.destination:
            context['destination'] = self.object.destination
        return context

def weather_info(request):
    form = WeatherSearchForm(request.GET or None)
    forecasts = None
    
    if form.is_valid():
        location = form.cleaned_data['location']
        forecasts = Weather.objects.filter(location__icontains=location)
    
    context = {
        'form': form,
        'forecasts': forecasts,
    }
    return render(request, 'weather/info.html', context)
