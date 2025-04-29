from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from destinations.models import Destination
from hotels.models import Hotel

class TravelStyle(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    icon = models.CharField(max_length=50, help_text="Font Awesome icon class")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']

class Package(models.Model):
    PACKAGE_TYPES = (
        ('B', 'Basic'),
        ('S', 'Standard'),
        ('P', 'Premium'),
        ('L', 'Luxury'),
    )

    name = models.CharField(max_length=100)
    description = models.TextField()
    destination = models.ForeignKey(Destination, on_delete=models.CASCADE, related_name='packages')
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name='packages')
    travel_style = models.ForeignKey(TravelStyle, on_delete=models.SET_NULL, null=True, related_name='packages')
    package_type = models.CharField(max_length=1, choices=PACKAGE_TYPES)
    duration = models.IntegerField(help_text="Duration in days")
    price = models.DecimalField(max_digits=10, decimal_places=2)
    inclusions = models.TextField()
    exclusions = models.TextField()
    image = models.ImageField(upload_to='packages/')
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} - {self.destination.name}"

    class Meta:
        ordering = ['-created_at']
