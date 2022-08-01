
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views

app_name = 'ntdome'
urlpatterns = [
    path('', views.index, name='index'),
    path('upload', views.image_request, name = "image-request")
]

# + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
