const chatbotMessages = document.getElementById('chatbot-messages');
const chatbotInput = document.getElementById('chatbot-input');
const fileInput = document.getElementById('chatbot-file');
const audioPreview = document.getElementById('audio-preview');

let mediaRecorder;
let audioChunks = [];

// Функция для получения CSRF-токена
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// Функция для добавления сообщения в чат
function appendMessage(sender, message) {
    const messageElement = document.createElement('div');
    messageElement.classList.add('message', sender);
    messageElement.innerText = message;
    chatbotMessages.appendChild(messageElement);
    chatbotMessages.scrollTop = chatbotMessages.scrollHeight; // Прокрутка вниз
}

// Общая функция для отправки запросов
async function sendRequest(url, data) {
    try {
        const response = await fetch(url, {
            method: 'POST',
            body: data,
            headers: {
                'X-CSRFToken': getCookie('csrftoken')
            }
        });

        if (!response.ok) {
            throw new Error('Ошибка сети или сервера');
        }

        const result = await response.json();
        return result;
    } catch (error) {
        console.error('Ошибка:', error);
        appendMessage('bot', 'Произошла ошибка. Пожалуйста, попробуйте позже.');
        return null;
    }
}

// Функция для отправки сообщения
function sendMessage() {
    const userMessage = chatbotInput.value.trim();
    const file = fileInput.files[0];
    const audioBlob = audioChunks.length > 0 ? new Blob(audioChunks, { type: 'audio/wav' }) : null;

    if (userMessage === "" && !file && !audioBlob) return;

    const formData = new FormData();
    if (userMessage) formData.append('message', userMessage);
    if (file) formData.append('file', file);
    if (audioBlob) formData.append('audio', audioBlob, 'audio.wav');

    sendRequest('/chatbot/', formData)
        .then(data => {
            if (data && data.response) {
                appendMessage('bot', data.response);
            }
        });

    chatbotInput.value = "";
    fileInput.value = "";
    audioPreview.style.display = 'none';
    audioChunks = []; // Очистка аудио-данных
}

// Обработка нажатия Enter
chatbotInput.addEventListener('keypress', function(e) {
    if (e.key === 'Enter') {
        sendMessage();
    }
});

// Функция для начала записи аудио
function startRecording() {
    navigator.mediaDevices.getUserMedia({ audio: true })
        .then(stream => {
            mediaRecorder = new MediaRecorder(stream);
            mediaRecorder.start();

            mediaRecorder.ondataavailable = event => {
                audioChunks.push(event.data);
            };

            mediaRecorder.onstop = () => {
                const audioBlob = new Blob(audioChunks, { type: 'audio/wav' });
                audioPreview.src = URL.createObjectURL(audioBlob);
                audioPreview.style.display = 'block';
            };
        })
        .catch(error => {
            console.error('Ошибка доступа к микрофону:', error);
            appendMessage('bot', 'Не удалось получить доступ к микрофону.');
        });
}

// Функция для остановки записи аудио
function stopRecording() {
    if (mediaRecorder) {
        mediaRecorder.stop();
    }
}