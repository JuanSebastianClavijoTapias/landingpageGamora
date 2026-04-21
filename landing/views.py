import json
import os
from urllib.parse import quote

from django.http import Http404, HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.templatetags.static import static
from django.urls import reverse
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST, require_http_methods

from .content import (
	ABOUT_STORY,
	BLOG_POSTS,
	CLIENT_LOGOS,
	FOUNDERS,
	NAV_ITEMS,
	ROI_EXAMPLE,
	ROI_SIGNALS,
	ROI_STEPS,
	SERVICE_STACKS,
	SOCIAL_LINKS,
)
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
	'tagline': 'Tecnologia de primer nivel para tu empresa.',
	'statement': 'Hacemos que tu empresa venda mejor, ahorre tiempo y trabaje con mas orden.',
	'subtagline': 'Sistemas de cobro, paginas web y automatizacion para crecer',
	'description': 'Empresa de tecnologia ubicada en Medellin, Colombia, que disena, desarrolla e implementa soluciones digitales inteligentes para empresas que quieren crecer y competir con las mas grandes.',
	'location': 'Medellin, Colombia',
	'coverage': 'Colombia y todo el mundo mediante trabajo remoto.',
}

BASE_SEO = {
	'title': 'Gamora Systems | Sistema de cobro, gestion empresarial, automatizacion y software con inteligencia artificial en Medellin',
	'description': 'Gamora Systems desarrolla sistemas de cobro (POS), gestion empresarial (ERP), automatizaciones, software a la medida, paginas web, apps e Internet de las Cosas con inteligencia artificial desde Medellin para empresas en Colombia y el mundo.',
}

