from django.contrib import admin
from django.urls import path, include  # Adicione 'include'
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),  # Redireciona todas as URLs não administrativas para 'core.urls'
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
