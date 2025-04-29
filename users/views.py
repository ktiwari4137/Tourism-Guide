from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView, UpdateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.conf import settings
from .models import User
from .forms import UserRegistrationForm, UserProfileForm
from bookings.models import Booking
from feedback.models import Feedback
from destinations.models import Destination

# Create your views here.

class UserRegistrationView(CreateView):
    form_class = UserRegistrationForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('destinations:list')

    def form_valid(self, form):
        response = super().form_valid(form)
        # Use the ModelBackend for authentication
        user = authenticate(
            username=form.cleaned_data['username'],
            password=form.cleaned_data['password1'],
            backend='django.contrib.auth.backends.ModelBackend'
        )
        if user is not None:
            login(self.request, user)
        return response

def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('destinations:list')
    else:
        form = AuthenticationForm()
    return render(request, 'users/login.html', {'form': form})

@login_required
def user_logout(request):
    logout(request)
    return redirect('users:login')

@login_required
def profile(request):
    # Get user's recent bookings
    bookings = Booking.objects.filter(user=request.user).order_by('-booking_date')[:5]
    
    # Get user's reviews
    feedbacks = Feedback.objects.filter(user=request.user).order_by('-created_at')[:5]
    
    # Get user's wishlist destinations
    wishlist_destinations = request.user.wishlist_destinations.all()
    
    context = {
        'bookings': bookings,
        'feedbacks': feedbacks,
        'wishlist_destinations': wishlist_destinations,
    }
    return render(request, 'users/profile.html', context)

class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserProfileForm
    template_name = 'users/profile_edit.html'
    success_url = reverse_lazy('users:profile')

    def get_object(self):
        return self.request.user

@login_required
def profile_edit_view(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated successfully!')
            return redirect('users:profile')
    else:
        form = UserProfileForm(instance=request.user)
    
    return render(request, 'users/profile_edit.html', {
        'form': form
    })

@login_required
def password_change_view(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your password has been changed successfully!')
            return redirect('users:profile')
    else:
        form = PasswordChangeForm(request.user)
    
    return render(request, 'users/password_change.html', {
        'form': form
    })
