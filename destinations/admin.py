from django.contrib import admin
from .models import Destination, DestinationImage, Attraction

class DestinationImageInline(admin.TabularInline):
    model = DestinationImage
    extra = 1
    fields = ['image', 'caption', 'is_featured']

class AttractionInline(admin.TabularInline):
    model = Attraction
    extra = 1
    fields = ['name', 'type', 'description', 'image', 'rating']

@admin.register(Destination)
class DestinationAdmin(admin.ModelAdmin):
    list_display = ['name', 'country', 'climate', 'rating', 'created_at']
    list_filter = ['country', 'climate', 'created_at']
    search_fields = ['name', 'country', 'description']
    prepopulated_fields = {'slug': ('name',)}
    inlines = [DestinationImageInline, AttractionInline]
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'slug', 'country', 'climate', 'description', 'image')
        }),
        ('Location', {
            'fields': ('latitude', 'longitude')
        }),
        ('Additional Information', {
            'fields': ('rating', 'review_count', 'best_time_to_visit', 'popular_activities', 
                      'local_cuisine', 'language', 'currency', 'time_zone')
        }),
    )

@admin.register(DestinationImage)
class DestinationImageAdmin(admin.ModelAdmin):
    list_display = ['destination', 'caption', 'is_featured', 'created_at']
    list_filter = ['is_featured', 'created_at']
    search_fields = ['destination__name', 'caption']

@admin.register(Attraction)
class AttractionAdmin(admin.ModelAdmin):
    list_display = ['name', 'destination', 'type', 'rating', 'created_at']
    list_filter = ['type', 'rating', 'created_at']
    search_fields = ['name', 'destination__name', 'description']
    prepopulated_fields = {'slug': ('name',)}
