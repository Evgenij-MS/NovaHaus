let currentSlide = 0;
const slides = document.querySelector('.slides');
const totalSlides = slides.children.length;

// Плавный переход между слайдами
function showSlide(index) {
    slides.style.transition = 'transform 0.5s ease-in-out';
    const offset = -index * 100;
    slides.style.transform = `translateX(${offset}%)`;
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

// Функция для переключения слайда
function goToSlide(index) {
    currentSlide = index;
    showSlide(currentSlide);
    updateIndicators();
}

// Следующий слайд
function nextSlide() {
    const nextSlideIndex = (currentSlide + 1) % totalSlides;
    goToSlide(nextSlideIndex);
}

// Автоматическая прокрутка каждые 5 секунд
let slideInterval = setInterval(nextSlide, 5000);

// Остановка автоматической прокрутки при наведении на слайдер
const slider = document.querySelector('.slider');
if (slider) {
    slider.addEventListener('mouseenter', () => clearInterval(slideInterval));
    slider.addEventListener('mouseleave', () => {
        slideInterval = setInterval(nextSlide, 5000);
    });
}

// Добавление индикаторов (точек) для навигации
const indicatorsContainer = document.createElement('div');
indicatorsContainer.classList.add('indicators');
if (slider) {
    slider.appendChild(indicatorsContainer);
}

for (let i = 0; i < totalSlides; i++) {
    const indicator = document.createElement('div');
    indicator.classList.add('indicator');
    indicator.addEventListener('click', () => goToSlide(i));
    indicatorsContainer.appendChild(indicator);
}

// Переключение на предыдущий слайд
const prevButton = document.querySelector('.prev');
if (prevButton) {
    prevButton.addEventListener('click', () => {
        const prevSlideIndex = (currentSlide - 1 + totalSlides) % totalSlides;
        goToSlide(prevSlideIndex);
    });
}

// Переключение на следующий слайд
const nextButton = document.querySelector('.next');
if (nextButton) {
    nextButton.addEventListener('click', nextSlide);
}

// Обновление индикаторов при смене слайда
slides.addEventListener('transitionend', updateIndicators);

// Инициализация активного индикатора
updateIndicators();



// const changeLanguageButton = document.getElementById('change-language-button');
// if (changeLanguageButton) {
//     changeLanguageButton.addEventListener('click', () => {
//         const newLanguage = currentLanguage === 'ru' ? 'en' : 'ru'; // Переключение между русским и английским
//         changeLanguage(newLanguage);
//     });
// }