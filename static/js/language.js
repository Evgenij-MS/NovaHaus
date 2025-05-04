document.addEventListener('DOMContentLoaded', () => {
  const select = document.querySelector('#language');
  const supportedLangs = ['de', 'en', 'tr', 'ru'];
  const defaultLang = 'de';

  // Получение CSRF-токена из cookies с использованием регулярного выражения
  function getCSRFToken() {
    const match = document.cookie.match(/(^|;)\s*csrftoken=([^;]+)/);
    return match ? match[2] : null;
  }

  // Автоматическое определение языка
  let selectedLang = localStorage.getItem('language');
  if (!selectedLang) {
    const userLang = (navigator.language || '').split('-')[0];
    selectedLang = supportedLangs.includes(userLang) ? userLang : defaultLang;
    localStorage.setItem('language', selectedLang);
  }

  // Установить значение селектора
  if (select && select.value !== selectedLang) {
    select.value = selectedLang;
  }

  // Переключение языка
  if (select) {
    select.addEventListener('change', (e) => {
      const lang = e.target.value;
      if (!supportedLangs.includes(lang)) return;

      localStorage.setItem('language', lang);

      fetch(`/set-language/${lang}/`, {
        method: 'POST',
        headers: {
          'X-CSRFToken': getCSRFToken(),
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ language: lang })
      })
        .then(response => response.json())
        .then(data => {
          if (data.success) {
            // Редирект с учётом нового языкового префикса
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