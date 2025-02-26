let currentSlide = 0;
const slides = document.querySelector('.slides');
const totalSlides = slides.children.length;

// Плавный переход между слайдами
function showSlide(index) {
    slides.style.transition = 'transform 0.5s ease-in-out';
    const offset = -index * 100;
    slides.style.transform = `translateX(${offset}%)`;
}

// Следующий слайд
function nextSlide() {
    currentSlide = (currentSlide + 1) % totalSlides;
    showSlide(currentSlide);
}

// Автоматическая прокрутка каждые 5 секунд
let slideInterval = setInterval(nextSlide, 5000);

// Остановка автоматической прокрутки при наведении на слайдер
const slider = document.querySelector('.slider');
slider.addEventListener('mouseenter', () => clearInterval(slideInterval));
slider.addEventListener('mouseleave', () => {
    slideInterval = setInterval(nextSlide, 5000);
});

// Добавление индикаторов (точек) для навигации
const indicatorsContainer = document.createElement('div');
indicatorsContainer.classList.add('indicators');
slider.appendChild(indicatorsContainer);

for (let i = 0; i < totalSlides; i++) {
    const indicator = document.createElement('div');
    indicator.classList.add('indicator');
    indicator.addEventListener('click', () => {
        currentSlide = i;
        showSlide(currentSlide);
    });
    indicatorsContainer.appendChild(indicator);
}

// Обновление активного индикатора
function updateIndicators() {
    const indicators = document.querySelectorAll('.indicator');
    indicators.forEach((indicator, index) => {
        if (index === currentSlide) {
            indicator.classList.add('active');
        } else {
            indicator.classList.remove('active');
        }
    });
}

// Обновление индикаторов при смене слайда
slides.addEventListener('transitionend', updateIndicators);