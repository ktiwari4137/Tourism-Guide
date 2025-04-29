from django.db import models
from destinations.models import Destination

class Weather(models.Model):
    WEATHER_CONDITIONS = (
        ('SUN', 'Sunny'),
        ('CLD', 'Cloudy'),
        ('RAIN', 'Rainy'),
        ('SNOW', 'Snowy'),
        ('STORM', 'Stormy'),
    )

    WIND_DIRECTIONS = (
        ('N', 'North'),
        ('NE', 'Northeast'),
        ('E', 'East'),
        ('SE', 'Southeast'),
        ('S', 'South'),
        ('SW', 'Southwest'),
        ('W', 'West'),
        ('NW', 'Northwest'),
    )

    location = models.CharField(max_length=100)
    destination = models.ForeignKey(Destination, on_delete=models.CASCADE, related_name='weather', null=True, blank=True)
    temperature = models.DecimalField(max_digits=5, decimal_places=2)
    condition = models.CharField(max_length=5, choices=WEATHER_CONDITIONS)
    humidity = models.IntegerField()
    wind_speed = models.DecimalField(max_digits=5, decimal_places=2)
    wind_direction = models.CharField(max_length=2, choices=WIND_DIRECTIONS)
    pressure = models.IntegerField(help_text='Pressure in hPa')
    uv_index = models.IntegerField()
    precipitation = models.IntegerField(help_text='Precipitation probability in percentage')
    forecast_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Weather for {self.location} on {self.forecast_date}"

    def get_weather_icon(self):
        icon_map = {
            'SUN': 'sun',
            'CLD': 'cloud',
            'RAIN': 'cloud-rain',
            'SNOW': 'snowflake',
            'STORM': 'bolt',
        }
        return icon_map.get(self.condition, 'cloud-sun')

    class Meta:
        ordering = ['-forecast_date']
