from django.contrib import admin
from .models import TourPackage

@admin.register(TourPackage)
class TourPackageAdmin(admin.ModelAdmin):
    list_display = ('name', 'destination', 'price', 'duration', 'is_available')
    list_filter = ('is_available', 'destination')
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}
    date_hierarchy = 'created_at'
