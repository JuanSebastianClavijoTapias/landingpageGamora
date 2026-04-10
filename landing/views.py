import json
import os
from urllib.parse import quote
from xml.sax.saxutils import escape

from django.http import Http404, HttpResponse
from django.shortcuts import redirect, render
from django.templatetags.static import static
from django.urls import reverse
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from .forms import LeadForm
from .models import InteractionEvent

SERVICE_ICONS = {
	'pos': """
		<svg viewBox='0 0 64 64' aria-hidden='true'>
			<rect x='10' y='14' width='44' height='30' rx='8'></rect>
			<path d='M18 24h28'></path>
			<path d='M18 32h16'></path>
			<rect x='20' y='48' width='24' height='6' rx='3'></rect>
		</svg>
	""",
	'erp': """
		<svg viewBox='0 0 64 64' aria-hidden='true'>
			<rect x='10' y='10' width='18' height='18' rx='5'></rect>
			<rect x='36' y='10' width='18' height='18' rx='5'></rect>
			<rect x='10' y='36' width='18' height='18' rx='5'></rect>
			<rect x='36' y='36' width='18' height='18' rx='5'></rect>
			<path d='M28 19h8'></path>
			<path d='M19 28v8'></path>
			<path d='M45 28v8'></path>
			<path d='M28 45h8'></path>
		</svg>
	""",
	'automation': """
		<svg viewBox='0 0 64 64' aria-hidden='true'>
			<circle cx='32' cy='32' r='8'></circle>
			<path d='M32 12v8'></path>
			<path d='M32 44v8'></path>
			<path d='M12 32h8'></path>
			<path d='M44 32h8'></path>
			<path d='M18 18l6 6'></path>
			<path d='M40 40l6 6'></path>
			<path d='M46 18l-6 6'></path>
			<path d='M24 40l-6 6'></path>
		</svg>
	""",
	'custom': """
		<svg viewBox='0 0 64 64' aria-hidden='true'>
			<path d='M24 18L12 32l12 14'></path>
			<path d='M40 18l12 14-12 14'></path>
			<path d='M34 16l-4 32'></path>
		</svg>
	""",
	'web': """
		<svg viewBox='0 0 64 64' aria-hidden='true'>
			<rect x='8' y='12' width='48' height='40' rx='8'></rect>
			<path d='M8 22h48'></path>
			<circle cx='16' cy='17' r='2'></circle>
			<circle cx='23' cy='17' r='2'></circle>
			<path d='M20 34h10'></path>
			<path d='M34 34h10'></path>
			<path d='M20 42h24'></path>
		</svg>
	""",
	'mobile': """
		<svg viewBox='0 0 64 64' aria-hidden='true'>
			<rect x='20' y='8' width='24' height='48' rx='7'></rect>
			<path d='M28 16h8'></path>
			<circle cx='32' cy='48' r='2'></circle>
		</svg>
	""",
	'iot': """
		<svg viewBox='0 0 64 64' aria-hidden='true'>
			<circle cx='18' cy='18' r='6'></circle>
			<circle cx='46' cy='18' r='6'></circle>
			<circle cx='18' cy='46' r='6'></circle>
			<circle cx='46' cy='46' r='6'></circle>
			<path d='M24 18h16'></path>
			<path d='M18 24v16'></path>
			<path d='M46 24v16'></path>
			<path d='M24 46h16'></path>
		</svg>
	""",
	'consulting': """
		<svg viewBox='0 0 64 64' aria-hidden='true'>
			<circle cx='32' cy='32' r='20'></circle>
			<path d='M32 22v10l8 8'></path>
			<path d='M32 12v4'></path>
			<path d='M32 48v4'></path>
			<path d='M12 32h4'></path>
			<path d='M48 32h4'></path>
		</svg>
	""",
}

