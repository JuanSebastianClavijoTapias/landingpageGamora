from django.test import TestCase
from django.urls import reverse

from .models import InteractionEvent, Lead


class LandingPageTests(TestCase):
	def test_home_page_renders(self):
		response = self.client.get(reverse('landing:home'))

		self.assertEqual(response.status_code, 200)
		self.assertContains(response, 'Gamora Systems')
		self.assertContains(response, 'A quien ayudamos')
		self.assertContains(response, 'Ingresa a cada uno para ver sus beneficios')
		self.assertContains(response, reverse('landing:service_detail', args=['pos']))
		self.assertContains(response, 'application/ld+json')
		self.assertContains(response, 'id="whatsapp-fab"')
		self.assertTemplateUsed(response, 'landing/index.html')

	def test_service_detail_page_renders(self):
		response = self.client.get(reverse('landing:service_detail', args=['pos']))

		self.assertEqual(response.status_code, 200)
		self.assertContains(response, 'Sistemas POS')
		self.assertContains(response, 'Asi podria verse en computador y celular')
		self.assertContains(response, 'application/ld+json')
		self.assertTemplateUsed(response, 'landing/service_detail.html')

	def test_robots_txt_exposes_sitemap(self):
		response = self.client.get(reverse('landing:robots_txt'))

		self.assertEqual(response.status_code, 200)
		self.assertContains(response, 'User-agent: *')
		self.assertContains(response, '/sitemap.xml')

	def test_sitemap_xml_lists_core_pages(self):
		response = self.client.get(reverse('landing:sitemap_xml'))

		self.assertEqual(response.status_code, 200)
		self.assertContains(response, '<urlset', html=False)
		self.assertContains(response, '/soluciones/pos/', html=False)

	def test_valid_lead_submission_creates_record(self):
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

		self.assertEqual(response.status_code, 302)
		self.assertEqual(response.url, '/?submitted=1#contact')
		self.assertEqual(Lead.objects.count(), 1)

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
