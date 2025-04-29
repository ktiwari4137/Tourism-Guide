from django.urls import path
from . import views

app_name = 'destinations'

urlpatterns = [
    path('', views.destination_list, name='list'),
    path('<slug:slug>/', views.destination_detail, name='detail'),
    path('<slug:slug>/add-to-wishlist/', views.add_to_wishlist, name='add_to_wishlist'),
    path('<slug:slug>/remove-from-wishlist/', views.remove_from_wishlist, name='remove_from_wishlist'),
    
    # Admin-only views
    path('create/', views.DestinationCreateView.as_view(), name='create'),
    path('<slug:slug>/update/', views.DestinationUpdateView.as_view(), name='update'),
    path('<slug:slug>/delete/', views.DestinationDeleteView.as_view(), name='delete'),
] 