from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path('', views.home, name='home'),  # Map the home view to the root URL
    path('get-image/', views.get_random_image, name='get_image'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
