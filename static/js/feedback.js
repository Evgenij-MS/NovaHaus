async function sendFeedback() {
    const name = document.getElementById('feedback-name').value;
    const email = document.getElementById('feedback-email').value;
    const message = document.getElementById('feedback-message').value;

    try {
        const response = await fetch('/send-feedback/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCSRFToken()
            },
            body: JSON.stringify({ name, email, message })
        });
        const data = await response.json();
        if (data.success) {
            alert('Спасибо за ваш отзыв!');
        } else {
            alert('Ошибка при отправке отзыва.');
        }
    } catch (error) {
        alert('Ошибка при отправке. Попробуйте снова.');
        console.error('Ошибка:', error);
    }
}

document.getElementById('submit-feedback')?.addEventListener('click', sendFeedback);