COMPANY = {
	'name': 'Gamora Systems',
	'tagline': 'Tecnologia de grande, precio de PYME.',
	'statement': 'Empowering enterprises through robust SaaS, clear data, and intelligent workflows.',
	'subtagline': 'Soluciones SaaS Personalizadas • Dashboards • Automatizacion',
	'description': 'Empresa de tecnologia ubicada en Medellin, Colombia, que disena, desarrolla e implementa soluciones digitales inteligentes para empresas que quieren crecer y competir como grandes.',
	'location': 'Medellin, Colombia',
	'coverage': 'Colombia y todo el mundo mediante trabajo remoto.',
}

BASE_SEO = {
	'title': 'Gamora Systems | POS, ERP, automatizacion y software con IA en Medellin',
	'description': 'Gamora Systems desarrolla POS, ERP, automatizaciones, software a la medida, paginas web, apps e IoT con IA desde Medellin para PYMES en Colombia y el mundo.',
}

AUDIENCE_SEGMENTS = [
	{
		'title': 'PYMES colombianas',
		'description': 'Empresas que quieren digitalizarse sin pagar precios corporativos.',
	},
	{
		'title': 'Emprendimientos en crecimiento',
		'description': 'Negocios que necesitan sistemas escalables desde el inicio.',
	},
	{
		'title': 'Sectores diversos',
		'description': 'Comercio, salud, logistica, educacion, manufactura y mas.',
	},
	{
		'title': 'Latinoamerica e internacional',
		'description': 'Empresas que buscan desarrollo de calidad a precio competitivo.',
	},
]

