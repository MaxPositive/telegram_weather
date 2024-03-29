from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path(settings.ADMIN_URL, admin.site.urls),
    path("", include("weather.urls")),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
