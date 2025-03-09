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
        const response = await fetch('/get-ai-recommendations/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken') // Для защиты от CSRF
            },
            body: JSON.stringify(data)
        });

        const result = await response.json();

        if (result.success) {
            // Отображаем рекомендации на странице
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