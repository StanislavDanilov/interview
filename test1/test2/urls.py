from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views

urlpatterns = [
    path('add', views.add, name='add'),
    path('index', views.index, name='index'),
    path('preview', views.preview, name='preview')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

