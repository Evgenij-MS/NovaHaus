// static/js/services.js
document.addEventListener('DOMContentLoaded', () => {
    // Анимация карточек
    const cards = document.querySelectorAll('.service-card');
    cards.forEach((card, index) => {
        setTimeout(() => {
            card.classList.add('animate');
        }, index * 200);
    });

    // Слайдер
    const slides = document.querySelector('.slides');
    const images = slides.querySelectorAll('img');
    const prev = document.querySelector('.prev');
    const next = document.querySelector('.next');
    const indicators = document.querySelectorAll('.indicator');
    let currentIndex = 0;

    function updateSlider() {
        slides.style.transform = `translateX(-${currentIndex * 100}%)`;
        indicators.forEach((indicator, index) => {
            indicator.classList.toggle('active', index === currentIndex);
        });
    }

    prev.addEventListener('click', () => {
        currentIndex = (currentIndex - 1 + images.length) % images.length;
        updateSlider();
    });

    next.addEventListener('click', () => {
        currentIndex = (currentIndex + 1) % images.length;
        updateSlider();
    });

    indicators.forEach((indicator, index) => {
        indicator.addEventListener('click', () => {
            currentIndex = index;
            updateSlider();
        });
    });

    // Автослайд
    setInterval(() => {
        currentIndex = (currentIndex + 1) % images.length;
        updateSlider();
    }, 5000);
});

// Модальное окно
function openPriceList() {
    document.getElementById('price-list-modal').style.display = 'block';
}

function closePriceList() {
    document.getElementById('price-list-modal').style.display = 'none';
}

window.onclick = function(event) {
    const modal = document.getElementById('price-list-modal');
    if (event.target === modal) {
        modal.style.display = 'none';
    }
};