from django.urls import path
from . import views

app_name = 'weather'

urlpatterns = [
    path('', views.weather_info, name='info'),
    path('list/', views.WeatherListView.as_view(), name='list'),
    path('forecast/<int:pk>/', views.WeatherDetailView.as_view(), name='forecast_detail'),
]
