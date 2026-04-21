NAV_ITEMS = [
	{'key': 'services', 'label': 'Servicios', 'section': 'servicios'},
	{'key': 'about', 'label': 'Sobre nosotros', 'url_name': 'about'},
	{'key': 'blog', 'label': 'Blog', 'url_name': 'blog'},
	{'key': 'testimonials', 'label': 'Testimonios', 'section': 'testimonios'},
	{'key': 'contact', 'label': 'Contactanos', 'section': 'contact'},
]

SOCIAL_LINKS = [
	{
		'label': 'LinkedIn',
		'url': 'https://www.linkedin.com/company/tu-empresa',
		'icon': """
			<svg viewBox='0 0 24 24' aria-hidden='true'>
				<path d='M6.94 8.5H3.56V20h3.38V8.5Z'></path>
				<path d='M5.25 3A2.05 2.05 0 1 0 5.25 7.1 2.05 2.05 0 0 0 5.25 3Z'></path>
				<path d='M20.44 12.77c0-3.47-1.85-5.08-4.32-5.08-1.99 0-2.88 1.09-3.38 1.86V8.5H9.37c.04.7 0 11.5 0 11.5h3.38v-6.42c0-.34.02-.68.13-.92.27-.68.87-1.38 1.88-1.38 1.33 0 1.87 1.01 1.87 2.49V20H20V13.4c0-.22.01-.42.01-.63Z'></path>
			</svg>
		""",
	},
	{
		'label': 'Instagram',
		'url': 'https://www.instagram.com/tu-cuenta',
		'icon': """
			<svg viewBox='0 0 24 24' aria-hidden='true'>
				<rect x='3.25' y='3.25' width='17.5' height='17.5' rx='5.25'></rect>
				<circle cx='12' cy='12' r='4.1'></circle>
				<circle cx='17.4' cy='6.6' r='1.15'></circle>
			</svg>
		""",
	},
	{
		'label': 'YouTube',
		'url': 'https://www.youtube.com/@tu-canal',
		'icon': """
			<svg viewBox='0 0 24 24' aria-hidden='true'>
				<path d='M20.45 7.1a2.82 2.82 0 0 0-1.98-1.99C16.72 4.62 12 4.62 12 4.62s-4.72 0-6.47.49A2.82 2.82 0 0 0 3.55 7.1 29.4 29.4 0 0 0 3.06 12a29.4 29.4 0 0 0 .49 4.9 2.82 2.82 0 0 0 1.98 1.99c1.75.49 6.47.49 6.47.49s4.72 0 6.47-.49a2.82 2.82 0 0 0 1.98-1.99 29.4 29.4 0 0 0 .49-4.9 29.4 29.4 0 0 0-.49-4.9Z'></path>
				<path d='m10.1 15.5 5.1-3.5-5.1-3.5v7Z'></path>
			</svg>
		""",
	},
]

FOUNDERS = [
	{
		'name': 'Founder de estrategia',
		'role': 'Growth, ventas y posicionamiento',
		'bio': 'Perfil orientado a discovery comercial, posicionamiento de oferta y lectura de ROI para PYMES que necesitan resultados rapidos.',
		'highlights': [
			'Experiencia en ventas consultivas B2B y crecimiento comercial.',
			'Define el alcance, la prioridad y el mensaje de cada lanzamiento.',
			'Conecta necesidades de negocio con hojas de ruta ejecutables.',
		],
		'linkedin': 'https://www.linkedin.com/in/tu-perfil-estrategia',
		'initials': 'GE',
	},
	{
		'name': 'Founder de automatizacion e IA',
		'role': 'Procesos, integraciones y eficiencia operativa',
		'bio': 'Enfocado en identificar cuellos de botella, convertir tareas repetitivas en flujos medibles y usar IA solo donde realmente mejora margen y tiempo.',
		'highlights': [
			'Experiencia automatizando operaciones con n8n, APIs y Python.',
			'Prioriza quick wins que generen ahorro visible en las primeras semanas.',
			'Disena tableros y alertas para medir adopcion y retorno.',
		],
		'linkedin': 'https://www.linkedin.com/in/tu-perfil-automatizacion',
		'initials': 'AI',
	},
	{
		'name': 'Founder de producto e ingenieria',
		'role': 'Arquitectura, experiencia digital y entregas',
		'bio': 'Responsable de convertir decisiones de negocio en producto usable, arquitectura estable y experiencias claras en web, software y apps.',
		'highlights': [
			'Experiencia construyendo productos con Python, React y arquitectura modular.',
			'Convierte alcance comercial en entregables listos para operar.',
			'Cuida performance, claridad visual y escalabilidad del ecosistema.',
		],
		'linkedin': 'https://www.linkedin.com/in/tu-perfil-ingenieria',
		'initials': 'PE',
	},
]

