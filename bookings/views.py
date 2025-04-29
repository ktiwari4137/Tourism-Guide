from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, CreateView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.urls import reverse_lazy
from .models import Booking
from packages.models import TourPackage
from hotels.models import Hotel
from .forms import BookingForm
from django.contrib.auth.decorators import login_required

class BookingCreateView(LoginRequiredMixin, CreateView):
    model = Booking
    form_class = BookingForm
    template_name = 'bookings/booking_create.html'
    success_url = reverse_lazy('bookings:history')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        package_id = self.kwargs.get('package_id')
        if package_id:
            context['package'] = get_object_or_404(TourPackage, id=package_id)
        return context

    def get_initial(self):
        initial = super().get_initial()
        package_id = self.kwargs.get('package_id')
        
        if package_id:
            package = get_object_or_404(TourPackage, id=package_id)
            initial['package'] = package
            initial['total_price'] = package.price
        
        return initial

    def form_valid(self, form):
        form.instance.user = self.request.user
        messages.success(self.request, 'Booking created successfully!')
        return super().form_valid(form)

class BookingHistoryView(LoginRequiredMixin, ListView):
    model = Booking
    template_name = 'bookings/booking_history.html'
    context_object_name = 'bookings'

    def get_queryset(self):
        return Booking.objects.filter(user=self.request.user).order_by('-booking_date')

class BookingDetailView(LoginRequiredMixin, DetailView):
    model = Booking
    template_name = 'bookings/booking_detail.html'
    context_object_name = 'booking'

    def get_queryset(self):
        return Booking.objects.filter(user=self.request.user)

@login_required
def cancel_booking(request, pk):
    booking = get_object_or_404(Booking, pk=pk, user=request.user)
    if booking.status == 'P':
        booking.status = 'X'
        booking.save()
        messages.success(request, 'Booking cancelled successfully!')
    else:
        messages.error(request, 'Cannot cancel this booking.')
    return redirect('bookings:history')
