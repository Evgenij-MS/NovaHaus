document.addEventListener('DOMContentLoaded', () => {
  const select = document.querySelector('#language');
  const supportedLangs = ['de', 'en', 'tr', 'ru'];

  // Автоматическое определение языка
  const userLang = navigator.language || navigator.userLanguage;
  let selectedLang = localStorage.getItem('language');

  if (!selectedLang) {
    selectedLang = supportedLangs.includes(userLang.split('-')[0]) ? userLang.split('-')[0] : 'de';
    localStorage.setItem('language', selectedLang);
  }

  // Установить язык
  if (select.value !== selectedLang) {
    select.value = selectedLang;
    fetch(`/set-language/${selectedLang}/`, {
      method: 'POST',
      headers: {
        'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
      }
    }).then(() => window.location.reload());
  }

  // Переключение языка
  select.addEventListener('change', (e) => {
    const lang = e.target.value;
    localStorage.setItem('language', lang);
    fetch(`/set-language/${lang}/`, {
      method: 'POST',
      headers: {
        'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
      }
    }).then(() => window.location.reload());
  });
});