ABOUT_STORY = [
	{
		'eyebrow': 'Origen',
		'title': 'Gamora nace para resolver una brecha clara en el mercado PYME.',
		'description': 'Muchas empresas pequenas y medianas necesitaban software serio, pero solo encontraban proyectos lentos, caros y poco conectados con su realidad operativa.',
	},
	{
		'eyebrow': 'Modelo',
		'title': 'La promesa es simple: tecnologia de nivel alto, entrega en dias.',
		'description': 'Estandarizamos discovery, desarrollo y lanzamiento con procesos asistidos por IA para bajar tiempos sin sacrificar personalizacion ni control tecnico.',
	},
	{
		'eyebrow': 'Operacion',
		'title': 'Unimos software, automatizacion y acompanamiento bajo un mismo techo.',
		'description': 'POS, ERP, automatizaciones, software a la medida, web, apps e IoT se conectan para que el cliente no tenga que coordinar cinco proveedores distintos.',
	},
	{
		'eyebrow': 'Hoy',
		'title': 'Operamos desde Medellin para Colombia y clientes remotos.',
		'description': 'El enfoque sigue siendo el mismo: quick wins visibles, una ruta clara de crecimiento y soporte continuo despues de salir a produccion.',
	},
]

ROI_SIGNALS = [
	{
		'value': '12-20 h',
		'label': 'semanales liberadas',
		'description': 'Automatizaciones y flujos asistidos por IA suelen eliminar tareas repetitivas de seguimiento, carga manual y consolidacion de datos.',
	},
	{
		'value': '8-15%',
		'label': 'mejora en conversion',
		'description': 'Landing pages, respuesta mas rapida y seguimiento automatizado recuperan oportunidades que antes se perdian por demora o desorden.',
	},
	{
		'value': '3-7%',
		'label': 'recuperacion de margen',
		'description': 'Control de inventario, mejor visibilidad y menos errores operativos reducen fugas silenciosas de rentabilidad.',
	},
	{
		'value': '< 60 dias',
		'label': 'payback objetivo',
		'description': 'Cuando se suman ahorro operativo, ventas recuperadas y menor fuga por errores, los quick wins bien elegidos pueden pagar el proyecto en menos de dos meses.',
	},
]

ROI_STEPS = [
	{
		'title': '1. Medimos la linea base del negocio.',
		'text': 'Antes de construir, levantamos horas manuales, tiempos de respuesta, ventas perdidas, errores recurrentes y costo por demora.',
	},
	{
		'title': '2. Elegimos un quick win con retorno visible.',
		'text': 'Priorizamos el frente que pueda mover mas rapido ventas, tiempo del equipo o control operativo: POS, automatizacion, seguimiento comercial o landing.',
	},
	{
		'title': '3. Lanzamos en dias y dejamos medicion activa.',
		'text': 'Cada entrega sale con eventos, reportes o tableros para ver adopcion, ahorro y nuevas oportunidades desde la primera semana.',
	},
	{
		'title': '4. Recalculamos en la ventana de 30 a 60 dias.',
		'text': 'Comparamos la linea base contra el nuevo flujo y actualizamos el payback real con datos de uso, ventas y horas recuperadas.',
	},
]

ROI_EXAMPLE = {
	'formula': 'ROI = ((ahorro mensual + ventas recuperadas - costo operativo) / inversion inicial) x 100',
	'description': 'Ejemplo: una empresa que recupera 50 horas al mes a $25.000 COP por hora y suma 10 ventas extra de $120.000 COP genera $2.450.000 COP mensuales de valor. Un proyecto de $4.500.000 COP alcanza payback cercano a 55 dias.',
}

CLIENT_LOGOS = [
	{'name': 'Cuir Tapiceria', 'sector': 'Retail y manufactura', 'mark': 'CT'},
	{'name': 'Comercializadora JT', 'sector': 'Distribucion y ventas', 'mark': 'JT'},
	{'name': 'Logistica AR', 'sector': 'Operacion y despachos', 'mark': 'AR'},
]

