from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Destination, Attraction, DestinationImage
from .forms import DestinationForm, AttractionForm, DestinationImageForm
from packages.models import TourPackage
from django.http import JsonResponse
from django.conf import settings

# Create your views here.

class DestinationListView(ListView):
    model = Destination
    template_name = 'destinations/list.html'
    context_object_name = 'destinations'
    paginate_by = 9

    def get_queryset(self):
        queryset = super().get_queryset()
        search = self.request.GET.get('search')
        country = self.request.GET.get('country')
        climate = self.request.GET.get('climate')

        if search:
            queryset = queryset.filter(
                Q(name__icontains=search) |
                Q(country__icontains=search) |
                Q(description__icontains=search)
            )
        if country:
            queryset = queryset.filter(country__icontains=country)
        if climate:
            queryset = queryset.filter(climate=climate)

        return queryset.select_related().prefetch_related('images', 'attractions')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['countries'] = Destination.objects.values_list('country', flat=True).distinct()
        context['climates'] = [choice[0] for choice in Destination.CLIMATE_CHOICES]
        return context

class DestinationDetailView(DetailView):
    model = Destination
    template_name = 'destinations/detail.html'
    context_object_name = 'destination'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['images'] = self.object.images.all()
        context['attractions'] = self.object.attractions.all()
        context['tour_packages'] = TourPackage.objects.filter(destination=self.object)
        context['weather_api_key'] = getattr(settings, 'OPENWEATHERMAP_API_KEY', '')
        return context

class DestinationCreateView(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, CreateView):
    model = Destination
    form_class = DestinationForm
    template_name = 'destinations/destination_form.html'
    success_url = reverse_lazy('destinations:list')
    success_message = "Destination was created successfully!"

    def test_func(self):
        return self.request.user.is_staff

class DestinationUpdateView(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, UpdateView):
    model = Destination
    form_class = DestinationForm
    template_name = 'destinations/destination_form.html'
    success_url = reverse_lazy('destinations:list')
    success_message = "Destination was updated successfully!"
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

    def test_func(self):
        return self.request.user.is_staff

class DestinationDeleteView(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, DeleteView):
    model = Destination
    template_name = 'destinations/destination_confirm_delete.html'
    success_url = reverse_lazy('destinations:list')
    success_message = "Destination was deleted successfully!"
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

    def test_func(self):
        return self.request.user.is_staff

class AttractionDetailView(DetailView):
    model = Attraction
    template_name = 'destinations/attraction_detail.html'
    context_object_name = 'attraction'

class AttractionCreateView(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, CreateView):
    model = Attraction
    form_class = AttractionForm
    template_name = 'destinations/attraction_form.html'
    success_message = "Attraction was created successfully!"

    def form_valid(self, form):
        form.instance.destination = get_object_or_404(Destination, slug=self.kwargs.get('slug'))
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('destinations:detail', kwargs={'slug': self.kwargs.get('slug')})

    def test_func(self):
        return self.request.user.is_staff

class AttractionUpdateView(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, UpdateView):
    model = Attraction
    form_class = AttractionForm
    template_name = 'destinations/attraction_form.html'
    success_message = "Attraction was updated successfully!"

    def get_success_url(self):
        return reverse_lazy('destinations:detail', kwargs={'slug': self.object.destination.slug})

    def test_func(self):
        return self.request.user.is_staff

class AttractionDeleteView(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, DeleteView):
    model = Attraction
    template_name = 'destinations/attraction_confirm_delete.html'
    success_message = "Attraction was deleted successfully!"

    def get_success_url(self):
        return reverse_lazy('destinations:detail', kwargs={'slug': self.object.destination.slug})

    def test_func(self):
        return self.request.user.is_staff

class DestinationImageCreateView(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, CreateView):
    model = DestinationImage
    form_class = DestinationImageForm
    template_name = 'destinations/image_form.html'
    success_message = "Image was added successfully!"

    def form_valid(self, form):
        form.instance.destination = get_object_or_404(Destination, slug=self.kwargs.get('slug'))
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('destinations:detail', kwargs={'slug': self.kwargs.get('slug')})

    def test_func(self):
        return self.request.user.is_staff

def destination_list(request):
    destinations = Destination.objects.all()
    return render(request, 'destinations/list.html', {'destinations': destinations})

def destination_detail(request, slug):
    destination = get_object_or_404(Destination, slug=slug)
    return render(request, 'destinations/detail.html', {'destination': destination})

@login_required
def add_to_wishlist(request, slug):
    destination = get_object_or_404(Destination, slug=slug)
    if destination not in request.user.wishlist_destinations.all():
        request.user.wishlist_destinations.add(destination)
        messages.success(request, f'{destination.name} added to your wishlist!')
    else:
        messages.info(request, f'{destination.name} is already in your wishlist!')
    return redirect('destinations:detail', slug=slug)

@login_required
def remove_from_wishlist(request, slug):
    destination = get_object_or_404(Destination, slug=slug)
    if destination in request.user.wishlist_destinations.all():
        request.user.wishlist_destinations.remove(destination)
        messages.success(request, f'{destination.name} removed from your wishlist!')
    return redirect('users:profile')

class ManageDestinationContentView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Destination
    template_name = 'destinations/manage_content.html'
    context_object_name = 'destination'

    def test_func(self):
        return self.request.user.is_staff

    def post(self, request, *args, **kwargs):
        destination = self.get_object()
        form_type = request.POST.get('form_type')

        if form_type == 'image':
            # Handle image upload
            image = request.FILES.get('image')
            caption = request.POST.get('caption', '')
            is_featured = request.POST.get('is_featured') == 'on'

            if image:
                DestinationImage.objects.create(
                    destination=destination,
                    image=image,
                    caption=caption,
                    is_featured=is_featured
                )
                messages.success(request, 'Image added successfully!')
            else:
                messages.error(request, 'Please select an image to upload.')

        elif form_type == 'attraction':
            # Handle attraction creation
            name = request.POST.get('name')
            description = request.POST.get('description')
            type = request.POST.get('type')
            image = request.FILES.get('image')
            address = request.POST.get('address')
            opening_hours = request.POST.get('opening_hours')
            ticket_price = request.POST.get('ticket_price')

            if name and description and type and image:
                Attraction.objects.create(
                    destination=destination,
                    name=name,
                    description=description,
                    type=type,
                    image=image,
                    address=address,
                    opening_hours=opening_hours,
                    ticket_price=ticket_price
                )
                messages.success(request, 'Attraction added successfully!')
            else:
                messages.error(request, 'Please fill in all required fields.')

        return redirect('destinations:manage_content', slug=destination.slug)

class DeleteDestinationImageView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = DestinationImage
    success_url = reverse_lazy('destinations:list')

    def test_func(self):
        return self.request.user.is_staff

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        destination_slug = self.object.destination.slug
        self.object.delete()
        messages.success(request, 'Image deleted successfully!')
        return redirect('destinations:manage_content', slug=destination_slug)

class DeleteAttractionView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Attraction
    success_url = reverse_lazy('destinations:list')

    def test_func(self):
        return self.request.user.is_staff

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        destination_slug = self.object.destination.slug
        self.object.delete()
        messages.success(request, 'Attraction deleted successfully!')
        return redirect('destinations:manage_content', slug=destination_slug)
