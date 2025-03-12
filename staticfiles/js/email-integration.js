// Интеграция с CRM/почтой
function sendCalculationByEmail(email) {
    const calculation = {
        workType: document.getElementById('work-type').value,
        area: document.getElementById('area').value,
        totalCost: totalCost
    };
    fetch('/send-email/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ email, calculation })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert('Расчет отправлен на ваш email!');
        } else {
            alert('Ошибка при отправке расчета.');
        }
    });
}