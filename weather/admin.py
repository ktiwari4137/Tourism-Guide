from django.contrib import admin
from .models import Weather

@admin.register(Weather)
class WeatherAdmin(admin.ModelAdmin):
    list_display = ('location', 'forecast_date', 'temperature', 'condition', 'humidity')
    list_filter = ('condition', 'forecast_date')
    search_fields = ('location',)
    date_hierarchy = 'forecast_date'
