from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from django.db.models import Q
from .models import Package
from destinations.models import Destination

# Create your views here.

class PackageListView(ListView):
    model = Package
    template_name = 'packages/package_list.html'
    context_object_name = 'packages'
    paginate_by = 9

    def get_queryset(self):
        queryset = super().get_queryset()
        destination_id = self.request.GET.get('destination')
        package_type = self.request.GET.get('package_type')
        min_price = self.request.GET.get('min_price')
        max_price = self.request.GET.get('max_price')
        duration = self.request.GET.get('duration')

        if destination_id:
            queryset = queryset.filter(destination_id=destination_id)
        if package_type:
            queryset = queryset.filter(package_type=package_type)
        if min_price:
            queryset = queryset.filter(price__gte=min_price)
        if max_price:
            queryset = queryset.filter(price__lte=max_price)
        if duration:
            queryset = queryset.filter(duration=duration)

        return queryset.filter(is_available=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['destinations'] = Destination.objects.all()
        return context

class PackageDetailView(DetailView):
    model = Package
    template_name = 'packages/package_detail.html'
    context_object_name = 'package'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['hotel'] = self.object.hotel
        return context
