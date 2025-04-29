from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from destinations.models import Destination

class Hotel(models.Model):
    ROOM_TYPES = (
        ('S', 'Single'),
        ('D', 'Double'),
        ('T', 'Twin'),
        ('Q', 'Quad'),
        ('SU', 'Suite'),
    )

    name = models.CharField(max_length=100)
    destination = models.ForeignKey(Destination, on_delete=models.CASCADE, related_name='hotels')
    description = models.TextField()
    address = models.TextField()
    rating = models.DecimalField(max_digits=3, decimal_places=2, validators=[MinValueValidator(0), MaxValueValidator(5)])
    price_per_night = models.DecimalField(max_digits=10, decimal_places=2)
    room_type = models.CharField(max_length=2, choices=ROOM_TYPES)
    amenities = models.TextField()
    image = models.ImageField(upload_to='hotels/')
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} - {self.destination.name}"

    class Meta:
        ordering = ['-rating']
