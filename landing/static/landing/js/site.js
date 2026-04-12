document.documentElement.classList.add('js-ready');

const lowEndDevice = Boolean(window.__lowEndDevice);
const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches || lowEndDevice;
const loader = document.getElementById('page-loader');

const loadGSAP = () => {
    if (reduceMotion) {
        return Promise.resolve(null);
    }

    if (window.gsap) {
        return Promise.resolve(window.gsap);
    }

    return new Promise((resolve) => {
        const script = document.createElement('script');
        script.src = 'https://cdn.jsdelivr.net/npm/gsap@3.12.5/dist/gsap.min.js';
        script.async = true;
        script.onload = () => resolve(window.gsap || null);
        script.onerror = () => resolve(null);
        document.head.appendChild(script);
    });
};

const revealHeroFallback = () => {
    document.querySelectorAll('.hero-animate, .hero-stage .hero-panel').forEach((item) => {
        item.style.opacity = '1';
        item.style.transform = 'none';
    });
};

const runHeroIntro = () => {
    if (reduceMotion || !window.gsap) {
        revealHeroFallback();
        return;
    }

    const timeline = window.gsap.timeline({ defaults: { ease: 'power3.out' } });

    timeline
        .from('.topbar', { y: -24, opacity: 0, duration: 0.7 })
        .fromTo(
            '.hero-animate',
            { y: 28, opacity: 0 },
            { y: 0, opacity: 1, duration: 0.8, stagger: 0.12 },
            '-=0.3',
        )
        .fromTo(
            '.hero-stage .hero-panel',
            { y: 34, opacity: 0, scale: 0.96 },
            { y: 0, opacity: 1, scale: 1, duration: 0.8, stagger: 0.1 },
            '-=0.5',
        );
};

window.addEventListener('load', () => {
    const finishIntro = () => {
        loader?.classList.add('is-hidden');
        runHeroIntro();
    };

    loadGSAP().finally(() => {
        window.setTimeout(finishIntro, lowEndDevice ? 0 : 180);
    });
});

document.querySelectorAll('a[href^="#"]').forEach((anchor) => {
    anchor.addEventListener('click', (event) => {
        const targetId = anchor.getAttribute('href');
        if (!targetId || targetId === '#') {
            return;
        }

        const target = document.querySelector(targetId);
        if (!target) {
            return;
        }

        event.preventDefault();
        target.scrollIntoView({ behavior: reduceMotion ? 'auto' : 'smooth', block: 'start' });
    });
});

const revealItems = document.querySelectorAll('.reveal');

if (lowEndDevice || typeof window.IntersectionObserver !== 'function') {
    revealItems.forEach((item) => {
        item.classList.add('is-visible');
    });
} else {
    const revealObserver = new IntersectionObserver(
        (entries, observer) => {
            entries.forEach((entry) => {
                if (!entry.isIntersecting) {
                    return;
                }

                entry.target.classList.add('is-visible');
                observer.unobserve(entry.target);
            });
        },
        { threshold: 0.18, rootMargin: '0px 0px -8% 0px' },
    );

    revealItems.forEach((item, index) => {
        item.style.setProperty('--delay', `${(index % 6) * 80}ms`);
        revealObserver.observe(item);
    });
}

const numberFormat = new Intl.NumberFormat('es-CO');
const animateCounter = (element) => {
    if (element.dataset.animated === 'true') {
        return;
    }

    element.dataset.animated = 'true';

    const target = Number(element.dataset.target || 0);
    const prefix = element.dataset.prefix || '';
    const suffix = element.dataset.suffix || '';
    const duration = reduceMotion ? 0 : 1500;
    const startTime = performance.now();

    const tick = (now) => {
        const progress = duration === 0 ? 1 : Math.min((now - startTime) / duration, 1);
        const eased = 1 - Math.pow(1 - progress, 3);
        const current = Math.round(target * eased);
        element.textContent = `${prefix}${numberFormat.format(current)}${suffix}`;

        if (progress < 1) {
            window.requestAnimationFrame(tick);
        }
    };

    window.requestAnimationFrame(tick);
};

const counters = document.querySelectorAll('.counter');

if (lowEndDevice || typeof window.IntersectionObserver !== 'function') {
    counters.forEach((counter) => {
        const target = Number(counter.dataset.target || 0);
        const prefix = counter.dataset.prefix || '';
        const suffix = counter.dataset.suffix || '';
        counter.textContent = `${prefix}${numberFormat.format(target)}${suffix}`;
    });
} else {
    const counterObserver = new IntersectionObserver(
        (entries, observer) => {
            entries.forEach((entry) => {
                if (!entry.isIntersecting) {
                    return;
                }

                animateCounter(entry.target);
                observer.unobserve(entry.target);
            });
        },
        { threshold: 0.45 },
    );

    counters.forEach((counter) => {
        counterObserver.observe(counter);
    });
}

