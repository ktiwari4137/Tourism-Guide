from django.urls import path
from . import views

app_name = 'destinations'

urlpatterns = [
    path('', views.DestinationListView.as_view(), name='list'),
    path('create/', views.DestinationCreateView.as_view(), name='create'),
    path('<slug:slug>/', views.DestinationDetailView.as_view(), name='detail'),
    path('<slug:slug>/update/', views.DestinationUpdateView.as_view(), name='update'),
    path('<slug:slug>/delete/', views.DestinationDeleteView.as_view(), name='delete'),
    path('<slug:slug>/manage/', views.ManageDestinationContentView.as_view(), name='manage_content'),
    path('images/<int:pk>/delete/', views.DeleteDestinationImageView.as_view(), name='delete_image'),
    path('attractions/<slug:slug>/delete/', views.DeleteAttractionView.as_view(), name='delete_attraction'),
    path('<slug:slug>/add-to-wishlist/', views.add_to_wishlist, name='add_to_wishlist'),
    path('<slug:slug>/remove-from-wishlist/', views.remove_from_wishlist, name='remove_from_wishlist'),
] 