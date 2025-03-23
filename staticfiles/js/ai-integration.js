// Функция для получения рекомендаций от ИИ
async function getAIRecommendations(totalCost, materialCost, laborCost, workType, area) {
    const data = {
        totalCost: totalCost,
        materialCost: materialCost,
        laborCost: laborCost,
        workType: workType,
        area: area
    };

    try {
        console.log("Отправка данных на сервер:", data); // Логирование данных

        const response = await fetch('/get-ai-recommendations/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken') // Получение CSRF-токена
            },
            body: JSON.stringify(data)  // Используем переменную data
        });

        const result = await response.json();
        console.log("Ответ сервера:", result); // Логирование ответа сервера

        if (result.success && result.recommendation) {
            document.getElementById('ai-recommendation-text').innerText = result.recommendation;
        } else {
            console.error('Ошибка при получении рекомендаций:', result.error);
            document.getElementById('ai-recommendation-text').innerText = 'Не удалось получить рекомендации. Попробуйте позже.';
        }
    } catch (error) {
        console.error('Ошибка:', error);
        document.getElementById('ai-recommendation-text').innerText = 'Произошла ошибка. Пожалуйста, попробуйте позже.';
    }
}

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

// Пример вызова функции getAIRecommendations
document.addEventListener('DOMContentLoaded', () => {
    const calculateButton = document.getElementById('calculate-button');
    if (calculateButton) {
        calculateButton.addEventListener('click', async () => {
            const totalCost = parseFloat(document.getElementById('total-cost').value);
            const materialCost = parseFloat(document.getElementById('material-cost').value);
            const laborCost = parseFloat(document.getElementById('labor-cost').value);
            const workType = document.getElementById('work-type').value;
            const area = parseFloat(document.getElementById('area').value);

            await getAIRecommendations(totalCost, materialCost, laborCost, workType, area);
        });
    }
});