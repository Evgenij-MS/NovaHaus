document.addEventListener('DOMContentLoaded', () => {
    // Globale Übersetzungen definieren (werden von base.html gesetzt)
    const translations = window.chatbotTranslations || {
        askQuestion: 'Ask a question',
        openChat: 'Open Chat',
        closeChat: 'Close Chat',
        typing: 'Typing...',
        error: 'Error',
        connectionError: 'Connection error',
        csrfNotFound: 'CSRF token not found',
        messageSent: 'Message sent!',
        failedToSend: 'Failed to send message',
        you: 'You',
        bot: 'Bot',
        system: 'System'
    };

    // Erstelle Chatbot Element mit korrekten Übersetzungen
    function createChatbotElement() {
        const chatbot = document.createElement('div');
        chatbot.className = 'chatbot fixed bottom-4 right-4 z-50';
        chatbot.innerHTML = `
            <div class="chatbot-window bg-white shadow-lg rounded-lg p-4 w-80 h-96 overflow-y-auto hidden">
                <div class="chatbot-header flex justify-between items-center mb-2">
                    <h3 class="font-bold text-blue-600">NovaHaus Chat</h3>
                    <button class="chatbot-close-btn text-gray-500 hover:text-red-500 text-xl font-bold">×</button>
                </div>
                <div class="chatbot-messages flex-1 overflow-y-auto mb-2 max-h-64"></div>
                <div class="input-area flex mt-2">
                    <textarea class="chatbot-input w-full p-2 border rounded-lg resize-none" 
                             placeholder="${translations.askQuestion}" 
                             rows="2"></textarea>
                    <button class="send-button bg-blue-500 text-white p-2 rounded-full ml-2 hover:bg-blue-600 transition">
                        ➤
                    </button>
                </div>
            </div>
            <button class="chatbot-toggle bg-blue-500 text-white p-4 rounded-full shadow-lg hover:bg-blue-600 transition">
                💬
            </button>
        `;
        return chatbot;
    }

    // Sprachspezifische Begrüßungsnachrichten
    const lang = document.documentElement.lang || 'ru';
    const welcomeMessages = {
        de: 'Hallo! Wie kann ich bei Ihrer Renovierung helfen?',
        en: 'Hi! How can I assist with your renovation?',
        tr: 'Merhaba! Tadilatınız için nasıl yardımcı olabilirim?',
        ru: 'Привет! Чем могу помочь с ремонтом?'
    };

    // Chatbot erstellen und zum Body hinzufügen
    const chatbot = createChatbotElement();
    document.body.appendChild(chatbot);

    // DOM-Elemente nach dem Hinzufügen zum DOM holen
    const chatbotToggle = chatbot.querySelector('.chatbot-toggle');
    const chatbotWindow = chatbot.querySelector('.chatbot-window');
    const chatbotInput = chatbot.querySelector('.chatbot-input');
    const chatbotMessages = chatbot.querySelector('.chatbot-messages');
    const sendButton = chatbot.querySelector('.send-button');
    const closeButton = chatbot.querySelector('.chatbot-close-btn');

    let isOpen = false;

    // Begrüßungsnachricht hinzufügen
    appendMessage(translations.bot, welcomeMessages[lang], 'bot-message');

    // Event Listeners
    chatbotToggle.addEventListener('click', toggleChatbot);
    closeButton.addEventListener('click', closeChatbot);
    sendButton.addEventListener('click', handleSendMessage);

    chatbotInput.addEventListener('keydown', async (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            await handleSendMessage();
        }
    });

    // Chatbot öffnen/schließen
    function toggleChatbot() {
        isOpen = !isOpen;
        chatbotWindow.classList.toggle('hidden');
        updateToggleButtonText();
    }

    function closeChatbot() {
        isOpen = false;
        chatbotWindow.classList.add('hidden');
        updateToggleButtonText();
    }

    // Button-Text aktualisieren (KORREKT übersetzt)
    function updateToggleButtonText() {
        chatbotToggle.innerHTML = isOpen ?
            `<span class="text-lg">💬</span>` :
            `<span class="text-lg">💬</span>`;
        chatbotToggle.setAttribute('aria-label',
            isOpen ? translations.closeChat : translations.openChat
        );
    }

    // Nachricht senden
    async function handleSendMessage() {
        try {
            await sendMessage();
            console.log('Сообщение успешно отправлено');
        } catch (error) {
            console.error('Ошибка при отправке:', error);
            appendMessage(translations.system, translations.failedToSend, 'system-message error');
        }
    }

    async function sendMessage() {
        const message = chatbotInput.value.trim();
        if (!message) return;

        // Benutzernachricht anzeigen
        appendMessage(translations.you, message, 'user-message');
        chatbotInput.value = '';

        // Lade-Indikator
        const loadingMessage = appendMessage(translations.bot, translations.typing, 'bot-message loading');

        try {
            const csrfToken = getCSRFToken();
            if (!csrfToken) {
                showError(translations.csrfNotFound);
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
                appendMessage(translations.bot, data.response, 'bot-message');
            } else {
                showError(data.error || 'Не удалось получить ответ');
            }
        } catch (error) {
            removeLoadingMessage(loadingMessage);
            showError(translations.connectionError);
            console.error('Chatbot error:', error);
            throw error;
        }
    }

    // Hilfsfunktionen
    function appendMessage(sender, text, className) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${className} p-3 mb-2 rounded-lg max-w-full`;

        // Styling basierend auf Nachrichtentyp
        if (className.includes('user-message')) {
            messageDiv.classList.add('bg-blue-500', 'text-white', 'ml-8', 'text-right');
        } else if (className.includes('bot-message')) {
            messageDiv.classList.add('bg-gray-100', 'text-gray-800', 'mr-8');
        } else if (className.includes('error')) {
            messageDiv.classList.add('bg-red-100', 'text-red-700', 'border', 'border-red-300');
        }

        messageDiv.innerHTML = `<div class="font-medium text-sm mb-1">${sender}</div><div>${text}</div>`;
        chatbotMessages.appendChild(messageDiv);
        chatbotMessages.scrollTop = chatbotMessages.scrollHeight;
        return messageDiv;
    }

    function showError(errorText) {
        appendMessage(translations.bot, `${translations.error}: ${errorText}`, 'bot-message error');
    }

    function removeLoadingMessage(loadingMessage) {
        if (loadingMessage && loadingMessage.parentNode) {
            loadingMessage.remove();
        }
    }

    function getCSRFToken() {
        // Zuerst aus Cookie versuchen
        const cookieValue = document.cookie.match(/csrftoken=([^;]+)/);
        if (cookieValue) {
            return cookieValue[1];
        }

        // Alternativ aus Meta-Tag oder verstecktem Input
        const metaToken = document.querySelector('meta[name="csrf-token"]');
        if (metaToken) {
            return metaToken.getAttribute('content');
        }

        const inputToken = document.querySelector('input[name="csrfmiddlewaretoken"]');
        if (inputToken) {
            return inputToken.value;
        }

        return null;
    }

    // Initialer Button-Text
    updateToggleButtonText();
});