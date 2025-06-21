// chatbot.js
document.addEventListener('DOMContentLoaded', () => {
    // DOM-Elemente
    const chatbotToggle = document.getElementById('chatbot-toggle');
    const chatbotWindow = document.getElementById('chatbot-window');
    const chatbotMessages = document.getElementById('chatbot-messages');
    const chatbotInput = document.getElementById('chatbot-input');
    const chatbotSendButton = document.getElementById('chatbot-send');

    // Zustandsvariablen
    let isOpen = false;

    // Chatbot-Konfiguration
    const config = {
        apiEndpoint: '/api/chatbot/',
        maxMessageLength: 500,
        typingDelay: 500
    };

    // Nachrichtenstatus-Enum
    const MessageType = {
        USER: 'user',
        BOT: 'bot',
        SYSTEM: 'system'
    };

    // Hilfsfunktionen
    function createMessageElement(message, type) {
        const messageElement = document.createElement('div');
        messageElement.classList.add('chatbot-message', `message-${type}`);
        messageElement.textContent = message;
        return messageElement;
    }

    function scrollToBottom() {
        chatbotMessages.scrollTop = chatbotMessages.scrollHeight;
    }

    function showTypingIndicator() {
        const typingIndicator = createMessageElement('Schreibt...', MessageType.SYSTEM);
        typingIndicator.classList.add('typing-indicator');
        chatbotMessages.appendChild(typingIndicator);
        scrollToBottom();
        return typingIndicator;
    }

    function removeTypingIndicator(indicator) {
        if (indicator) {
            chatbotMessages.removeChild(indicator);
        }
    }

    // Haupt-Chatbot-Funktionen
    function toggleChatbot() {
        isOpen = !isOpen;
        chatbotWindow.classList.toggle('hidden');
        updateToggleButtonText();
    }

    function updateToggleButtonText() {
        chatbotToggle.textContent = isOpen ? 'Schließen' : 'Chat öffnen';
    }

    async function sendMessage() {
        const userMessage = chatbotInput.value.trim();

        if (!userMessage) return;

        if (userMessage.length > config.maxMessageLength) {
            alert(`Nachricht zu lang. Maximal ${config.maxMessageLength} Zeichen.`);
            return;
        }

        // Benutzernachricht anzeigen
        const userMessageElement = createMessageElement(userMessage, MessageType.USER);
        chatbotMessages.appendChild(userMessageElement);
        scrollToBottom();

        // Eingabefeld leeren
        chatbotInput.value = '';
        chatbotInput.disabled = true;
        chatbotSendButton.disabled = true;

        try {
            // Typing-Indikator anzeigen
            const typingIndicator = showTypingIndicator();

            // API-Aufruf für Chatbot-Antwort
            const response = await fetch(config.apiEndpoint, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCsrfToken()
                },
                body: JSON.stringify({ message: userMessage })
            });

            const data = await response.json();

            // Typing-Indikator entfernen
            removeTypingIndicator(typingIndicator);

            // Bot-Nachricht anzeigen
            const botMessageElement = createMessageElement(data.response, MessageType.BOT);
            chatbotMessages.appendChild(botMessageElement);
            scrollToBottom();
        } catch (error) {
            console.error('Chatbot-Fehler:', error);
            const errorMessage = createMessageElement('Entschuldigung, es gab ein Problem.', MessageType.SYSTEM);
            chatbotMessages.appendChild(errorMessage);
        } finally {
            chatbotInput.disabled = false;
            chatbotSendButton.disabled = false;
            chatbotInput.focus();
        }
    }

    // CSRF-Token für sichere Django-Anfragen
    function getCsrfToken() {
        const csrfTokenElement = document.querySelector('[name=csrfmiddlewaretoken]');
        return csrfTokenElement ? csrfTokenElement.value : '';
    }

    // Event-Listener
    chatbotToggle.addEventListener('click', toggleChatbot);
    chatbotSendButton.addEventListener('click', sendMessage);
    chatbotInput.addEventListener('keypress', (event) => {
        if (event.key === 'Enter') {
            sendMessage();
        }
    });

    // Initialer Zustand
    updateToggleButtonText();
});