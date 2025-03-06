// Мультиязычная поддержка
const translations = {
    ru: {
        calculate: 'Рассчитать',
        area: 'Площадь (м²)',
        result: 'Примерная стоимость: €'
    },
    en: {
        calculate: 'Calculate',
        area: 'Area (m²)',
        result: 'Estimated cost: €'
    }
};

function changeLanguage(lang) {
    document.getElementById('calculate-button').innerText = translations[lang].calculate;
    document.getElementById('area-label').innerText = translations[lang].area;
    document.getElementById('result-label').innerText = translations[lang].result;
}