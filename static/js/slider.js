// slider.js
let currentSlide = 0;
const slides = document.querySelector('.slides');
const totalSlides = slides.children.length;

function showSlide(index) {
    const offset = -index * 100;
    slides.style.transform = `translateX(${offset}%)`;
    updateIndicators(index);
}

function nextSlide() {
    currentSlide = (currentSlide + 1) % totalSlides;
    showSlide(currentSlide);
}

function updateIndicators(index) {
    const indicators = document.querySelectorAll('.slider-indicators button');
    indicators.forEach((indicator, i) => {
        indicator.classList.toggle('active', i === index);
    });
}

// Автоматическая прокрутка
setInterval(nextSlide, 5000);

// Обработка кликов на индикаторы
document.querySelectorAll('.slider-indicators button').forEach((button, index) => {
    button.addEventListener('click', () => showSlide(index));
});