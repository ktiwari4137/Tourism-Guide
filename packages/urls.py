from django.urls import path
from . import views

app_name = 'packages'

urlpatterns = [
    path('', views.TourPackageListView.as_view(), name='list'),
    path('create/', views.TourPackageCreateView.as_view(), name='create'),
    path('<slug:slug>/', views.TourPackageDetailView.as_view(), name='detail'),
    path('<slug:slug>/update/', views.TourPackageUpdateView.as_view(), name='update'),
    path('<slug:slug>/delete/', views.TourPackageDeleteView.as_view(), name='delete'),
]
