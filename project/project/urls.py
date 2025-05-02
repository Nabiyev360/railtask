from django.contrib import admin
from django.urls import path, include

from tasks.views import index_view

from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('tasks/', include('tasks.urls')),
    path('auths/', include('auths.urls')),
    path('', index_view, name='index'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
