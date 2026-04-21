from django.contrib.sitemaps import Sitemap
from django.urls import reverse


SERVICE_SLUGS = [
	'pos',
	'erp',
	'automatizaciones',
	'a-medida',
	'web',
	'apps',
	'iot',
	'consultorias',
]


class StaticViewSitemap(Sitemap):
	protocol = 'https'

	def items(self):
		return ['home', 'privacidad']

	def location(self, item):
		return reverse(f'landing:{item}')

	def priority(self, item):
		return {'home': 1.0, 'privacidad': 0.3}[item]

	def changefreq(self, item):
		return {'home': 'weekly', 'privacidad': 'yearly'}[item]


class ServiceViewSitemap(Sitemap):
	protocol = 'https'
	priority = 0.8
	changefreq = 'monthly'

	def items(self):
		return SERVICE_SLUGS

	def location(self, item):
		return reverse('landing:service_detail', kwargs={'slug': item})


sitemaps = {
	'static': StaticViewSitemap,
	'services': ServiceViewSitemap,
}