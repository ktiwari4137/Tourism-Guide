from django.urls import path
from . import views

app_name = 'chat'

urlpatterns = [
    path('', views.ChatRoomListView.as_view(), name='list'),
    path('<int:pk>/', views.ChatRoomDetailView.as_view(), name='detail'),
    path('create/', views.ChatRoomCreateView.as_view(), name='create'),
    path('<int:pk>/send/', views.MessageCreateView.as_view(), name='send_message'),
]
