from django.db import models
from django.core.validators import MinValueValidator
from django.utils.text import slugify
from django.urls import reverse
from destinations.models import Destination

class TourPackage(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    destination = models.ForeignKey(Destination, on_delete=models.CASCADE, related_name='packages')
    description = models.TextField()
    duration = models.PositiveIntegerField(help_text="Duration in days")
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    max_participants = models.PositiveIntegerField()
    start_date = models.DateField()
    end_date = models.DateField()
    inclusions = models.TextField(help_text="What's included in the package")
    exclusions = models.TextField(help_text="What's not included in the package")
    image = models.ImageField(upload_to='packages/', blank=True, null=True)
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} - {self.destination.name}"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('packages:detail', kwargs={'pk': self.pk})

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['name']),
            models.Index(fields=['destination']),
            models.Index(fields=['price']),
            models.Index(fields=['is_available']),
        ] 