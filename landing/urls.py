from django.urls import path

from .views import home, robots_txt, service_detail, sitemap_xml, track_whatsapp_click, submit_lead_ajax

app_name = 'landing'

urlpatterns = [
    path('', home, name='home'),
    path('api/submit-lead/', submit_lead_ajax, name='submit_lead_ajax'),
    path('robots.txt', robots_txt, name='robots_txt'),
    path('sitemap.xml', sitemap_xml, name='sitemap_xml'),
    path('soluciones/<slug:slug>/', service_detail, name='service_detail'),
    path('track/whatsapp-click/', track_whatsapp_click, name='track_whatsapp_click'),
]