SERVICES = [
	{
		'slug': 'pos',
		'icon_key': 'pos',
		'eyebrow': 'Ventas en tiempo real',
		'title': 'Sistemas POS',
		'description': 'Puntos de venta agiles, intuitivos y conectados en tiempo real.',
		'detail_title': 'Vende con un POS agil, intuitivo y conectado en tiempo real.',
		'detail_intro': 'Gamora integra esta solucion dentro de un ecosistema digital pensado para empresas que quieren crecer y competir como grandes.',
		'benefits': [
			'Puntos de venta agiles, intuitivos y conectados en tiempo real.',
			'La promesa de velocidad de la marca incluye un POS en 5 dias habiles.',
			'Tecnologia empresarial a precio PYME, con soporte continuo y mantenimiento real.',
		],
		'desktop_title': 'Centro POS',
		'desktop_metrics': [
			{'label': 'Entrega', 'value': '5 dias habiles'},
			{'label': 'Operacion', 'value': 'Tiempo real'},
			{'label': 'Modelo', 'value': 'IA integrada'},
		],
		'desktop_rows': [
			{'label': 'Ventas', 'value': 'Movimiento al instante'},
			{'label': 'Operacion', 'value': 'Cobro agil e intuitivo'},
			{'label': 'Soporte', 'value': 'Acompanamiento continuo'},
		],
		'mobile_title': 'POS movil',
		'mobile_cards': ['Cobro rapido', 'Tiempo real', 'Soporte continuo'],
	},
	{
		'slug': 'erp',
		'icon_key': 'erp',
		'eyebrow': 'Operacion integral',
		'title': 'Sistemas ERP',
		'description': 'Gestion integral de tu empresa: finanzas, inventario, talento y mas.',
		'detail_title': 'Centraliza finanzas, inventario y talento en un solo sistema.',
		'detail_intro': 'Gamora lo plantea como parte de un ecosistema unificado para empresas que buscan operar con estructura de grande sin pagar precios corporativos.',
		'benefits': [
			'Gestion integral para finanzas, inventario, talento y mas.',
			'Un solo aliado tecnologico para integrar tu ecosistema digital bajo un mismo techo.',
			'ROI medible, soporte continuo y acompanamiento real despues de la entrega.',
		],
		'desktop_title': 'Centro ERP',
		'desktop_metrics': [
			{'label': 'Cobertura', 'value': 'Operacion integral'},
			{'label': 'Modelo', 'value': 'Todo en uno'},
			{'label': 'Soporte', 'value': 'Continuo'},
		],
		'desktop_rows': [
			{'label': 'Finanzas', 'value': 'Control centralizado'},
			{'label': 'Inventario', 'value': 'Visibilidad operativa'},
			{'label': 'Talento', 'value': 'Gestion conectada'},
		],
		'mobile_title': 'ERP movil',
		'mobile_cards': ['Finanzas', 'Inventario', 'Talento'],
	},
	{
		'slug': 'automatizaciones',
		'icon_key': 'automation',
		'eyebrow': 'Eficiencia con IA',
		'title': 'Automatizaciones',
		'description': 'Elimina tareas repetitivas y reduce costos operativos con IA.',
		'detail_title': 'Reduce costos operativos eliminando tareas repetitivas con IA.',
		'detail_intro': 'Esta solucion responde al diferencial mas fuerte de Gamora: integrar IA en cada sistema para acelerar operaciones y crecimiento.',
		'benefits': [
			'Elimina tareas repetitivas y reduce costos operativos con IA.',
			'La promesa de velocidad contempla automatizaciones entregadas en 2 dias.',
			'Se conecta con el resto de tu ecosistema digital para operar sin friccion.',
		],
		'desktop_title': 'Centro de automatizacion',
		'desktop_metrics': [
			{'label': 'Entrega', 'value': '2 dias'},
			{'label': 'Enfoque', 'value': 'IA embebida'},
			{'label': 'Impacto', 'value': 'Menor costo'},
		],
		'desktop_rows': [
			{'label': 'Tareas', 'value': 'Menos trabajo manual'},
			{'label': 'Flujo', 'value': 'Procesos conectados'},
			{'label': 'Operacion', 'value': 'Escala con menos friccion'},
		],
		'mobile_title': 'Flujo movil',
		'mobile_cards': ['IA activa', 'Menos tareas', 'Mas velocidad'],
	},
	{
		'slug': 'a-medida',
		'icon_key': 'custom',
		'eyebrow': 'Desarrollo a medida',
		'title': 'Sistemas a la medida',
		'description': 'Software personalizado disenado exactamente para tu proceso de negocio.',
		'detail_title': 'Construye un sistema disenado exactamente para tu proceso de negocio.',
		'detail_intro': 'Gamora desarrolla software a la medida para empresas que necesitan digitalizar su operacion sin adaptarse a herramientas genericas.',
		'benefits': [
			'Software personalizado disenado exactamente para tu proceso de negocio.',
			'IA integrada dentro de la solucion para aprender, predecir y automatizar.',
			'Capacitacion, mantenimiento y acompanamiento continuo despues de la entrega.',
		],
		'desktop_title': 'Sistema a la medida',
		'desktop_metrics': [
			{'label': 'Diseño', 'value': 'Personalizado'},
			{'label': 'Modelo', 'value': 'IA integrada'},
			{'label': 'Soporte', 'value': 'Real'},
		],
		'desktop_rows': [
			{'label': 'Proceso', 'value': 'Hecho para tu operacion'},
			{'label': 'Integracion', 'value': 'Ecosistema conectado'},
			{'label': 'Crecimiento', 'value': 'Escalable desde el inicio'},
		],
		'mobile_title': 'Control movil',
		'mobile_cards': ['Proceso propio', 'IA integrada', 'Escalable'],
	},
	{
		'slug': 'web',
		'icon_key': 'web',
		'eyebrow': 'Conversion digital',
		'title': 'Paginas web',
		'description': 'Sitios profesionales, rapidos y optimizados para convertir visitas en clientes.',
		'detail_title': 'Convierte visitas en clientes con una web rapida y profesional.',
		'detail_intro': 'Gamora usa velocidad, claridad y conversion como ejes para que la presencia digital no sea solo bonita, sino rentable.',
		'benefits': [
			'Sitios profesionales, rapidos y optimizados para convertir visitas en clientes.',
			'La promesa de velocidad contempla una pagina web en 3 dias.',
			'Tu web se integra con el resto de tu ecosistema digital desde un mismo proveedor.',
		],
		'desktop_title': 'Web de conversion',
		'desktop_metrics': [
			{'label': 'Entrega', 'value': '3 dias'},
			{'label': 'Objetivo', 'value': 'Conversion'},
			{'label': 'Rendimiento', 'value': 'Rapida'},
		],
		'desktop_rows': [
			{'label': 'Hero', 'value': 'Mensaje directo al dolor'},
			{'label': 'CTA', 'value': 'Llamado a accion claro'},
			{'label': 'Contacto', 'value': 'Mas leads y conversaciones'},
		],
		'mobile_title': 'Web movil',
		'mobile_cards': ['Hero', 'CTA', 'Contacto'],
	},
	{
		'slug': 'apps',
		'icon_key': 'mobile',
		'eyebrow': 'Ecosistema movil',
		'title': 'Aplicaciones moviles',
		'description': 'Apps nativas e hibridas para iOS y Android conectadas a tu ecosistema.',
		'detail_title': 'Lleva tu operacion a iOS y Android con apps conectadas a tu ecosistema.',
		'detail_intro': 'Gamora conecta las aplicaciones moviles con el resto de tus sistemas para que la operacion siga fluyendo desde cualquier punto.',
		'benefits': [
			'Apps nativas e hibridas para iOS y Android.',
			'Conectadas a tu ecosistema digital para operar desde cualquier lugar.',
			'Calidad corporativa, precio PYME y acompanamiento real en el despliegue.',
		],
		'desktop_title': 'Centro de app movil',
		'desktop_metrics': [
			{'label': 'Plataformas', 'value': 'iOS + Android'},
			{'label': 'Conexion', 'value': 'Ecosistema'},
			{'label': 'Enfoque', 'value': 'Operacion'},
		],
		'desktop_rows': [
			{'label': 'Usuarios', 'value': 'Experiencia conectada'},
			{'label': 'Datos', 'value': 'Sincronizacion constante'},
			{'label': 'Escala', 'value': 'Lista para crecer'},
		],
		'mobile_title': 'App movil',
		'mobile_cards': ['iOS', 'Android', 'Sincronizada'],
	},
	{
		'slug': 'iot',
		'icon_key': 'iot',
		'eyebrow': 'Mundo fisico + digital',
		'title': 'Sistemas IoT',
		'description': 'Conecta tus dispositivos fisicos al mundo digital para monitorear y automatizar.',
		'detail_title': 'Monitorea y automatiza conectando tus dispositivos fisicos al mundo digital.',
		'detail_intro': 'Gamora integra datos, monitoreo y automatizacion para que la operacion fisica entre al ecosistema digital con claridad.',
		'benefits': [
			'Conecta dispositivos fisicos al mundo digital para monitorear y automatizar.',
			'Aporta datos claros y visibilidad operativa desde un mismo ecosistema.',
			'Se integra con automatizaciones, dashboards y soluciones a la medida.',
		],
		'desktop_title': 'Centro IoT',
		'desktop_metrics': [
			{'label': 'Dispositivos', 'value': 'Conectados'},
			{'label': 'Monitoreo', 'value': 'Continuo'},
			{'label': 'Accion', 'value': 'Automatizacion'},
		],
		'desktop_rows': [
			{'label': 'Lecturas', 'value': 'Datos claros'},
			{'label': 'Alertas', 'value': 'Visibilidad operativa'},
			{'label': 'Respuesta', 'value': 'Procesos automaticos'},
		],
		'mobile_title': 'IoT movil',
		'mobile_cards': ['Monitoreo', 'Alertas', 'Automatizacion'],
	},
	{
		'slug': 'consultorias',
		'icon_key': 'consulting',
		'eyebrow': 'Acompanamiento real',
		'title': 'Consultorias tecnologicas',
		'description': 'Diagnostico, estrategia y acompanamiento para transformar tu empresa digitalmente.',
		'detail_title': 'Traza una ruta digital con diagnostico, estrategia y acompanamiento real.',
		'detail_intro': 'Gamora no entrega solo tecnologia: acompana la transformacion para que cada decision digital tenga direccion, integracion y retorno.',
		'benefits': [
			'Diagnostico, estrategia y acompanamiento para transformar tu empresa digitalmente.',
			'Un aliado tecnologico todo en uno para ordenar prioridades y ejecutar con integracion.',
			'Proyeccion de ROI y soporte continuo para convertir la inversion en resultado.',
		],
		'desktop_title': 'Mapa estrategico',
		'desktop_metrics': [
			{'label': 'Diagnostico', 'value': 'Claro'},
			{'label': 'Ruta', 'value': 'Estrategica'},
			{'label': 'ROI', 'value': 'Medible'},
		],
		'desktop_rows': [
			{'label': 'Analisis', 'value': 'Prioridades de negocio'},
			{'label': 'Plan', 'value': 'Ruta de implementacion'},
			{'label': 'Acompanamiento', 'value': 'Soporte continuo'},
		],
		'mobile_title': 'Ruta movil',
		'mobile_cards': ['Diagnostico', 'Estrategia', 'Acompanamiento'],
	},
]

