from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from tourism_guide.views import home, about, contact

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('about/', about, name='about'),
    path('contact/', contact, name='contact'),
    path('destinations/', include('destinations.urls', namespace='destinations')),
    path('hotels/', include('hotels.urls', namespace='hotels')),
    path('packages/', include('packages.urls', namespace='packages')),
    path('bookings/', include('bookings.urls', namespace='bookings')),
    path('users/', include('users.urls', namespace='users')),
    path('feedback/', include('feedback.urls', namespace='feedback')),
    path('chat/', include('chat.urls', namespace='chat')),
    path('weather/', include('weather.urls', namespace='weather')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