const whatsappFab = document.getElementById('whatsapp-fab');
if (whatsappFab) {
    whatsappFab.addEventListener('click', () => {
        const payload = new URLSearchParams({
            target: whatsappFab.dataset.whatsappTarget || '',
            fallback: whatsappFab.dataset.whatsappEnabled === '1' ? '0' : '1',
            path: window.location.pathname,
        });

        const trackUrl = whatsappFab.dataset.trackUrl;
        if (trackUrl) {
            window.fetch(trackUrl, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                },
                body: payload.toString(),
                keepalive: true,
            }).catch(() => {});
        }

        const clickCount = Number(window.localStorage.getItem('whatsapp_clicks') || '0') + 1;
        window.localStorage.setItem('whatsapp_clicks', String(clickCount));

        if (typeof window.gtag === 'function') {
            window.gtag('event', 'whatsapp_click', {
                event_category: 'engagement',
                event_label: 'floating_button',
                value: clickCount,
            });
        }

        if (Array.isArray(window.dataLayer)) {
            window.dataLayer.push({
                event: 'whatsapp_click',
                source: 'floating_button',
                click_count: clickCount,
                whatsapp_enabled: whatsappFab.dataset.whatsappEnabled === '1',
            });
        }
    });
}

const scene = document.querySelector('[data-parallax-scene]');
if (scene && !reduceMotion) {
    const layers = scene.querySelectorAll('[data-depth]');

    scene.addEventListener('pointermove', (event) => {
        const bounds = scene.getBoundingClientRect();
        const offsetX = event.clientX - bounds.left - bounds.width / 2;
        const offsetY = event.clientY - bounds.top - bounds.height / 2;

        layers.forEach((layer) => {
            const depth = Number(layer.dataset.depth || 0);
            const moveX = (offsetX / bounds.width) * depth;
            const moveY = (offsetY / bounds.height) * depth;
            layer.style.transform = `translate3d(${moveX}px, ${moveY}px, 0)`;
        });
    });

    scene.addEventListener('pointerleave', () => {
        layers.forEach((layer) => {
            layer.style.transform = 'translate3d(0, 0, 0)';
        });
    });
}

const cursorOuter = document.querySelector('.cursor--outer');
const cursorInner = document.querySelector('.cursor--inner');

if (cursorOuter && cursorInner && window.matchMedia('(pointer: fine)').matches) {
    document.addEventListener('pointermove', (event) => {
        const x = `${event.clientX}px`;
        const y = `${event.clientY}px`;
        cursorOuter.style.left = x;
        cursorOuter.style.top = y;
        cursorInner.style.left = x;
        cursorInner.style.top = y;
    });

    document.querySelectorAll('a, button, input, textarea, .service-card, .bento-card, .stat-card, .story-row').forEach((item) => {
        item.addEventListener('pointerenter', () => document.body.classList.add('cursor-hover'));
        item.addEventListener('pointerleave', () => document.body.classList.remove('cursor-hover'));
    });
}

// Menu hamburguesa
const navToggle = document.getElementById('nav-toggle');
const mobileNav = document.getElementById('mobile-nav');
const mobileNavClose = document.getElementById('mobile-nav-close');

if (navToggle && mobileNav) {
    const closeMenu = () => {
        mobileNav.classList.remove('is-open');
        navToggle.setAttribute('aria-expanded', 'false');
        mobileNav.setAttribute('aria-hidden', 'true');
        document.body.style.overflow = '';
    };

    const openMenu = () => {
        mobileNav.classList.add('is-open');
        navToggle.setAttribute('aria-expanded', 'true');
        mobileNav.setAttribute('aria-hidden', 'false');
        document.body.style.overflow = 'hidden';
    };

    navToggle.addEventListener('click', () => {
        if (mobileNav.classList.contains('is-open')) {
            closeMenu();
            return;
        }

        openMenu();
    });

    mobileNavClose?.addEventListener('click', closeMenu);

    mobileNav.querySelectorAll('a').forEach((link) => {
        link.addEventListener('click', closeMenu);
    });

    mobileNav.addEventListener('click', (event) => {
        if (event.target === mobileNav) {
            closeMenu();
        }
    });

    document.addEventListener('keydown', (event) => {
        if (event.key === 'Escape' && mobileNav.classList.contains('is-open')) {
            closeMenu();
            navToggle.focus();
        }
    });

    window.addEventListener('resize', () => {
        if (window.innerWidth > 860 && mobileNav.classList.contains('is-open')) {
            closeMenu();
        }
    });
}