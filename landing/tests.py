from django.test import TestCase, override_settings
from django.urls import reverse

from .models import InteractionEvent, Lead


class LandingPageTests(TestCase):
	def test_home_page_renders(self):
		response = self.client.get(reverse('landing:home'))

		self.assertEqual(response.status_code, 200)
		self.assertContains(response, 'Gamora Systems')
		self.assertContains(response, 'Todo lo que tu empresa necesita digitalmente, en un solo lugar')
		self.assertContains(response, 'Ingresa a cada uno para ver sus beneficios')
		self.assertContains(response, reverse('landing:service_detail', args=['pos']))
		self.assertContains(response, 'application/ld+json')
		self.assertContains(response, 'id="whatsapp-fab"')
		self.assertContains(response, 'https://www.linkedin.com/company/tu-empresa')
		self.assertContains(response, 'https://www.instagram.com/tu-cuenta')
		self.assertContains(response, 'https://www.youtube.com/@tu-canal')
		self.assertContains(response, reverse('landing:about'))
		self.assertContains(response, reverse('landing:blog'))
		self.assertContains(response, reverse('landing:privacidad'))
		self.assertContains(response, 'name="accept_privacy"')
		self.assertContains(response, 'Política de Tratamiento de Datos')
		self.assertContains(response, '4tNYG-fk-V3mVpkNOfRtDIbkI5Kg_rt3eBi5b5G6CPo')
		self.assertContains(response, '"@type": "Organization"')
		self.assertTemplateUsed(response, 'landing/index.html')

	def test_service_detail_page_renders(self):
		response = self.client.get(reverse('landing:service_detail', args=['pos']))

		self.assertEqual(response.status_code, 200)
		self.assertContains(response, 'Sistemas de cobro (POS)')
		self.assertContains(response, 'Asi podria verse en computador y celular')
		self.assertContains(response, 'Stack tecnologico')
		self.assertContains(response, 'application/ld+json')
		self.assertContains(response, 'aria-label="LinkedIn"')
		self.assertTemplateUsed(response, 'landing/service_detail.html')

	def test_about_page_renders(self):
		response = self.client.get(reverse('landing:about'))

		self.assertEqual(response.status_code, 200)
		self.assertContains(response, 'Sobre nosotros')
		self.assertContains(response, 'Equipo fundador')
		self.assertContains(response, 'Metodologia ROI')
		self.assertContains(response, 'Como explicamos el retorno en menos de 60 dias con datos')
		self.assertTemplateUsed(response, 'landing/about.html')

	def test_privacidad_page_renders(self):
		response = self.client.get(reverse('landing:privacidad'))

		self.assertEqual(response.status_code, 200)
		self.assertContains(response, 'POLÍTICA DE TRATAMIENTO DE DATOS PERSONALES — Gamora Systems — 2026')
		self.assertContains(response, 'Juan Sebastián Clavijo Tapias')
		self.assertContains(response, 'Ley 1581 de 2012')
		self.assertContains(response, 'Política de Privacidad | Gamora Systems')
		self.assertContains(response, reverse('landing:home'))
		self.assertTemplateUsed(response, 'landing/privacidad.html')

	def test_blog_pages_render(self):
		blog_response = self.client.get(reverse('landing:blog'))
		post_response = self.client.get(reverse('landing:blog_detail', args=['caso-cuir-tapiceria-pos-5-dias']))

		self.assertEqual(blog_response.status_code, 200)
		self.assertContains(blog_response, 'Casos de exito y articulos tecnicos')
		self.assertContains(blog_response, 'Como Cuir Tapiceria activo su POS en 5 dias y dejo de vender a ciegas')
		self.assertTemplateUsed(blog_response, 'landing/blog.html')

		self.assertEqual(post_response.status_code, 200)
		self.assertContains(post_response, 'Volver al blog')
		self.assertContains(post_response, '5 dias')
		self.assertContains(post_response, 'POS')
		self.assertTemplateUsed(post_response, 'landing/blog_detail.html')

	def test_robots_txt_exposes_sitemap(self):
		response = self.client.get(reverse('robots_txt'))

		self.assertEqual(response.status_code, 200)
		self.assertEqual(
			response.content.decode('utf-8'),
			'User-agent: *\nAllow: /\nDisallow: /admin/\nSitemap: https://gamorasystems.dev/sitemap.xml\n',
		)

	@override_settings(ALLOWED_HOSTS=['testserver'])
	def test_sitemap_xml_lists_search_console_pages(self):
		response = self.client.get(reverse('sitemap_xml'))

		self.assertEqual(response.status_code, 200)
		self.assertContains(response, '<urlset', html=False)
		self.assertContains(response, '/privacidad/', html=False)
		self.assertContains(response, 'changefreq>yearly<', html=False)
		self.assertContains(response, 'priority>1.0<', html=False)
		self.assertContains(response, '/soluciones/pos/', html=False)
		self.assertContains(response, '/soluciones/erp/', html=False)
		self.assertContains(response, '/soluciones/automatizaciones/', html=False)
		self.assertContains(response, '/soluciones/a-medida/', html=False)
		self.assertContains(response, '/soluciones/web/', html=False)
		self.assertContains(response, '/soluciones/apps/', html=False)
		self.assertContains(response, '/soluciones/iot/', html=False)
		self.assertContains(response, '/soluciones/consultorias/', html=False)
		self.assertNotContains(response, '/sobre-nosotros/', html=False)
		self.assertNotContains(response, '/blog/', html=False)

	def test_valid_lead_submission_creates_record(self):
		response = self.client.post(
			reverse('landing:home'),
			{
				'name': 'Ana Gomez',
				'company': 'Comercial Andina',
				'email': 'ana@example.com',
				'phone': '3001234567',
				'need': 'Necesitamos automatizar inventario y ventas.',
				'accept_privacy': 'on',
			},
		)

		self.assertEqual(response.status_code, 302)
		self.assertEqual(response.url, '/?submitted=1#contact')
		self.assertEqual(Lead.objects.count(), 1)

	def test_async_lead_submission_returns_json(self):
		response = self.client.post(
			reverse('landing:home'),
			{
				'name': 'Ana Gomez',
				'company': 'Comercial Andina',
				'email': 'ana@example.com',
				'phone': '3001234567',
				'need': 'Necesitamos automatizar inventario y ventas.',
				'accept_privacy': 'on',
			},
			HTTP_X_REQUESTED_WITH='XMLHttpRequest',
			HTTP_ACCEPT='application/json',
		)

		self.assertEqual(response.status_code, 200)
		self.assertEqual(Lead.objects.count(), 1)
		self.assertTrue(response.json()['ok'])
		self.assertIn('Tu informacion ya quedo registrada', response.json()['message'])

	def test_lead_submission_requires_privacy_consent(self):
		response = self.client.post(
			reverse('landing:home'),
			{
				'name': 'Ana Gomez',
				'company': 'Comercial Andina',
				'email': 'ana@example.com',
				'phone': '3001234567',
				'need': 'Necesitamos automatizar inventario y ventas.',
			},
		)

		self.assertEqual(response.status_code, 200)
		self.assertEqual(Lead.objects.count(), 0)
		self.assertContains(response, 'Debes aceptar la Política de Tratamiento de Datos.')

	def test_async_lead_submission_returns_errors_without_reload(self):
		response = self.client.post(
			reverse('landing:home'),
			{
				'name': 'Ana Gomez',
				'company': 'Comercial Andina',
				'email': 'ana@example.com',
				'phone': '3001234567',
				'need': 'Necesitamos automatizar inventario y ventas.',
			},
			HTTP_X_REQUESTED_WITH='XMLHttpRequest',
			HTTP_ACCEPT='application/json',
		)

		self.assertEqual(response.status_code, 400)
		self.assertEqual(Lead.objects.count(), 0)
		self.assertFalse(response.json()['ok'])
		self.assertIn('accept_privacy', response.json()['errors'])

	def test_whatsapp_click_tracking_creates_event(self):
		response = self.client.post(
			reverse('landing:track_whatsapp_click'),
			{
				'target': 'https://www.whatsapp.com/business/',
				'fallback': '1',
				'path': '/',
			},
		)

		self.assertEqual(response.status_code, 204)
		self.assertEqual(InteractionEvent.objects.count(), 1)
		event = InteractionEvent.objects.get()
		self.assertEqual(event.channel, 'whatsapp')
		self.assertEqual(event.event_type, 'click')
		self.assertTrue(event.metadata['fallback'])
