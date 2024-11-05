# blogicum/blogicum/urls.py
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from blog.views import UserRegisterView

handler404 = 'pages.views.custom_404_view'
handler500 = 'pages.views.custom_500_view'
handler403 = 'pages.views.custom_403_view'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('django.contrib.auth.urls')),
    path('pages/', include('pages.urls')),
    path('auth/registration/',
         UserRegisterView.as_view(),
         name='registration'),
    path('', include('blog.urls')),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT)
