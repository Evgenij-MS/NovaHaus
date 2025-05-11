// Google Analytics: Проверка загрузки gtag.js
function checkGoogleAnalytics() {
    if (typeof gtag === 'undefined') {
        console.error('Google Analytics: gtag.js не загружен. Проверьте подключение скрипта.');
        return false;
    }
    console.log('Google Analytics: gtag.js загружен успешно.');
    return true;
}

// Google Analytics: Отправка тестового события
function sendTestEvent() {
    if (checkGoogleAnalytics()) {
        try {
            gtag('event', 'test_event', {
                'event_category': 'Debug',
                'event_label': 'Test GA4',
                'value': 1
            });
            console.log('Google Analytics: Тестовое событие отправлено.');
        } catch (e) {
            console.error('Google Analytics: Ошибка отправки события:', e);
        }
    }
}

// Google Analytics: Проверка междоменного отслеживания
function checkCrossDomain() {
    if (checkGoogleAnalytics()) {
        const domains = ['novahaus-hamburg.de', 'novahaus-koeln.de'];
        const currentDomain = window.location.hostname;
        if (domains.includes(currentDomain)) {
            console.log('Google Analytics: Междоменное отслеживание для:', currentDomain);
        } else {
            console.warn('Google Analytics: Домен не в списке:', currentDomain);
        }
    }
}

// Google Analytics: Проверка ID аналитики
function checkGAId() {
    const host = window.location.hostname;
    if (host === 'novahaus-hamburg.de' || host === 'www.novahaus-hamburg.de') {
        console.log('Google Analytics: Ожидается ID G-19RQG7TDMC для Hamburg');
    } else if (host === 'novahaus-koeln.de' || host === 'www.novahaus-koeln.de') {
        console.log('Google Analytics: Ожидается ID G-BS4J4PD0WF для Köln');
    } else {
        console.warn('Google Analytics: Неизвестный домен:', host);
    }
}

// Мобильное меню: Переключение навигации
function toggleMobileMenu() {
    const menu = document.getElementById('nav-menu');
    const toggleButton = document.querySelector('.mobile-menu-toggle');

    if (menu && toggleButton) {
        menu.classList.toggle('active');
        const isExpanded = menu.classList.contains('active');
        toggleButton.setAttribute('aria-expanded', isExpanded ? 'true' : 'false');
    } else {
        console.warn('Мобильное меню: Элементы nav-menu или mobile-menu-toggle не найдены.');
    }
}

// Инициализация скриптов после загрузки DOM
document.addEventListener('DOMContentLoaded', () => {
    // Проверки Google Analytics
    checkGoogleAnalytics();
    checkGAId();
    sendTestEvent();
    checkCrossDomain();

    // Обработчик кнопки мобильного меню
    const toggleButton = document.querySelector('.mobile-menu-toggle');
    if (toggleButton) {
        toggleButton.addEventListener('click', toggleMobileMenu);
    }
});