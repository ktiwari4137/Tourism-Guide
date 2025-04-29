from django.urls import path
from . import views

app_name = 'feedback'

urlpatterns = [
    path('', views.FeedbackListView.as_view(), name='list'),
    path('create/', views.FeedbackCreateView.as_view(), name='create'),
] 