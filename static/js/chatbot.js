document.addEventListener('DOMContentLoaded', () => {
  const chatbot = document.createElement('div');
  chatbot.className = 'chatbot';
  chatbot.innerHTML = `
    <div class="chatbot-window" style="display: none;">
      <div class="chatbot-messages"></div>
      <input type="text" class="chatbot-input" placeholder="{% trans 'Задайте вопрос' %}">
    </div>
    <button class="chatbot-toggle">{% trans 'Чат' %}</button>
  `;
  document.body.appendChild(chatbot);

  const messages = {
    ru: 'Привет! Чем могу помочь с ремонтом?',
    de: 'Hallo! Wie kann ich bei Ihrer Renovierung helfen?',
    en: 'Hi! How can I assist with your renovation?'
  };
  const lang = document.documentElement.lang || 'ru';
  const chatbotMessages = document.querySelector('.chatbot-messages');
  chatbotMessages.innerHTML = `<p class="bot">${messages[lang]}</p>`;

  document.querySelector('.chatbot-toggle').addEventListener('click', () => {
    document.querySelector('.chatbot-window').style.display = 'block';
  });

  document.querySelector('.chatbot-input').addEventListener('keypress', async (e) => {
    if (e.key === 'Enter') {
      const input = e.target.value.trim();
      if (!input) return;
      chatbotMessages.innerHTML += `<p class="user">${input}</p>`;
      const response = await fetch('/chatbot/', {
        method: 'POST',
        headers: {
          'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ message: input, language: lang })
      });
      const data = await response.json();
      chatbotMessages.innerHTML += `<p class="bot">${data.response}</p>`;
      chatbotMessages.scrollTop = chatbotMessages.scrollHeight;
      e.target.value = '';
    }
  });
});