SERVICE_MAP = {service['slug']: service for service in SERVICES}

DIFFERENTIATORS = [
	{
		'index': '01',
		'class_name': 'bento-card--wide',
		'title': 'Precio PYME, calidad corporativa',
		'description': 'Accedes a tecnologia de nivel empresarial sin pagar precios de empresa grande.',
	},
	{
		'index': '02',
		'class_name': '',
		'title': 'Entrega ultra rapida',
		'description': 'Mientras la competencia tarda semanas o meses, Gamora entrega en dias.',
	},
	{
		'index': '03',
		'class_name': 'bento-card--tall',
		'title': 'IA integrada en cada solucion',
		'description': 'La IA acelera el desarrollo y queda embebida dentro de los sistemas para aprender, predecir y automatizar.',
	},
	{
		'index': '04',
		'class_name': '',
		'title': 'Aliado tecnologico todo en uno',
		'description': 'Todo tu ecosistema digital bajo un mismo techo, con integracion total entre sistemas.',
	},
	{
		'index': '05',
		'class_name': '',
		'title': 'Soporte, capacitacion y mantenimiento real',
		'description': 'Acompanamiento continuo para que tu operacion este siempre al dia y funcionando al 100%.',
	},
	{
		'index': '06',
		'class_name': 'bento-card--wide',
		'title': 'ROI medible',
		'description': 'Cada proyecto incluye una proyeccion de retorno sobre inversion para que sepas cuando y como la tecnologia se paga sola.',
	},
]

