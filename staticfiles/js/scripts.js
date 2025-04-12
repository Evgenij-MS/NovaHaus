// static/js/scripts.js

// ===== ПЕРЕКЛЮЧЕНИЕ ТЕМЫ =====
function toggleTheme() {
    document.body.classList.toggle('dark-theme');
    localStorage.setItem('theme', document.body.classList.contains('dark-theme') ? 'dark' : 'light');
}

// Применение сохранённой темы
const savedTheme = localStorage.getItem('theme');
if (savedTheme === 'dark') {
    document.body.classList.add('dark-theme');
} else if (savedTheme === 'light') {
    document.body.classList.remove('dark-theme');
}

document.getElementById('theme-toggle')?.addEventListener('click', toggleTheme);

// ===== МОБИЛЬНОЕ МЕНЮ =====
document.addEventListener('DOMContentLoaded', () => {
    console.log('Scripts.js loaded');
    const mobileToggle = document.querySelector('.mobile-menu-toggle');
    const mobileNav = document.querySelector('.mobile-nav');

    if (!mobileToggle || !mobileNav) {
        console.warn('Mobile menu elements not found');
        return;
    }

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

// ===== МОДАЛЬНОЕ ОКНО =====
function openPriceList() {
    const modal = document.getElementById('price-list-modal');
    if (modal) {
        modal.style.display = 'block';
    }
}

function closePriceList() {
    const modal = document.getElementById('price-list-modal');
    if (modal) {
        modal.style.display = 'none';
    }
}

window.addEventListener('click', function(event) {
    const modal = document.getElementById('price-list-modal');
    if (modal && event.target === modal) {
        modal.style.display = 'none';
    }
});