SERVICE_STACKS = {
	'pos': {
		'summary': 'Caja, inventario y cierres en tiempo real con backend transaccional y una interfaz de cobro clara para el equipo.',
		'items': ['Python', 'Django', 'PostgreSQL', 'React', 'Docker'],
	},
	'erp': {
		'summary': 'Operacion centralizada con modulos conectados, permisos, reporting y control de datos sobre una sola base.',
		'items': ['Python', 'Django', 'PostgreSQL', 'React', 'Metabase'],
	},
	'automatizaciones': {
		'summary': 'Orquestacion de procesos, integraciones y agentes asistidos por IA para mover informacion sin trabajo manual.',
		'items': ['n8n', 'Python', 'OpenAI API', 'PostgreSQL', 'Webhooks'],
	},
	'a-medida': {
		'summary': 'Arquitectura modular para procesos unicos, con APIs y frontends que se adaptan a tu operacion.',
		'items': ['Python', 'FastAPI', 'React', 'PostgreSQL', 'Docker'],
	},
	'web': {
		'summary': 'Experiencias rapidas, enfocadas en conversion y conectadas al stack comercial del cliente.',
		'items': ['React', 'Next.js', 'Python APIs', 'Tailwind CSS', 'Vercel'],
	},
	'apps': {
		'summary': 'Aplicaciones moviles enlazadas al core del negocio para mantener operacion y datos sincronizados.',
		'items': ['React Native', 'Expo', 'Python APIs', 'Firebase', 'PostgreSQL'],
	},
	'iot': {
		'summary': 'Dispositivos conectados con lectura en tiempo real, alertas y tableros para tomar accion mas rapido.',
		'items': ['Python', 'MQTT', 'ESP32', 'React', 'PostgreSQL'],
	},
	'consultorias': {
		'summary': 'Diagnostico, roadmap y medicion para decidir que automatizar, que construir y como medir retorno.',
		'items': ['Python', 'n8n', 'Metabase', 'Notion', 'Looker Studio'],
	},
}

