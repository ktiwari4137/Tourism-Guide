from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import CreateView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.urls import reverse_lazy
from .models import Feedback
from packages.models import TourPackage
from hotels.models import Hotel
from .forms import FeedbackForm

# Create your views here.

class FeedbackCreateView(LoginRequiredMixin, CreateView):
    model = Feedback
    form_class = FeedbackForm
    template_name = 'feedback/create.html'
    success_url = reverse_lazy('feedback:list')

    def get_initial(self):
        initial = super().get_initial()
        hotel_id = self.request.GET.get('hotel')
        if hotel_id:
            initial['hotel'] = get_object_or_404(Hotel, id=hotel_id)
        return initial

    def form_valid(self, form):
        form.instance.user = self.request.user
        messages.success(self.request, 'Feedback submitted successfully!')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['hotels'] = Hotel.objects.all()
        return context

class FeedbackListView(ListView):
    model = Feedback
    template_name = 'feedback/list.html'
    context_object_name = 'feedbacks'
    paginate_by = 10

    def get_queryset(self):
        queryset = Feedback.objects.select_related('user', 'hotel').order_by('-created_at')
        rating = self.request.GET.get('rating')
        hotel_id = self.request.GET.get('hotel')

        if rating:
            queryset = queryset.filter(rating=rating)
        if hotel_id:
            queryset = queryset.filter(hotel_id=hotel_id)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['hotels'] = Hotel.objects.all()
        return context
