from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import CreateView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.urls import reverse_lazy
from .models import Feedback
from packages.models import Package
from hotels.models import Hotel
from .forms import FeedbackForm

# Create your views here.

class FeedbackCreateView(LoginRequiredMixin, CreateView):
    model = Feedback
    form_class = FeedbackForm
    template_name = 'feedback/feedback_create.html'
    success_url = reverse_lazy('feedback:list')

    def get_initial(self):
        initial = super().get_initial()
        package_id = self.request.GET.get('package')
        hotel_id = self.request.GET.get('hotel')
        
        if package_id:
            package = get_object_or_404(Package, id=package_id)
            initial['package'] = package
        elif hotel_id:
            hotel = get_object_or_404(Hotel, id=hotel_id)
            initial['hotel'] = hotel
        
        return initial

    def form_valid(self, form):
        form.instance.user = self.request.user
        messages.success(self.request, 'Feedback submitted successfully!')
        return super().form_valid(form)

class FeedbackListView(ListView):
    model = Feedback
    template_name = 'feedback/feedback_list.html'
    context_object_name = 'feedbacks'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        package_id = self.request.GET.get('package')
        hotel_id = self.request.GET.get('hotel')
        
        if package_id:
            queryset = queryset.filter(package_id=package_id)
        elif hotel_id:
            queryset = queryset.filter(hotel_id=hotel_id)
        
        return queryset.order_by('-created_at')
