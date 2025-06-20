// Chatbot JavaScript
class ChatBot {
    constructor() {
        this.init();
        this.csrfToken = window.csrfToken || document.querySelector('[name=csrfmiddlewaretoken]').value;
        this.isRecording = false;
        this.mediaRecorder = null;
        this.audioChunks = [];
        this.recordedBlob = null;
    }

    init() {
        this.bindEvents();
        this.loadChatHistory();
    }

    bindEvents() {
        // Form submission
        const form = document.getElementById('chatbotForm');
        if (form) {
            form.addEventListener('submit', (e) => this.handleFormSubmit(e));
        }

        // Close button
        const closeBtn = document.querySelector('.chatbot-close');
        if (closeBtn) {
            closeBtn.addEventListener('click', () => this.closeChatbot());
        }

        // Record button
        const recordBtn = document.querySelector('.record-button');
        if (recordBtn) {
            recordBtn.addEventListener('click', () => this.toggleRecording());
        }

        // Recording controls
        const stopBtn = document.querySelector('.stop-recording');
        const playBtn = document.querySelector('.play-recording');
        const cancelBtn = document.querySelector('.cancel-recording');

        if (stopBtn) stopBtn.addEventListener('click', () => this.stopRecording());
        if (playBtn) playBtn.addEventListener('click', () => this.playRecording());
        if (cancelBtn) cancelBtn.addEventListener('click', () => this.cancelRecording());

        // File input change
        const fileInput = document.getElementById('chatbot-file');
        if (fileInput) {
            fileInput.addEventListener('change', (e) => this.handleFileSelect(e));
        }

        // Auto-resize textarea
        const textarea = document.getElementById('chatbot-message');
        if (textarea) {
            textarea.addEventListener('input', () => this.autoResizeTextarea(textarea));
        }

        // Enter key submission (Ctrl+Enter)
        if (textarea) {
            textarea.addEventListener('keydown', (e) => {
                if (e.ctrlKey && e.key === 'Enter') {
                    e.preventDefault();
                    form.dispatchEvent(new Event('submit'));
                }
            });
        }
    }

    handleFormSubmit(e) {
        e.preventDefault();

        const form = e.target;
        const formData = new FormData(form);
        const message = formData.get('message')?.trim();

        // Client-side validation
        if (!this.validateForm(message)) {
            return;
        }

        // Add recorded audio if available
        if (this.recordedBlob) {
            formData.append('audio', this.recordedBlob, 'recording.wav');
        }

        this.sendMessage(formData);
        this.clearForm();
    }

    validateForm(message) {
        const errorContainer = document.getElementById('formErrors');
        let errors = [];

        // Check message
        if (!message) {
            errors.push('Пожалуйста, введите сообщение.');
        } else if (message.length > 1000) {
            errors.push('Сообщение не может быть длиннее 1000 символов.');
        }

        // Check file
        const fileInput = document.getElementById('chatbot-file');
        if (fileInput.files.length > 0) {
            const file = fileInput.files[0];
            const maxSize = 5 * 1024 * 1024; // 5MB
            const allowedTypes = ['image/jpeg', 'image/jpg', 'image/png', 'application/pdf'];

            if (file.size > maxSize) {
                errors.push('Размер файла не должен превышать 5MB.');
            }

            if (!allowedTypes.includes(file.type)) {
                errors.push('Разрешены только файлы JPG, PNG и PDF.');
            }
        }

        if (errors.length > 0) {
            this.showErrors(errors);
            return false;
        }

        this.hideErrors();
        return true;
    }

    async sendMessage(formData) {
        this.showLoading(true);

        try {
            const response = await fetch(window.location.href, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': this.csrfToken,
                },
                body: formData
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const data = await response.json();

            if (data.success) {
                this.addMessageToChat(data.user_message, 'user');
                if (data.bot_response) {
                    this.addMessageToChat(data.bot_response, 'bot');
                }
                this.scrollToBottom();
            } else {
                this.showErrors(data.errors || ['Произошла ошибка при отправке сообщения.']);
            }

        } catch (error) {
            console.error('Error sending message:', error);
            this.showErrors(['Ошибка соединения. Попробуйте еще раз.']);
        } finally {
            this.showLoading(false);
        }
    }

    addMessageToChat(message, type) {
        const messagesContainer = document.querySelector('.chatbot-messages');
        const messageDiv = document.createElement('div');
        messageDiv.className = `message message-${type}`;

        const timestamp = new Date().toLocaleTimeString('ru-RU', {
            hour: '2-digit',
            minute: '2-digit'
        });

        messageDiv.innerHTML = `
            <div class="message-content">
                <div class="message-text">${this.escapeHtml(message)}</div>
                <div class="message-time">${timestamp}</div>
            </div>
        `;

        messagesContainer.appendChild(messageDiv);
        this.scrollToBottom();
    }

    escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }

    clearForm() {
        const form = document.getElementById('chatbotForm');
        const textarea = document.getElementById('chatbot-message');
        const fileInput = document.getElementById('chatbot-file');

        if (textarea) {
            textarea.value = '';
            this.autoResizeTextarea(textarea);
        }

        if (fileInput) {
            fileInput.value = '';
        }

        // Clear recorded audio
        this.recordedBlob = null;
        this.hideRecordingControls();
    }

    showLoading(show) {
        const loadingIndicator = document.getElementById('loadingIndicator');
        const sendButton = document.querySelector('.send-button');

        if (loadingIndicator) {
            loadingIndicator.style.display = show ? 'block' : 'none';
        }

        if (sendButton) {
            sendButton.disabled = show;
            sendButton.textContent = show ? 'Отправка...' : 'Отправить';
        }
    }

    showErrors(errors) {
        const errorContainer = document.getElementById('formErrors');
        if (errorContainer) {
            errorContainer.innerHTML = errors.map(error =>
                `<div class="alert alert-danger">${this.escapeHtml(error)}</div>`
            ).join('');
            errorContainer.style.display = 'block';
        }
    }

    hideErrors() {
        const errorContainer = document.getElementById('formErrors');
        if (errorContainer) {
            errorContainer.style.display = 'none';
            errorContainer.innerHTML = '';
        }
    }

    scrollToBottom() {
        const messagesContainer = document.querySelector('.chatbot-messages');
        if (messagesContainer) {
            messagesContainer.scrollTop = messagesContainer.scrollHeight;
        }
    }

    autoResizeTextarea(textarea) {
        textarea.style.height = 'auto';
        textarea.style.height = Math.min(textarea.scrollHeight, 150) + 'px';
    }

    closeChatbot() {
        const container = document.querySelector('.chatbot-container');
        if (container) {
            container.style.display = 'none';
        }
    }

    // Audio recording methods
    async toggleRecording() {
        if (this.isRecording) {
            this.stopRecording();
        } else {
            await this.startRecording();
        }
    }

    async startRecording() {
        try {
            const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
            this.mediaRecorder = new MediaRecorder(stream);
            this.audioChunks = [];

            this.mediaRecorder.ondataavailable = (event) => {
                this.audioChunks.push(event.data);
            };

            this.mediaRecorder.onstop = () => {
                this.recordedBlob = new Blob(this.audioChunks, { type: 'audio/wav' });
                this.showRecordingControls();
                stream.getTracks().forEach(track => track.stop());
            };

            this.mediaRecorder.start();
            this.isRecording = true;
            this.updateRecordButton();

        } catch (error) {
            console.error('Error starting recording:', error);
            this.showErrors(['Не удалось получить доступ к микрофону.']);
        }
    }

    stopRecording() {
        if (this.mediaRecorder && this.isRecording) {
            this.mediaRecorder.stop();
            this.isRecording = false;
            this.updateRecordButton();
        }
    }

    playRecording() {
        if (this.recordedBlob) {
            const audio = new Audio(URL.createObjectURL(this.recordedBlob));
            audio.play().catch(error => {
                console.error('Error playing audio:', error);
                this.showErrors(['Не удалось воспроизвести запись.']);
            });
        }
    }

    cancelRecording() {
        this.recordedBlob = null;
        this.hideRecordingControls();
    }

    updateRecordButton() {
        const recordBtn = document.querySelector('.record-button');
        if (recordBtn) {
            recordBtn.classList.toggle('recording', this.isRecording);
            recordBtn.setAttribute('aria-label',
                this.isRecording ? 'Остановить запись' : 'Записать голосовое сообщение'
            );
        }
    }

    showRecordingControls() {
        const controls = document.querySelector('.recording-controls');
        if (controls) {
            controls.style.display = 'block';
        }
    }

    hideRecordingControls() {
        const controls = document.querySelector('.recording-controls');
        if (controls) {
            controls.style.display = 'none';
        }
    }

    handleFileSelect(e) {
        const file = e.target.files[0];
        if (file) {
            // Show file info
            const fileName = file.name;
            const fileSize = (file.size / 1024 / 1024).toFixed(2);
            console.log(`Selected file: ${fileName} (${fileSize} MB)`);
        }
    }

    loadChatHistory() {
        // Load chat history from localStorage or server
        const savedMessages = localStorage.getItem('chatbot_messages');
        if (savedMessages) {
            try {
                const messages = JSON.parse(savedMessages);
                messages.forEach(msg => {
                    this.addMessageToChat(msg.text, msg.type);
                });
            } catch (error) {
                console.error('Error loading chat history:', error);
            }
        }
    }

    saveChatHistory(message, type) {
        try {
            const savedMessages = JSON.parse(localStorage.getItem('chatbot_messages') || '[]');
            savedMessages.push({ text: message, type: type, timestamp: Date.now() });

            // Keep only last 50 messages
            if (savedMessages.length > 50) {
                savedMessages.splice(0, savedMessages.length - 50);
            }

            localStorage.setItem('chatbot_messages', JSON.stringify(savedMessages));
        } catch (error) {
            console.error('Error saving chat history:', error);
        }
    }
}

// Initialize chatbot when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    window.chatbot = new ChatBot();
});

// Export for module usage
if (typeof module !== 'undefined' && module.exports) {
    module.exports = ChatBot;
}