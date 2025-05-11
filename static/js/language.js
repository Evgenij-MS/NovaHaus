document.addEventListener('DOMContentLoaded', () => {
    const select = document.querySelector('#language');
    const supportedLangs = ['de', 'en', 'tr', 'ru'];
    const defaultLang = 'de';

    let selectedLang = localStorage.getItem('language');
    if (!selectedLang) {
        const userLang = (navigator.language || '').split('-')[0];
        selectedLang = supportedLangs.includes(userLang) ? userLang : defaultLang;
        localStorage.setItem('language', selectedLang);
    }

    if (select && select.value !== selectedLang) {
        select.value = selectedLang;
    }

    if (select) {
        select.addEventListener('change', (e) => {
            const lang = e.target.value;
            if (!supportedLangs.includes(lang)) return;

            localStorage.setItem('language', lang);

            const csrfToken = getCSRFToken();
            if (!csrfToken) {
                console.error('CSRF-токен не найден');
                return;
            }

            fetch(`/set-language/${lang}/`, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': csrfToken,
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ language: lang })
            })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        const currentPath = window.location.pathname;
                        location.assign(currentPath.replace(/^\/(de|en|tr|ru)\//, `/${lang}/`));
                    } else {
                        console.error('Failed to set language:', data.error);
                        select.value = selectedLang;
                    }
                })
                .catch(error => {
                    console.error('Error setting language:', error);
                    select.value = selectedLang;
                });
        });
    }
});