// Мультиязычная поддержка
const translations = {
    ru: {
        calculate: 'Рассчитать',
        area: 'Площадь (м²)',
        result: 'Примерная стоимость: €',
        welcome: 'Добро пожаловать в NovaHaus!',
        services: 'Наши услуги',
        reviews: 'Отзывы клиентов',
        contact: 'Контакты',
        // Добавьте другие тексты, которые нужно переводить
    },
    en: {
        calculate: 'Calculate',
        area: 'Area (m²)',
        result: 'Estimated cost: €',
        welcome: 'Welcome to NovaHaus!',
        services: 'Our Services',
        reviews: 'Customer Reviews',
        contact: 'Contact Us',
        // Добавьте другие тексты, которые нужно переводить
    },
    de: {
        calculate: 'Berechnen',
        area: 'Fläche (m²)',
        result: 'Geschätzte Kosten: €',
        welcome: 'Willkommen bei NovaHaus!',
        services: 'Unsere Dienstleistungen',
        reviews: 'Kundenbewertungen',
        contact: 'Kontakt',
        // Добавьте другие тексты, которые нужно переводить
    }
};

// Функция для изменения языка
function changeLanguage(lang) {
    // Обновляем тексты на странице
    const elementsToTranslate = document.querySelectorAll('[data-translate]');
    elementsToTranslate.forEach(element => {
        const key = element.getAttribute('data-translate');
        if (translations[lang] && translations[lang][key]) {
            element.innerText = translations[lang][key];
        }
    });

    // Сохраняем выбранный язык в localStorage
    localStorage.setItem('preferredLanguage', lang);

    // Обновляем выбранный язык в переключателе
    const languageSelect = document.getElementById('language-select');
    if (languageSelect) {
        languageSelect.value = lang;
    }
}

// Функция для загрузки сохраненного языка
function loadPreferredLanguage() {
    const savedLanguage = localStorage.getItem('preferredLanguage') || 'ru'; // По умолчанию русский
    changeLanguage(savedLanguage);
}

// Инициализация при загрузке страницы
document.addEventListener('DOMContentLoaded', () => {
    loadPreferredLanguage();

    // Обработка изменения языка в переключателе
    const languageSelect = document.getElementById('language-select');
    if (languageSelect) {
        languageSelect.addEventListener('change', (event) => {
            changeLanguage(event.target.value);
        });
    }
});