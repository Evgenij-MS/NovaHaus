// Функция для проверки загрузки Google Analytics
function checkGoogleAnalytics() {
    if (typeof gtag === 'undefined') {
        console.error('Google Analytics: gtag.js не загружен. Проверьте подключение скрипта.');
        return false;
    }
    console.log('Google Analytics: gtag.js загружен успешно.');
    return true;
}

// Отправка тестового события для отладки
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
            console.error('Google Analytics: Ошибка при отправке события:', e);
        }
    }
}

// Проверка междоменного отслеживания
function checkCrossDomain() {
    if (checkGoogleAnalytics()) {
        const domains = ['novahaus-hamburg.de', 'novahaus-koeln.de'];
        const currentDomain = window.location.hostname;
        if (domains.includes(currentDomain)) {
            console.log('Google Analytics: Текущий домен поддерживает междоменное отслеживание:', currentDomain);
        } else {
            console.warn('Google Analytics: Текущий домен не в списке междоменного отслеживания:', currentDomain);
        }
    }
}

// Проверка текущего GA ID
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

// Запуск проверок после загрузки страницы
document.addEventListener('DOMContentLoaded', () => {
    console.log('Запуск отладки Google Analytics...');
    checkGoogleAnalytics();
    checkGAId();
    sendTestEvent();
    checkCrossDomain();
});