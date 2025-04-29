from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('register/', views.UserRegistrationView.as_view(), name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('profile/', views.UserProfileUpdateView.as_view(), name='profile'),
    path('profile/edit/', views.profile_edit_view, name='profile_edit'),
    path('password-change/', views.password_change_view, name='password_change'),
] 