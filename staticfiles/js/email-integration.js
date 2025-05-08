// Интеграция с CRM/почтой
function getCSRFToken() {
    const match = document.cookie.match(/(^|;)\s*csrftoken=([^;]+)/);
    return match ? match[2] : null;
}

async function sendCalculationByEmail(email) {
    const totalCost = parseFloat(document.getElementById('result').innerText.match(/[\d,.]+/)?.[0]?.replace(',', '.') || 0);
    const calculation = {
        workType: document.getElementById('work-type').value,
        area: document.getElementById('area').value,
        totalCost: totalCost
    };
    try {
        const response = await fetch('/send-email/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCSRFToken()
            },
            body: JSON.stringify({ email, calculation })
        });
        const data = await response.json();
        if (data.success) {
            alert('Расчет отправлен на ваш email!');
        } else {
            alert('Ошибка при отправке расчета.');
        }
    } catch (error) {
        alert('Ошибка при отправке. Попробуйте снова.');
        console.error('Ошибка:', error);
    }
}

document.getElementById('send-email-button')?.addEventListener('click', () => {
    const email = prompt('Введите ваш email:');
    if (email) sendCalculationByEmail(email);
});