AUDIENCE_SEGMENTS = [
	{
		'title': 'Empresas pequenas y medianas en Colombia',
		'description': 'Negocios que quieren entrar al mundo digital sin pagar lo que cobran las grandes empresas.',
	},
	{
		'title': 'Emprendimientos en crecimiento',
		'description': 'Negocios que necesitan herramientas digitales solidas desde el inicio.',
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
		'title': 'Sistemas de cobro (POS)',
		'description': 'Puntos de venta agiles, intuitivos y conectados en tiempo real.',
		'detail_title': 'Vende con un sistema de cobro agil, intuitivo y conectado en tiempo real.',
		'detail_intro': 'Gamora integra esta solucion dentro de un conjunto de herramientas digitales pensado para empresas que quieren crecer y competir con las mas grandes.',
		'benefits': [
			'Puntos de venta agiles, intuitivos y conectados en tiempo real.',
			'La promesa de velocidad de la marca incluye un sistema de cobro listo en 5 dias habiles.',
			'Tecnologia de primera calidad a precio de empresa mediana, con soporte continuo y mantenimiento real.',
		],
		'desktop_title': 'Centro de cobro',
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
		'mobile_title': 'Cobro movil',
		'mobile_cards': ['Cobro rapido', 'Tiempo real', 'Soporte continuo'],
	},
	{
		'slug': 'erp',
		'icon_key': 'erp',
		'eyebrow': 'Operacion integral',
		'title': 'Sistemas de gestion empresarial (ERP)',
		'description': 'Controla toda tu empresa desde un solo lugar: finanzas, inventario, personal y mas.',
		'detail_title': 'Centraliza finanzas, inventario y personal en un solo sistema.',
		'detail_intro': 'Gamora lo plantea como parte de un conjunto unificado de herramientas para empresas que buscan operar con estructura de grande sin pagar precios de empresa grande.',
		'benefits': [
			'Controla toda tu empresa: finanzas, inventario, personal y mas, desde un solo lugar.',
			'Un solo proveedor tecnologico para integrar todo tu negocio digital bajo un mismo techo.',
			'Resultados medibles, soporte continuo y acompanamiento real despues de la entrega.',
		],
		'desktop_title': 'Centro ERP',
		'desktop_metrics': [
			{'label': 'Cobertura', 'value': 'Operacion integral'},
			{'label': 'Modelo', 'value': 'Todo en uno'},
			{'label': 'Soporte', 'value': 'Continuo'},
		],
		'desktop_rows': [
			{'label': 'Finanzas', 'value': 'Control de cuentas'},
			{'label': 'Inventario', 'value': 'Siempre al dia'},
			{'label': 'Personal', 'value': 'Gestion conectada'},
		],
		'mobile_title': 'Gestion movil',
		'mobile_cards': ['Finanzas', 'Inventario', 'Personal'],
	},
	{
		'slug': 'automatizaciones',
		'icon_key': 'automation',
		'eyebrow': 'Eficiencia con IA',
		'title': 'Automatizaciones',
		'description': 'Elimina tareas repetitivas y reduce costos operativos con IA.',
		'detail_title': 'Reduce costos operativos eliminando tareas repetitivas con IA.',
		'detail_intro': 'Esta solucion responde al diferencial mas fuerte de Gamora: integrar inteligencia artificial en cada sistema para acelerar operaciones y crecimiento.',
		'benefits': [
			'Elimina tareas repetitivas y reduce los costos de tu operacion con inteligencia artificial.',
			'La promesa de velocidad contempla automatizaciones entregadas en 2 dias.',
			'Se conecta con el resto de tus herramientas digitales para que todo funcione sin complicaciones.',
		],
		'desktop_title': 'Centro de automatizacion',
		'desktop_metrics': [
			{'label': 'Entrega', 'value': '2 dias'},
			{'label': 'Enfoque', 'value': 'IA embebida'},
			{'label': 'Impacto', 'value': 'Menos costos'},
		],
		'desktop_rows': [
			{'label': 'Tareas', 'value': 'Menos trabajo manual'},
			{'label': 'Flujo', 'value': 'Procesos conectados'},
			{'label': 'Operacion', 'value': 'Crece sin complicaciones'},
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
		'detail_intro': 'Gamora desarrolla software a la medida para empresas que necesitan digitalizar su operacion sin adaptarse a herramientas genericas que no encajan con su negocio.',
		'benefits': [
			'Software hecho exactamente para tu forma de trabajar y tu negocio.',
			'Inteligencia artificial integrada para aprender, predecir y automatizar dentro de tu solucion.',
			'Capacitacion, mantenimiento y acompanamiento continuo despues de la entrega.',
		],
		'desktop_title': 'Sistema a la medida',
		'desktop_metrics': [
			{'label': 'Diseño', 'value': 'Personalizado'},
			{'label': 'Modelo', 'value': 'IA integrada'},
			{'label': 'Soporte', 'value': 'Real'},
		],
		'desktop_rows': [
			{'label': 'Proceso', 'value': 'Hecho para tu negocio'},
			{'label': 'Integracion', 'value': 'Todo conectado'},
			{'label': 'Crecimiento', 'value': 'Escalable desde el inicio'},
		],
		'mobile_title': 'Control movil',
		'mobile_cards': ['Proceso propio', 'IA integrada', 'Escalable'],
	},
	{
		'slug': 'web',
		'icon_key': 'web',
		'eyebrow': 'Presencia en internet',
		'title': 'Paginas web',
		'description': 'Sitios profesionales, rapidos y optimizados para convertir visitas en clientes.',
		'detail_title': 'Convierte visitas en clientes con una web rapida y profesional.',
		'detail_intro': 'Gamora usa velocidad, claridad y conversion como ejes para que la presencia digital no sea solo bonita, sino rentable.',
		'benefits': [
			'Sitios profesionales, rapidos y optimizados para convertir visitas en clientes.',
			'La promesa de velocidad contempla una pagina web lista en 3 dias.',
			'Tu pagina web se conecta con el resto de tus herramientas digitales desde un mismo proveedor.',
		],
		'desktop_title': 'Web de conversion',
		'desktop_metrics': [
			{'label': 'Entrega', 'value': '3 dias'},
			{'label': 'Objetivo', 'value': 'Conversion'},
			{'label': 'Rendimiento', 'value': 'Rapida'},
		],
		'desktop_rows': [
			{'label': 'Portada', 'value': 'Mensaje directo a tu cliente'},
			{'label': 'Boton de accion', 'value': 'Llamado claro al visitante'},
			{'label': 'Contacto', 'value': 'Mas clientes y conversaciones'},
		],
		'mobile_title': 'Web movil',
		'mobile_cards': ['Portada', 'Boton de accion', 'Contacto'],
	},
	{
		'slug': 'apps',
		'icon_key': 'mobile',
		'eyebrow': 'Aplicacion para tu celular',
		'title': 'Aplicaciones moviles',
		'description': 'Aplicaciones para celular y tableta en iOS y Android, conectadas a tus sistemas.',
		'detail_title': 'Lleva tu negocio a iOS y Android con aplicaciones conectadas a tus sistemas.',
		'detail_intro': 'Gamora conecta las aplicaciones moviles con el resto de tus sistemas para que el negocio siga funcionando desde cualquier lugar.',
		'benefits': [
			'Aplicaciones para celular y tableta en iOS y Android.',
			'Conectadas a tus sistemas para trabajar desde cualquier lugar.',
			'Calidad de primer nivel, precio accesible y acompanamiento real en la entrega.',
		],
		'desktop_title': 'Centro de app movil',
		'desktop_metrics': [
			{'label': 'Plataformas', 'value': 'iOS + Android'},
			{'label': 'Conexion', 'value': 'Con tus sistemas'},
			{'label': 'Enfoque', 'value': 'Tu negocio'},
		],
		'desktop_rows': [
			{'label': 'Usuarios', 'value': 'Experiencia conectada'},
			{'label': 'Datos', 'value': 'Siempre actualizados'},
			{'label': 'Escala', 'value': 'Lista para crecer'},
		],
		'mobile_title': 'App movil',
		'mobile_cards': ['iOS', 'Android', 'Siempre conectada'],
	},
	{
		'slug': 'iot',
		'icon_key': 'iot',
		'eyebrow': 'Mundo fisico + digital',
		'title': 'Dispositivos conectados (IoT)',
		'description': 'Conecta tus maquinas, sensores y equipos al mundo digital para verlos y controlarlos en tiempo real.',
		'detail_title': 'Controla y automatiza conectando tus equipos y maquinas al mundo digital.',
		'detail_intro': 'Gamora integra datos, monitoreo y automatizacion para que tus equipos fisicos formen parte de tus herramientas digitales con claridad.',
		'benefits': [
			'Conecta tus maquinas y equipos al mundo digital para verlos y controlarlos.',
			'Datos claros y visibilidad en tiempo real desde un mismo lugar.',
			'Se conecta con automatizaciones, paneles de control y soluciones a la medida.',
		],
		'desktop_title': 'Centro de dispositivos',
		'desktop_metrics': [
			{'label': 'Dispositivos', 'value': 'Conectados'},
			{'label': 'Vigilancia', 'value': 'Continua'},
			{'label': 'Accion', 'value': 'Automatizacion'},
		],
		'desktop_rows': [
			{'label': 'Lecturas', 'value': 'Datos claros'},
			{'label': 'Alertas', 'value': 'Visibilidad en tiempo real'},
			{'label': 'Respuesta', 'value': 'Procesos automaticos'},
		],
		'mobile_title': 'Control movil',
		'mobile_cards': ['Vigilancia', 'Alertas', 'Automatizacion'],
	},
	{
		'slug': 'consultorias',
		'icon_key': 'consulting',
		'eyebrow': 'Acompanamiento real',
		'title': 'Asesorias tecnologicas',
		'description': 'Te ayudamos a entender que necesita tu empresa digitalmente y te acompanamos en cada paso.',
		'detail_title': 'Define un plan digital claro con diagnostico, estrategia y acompanamiento real.',
		'detail_intro': 'Gamora no entrega solo tecnologia: acompana todo el proceso para que cada decision digital tenga direccion, integracion y resultados.',
		'benefits': [
			'Te ayudamos a entender que necesita tu empresa y como digitalizarte paso a paso.',
			'Un solo proveedor tecnologico para organizar prioridades y ejecutar con todo conectado.',
			'Proyeccion de resultados y soporte continuo para convertir la inversion en ganancias reales.',
		],
		'desktop_title': 'Mapa estrategico',
		'desktop_metrics': [
			{'label': 'Diagnostico', 'value': 'Claro'},
			{'label': 'Plan', 'value': 'Bien definido'},
			{'label': 'Resultado', 'value': 'Medible'},
		],
		'desktop_rows': [
			{'label': 'Analisis', 'value': 'Prioridades de tu negocio'},
			{'label': 'Plan', 'value': 'Camino a seguir'},
			{'label': 'Acompanamiento', 'value': 'Soporte continuo'},
		],
		'mobile_title': 'Asesoria movil',
		'mobile_cards': ['Diagnostico', 'Plan de accion', 'Acompanamiento'],
	},
]

SERVICE_MAP = {service['slug']: service for service in SERVICES}
BLOG_POST_MAP = {post['slug']: post for post in BLOG_POSTS}

DIFFERENTIATORS = [
	{
		'index': '01',
		'class_name': 'bento-card--wide',
		'title': 'Precio accesible, calidad de alto nivel',
		'description': 'Accedes a tecnologia de primer nivel sin pagar lo que cobran las grandes empresas.',
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
		'title': 'Inteligencia artificial en cada solucion',
		'description': 'La inteligencia artificial acelera el desarrollo y queda integrada dentro de los sistemas para aprender, predecir y automatizar.',
	},
	{
		'index': '04',
		'class_name': '',
		'title': 'Un solo proveedor para todo lo digital',
		'description': 'Todo lo que tu empresa necesita digitalmente bajo un mismo techo, conectado entre si.',
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
		'title': 'Tu inversion se recupera rapido',
		'description': 'Cada proyecto incluye una proyeccion de cuanto y cuando recuperas lo que invertiste, para que sepas si la tecnologia se paga sola.',
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
		'impact': 'Lo digital de tu empresa se divide y cada cambio se vuelve mas lento y costoso.',
		'solution': 'Un solo proveedor para todo lo digital.',
		'outcome': 'Sistema de cobro, gestion empresarial, automatizaciones, web, apps, dispositivos conectados y asesoria, todo en un mismo lugar.',
	},
	{
		'problem': 'Pagar precios de empresa grande para digitalizarte.',
		'impact': 'Muchas empresas medianas y pequenas se quedan atras por costos que no se ajustan a su realidad.',
		'solution': 'Tecnologia de primer nivel a precio accesible.',
		'outcome': 'La eficiencia de la inteligencia artificial reduce tiempos y ese ahorro se traslada al cliente.',
	},
	{
		'problem': 'Tareas repetitivas y sistemas que no aprenden.',
		'impact': 'Trabajo manual, costos altos y decisiones lentas.',
		'solution': 'Inteligencia artificial integrada en tu negocio.',
		'outcome': 'Herramientas que automatizan, predicen y ayudan a que tu empresa crezca sin complicaciones.',
	},
]

STATS = [
	{
		'value': 8,
		'prefix': '',
		'suffix': '+',
		'label': 'tipos de soluciones',
		'description': 'Sistema de cobro, gestion empresarial, automatizacion, software a la medida, web, apps, dispositivos conectados y asesorias.',
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
		'label': 'para recuperar lo que inviertes',
		'description': 'Gamora garantiza que su tecnologia se paga sola en menos de 60 dias.',
	},
	{
		'value': 5,
		'prefix': '',
		'suffix': ' dias',
		'label': 'para entregar un sistema de cobro',
		'description': 'Gamora entrega con tiempos concretos como parte central de su promesa.',
	},
]

TESTIMONIALS = [
	{
		'name': 'Cuir Tapiceria',
		'role': 'Propietario',
		'company': 'Tapiceria cuir, La Estrella',
		'text': 'En menos de una semana ya teniamos el sistema funcionando. Antes perdiamos tiempo y ventas por no tener un registro claro. Ahora todo esta bajo control y el equipo lo usa sin ningun problema.',
		'initials': 'CT',
	},
	{
		'name': 'Comercializadora JT',
		'role': 'Gerente ',
		'company': 'Comercializadora JT, Medellin',
		'text': 'Gamora nos ayudo a digitalizar el inventario y las ventas. El equipo nos explico cada paso y el soporte ha sido excelente desde el primer dia. Vale cada peso invertido.',
		'initials': 'JT',
	},
	{
		'name': 'Andres Restrepo',
		'role': 'Director de Operaciones',
		'company': 'Logistica AR, Medellin',
		'text': 'Lo que mas me sorprendio fue la velocidad. Teniamos el sistema listo antes de lo que esperabamos y funcionando perfectamente desde el primer dia. Lo recomiendo a cualquier empresa.',
		'initials': 'AR',
	},
]

DELIVERY_PROMISES = [
	{'value': '5 dias habiles', 'label': 'para un sistema de cobro'},
	{'value': '3 dias', 'label': 'para una pagina web'},
	{'value': '2 dias', 'label': 'para una automatizacion'},
]

HERO_HIGHLIGHTS = [
	{'label': 'Modelo', 'value': 'Inteligencia artificial en cada solucion'},
	{'label': 'Cobertura', 'value': 'Medellin + remoto global'},
	{'label': 'Promesa', 'value': 'Entrega ultra rapida'},
	{'label': 'Soporte', 'value': 'Capacitacion y mantenimiento real'},
]

CTA_POINTS = [
	'Tecnologia de primer nivel, precio accesible.',
	'Entrega ultra rapida potenciada por inteligencia artificial.',
	'Tu inversion se recupera rapido y te acompanamos todo el tiempo.',
	'Un solo proveedor para todo lo digital de tu empresa.',
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
				'sameAs': [social['url'] for social in SOCIAL_LINKS],
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
		'sitemap_url': build_absolute_url(request, reverse('sitemap_xml')),
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
		'sitemap_url': build_absolute_url(request, reverse('sitemap_xml')),
		'schema_json': build_service_schema(request, service),
	}


def build_standard_seo(request, title, description, path, schema_json, og_type='website'):
	page_url = build_absolute_url(request, path)
	logo_url = build_absolute_static_url(request, 'landing/images/logo_gamora_fondo_eliminado.png')
	return {
		'title': title,
		'description': description,
		'canonical_url': page_url,
		'og_url': page_url,
		'og_image_url': logo_url,
		'og_image_alt': title,
		'og_type': og_type,
		'robots': 'index,follow,max-snippet:-1,max-image-preview:large,max-video-preview:-1',
		'sitemap_url': build_absolute_url(request, reverse('sitemap_xml')),
		'schema_json': schema_json,
	}


def build_page_schema(request, path, title, description, page_type='WebPage'):
	page_url = build_absolute_url(request, path)
	home_url = build_absolute_url(request, reverse('landing:home'))
	schema = {
		'@context': 'https://schema.org',
		'@graph': [
			{
				'@type': page_type,
				'url': page_url,
				'name': title,
				'description': description,
				'isPartOf': {
					'@type': 'WebSite',
					'url': home_url,
					'name': COMPANY['name'],
				},
			},
		],
	}
	return json.dumps(schema)


def build_blog_index_schema(request):
	blog_url = build_absolute_url(request, reverse('landing:blog'))
	schema = {
		'@context': 'https://schema.org',
		'@graph': [
			{
				'@type': 'Blog',
				'url': blog_url,
				'name': f'Blog de {COMPANY["name"]}',
				'description': 'Casos de exito y articulos tecnicos sobre software, automatizacion, IA y conversion digital.',
				'blogPost': [
					{
						'@type': 'BlogPosting',
						'headline': post['title'],
						'url': build_absolute_url(
							request,
							reverse('landing:blog_detail', kwargs={'slug': post['slug']}),
						),
						'datePublished': post['published_iso'],
						'description': post['excerpt'],
					}
					for post in BLOG_POSTS
				],
			},
		],
	}
	return json.dumps(schema)


def build_blog_post_schema(request, post):
	post_url = build_absolute_url(
		request,
		reverse('landing:blog_detail', kwargs={'slug': post['slug']}),
	)
	schema = {
		'@context': 'https://schema.org',
		'@type': 'BlogPosting',
		'headline': post['title'],
		'description': post['excerpt'],
		'url': post_url,
		'datePublished': post['published_iso'],
		'author': {
			'@type': 'Organization',
			'name': COMPANY['name'],
		},
		'publisher': {
			'@type': 'Organization',
			'name': COMPANY['name'],
		},
	}
	return json.dumps(schema)


def build_about_seo(request):
	title = f'Sobre nosotros | {COMPANY["name"]}'
	description = 'Historia, equipo fundador, metodologia ROI y stack de trabajo de Gamora Systems.'
	return build_standard_seo(
		request,
		title,
		description,
		reverse('landing:about'),
		build_page_schema(request, reverse('landing:about'), title, description, 'AboutPage'),
	)


def build_privacidad_seo(request):
	title = 'Política de Privacidad | Gamora Systems'
	description = 'Política de Tratamiento de Datos Personales de Gamora Systems conforme a la Ley 1581 de 2012 de Colombia.'
	return build_standard_seo(
		request,
		title,
		description,
		reverse('landing:privacidad'),
		build_page_schema(request, reverse('landing:privacidad'), title, description),
	)


def build_blog_seo(request):
	title = f'Blog | {COMPANY["name"]}'
	description = 'Casos de exito y articulos tecnicos sobre automatizacion, software, IA y crecimiento digital.'
	return build_standard_seo(
		request,
		title,
		description,
		reverse('landing:blog'),
		build_blog_index_schema(request),
	)


def build_blog_post_seo(request, post):
	title = f'{post["title"]} | {COMPANY["name"]}'
	return build_standard_seo(
		request,
		title,
		post['excerpt'],
		reverse('landing:blog_detail', kwargs={'slug': post['slug']}),
		build_blog_post_schema(request, post),
		og_type='article',
	)


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


def build_section_href(request, section_id):
	if request.resolver_match and request.resolver_match.url_name == 'home':
		return f'#{section_id}'
	return f"{reverse('landing:home')}#{section_id}"


def build_nav_items(request):
	current_name = request.resolver_match.url_name if request.resolver_match else ''
	items = []
	for item in NAV_ITEMS:
		if 'url_name' in item:
			href = reverse(f"landing:{item['url_name']}")
			active = current_name == item['url_name']
		else:
			href = build_section_href(request, item['section'])
			active = False
		items.append({'label': item['label'], 'href': href, 'active': active})
	return items


def build_base_context(request):
	current_name = request.resolver_match.url_name if request.resolver_match else ''
	return {
		'company': COMPANY,
		'nav_items': build_nav_items(request),
		'social_links': SOCIAL_LINKS,
		'brand_href': '#hero' if current_name == 'home' else reverse('landing:home'),
		'contact_href': build_section_href(request, 'contact'),
		'services_href': build_section_href(request, 'servicios'),
		'current_year': timezone.now().year,
		'whatsapp': build_whatsapp_context(),
	}


def serialize_service(service):
	stack = SERVICE_STACKS[service['slug']]
	return {
		**service,
		'icon': SERVICE_ICONS[service['icon_key']],
		'stack': stack['items'],
		'stack_summary': stack['summary'],
		'url': reverse('landing:service_detail', kwargs={'slug': service['slug']}),
	}


def get_services():
	return [serialize_service(service) for service in SERVICES]


def get_service_or_404(slug):
	service = SERVICE_MAP.get(slug)
	if service is None:
		raise Http404('Service not found.')
	return serialize_service(service)


def serialize_blog_post(post):
	return {
		**post,
		'url': reverse('landing:blog_detail', kwargs={'slug': post['slug']}),
	}


def get_blog_posts():
	return [serialize_blog_post(post) for post in BLOG_POSTS]


def get_blog_post_or_404(slug):
	post = BLOG_POST_MAP.get(slug)
	if post is None:
		raise Http404('Post not found.')
	return serialize_blog_post(post)


def is_async_form_request(request):
	return request.headers.get('x-requested-with') == 'XMLHttpRequest'


def serialize_form_errors(form):
	serialized_errors = {}
	for field_name, error_items in form.errors.get_json_data().items():
		serialized_errors[field_name] = [item['message'] for item in error_items]
	return serialized_errors


def home(request):
	submitted = request.GET.get('submitted') == '1'

	if request.method == 'POST':
		form = LeadForm(request.POST)
		if form.is_valid():
			form.save()
			if is_async_form_request(request):
				return JsonResponse(
					{
						'ok': True,
						'message': 'Tu informacion ya quedo registrada. El siguiente paso es revisar tu necesidad y preparar el contacto desde Gamora Systems.',
					}
				)
			return redirect(f"{reverse('landing:home')}?submitted=1#contact")
		if is_async_form_request(request):
			return JsonResponse(
				{
					'ok': False,
					'errors': serialize_form_errors(form),
				},
				status=400,
			)
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
		'testimonials': TESTIMONIALS,
	}
	return render(request, 'landing/index.html', context)


