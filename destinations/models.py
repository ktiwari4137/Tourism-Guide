from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.text import slugify
from django.urls import reverse

class Destination(models.Model):
    CLIMATE_CHOICES = [
        ('tropical', 'Tropical'),
        ('temperate', 'Temperate'),
        ('arid', 'Arid'),
        ('continental', 'Continental'),
        ('polar', 'Polar'),
    ]

    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    country = models.CharField(max_length=100)
    climate = models.CharField(max_length=20, choices=CLIMATE_CHOICES)
    description = models.TextField()
    rating = models.DecimalField(max_digits=3, decimal_places=1, validators=[MinValueValidator(0), MaxValueValidator(5)])
    review_count = models.IntegerField(default=0)
    image = models.ImageField(upload_to='destinations/')
    best_time_to_visit = models.CharField(max_length=200, blank=True)
    popular_activities = models.TextField(blank=True)
    local_cuisine = models.TextField(blank=True)
    language = models.CharField(max_length=100, blank=True)
    currency = models.CharField(max_length=50, blank=True)
    time_zone = models.CharField(max_length=50, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name}, {self.country}"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('destinations:detail', kwargs={'slug': self.slug})

    class Meta:
        ordering = ['-rating']
        indexes = [
            models.Index(fields=['name']),
            models.Index(fields=['country']),
            models.Index(fields=['climate']),
            models.Index(fields=['rating']),
        ]

class DestinationImage(models.Model):
    destination = models.ForeignKey(Destination, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='destinations/gallery/')
    caption = models.CharField(max_length=200, blank=True)
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Image for {self.destination.name}"

    class Meta:
        ordering = ['-is_featured', 'created_at']

class Attraction(models.Model):
    ATTRACTION_TYPES = [
        ('natural', 'Natural'),
        ('cultural', 'Cultural'),
        ('historical', 'Historical'),
        ('entertainment', 'Entertainment'),
        ('shopping', 'Shopping'),
    ]

    destination = models.ForeignKey(Destination, related_name='attractions', on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    type = models.CharField(max_length=20, choices=ATTRACTION_TYPES)
    image = models.ImageField(upload_to='attractions/')
    address = models.CharField(max_length=200, blank=True)
    opening_hours = models.CharField(max_length=200, blank=True)
    ticket_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    rating = models.DecimalField(max_digits=3, decimal_places=1, validators=[MinValueValidator(0), MaxValueValidator(5)], default=0)
    review_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('destinations:attraction_detail', kwargs={'slug': self.slug})

    class Meta:
        ordering = ['-rating']
        indexes = [
            models.Index(fields=['name']),
            models.Index(fields=['type']),
            models.Index(fields=['rating']),
        ]
