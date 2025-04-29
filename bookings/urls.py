from django.urls import path
from . import views

app_name = 'bookings'

urlpatterns = [
    path('create/<int:package_id>/', views.BookingCreateView.as_view(), name='create'),
    path('history/', views.BookingHistoryView.as_view(), name='history'),
    path('<int:pk>/', views.BookingDetailView.as_view(), name='detail'),
    path('<int:pk>/cancel/', views.cancel_booking, name='cancel'),
] 