const translations = {
    ru: {
        calculate: 'Рассчитать',
        area: 'Площадь (м²)',
        result: 'Примерная стоимость: €',
        welcome: 'Добро пожаловать в NovaHaus!',
        services: 'Наши услуги',
        reviews: 'Отзывы клиентов',
        contact: 'Контакты',
    },
    en: {
        calculate: 'Calculate',
        area: 'Area (m²)',
        result: 'Estimated cost: €',
        welcome: 'Welcome to NovaHaus!',
        services: 'Our Services',
        reviews: 'Customer Reviews',
        contact: 'Contact Us',
    },
    de: {
        calculate: 'Berechnen',
        area: 'Fläche (m²)',
        result: 'Geschätzte Kosten: €',
        welcome: 'Willkommen bei NovaHaus!',
        services: 'Unsere Dienstleistungen',
        reviews: 'Kundenbewertungen',
        contact: 'Kontakt',
    }
};

function changeLanguage(lang) {
    const elementsToTranslate = document.querySelectorAll('[data-translate]');
    elementsToTranslate.forEach(element => {
        const key = element.getAttribute('data-translate');
        if (translations[lang] && translations[lang][key]) {
            element.innerText = translations[lang][key];
        }
    });

    localStorage.setItem('preferredLanguage', lang);
    const languageSelect = document.getElementById('language-select');
    if (languageSelect) {
        languageSelect.value = lang;
    }
}

function loadPreferredLanguage() {
    const savedLanguage = localStorage.getItem('preferredLanguage') || 'ru';
    changeLanguage(savedLanguage);
}

document.addEventListener('DOMContentLoaded', () => {
    loadPreferredLanguage();

    const languageSelect = document.getElementById('language-select');
    if (languageSelect) {
        languageSelect.addEventListener('change', (event) => {
            changeLanguage(event.target.value);
        });
    }
});