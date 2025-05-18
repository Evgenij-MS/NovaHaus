document.addEventListener('DOMContentLoaded', () => {
    // Создание элемента чатбота
    function createChatbotElement() {
        const chatbot = document.createElement('div');
        chatbot.className = 'chatbot fixed bottom-4 right-4 z-50';
        chatbot.innerHTML = `
            <div class="chatbot-window bg-white shadow-lg rounded-lg p-4 w-80 h-96 overflow-y-auto hidden">
                <div class="chatbot-messages"></div>
                <div class="input-area flex mt-2">
                    <textarea class="chatbot-input w-full p-2 border rounded-lg" placeholder="{% trans 'Ask a question' %}" rows="2"></textarea>
                    <button class="send-button bg-primary text-white p-2 rounded-full ml-2">➤</button>
                </div>
            </div>
            <button class="chatbot-toggle bg-primary text-white p-4 rounded-full shadow-md hover:bg-primary-dark transition">
                {% trans 'Open Chat' %}
            </button>
        `;
        return chatbot;
    }

    // Инициализация элементов
    const lang = document.documentElement.lang || 'ru';
    const chatbot = createChatbotElement();
    document.body.appendChild(chatbot);

    const messages = {
        de: 'Hallo! Wie kann ich bei Ihrer Renovierung helfen?',
        en: 'Hi! How can I assist with your renovation?',
        tr: 'Merhaba! Tadilatınız için nasıl yardımcı olabilirim?',
        ru: 'Привет! Чем могу помочь с ремонтом?'
    };

    // Элементы интерфейса
    const chatbotToggle = document.querySelector('.chatbot-toggle');
    const chatbotWindow = document.querySelector('.chatbot-window');
    const chatbotInput = document.querySelector('.chatbot-input');
    const chatbotMessages = document.querySelector('.chatbot-messages');
    const sendButton = document.querySelector('.send-button');

    // Начальное сообщение (добавляется только один раз)
    appendMessage('Бот', messages[lang], 'bot-message');

    // Обработчики событий
    chatbotToggle.addEventListener('click', () => {
        chatbotWindow.classList.toggle('hidden');
        updateToggleButtonText();
    });

    // Новая функция для обработки отправки сообщения
    async function handleSendMessage() {
        try {
            await sendMessage();
            console.log('Сообщение успешно отправлено');
            appendMessage('Система', 'Сообщение отправлено!', 'system-message success');
        } catch (error) {
            console.error('Ошибка при отправке:', error);
            appendMessage('Система', 'Не удалось отправить сообщение', 'system-message error');
        }
    }

    // Обработчик клика на кнопку отправки
    sendButton.addEventListener('click', handleSendMessage);

    // Обработчик нажатия клавиши Enter
    chatbotInput.addEventListener('keydown', async (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            await handleSendMessage();
        }
    });

    async function sendMessage() {
        const message = chatbotInput.value.trim();
        if (!message) return;

        appendMessage('Вы', message, 'user-message');
        chatbotInput.value = '';

        // Показать индикатор загрузки
        const loadingMessage = appendMessage('Бот', 'Печатает...', 'bot-message loading');

        try {
            const csrfToken = getCSRFToken();
            if (!csrfToken) {
                showError('CSRF-токен не найден');
                removeLoadingMessage(loadingMessage);
                return;
            }

            const response = await fetch('/chatbot/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrfToken
                },
                body: JSON.stringify({
                    message,
                    language: lang
                })
            });

            const data = await response.json();
            removeLoadingMessage(loadingMessage);
            if (data.response) {
                appendMessage('Бот', data.response, 'bot-message');
            } else {
                showError(data.error || 'Не удалось получить ответ');
            }
        } catch (error) {
            removeLoadingMessage(loadingMessage);
            showError('Ошибка подключения');
            console.error('Chatbot error:', error);
            throw error;
        }
    }

    // Вспомогательные функции
    function appendMessage(sender, text, className) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${className} p-2 mb-2 rounded-lg`;
        messageDiv.innerHTML = `<strong>${sender}:</strong> ${text}`;
        chatbotMessages.appendChild(messageDiv);
        chatbotMessages.scrollTop = chatbotMessages.scrollHeight;
        return messageDiv;
    }

    function showError(errorText) {
        appendMessage('Бот', `Ошибка: ${errorText}`, 'bot-message error text-red-500');
    }

    function removeLoadingMessage(loadingMessage) {
        if (loadingMessage) {
            loadingMessage.remove();
        }
    }

    function getCSRFToken() {
        const cookieValue = document.cookie.match(/csrftoken=([^;]+)/);
        return cookieValue ? cookieValue[1] : null;
    }

    function updateToggleButtonText() {
        const isHidden = chatbotWindow.classList.contains('hidden');
        chatbotToggle.textContent = isHidden ? '{% trans "Open Chat" %}' : '{% trans "Close Chat" %}';
    }

    // Установить начальный текст кнопки
    updateToggleButtonText();
});