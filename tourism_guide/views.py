from django.shortcuts import render
from destinations.models import Destination
from packages.models import TourPackage
from feedback.models import Feedback

def home(request):
    # Get top rated destinations
    featured_destinations = Destination.objects.order_by('-rating')[:3]
    
    # Get available packages ordered by price (ascending)
    popular_packages = TourPackage.objects.filter(is_available=True).order_by('price')[:3]
    
    # Get recent testimonials with user data
    testimonials = Feedback.objects.select_related('user').order_by('-created_at')[:3]
    
    context = {
        'featured_destinations': featured_destinations,
        'popular_packages': popular_packages,
        'testimonials': testimonials,
    }
    
    return render(request, 'home.html', context)

def about(request):
    return render(request, 'about.html')

def contact(request):
    return render(request, 'contact.html') 