STORY_STEPS = [
	{
		'problem': 'Semanas o meses esperando una entrega.',
		'impact': 'La mayoria de agencias y desarrolladores entregan tarde, frenando ventas y crecimiento.',
		'solution': 'Promesa oficial de entrega en dias.',
		'outcome': 'Gamora convierte la velocidad en una promesa de marca con desarrollo potenciado por IA.',
	},
	{
		'problem': 'Coordinar 4 o 5 proveedores distintos.',
		'impact': 'Tu ecosistema digital se fragmenta y cada cambio se vuelve mas lento y costoso.',
		'solution': 'Un solo aliado para todo tu stack.',
		'outcome': 'POS, ERP, automatizaciones, web, apps, IoT y consultoria integrados bajo un mismo techo.',
	},
	{
		'problem': 'Pagar precios corporativos para digitalizarte.',
		'impact': 'Muchas PYMES se quedan atras por presupuestos que no reflejan su realidad.',
		'solution': 'Tecnologia empresarial a precio PYME.',
		'outcome': 'La eficiencia operativa de la IA reduce tiempos y traslada ese ahorro al cliente.',
	},
	{
		'problem': 'Tareas repetitivas y sistemas que no aprenden.',
		'impact': 'Procesos manuales, costos operativos altos y decisiones lentas.',
		'solution': 'IA integrada en la operacion.',
		'outcome': 'Herramientas que automatizan, predicen y ayudan a que el negocio crezca con menos friccion.',
	},
]

