from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.urls import include, path

from landing.sitemaps import sitemaps
from landing.views import robots_txt

urlpatterns = [
    path('admin/', admin.site.urls),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='sitemap_xml'),
    path('robots.txt', robots_txt, name='robots_txt'),
    path('', include('landing.urls')),
]
