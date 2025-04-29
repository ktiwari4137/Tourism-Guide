from django.urls import path
from . import views

app_name = 'destinations'

urlpatterns = [
    path('', views.DestinationListView.as_view(), name='list'),
    path('<int:pk>/', views.DestinationDetailView.as_view(), name='detail'),
] 