@require_http_methods(["POST"])
def submit_lead_ajax(request):
	"""
	Endpoint AJAX para enviar el formulario de contacto sin recargar la página.
	Devuelve JSON con el estado del envío.
	"""
	form = LeadForm(request.POST)
	
	if form.is_valid():
		form.save()
		return JsonResponse({
			'success': True,
			'message': 'Diagnóstico Enviado'
		})
	else:
		# Devolver errores del formulario
		errors = {}
		for field, error_list in form.errors.items():
			errors[field] = [str(error) for error in error_list]
		
		return JsonResponse({
			'success': False,
			'message': 'Por favor revisa los datos ingresados',
			'errors': errors
		}, status=400)


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


def about(request):
	context = {
		**build_base_context(request),
		'seo': build_about_seo(request),
		'founders': FOUNDERS,
		'about_story': ABOUT_STORY,
		'roi_signals': ROI_SIGNALS,
		'roi_steps': ROI_STEPS,
		'roi_example': ROI_EXAMPLE,
		'client_logos': CLIENT_LOGOS,
		'services': get_services(),
		'testimonials': TESTIMONIALS,
	}
	return render(request, 'landing/about.html', context)


def privacidad(request):
	context = {
		**build_base_context(request),
		'seo': build_privacidad_seo(request),
	}
	return render(request, 'landing/privacidad.html', context)


def blog(request):
	context = {
		**build_base_context(request),
		'seo': build_blog_seo(request),
		'blog_posts': get_blog_posts(),
	}
	return render(request, 'landing/blog.html', context)


def blog_detail(request, slug):
	post = get_blog_post_or_404(slug)
	related_posts = [item for item in get_blog_posts() if item['slug'] != slug][:3]
	context = {
		**build_base_context(request),
		'seo': build_blog_post_seo(request, post),
		'post': post,
		'related_posts': related_posts,
	}
	return render(request, 'landing/blog_detail.html', context)


def robots_txt(request):
	body = 'User-agent: *\nAllow: /\nDisallow: /admin/\nSitemap: https://gamorasystems.dev/sitemap.xml\n'
	return HttpResponse(body, content_type='text/plain; charset=utf-8')


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