BLOG_POSTS = [
	{
		'slug': 'caso-cuir-tapiceria-pos-5-dias',
		'category': 'Caso de exito',
		'title': 'Como Cuir Tapiceria activo su POS en 5 dias y dejo de vender a ciegas',
		'excerpt': 'El negocio paso de cierres manuales y ventas sin trazabilidad a una operacion con caja, inventario y visibilidad en tiempo real.',
		'published_label': '18 abril 2026',
		'published_iso': '2026-04-18',
		'reading_time': '5 min',
		'metric_value': '5 dias',
		'metric_label': 'para salir a produccion',
		'tags': ['POS', 'Python', 'React', 'PostgreSQL'],
		'results': [
			{'label': 'Implementacion', 'value': '5 dias'},
			{'label': 'Control de ventas', 'value': 'Tiempo real'},
			{'label': 'Capacitacion', 'value': '1 jornada'},
		],
		'sections': [
			{
				'title': 'El problema',
				'paragraphs': [
					'Cuir Tapiceria llevaba registros dispersos y dependia de memoria, apuntes y cierres lentos para entender como habia vendido durante el dia.',
					'Eso hacia dificil detectar faltantes, conciliar caja y saber que productos realmente estaban moviendo margen.',
				],
				'bullets': [
					'No habia visibilidad inmediata de ventas por turno.',
					'El control de inventario dependia de procesos manuales.',
					'Cada cierre consumia tiempo operativo del equipo.',
				],
			},
			{
				'title': 'La solucion',
				'paragraphs': [
					'Se implemento un POS con arquitectura Python + Django en backend y una interfaz React para caja, pensado para operar rapido desde el primer turno.',
					'La puesta en marcha se cerro en cinco dias habiles con soporte directo para adopcion del equipo.',
				],
			},
			{
				'title': 'Lo que hizo diferencia',
				'paragraphs': [
					'No se trato solo de software, sino de quitar friccion operativa: caja mas clara, datos al instante y acompanamiento para que el cambio no se quedara en presentacion.',
				],
			},
		],
	},
	{
		'slug': 'caso-comercializadora-jt-control-inventario-y-ventas',
		'category': 'Caso de exito',
		'title': 'Comercializadora JT: mas control de inventario y ventas sin frenar la operacion',
		'excerpt': 'La prioridad era digitalizar inventario y ventas con una solucion que el equipo pudiera adoptar sin detener el negocio.',
		'published_label': '16 abril 2026',
		'published_iso': '2026-04-16',
		'reading_time': '6 min',
		'metric_value': '1 flujo',
		'metric_label': 'de ventas e inventario conectado',
		'tags': ['Inventario', 'ERP', 'Python', 'Soporte'],
		'results': [
			{'label': 'Inventario', 'value': 'Mas visible'},
			{'label': 'Ventas', 'value': 'Mejor trazabilidad'},
			{'label': 'Soporte', 'value': 'Continuo'},
		],
		'sections': [
			{
				'title': 'Punto de partida',
				'paragraphs': [
					'El equipo necesitaba una forma mas clara de seguir movimiento de inventario y ventas sin introducir una plataforma pesada o lenta de adoptar.',
				],
			},
			{
				'title': 'Ejecucion',
				'paragraphs': [
					'Se priorizo una experiencia simple y soporte cercano para que la digitalizacion no dependiera de largos periodos de capacitacion.',
					'La combinacion de backend en Python y una interfaz clara permitio ordenar operaciones sin romper el flujo diario.',
				],
				'bullets': [
					'Datos centralizados para ventas e inventario.',
					'Ruta de soporte activa desde el primer dia.',
					'Mejores decisiones con informacion menos dispersa.',
				],
			},
			{
				'title': 'Aprendizaje clave',
				'paragraphs': [
					'En PYMES, la adopcion vale tanto como la funcionalidad. Por eso el proyecto se penso para operar rapido, con menos ruido tecnico y mas claridad en el uso.',
				],
			},
		],
	},
	{
		'slug': 'automatizaciones-con-n8n-y-python-para-roi-en-60-dias',
		'category': 'Articulo tecnico',
		'title': 'Automatizaciones con n8n y Python: la ruta mas corta para buscar ROI antes de 60 dias',
		'excerpt': 'Cuando el cuello de botella es operativo, automatizar seguimiento, consolidacion y alertas suele generar el retorno mas rapido.',
		'published_label': '12 abril 2026',
		'published_iso': '2026-04-12',
		'reading_time': '7 min',
		'metric_value': '< 60 dias',
		'metric_label': 'payback objetivo para quick wins',
		'tags': ['n8n', 'Python', 'ROI', 'Automatizacion'],
		'results': [
			{'label': 'Stack', 'value': 'n8n + Python'},
			{'label': 'Enfoque', 'value': 'Quick wins'},
			{'label': 'Senal', 'value': 'Ahorro visible'},
		],
		'sections': [
			{
				'title': 'Por que este stack funciona rapido',
				'paragraphs': [
					'n8n permite orquestar eventos, integraciones y webhooks con mucha velocidad, mientras Python resuelve logica de negocio, validaciones y procesamiento mas fino.',
					'Esa combinacion reduce tiempo de implementacion y deja espacio para personalizacion real cuando el flujo lo necesita.',
				],
			},
			{
				'title': 'Donde suele aparecer el ROI',
				'paragraphs': [
					'Los retornos mas rapidos aparecen cuando se automatiza seguimiento comercial, tareas administrativas repetitivas, consolidacion de reportes o alertas de operacion.',
				],
				'bullets': [
					'Menos horas manuales cada semana.',
					'Respuesta mas rapida a leads o incidencias.',
					'Menos fuga por tareas que dependian de memoria.',
				],
			},
			{
				'title': 'La clave no es automatizar todo',
				'paragraphs': [
					'Se empieza por el frente con mas friccion y retorno mas medible. El error comun es querer resolver todo a la vez y terminar demorando el valor.',
				],
			},
		],
	},
	{
		'slug': 'react-y-python-para-webs-que-convierten-mas-rapido',
		'category': 'Articulo tecnico',
		'title': 'React y Python para webs que convierten mas rapido sin perder control tecnico',
		'excerpt': 'Una landing no deberia ser solo una vitrina bonita. Debe capturar demanda, responder rapido y conectarse al resto del negocio.',
		'published_label': '09 abril 2026',
		'published_iso': '2026-04-09',
		'reading_time': '6 min',
		'metric_value': '3 dias',
		'metric_label': 'para lanzar una web comercial',
		'tags': ['React', 'Python', 'Landing pages', 'Conversion'],
		'results': [
			{'label': 'Front', 'value': 'React'},
			{'label': 'Back', 'value': 'Python APIs'},
			{'label': 'Objetivo', 'value': 'Conversion'},
		],
		'sections': [
			{
				'title': 'La combinacion',
				'paragraphs': [
					'React acelera experiencia y claridad visual. Python permite conectar formularios, eventos, CRM, automatizaciones y medicion sin depender de parches manuales.',
				],
			},
			{
				'title': 'Que convierte de verdad',
				'paragraphs': [
					'No basta con un buen diseno. La conversion mejora cuando el mensaje es claro, la accion es evidente y la respuesta a cada lead no queda en bandeja de entrada olvidada.',
				],
				'bullets': [
					'Mensaje directo al dolor del cliente.',
					'CTA visible y sin friccion.',
					'Integracion inmediata con automatizaciones o seguimiento.',
				],
			},
			{
				'title': 'Control despues del lanzamiento',
				'paragraphs': [
					'Cuando el sitio sale conectado al flujo comercial, deja de ser brochure y empieza a operar como una pieza del sistema de ventas.',
				],
			},
		],
	},
]