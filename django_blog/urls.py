from django.contrib import admin
from django.urls import path
from django.urls.conf import include
from django.conf import settings
from django.conf.urls.static import static

admin.site.site_header  =  "Django Blog"  
admin.site.site_title  =  "Django Blog"
admin.site.index_title  =  "Django Blog"

urlpatterns = [
    path("admin/", admin.site.urls),
    path('', include('blog.urls')),
    path('auth/', include('authentication.urls')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)




urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
