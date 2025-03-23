let currentSlide = 0;
const slides = document.querySelector('.slides');
const totalSlides = slides ? slides.children.length : 0;

// Плавный переход между слайдами
function showSlide(index) {
    if (!slides || totalSlides === 0 || index < 0 || index >= totalSlides) return; // Проверка на наличие слайдов и корректность индекса
    slides.style.transition = 'transform 0.5s ease-in-out';
    const offset = -index * 100;
    slides.style.transform = `translateX(${offset}%)`;
}

// Обновление активного индикатора
function updateIndicators() {
    const indicators = document.querySelectorAll('.indicator');
    if (!indicators.length) return; // Проверка на наличие индикаторов
    indicators.forEach((indicator, index) => {
        indicator.classList.toggle('active', index === currentSlide); // Упрощенный вариант
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
let slideInterval;
if (totalSlides > 1) { // Автоматическая прокрутка только если слайдов больше одного
    slideInterval = setInterval(() => {
        if (currentSlide === totalSlides - 1) {
            clearInterval(slideInterval); // Остановить интервал на последнем слайде
        } else {
            nextSlide();
        }
    }, 5000);
}

// Остановка автоматической прокрутки при наведении на слайдер
const slider = document.querySelector('.slider');
if (slider && totalSlides > 1) {
    slider.addEventListener('mouseenter', () => {
        if (slideInterval) clearInterval(slideInterval); // Проверка на наличие интервала
    });
    slider.addEventListener('mouseleave', () => {
        if (slideInterval) clearInterval(slideInterval); // Очистка предыдущего интервала
        slideInterval = setInterval(nextSlide, 5000);
    });
}

// Добавление индикаторов (точек) для навигации
if (slider && totalSlides > 0) {
    const indicatorsContainer = document.createElement('div');
    indicatorsContainer.classList.add('indicators');
    slider.appendChild(indicatorsContainer);

    for (let i = 0; i < totalSlides; i++) {
        const indicator = document.createElement('div');
        indicator.classList.add('indicator');
        indicator.setAttribute('role', 'button'); // Улучшение доступности
        indicator.setAttribute('aria-label', `Перейти к слайду ${i + 1}`); // Улучшение доступности
        indicator.addEventListener('click', () => goToSlide(i));
        indicatorsContainer.appendChild(indicator);
    }
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
if (slides) {
    slides.addEventListener('transitionend', updateIndicators);
}

// Инициализация активного индикатора
updateIndicators();

// Переключение темы
const toggleTheme = () => {
    document.body.classList.toggle('dark-theme');
    localStorage.setItem('theme', document.body.classList.contains('dark-theme') ? 'dark' : 'light');
};

// Восстановление темы при загрузке страницы
const savedTheme = localStorage.getItem('theme');
if (savedTheme === 'dark') {
    document.body.classList.add('dark-theme');
} else {
    document.body.classList.remove('dark-theme');
}

// Обработчик для кнопки переключения темы
const themeToggleButton = document.getElementById('theme-toggle');
if (themeToggleButton) {
    themeToggleButton.addEventListener('click', toggleTheme);
}

// Добавление клавиатурной навигации для слайдера
document.addEventListener('keydown', (event) => {
    if (event.key === 'ArrowLeft') {
        const prevSlideIndex = (currentSlide - 1 + totalSlides) % totalSlides;
        goToSlide(prevSlideIndex);
    } else if (event.key === 'ArrowRight') {
        nextSlide();
    }
});

// Добавление touch-событий для мобильных устройств
if (slider) {
    let touchStartX = 0;
    let touchEndX = 0;

    slider.addEventListener('touchstart', (event) => {
        touchStartX = event.touches[0].clientX;
    });

    slider.addEventListener('touchend', (event) => {
        touchEndX = event.changedTouches[0].clientX;
        handleSwipe();
    });

    function handleSwipe() {
        const swipeDistance = touchEndX - touchStartX;
        if (swipeDistance > 50) {
            const prevSlideIndex = (currentSlide - 1 + totalSlides) % totalSlides;
            goToSlide(prevSlideIndex);
        } else if (swipeDistance < -50) {
            nextSlide();
        }
    }
}