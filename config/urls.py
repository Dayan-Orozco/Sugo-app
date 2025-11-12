from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
import os
from config.settings import *
from .views import *
urlpatterns = [
    
    path('', home, name="home"),  
    path('course/', include('apps.course.urls')),
    path('sugo/', include('apps.sugo.urls')),
    path('admin/', admin.site.urls),
    path('user/', include('apps.user.urls')),
]

# Sirve archivos estáticos y de medios solo en desarrollo
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=os.path.join(BASE_DIR, 'static'))
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)