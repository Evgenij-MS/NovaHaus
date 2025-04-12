// static/js/services.js
document.addEventListener('DOMContentLoaded', () => {
    // Анимация карточек
    const cards = document.querySelectorAll('.service-card');
    cards.forEach((card, index) => {
        setTimeout(() => {
            card.classList.add('animate');
        }, index * 200);
    });
});