const chatbotMessages = document.getElementById('chatbot-messages');
const chatbotInput = document.getElementById('chatbot-input');

// Функция для отправки сообщения
function sendMessage() {
    const userMessage = chatbotInput.value.trim();
    if (userMessage === "") return;

    // Добавляем сообщение пользователя в чат
    appendMessage('user', userMessage);
    chatbotInput.value = "";

    // Отправляем сообщение на сервер для обработки AI
    fetch('/chatbot/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ message: userMessage }),
    })
    .then(response => response.json())
    .then(data => {
        // Добавляем ответ AI в чат
        appendMessage('bot', data.response);
    })
    .catch(error => {
        console.error('Ошибка:', error);
        appendMessage('bot', 'Произошла ошибка. Пожалуйста, попробуйте позже.');
    });
}

// Функция для добавления сообщения в чат
function appendMessage(sender, message) {
    const messageElement = document.createElement('div');
    messageElement.classList.add('message', sender);
    messageElement.innerText = message;
    chatbotMessages.appendChild(messageElement);
    chatbotMessages.scrollTop = chatbotMessages.scrollHeight; // Прокрутка вниз
}

// Обработка нажатия Enter
chatbotInput.addEventListener('keypress', function(e) {
    if (e.key === 'Enter') {
        sendMessage();
    }
});