from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.contrib import messages
from .models import TourPackage
from .forms import TourPackageForm
from destinations.models import Destination

# Create your views here.

class TourPackageListView(ListView):
    model = TourPackage
    template_name = 'packages/list.html'
    context_object_name = 'packages'
    paginate_by = 9

    def get_queryset(self):
        queryset = super().get_queryset()
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(name__icontains=search)
        return queryset.select_related('destination')

class TourPackageDetailView(DetailView):
    model = TourPackage
    template_name = 'packages/detail.html'
    context_object_name = 'package'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

class TourPackageCreateView(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, CreateView):
    model = TourPackage
    form_class = TourPackageForm
    template_name = 'packages/form.html'
    success_url = reverse_lazy('packages:list')
    success_message = "Tour package was created successfully!"

    def test_func(self):
        return self.request.user.is_staff

class TourPackageUpdateView(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, UpdateView):
    model = TourPackage
    form_class = TourPackageForm
    template_name = 'packages/form.html'
    success_url = reverse_lazy('packages:list')
    success_message = "Tour package was updated successfully!"
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

    def test_func(self):
        return self.request.user.is_staff

class TourPackageDeleteView(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, DeleteView):
    model = TourPackage
    template_name = 'packages/confirm_delete.html'
    success_url = reverse_lazy('packages:list')
    success_message = "Tour package was deleted successfully!"
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

    def test_func(self):
        return self.request.user.is_staff

class PackageListView(ListView):
    model = TourPackage
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
    model = TourPackage
    template_name = 'packages/package_detail.html'
    context_object_name = 'package'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['hotel'] = self.object.hotel
        return context
