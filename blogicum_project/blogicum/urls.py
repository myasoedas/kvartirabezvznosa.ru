# blogicum/blogicum/urls.py
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.urls import include, path
from django.views.generic import RedirectView

from blog.views import UserRegisterView
from blog.sitemaps import StaticViewSitemap

sitemaps = {
    'static': StaticViewSitemap,
}

handler404 = 'pages.views.custom_404_view'
handler500 = 'pages.views.custom_500_view'
handler403 = 'pages.views.custom_403_view'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('django.contrib.auth.urls')),
    path('auth/registration/',
         UserRegisterView.as_view(),
         name='registration'),
    path('ckeditor/', include('django_ckeditor_5.urls')),
    path('favicon.ico', RedirectView.as_view(url='/static/img/fav/favicon.ico', permanent=True)),
    path('pages/', include('pages.urls')),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='sitemap'),
    path('', include('blog.urls')),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT)