STATS = [
	{
		'value': 8,
		'prefix': '',
		'suffix': '+',
		'label': 'frentes de solucion',
		'description': 'POS, ERP, automatizacion, desarrollo a la medida, web, apps, IoT y consultoria.',
	},
	{
		'value': 3,
		'prefix': '',
		'suffix': '',
		'label': 'empresas satisfechas en Medellin',
		'description': 'Proyectos reales en marcha que estan transformando operaciones.',
	},
	{
		'value': 60,
		'prefix': '<',
		'suffix': ' dias',
		'label': 'para recuperar la inversion',
		'description': 'La propuesta comercial afirma que Gamora se paga sola en menos de 60 dias.',
	},
	{
		'value': 5,
		'prefix': '',
		'suffix': ' dias',
		'label': 'para entregar un POS',
		'description': 'La velocidad se comunica con tiempos concretos como parte central de la marca.',
	},
]

DELIVERY_PROMISES = [
	{'value': '5 dias habiles', 'label': 'para un POS'},
	{'value': '3 dias', 'label': 'para una pagina web'},
	{'value': '2 dias', 'label': 'para una automatizacion'},
]

HERO_HIGHLIGHTS = [
	{'label': 'Modelo', 'value': 'IA embebida en cada solucion'},
	{'label': 'Cobertura', 'value': 'Medellin + remoto global'},
	{'label': 'Promesa', 'value': 'Entrega ultra rapida'},
	{'label': 'Soporte', 'value': 'Capacitacion y mantenimiento real'},
]

CTA_POINTS = [
	'Tecnologia de grande, precio de PYME.',
	'Entrega ultra rapida potenciada por IA.',
	'ROI medible y acompanamiento continuo.',
	'Un solo aliado para todo tu ecosistema digital.',
]

NAV_ITEMS = [
	{'id': 'value', 'label': 'Soluciones'},
	{'id': 'audience', 'label': 'A quien ayudamos'},
	{'id': 'story', 'label': 'Problema -> solucion'},
	{'id': 'proof', 'label': 'Resultados'},
	{'id': 'contact', 'label': 'Contacto'},
]

WHATSAPP_MESSAGE = 'Hola, quiero conocer una propuesta de Gamora Systems para mi empresa.'
WHATSAPP_BUSINESS_URL = 'https://www.whatsapp.com/business/'
SITE_URL = os.getenv('GAMORA_SITE_URL', '').rstrip('/')


def build_absolute_url(request, path):
	if path.startswith('http://') or path.startswith('https://'):
		return path
	if SITE_URL:
		return f'{SITE_URL}{path}'
	return request.build_absolute_uri(path)


def build_absolute_static_url(request, asset_path):
	return build_absolute_url(request, static(asset_path))


