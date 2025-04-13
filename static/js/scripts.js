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

// Запуск проверок после загрузки страницы
document.addEventListener('DOMContentLoaded', () => {
    console.log('Запуск отладки Google Analytics...');
    checkGoogleAnalytics();
    sendTestEvent();
    checkCrossDomain();
});