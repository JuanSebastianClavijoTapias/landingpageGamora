from django.urls import path

from .views import about, blog, blog_detail, home, privacidad, service_detail, submit_lead_ajax, track_whatsapp_click

app_name = 'landing'

urlpatterns = [
    path('', home, name='home'),
    path('sobre-nosotros/', about, name='about'),
    path('privacidad/', privacidad, name='privacidad'),
    path('blog/', blog, name='blog'),
    path('blog/<slug:slug>/', blog_detail, name='blog_detail'),
    path('api/submit-lead/', submit_lead_ajax, name='submit_lead_ajax'),
    path('soluciones/<slug:slug>/', service_detail, name='service_detail'),
    path('track/whatsapp-click/', track_whatsapp_click, name='track_whatsapp_click'),
]