def build_home_schema(request):
	home_url = build_absolute_url(request, reverse('landing:home'))
	logo_url = build_absolute_static_url(request, 'landing/images/logo_gamora_fondo_eliminado.png')
	service_offers = []
	for service in SERVICES:
		service_offers.append(
			{
				'@type': 'Offer',
				'itemOffered': {
					'@type': 'Service',
					'name': service['title'],
					'description': service['description'],
					'url': build_absolute_url(
						request,
						reverse('landing:service_detail', kwargs={'slug': service['slug']}),
					),
				},
			}
		)

	schema = {
		'@context': 'https://schema.org',
		'@graph': [
			{
				'@type': 'ProfessionalService',
				'@id': f'{home_url}#organization',
				'name': COMPANY['name'],
				'url': home_url,
				'logo': logo_url,
				'description': BASE_SEO['description'],
				'address': {
					'@type': 'PostalAddress',
					'addressLocality': 'Medellin',
					'addressCountry': 'CO',
				},
				'areaServed': ['Colombia', 'Worldwide'],
			},
			{
				'@type': 'WebSite',
				'@id': f'{home_url}#website',
				'url': home_url,
				'name': COMPANY['name'],
				'description': BASE_SEO['description'],
				'inLanguage': 'es-CO',
			},
			{
				'@type': 'OfferCatalog',
				'name': 'Soluciones digitales inteligentes con IA',
				'itemListElement': service_offers,
			},
		],
	}
	return json.dumps(schema)


def build_service_schema(request, service):
	home_url = build_absolute_url(request, reverse('landing:home'))
	service_url = build_absolute_url(
		request,
		reverse('landing:service_detail', kwargs={'slug': service['slug']}),
	)
	schema = {
		'@context': 'https://schema.org',
		'@graph': [
			{
				'@type': 'BreadcrumbList',
				'itemListElement': [
					{
						'@type': 'ListItem',
						'position': 1,
						'name': COMPANY['name'],
						'item': home_url,
					},
					{
						'@type': 'ListItem',
						'position': 2,
						'name': service['title'],
						'item': service_url,
					},
				],
			},
			{
				'@type': 'Service',
				'name': service['title'],
				'url': service_url,
				'description': service['description'],
				'provider': {
					'@type': 'ProfessionalService',
					'name': COMPANY['name'],
					'areaServed': ['Colombia', 'Worldwide'],
				},
				'areaServed': ['Colombia', 'Worldwide'],
			},
		],
	}
	return json.dumps(schema)


def build_home_seo(request):
	home_url = build_absolute_url(request, reverse('landing:home'))
	logo_url = build_absolute_static_url(request, 'landing/images/logo_gamora_fondo_eliminado.png')
	return {
		'title': BASE_SEO['title'],
		'description': BASE_SEO['description'],
		'canonical_url': home_url,
		'og_url': home_url,
		'og_image_url': logo_url,
		'og_image_alt': f"Logo de {COMPANY['name']}",
		'og_type': 'website',
		'robots': 'index,follow,max-snippet:-1,max-image-preview:large,max-video-preview:-1',
		'sitemap_url': build_absolute_url(request, reverse('landing:sitemap_xml')),
		'schema_json': build_home_schema(request),
	}


def build_service_seo(request, service):
	service_url = build_absolute_url(
		request,
		reverse('landing:service_detail', kwargs={'slug': service['slug']}),
	)
	logo_url = build_absolute_static_url(request, 'landing/images/logo_gamora_fondo_eliminado.png')
	return {
		'title': f"{service['title']} con IA en Medellin | {COMPANY['name']}",
		'description': f"{service['description']} Beneficios, mockup desktop y movil de {service['title']} para empresas en Medellin, Colombia y mercados remotos.",
		'canonical_url': service_url,
		'og_url': service_url,
		'og_image_url': logo_url,
		'og_image_alt': f"{service['title']} - {COMPANY['name']}",
		'og_type': 'website',
		'robots': 'index,follow,max-snippet:-1,max-image-preview:large,max-video-preview:-1',
		'sitemap_url': build_absolute_url(request, reverse('landing:sitemap_xml')),
		'schema_json': build_service_schema(request, service),
	}


def build_whatsapp_link():
	whatsapp_number = os.getenv('GAMORA_WHATSAPP_NUMBER', '').strip()
	if not whatsapp_number:
		return ''

	return f"https://wa.me/{whatsapp_number}?text={quote(WHATSAPP_MESSAGE)}"


