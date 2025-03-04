const chatbotMessages = document.getElementById('chatbot-messages');
const chatbotInput = document.getElementById('chatbot-input');
const fileInput = document.getElementById('chatbot-file');
const audioPreview = document.getElementById('audio-preview');

let currentLanguage = 'ru'; // По умолчанию русский
let mediaRecorder;
let audioChunks = [];

// Функция для смены языка (будет использоваться в будущем)
function changeLanguage(lang) {
    currentLanguage = lang;
    appendMessage('bot', `Язык изменен на ${lang === 'ru' ? 'русский' : lang === 'en' ? 'английский' : 'немецкий'}.`);
}

// Функция для добавления сообщения в чат
function appendMessage(sender, message) {
    const messageElement = document.createElement('div');
    messageElement.classList.add('message', sender);
    messageElement.innerText = message;
    chatbotMessages.appendChild(messageElement);
    chatbotMessages.scrollTop = chatbotMessages.scrollHeight; // Прокрутка вниз
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

    fetch('/chatbot/', {
        method: 'POST',
        body: formData,
    })
    .then(response => response.json())
    .then(data => {
        appendMessage('bot', data.response);
    })
    .catch(error => {
        console.error('Ошибка:', error);
        appendMessage('bot', 'Произошла ошибка. Пожалуйста, попробуйте позже.');
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
                audioPreview.src = URL.createObjectURL(audioBlob); // Убрана избыточная переменная audioUrl
                audioPreview.style.display = 'block';
            };
        })
        .catch(error => {
            console.error('Ошибка доступа к микрофону:', error);
        });
}

// Функция для остановки записи аудио
function stopRecording() {
    if (mediaRecorder) {
        mediaRecorder.stop();
    }
}