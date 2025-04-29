from django.urls import path
from . import views

app_name = 'destinations'

urlpatterns = [
    path('', views.DestinationListView.as_view(), name='list'),
    path('create/', views.DestinationCreateView.as_view(), name='create'),
    path('<slug:slug>/', views.DestinationDetailView.as_view(), name='detail'),
    path('<slug:slug>/update/', views.DestinationUpdateView.as_view(), name='update'),
    path('<slug:slug>/delete/', views.DestinationDeleteView.as_view(), name='delete'),
] 