// main.js
document.addEventListener('DOMContentLoaded', () => {
    console.log('NovaHaus main.js loaded');

    // Theme Toggle
    const themeToggle = document.getElementById('theme-toggle');
    if (themeToggle) {
        themeToggle.addEventListener('click', () => {
            document.body.classList.toggle('dark-theme');
            const isDark = document.body.classList.contains('dark-theme');
            themeToggle.textContent = isDark ? 'Светлая тема' : 'Тёмная тема';
            localStorage.setItem('theme', isDark ? 'dark' : 'light');
        });

        // Load saved theme
        const savedTheme = localStorage.getItem('theme');
        if (savedTheme === 'dark') {
            document.body.classList.add('dark-theme');
            themeToggle.textContent = 'Светлая тема';
        }
    }

    // Initialize other features (e.g., chatbot, slider) as needed
});

// Service Worker Registration
if ('serviceWorker' in navigator) {
    navigator.serviceWorker.register('/static/js/service-worker.js')
        .then(reg => console.log('Service Worker registered', reg))
        .catch(err => console.error('Service Worker registration failed', err));
}