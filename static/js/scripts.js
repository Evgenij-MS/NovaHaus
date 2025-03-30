// ===== ФУНКЦИОНАЛ СЛАЙДЕРА =====
let currentSlide = 0;
const slider = document.querySelector('.slider');
const slides = document.querySelector('.slides');
const totalSlides = slides?.children.length || 0;

// Показать конкретный слайд
function showSlide(index) {
  if (!slides || index < 0 || index >= totalSlides) return;

  slides.style.transition = 'transform 0.5s ease-in-out';
  slides.style.transform = `translateX(${-index * 100}%)`;
  currentSlide = index;
  updateIndicators();
}

// Обновить индикаторы
function updateIndicators() {
  document.querySelectorAll('.indicator').forEach((indicator, i) => {
    indicator.classList.toggle('active', i === currentSlide);
  });
}

// Следующий слайд
function nextSlide() {
  showSlide((currentSlide + 1) % totalSlides);
}

// Инициализация слайдера
if (totalSlides > 0) {
  // Автопрокрутка
  let slideInterval = totalSlides > 1 ? setInterval(() => {
    currentSlide === totalSlides - 1 ? clearInterval(slideInterval) : nextSlide();
  }, 5000) : null;

  // Управление мышью
  if (slider) {
    slider.addEventListener('mouseenter', () => {
      if (slideInterval) clearInterval(slideInterval);
    });

    slider.addEventListener('mouseleave', () => {
      if (slideInterval) clearInterval(slideInterval);
      slideInterval = totalSlides > 1 ? setInterval(nextSlide, 5000) : null;
    });

    // Управление касанием
    let touchStartX = 0;
    slider.addEventListener('touchstart', e => {
      touchStartX = e.touches[0].clientX;
    });

    slider.addEventListener('touchend', e => {
      const touchEndX = e.changedTouches[0].clientX;
      const swipeDistance = touchEndX - touchStartX;

      if (swipeDistance > 50) {
        showSlide((currentSlide - 1 + totalSlides) % totalSlides);
      } else if (swipeDistance < -50) {
        nextSlide();
      }
    });
  }

  // Создание индикаторов
  const indicatorsContainer = document.createElement('div');
  indicatorsContainer.className = 'indicators';
  slider?.appendChild(indicatorsContainer);

  for (let i = 0; i < totalSlides; i++) {
    const indicator = document.createElement('div');
    indicator.className = 'indicator';
    indicator.setAttribute('role', 'button');
    indicator.setAttribute('aria-label', `Перейти к слайду ${i + 1}`);
    indicator.addEventListener('click', () => showSlide(i));
    indicatorsContainer.appendChild(indicator);
  }

  // Кнопки навигации
  document.querySelector('.prev')?.addEventListener('click', () => {
    showSlide((currentSlide - 1 + totalSlides) % totalSlides);
  });

  document.querySelector('.next')?.addEventListener('click', nextSlide);

  // Навигация с клавиатуры
  document.addEventListener('keydown', e => {
    if (e.key === 'ArrowLeft') {
      showSlide((currentSlide - 1 + totalSlides) % totalSlides);
    } else if (e.key === 'ArrowRight') {
      nextSlide();
    }
  });
}

// ===== ПЕРЕКЛЮЧЕНИЕ ТЕМЫ =====
function toggleTheme() {
  document.body.classList.toggle('dark-theme');
  localStorage.setItem('theme', document.body.classList.contains('dark-theme') ? 'dark' : 'light');
}

// Применение сохраненной темы
const savedTheme = localStorage.getItem('theme');
if (savedTheme === 'dark') {
  document.body.classList.add('dark-theme');
} else if (savedTheme === 'light') {
  document.body.classList.remove('dark-theme');
}

document.getElementById('theme-toggle')?.addEventListener('click', toggleTheme);

// ===== МОБИЛЬНОЕ МЕНЮ =====
document.addEventListener('DOMContentLoaded', () => {
  const mobileToggle = document.querySelector('.mobile-menu-toggle');
  const mobileNav = document.querySelector('.mobile-nav');

  if (!mobileToggle || !mobileNav) return;

  // Переключение состояния меню
  function toggleMenu(shouldOpen) {
    const isOpen = shouldOpen ?? !mobileNav.classList.contains('active');
    const spans = mobileToggle.querySelectorAll('span');

    // Анимация бургер-иконки
    if (isOpen) {
      spans[0].style.transform = 'rotate(45deg) translate(5px, 5px)';
      spans[1].style.opacity = '0';
      spans[2].style.transform = 'rotate(-45deg) translate(7px, -6px)';
    } else {
      spans[0].style.transform = '';
      spans[1].style.opacity = '';
      spans[2].style.transform = '';
    }

    // Управление классами
    mobileToggle.classList.toggle('active', isOpen);
    mobileNav.classList.toggle('active', isOpen);
    document.body.classList.toggle('no-scroll', isOpen);

    // ARIA-атрибуты
    mobileToggle.setAttribute('aria-expanded', String(isOpen));
    mobileNav.setAttribute('aria-hidden', String(!isOpen));
  }

  // Обработчики событий
  mobileToggle.addEventListener('click', () => toggleMenu());

  // Закрытие при клике на ссылку
  document.querySelectorAll('.mobile-nav a').forEach(link => {
    link.addEventListener('click', () => toggleMenu(false));
  });

  // Закрытие при клике вне меню
  document.addEventListener('click', e => {
    if (!e.target.closest('.header-content') && !e.target.closest('.mobile-nav')) {
      toggleMenu(false);
    }
  });

  // Подсветка активного пункта меню
  const currentPath = window.location.pathname;
  document.querySelectorAll('nav a').forEach(link => {
    if (link.getAttribute('href') === currentPath) {
      link.classList.add('active');
    }
  });
});