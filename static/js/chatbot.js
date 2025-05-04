document.addEventListener('DOMContentLoaded', () => {
  function createChatbotElement() {
    const chatbot = document.createElement('div');
    chatbot.className = 'chatbot fixed bottom-4 right-4 z-50';
    chatbot.innerHTML = `
      <div class="chatbot-window bg-white shadow-lg rounded-lg p-4 w-80 h-96 overflow-y-auto hidden">
        <div class="chatbot-messages"></div>
        <input type="text" class="chatbot-input w-full p-2 border rounded-lg" placeholder="{% trans 'Ask a question' %}">
      </div>
      <button class="chatbot-toggle bg-primary text-white p-4 rounded-full">{% trans 'Chat' %}</button>
    `;
    return chatbot;
  }

  function getCSRFToken() {
    const match = document.cookie.match(/(^|;)\s*csrftoken=([^;]+)/);
    return match ? match[2] : null;
  }

  const messages = {
    de: 'Hallo! Wie kann ich bei Ihrer Renovierung helfen?',
    en: 'Hi! How can I assist with your renovation?',
    tr: 'Merhaba! Tadilatınız için nasıl yardımcı olabilirim?',
    ru: 'Привет! Чем могу помочь с ремонтом?'
  };

  const lang = document.documentElement.lang || 'de';
  const chatbot = createChatbotElement();
  document.body.appendChild(chatbot);

  const chatbotMessages = document.querySelector('.chatbot-messages');
  chatbotMessages.innerHTML = `<p class="bot">${messages[lang]}</p>`;

  document.querySelector('.chatbot-toggle').addEventListener('click', () => {
    const window = document.querySelector('.chatbot-window');
    window.style.display = window.style.display === 'block' ? 'none' : 'block';
  });

  document.querySelector('.chatbot-input').addEventListener('keypress', async (e) => {
    if (e.key === 'Enter') {
      const input = e.target.value.trim();
      if (!input) return;
      chatbotMessages.innerHTML += `<p class="user">${input}</p>`;
      try {
        const csrfToken = getCSRFToken();
        if (!csrfToken) throw new Error('CSRF token not found');
        const response = await fetch('/chatbot/', {
          method: 'POST',
          headers: {
            'X-CSRFToken': csrfToken,
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({ message: input, language: lang })
        });
        const data = await response.json();
        if (data.response) {
          chatbotMessages.innerHTML += `<p class="bot">${data.response}</p>`;
        } else {
          chatbotMessages.innerHTML += `<p class="bot">Fehler: ${data.error}</p>`;
        }
        chatbotMessages.scrollTop = chatbotMessages.scrollHeight;
        e.target.value = '';
      } catch (error) {
        chatbotMessages.innerHTML += `<p class="bot">Verbindungsfehler. Bitte versuchen Sie es später.</p>`;
        console.error('Chatbot error:', error);
      }
    }
  });
});