def build_whatsapp_context():
	whatsapp_link = build_whatsapp_link()
	return {
		'link': whatsapp_link,
		'enabled': bool(whatsapp_link),
		'business_url': WHATSAPP_BUSINESS_URL,
		'message': WHATSAPP_MESSAGE,
	}


def build_base_context(request):
	return {
		'company': COMPANY,
		'nav_items': NAV_ITEMS,
		'current_year': timezone.now().year,
		'whatsapp': build_whatsapp_context(),
	}


def serialize_service(service):
	return {
		**service,
		'icon': SERVICE_ICONS[service['icon_key']],
		'url': reverse('landing:service_detail', kwargs={'slug': service['slug']}),
	}


def get_services():
	return [serialize_service(service) for service in SERVICES]


def get_service_or_404(slug):
	service = SERVICE_MAP.get(slug)
	if service is None:
		raise Http404('Service not found.')
	return serialize_service(service)


def home(request):
	submitted = request.GET.get('submitted') == '1'

	if request.method == 'POST':
		form = LeadForm(request.POST)
		if form.is_valid():
			form.save()
			return redirect(f"{reverse('landing:home')}?submitted=1#contact")
	else:
		form = LeadForm()

	context = {
		**build_base_context(request),
		'seo': build_home_seo(request),
		'form': form,
		'submitted': submitted,
		'services': get_services(),
		'audience_segments': AUDIENCE_SEGMENTS,
		'differentiators': DIFFERENTIATORS,
		'story_steps': STORY_STEPS,
		'stats': STATS,
		'delivery_promises': DELIVERY_PROMISES,
		'hero_highlights': HERO_HIGHLIGHTS,
		'cta_points': CTA_POINTS,
	}
	return render(request, 'landing/index.html', context)


def service_detail(request, slug):
	service = get_service_or_404(slug)
	other_services = [item for item in get_services() if item['slug'] != slug]

	context = {
		**build_base_context(request),
		'service': service,
		'other_services': other_services,
		'seo': build_service_seo(request, service),
	}
	return render(request, 'landing/service_detail.html', context)


def robots_txt(request):
	sitemap_url = build_absolute_url(request, reverse('landing:sitemap_xml'))
	body = f"User-agent: *\nAllow: /\n\nSitemap: {sitemap_url}\n"
	return HttpResponse(body, content_type='text/plain; charset=utf-8')


def sitemap_xml(request):
	today = timezone.now().date().isoformat()
	entries = [
		(
			build_absolute_url(request, reverse('landing:home')),
			'weekly',
			'1.0',
		),
	]
	for service in SERVICES:
		entries.append(
			(
				build_absolute_url(
					request,
					reverse('landing:service_detail', kwargs={'slug': service['slug']}),
				),
				'weekly',
				'0.8',
			)
		)

	url_nodes = []
	for location, changefreq, priority in entries:
		url_nodes.append(
			'<url>'
			f'<loc>{escape(location)}</loc>'
			f'<lastmod>{today}</lastmod>'
			f'<changefreq>{changefreq}</changefreq>'
			f'<priority>{priority}</priority>'
			'</url>'
		)

	xml = (
		'<?xml version="1.0" encoding="UTF-8"?>'
		'<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
		f"{''.join(url_nodes)}"
		'</urlset>'
	)
	return HttpResponse(xml, content_type='application/xml; charset=utf-8')


@csrf_exempt
@require_POST
def track_whatsapp_click(request):
	target = request.POST.get('target', '')[:500]
	fallback = request.POST.get('fallback') == '1'
	InteractionEvent.objects.create(
		channel='whatsapp',
		event_type='click',
		label='floating_button',
		target=target,
		metadata={
			'fallback': fallback,
			'path': request.POST.get('path', ''),
			'referer': request.headers.get('Referer', ''),
		},
	)
	return HttpResponse(status=204)
