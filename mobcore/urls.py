from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('apps.frontend.urls')),
    path('mobsinet/', include('apps.mobsinet.urls'))
]
