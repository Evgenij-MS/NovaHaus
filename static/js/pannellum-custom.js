document.addEventListener('DOMContentLoaded', () => {
    const modal = document.querySelector('.panorama-modal');
    const panoramaContainer = document.querySelector('#panorama');
    const closeButton = document.querySelector('.panorama-close');
    const toggles = document.querySelectorAll('.panorama-toggle');

    toggles.forEach(toggle => {
        toggle.addEventListener('click', () => {
            const panoramaUrl = toggle.getAttribute('data-panorama');
            modal.classList.remove('hidden');
            if (typeof pannellum !== 'undefined') {
                pannellum.viewer('panorama', {
                    "type": "equirectangular",
                    "panorama": panoramaUrl,
                    "autoLoad": true,
                    "autoRotate": -2,
                    "compass": true,
                    "title": "NovaHaus Project",
                    "author": "NovaHaus"
                });
                console.log('Pannellum: Панорама загружена:', panoramaUrl);
            } else {
                console.error('Pannellum: Библиотека не найдена.');
            }
        });
    });

    closeButton.addEventListener('click', () => {
        modal.classList.add('hidden');
        panoramaContainer.innerHTML = '';
    });

    modal.addEventListener('click', (e) => {
        if (e.target === modal) {
            modal.classList.add('hidden');
            panoramaContainer.innerHTML = '';
        }
    });
});