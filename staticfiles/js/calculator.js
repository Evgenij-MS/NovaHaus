// Цены на услуги (€ за м²)
const prices = {
    apartment: { economy: 70, standard: 100, premium: 130 }, // Ремонт квартир
    house: { economy: 80, standard: 110, premium: 140 },     // Ремонт домов
    office: { economy: 90, standard: 120, premium: 150 },    // Ремонт офисов
    warehouse: { economy: 50, standard: 70, premium: 90 },   // Ремонт складов
    facade: { economy: 40, standard: 50, premium: 60 },      // Фасадные работы
    insulation: { economy: 45, standard: 55, premium: 65 },  // Утепление домов
    demolition: 25,                                          // Демонтажные работы
    cleaning: 8                                              // Уборка после ремонта
};

// Дополнительные услуги
const additionalServices = {
    cleaning: 8, // € за м²
    delivery: 100 // Фиксированная стоимость
};

// Функция для расчета стоимости
function calculateCost() {
    const workType = document.getElementById('work-type').value;
    const area = parseFloat(document.getElementById('area').value);
    const material = document.getElementById('material').value;
    const includeMaterials = document.getElementById('include-materials').value;
    const urgency = document.getElementById('urgency').value;
    const cleaning = document.getElementById('cleaning').checked;
    const delivery = document.getElementById('delivery').checked;

    // Расчет стоимости за м²
    let costPerSquareMeter = prices[workType][material] || prices[workType];
    if (urgency === 'fast') costPerSquareMeter *= 1.2; // Срочные работы дороже на 20%

    // Расчет стоимости материалов и работы
    let materialCost = includeMaterials === 'yes' ? area * costPerSquareMeter * 0.4 : 0;
    let laborCost = includeMaterials === 'yes' ? area * costPerSquareMeter * 0.6 : area * costPerSquareMeter;

    // Дополнительные услуги
    let additionalCost = 0;
    if (cleaning) additionalCost += area * additionalServices.cleaning;
    if (delivery) additionalCost += additionalServices.delivery;

    // Итоговая стоимость
    const totalCost = materialCost + laborCost + additionalCost;

    // Отображение результата
    document.getElementById('result').innerText = `Примерная стоимость: €${totalCost.toFixed(2)}`;

    // Показ графика
    showChart(totalCost, materialCost, laborCost);

    // Получение рекомендаций от ИИ
    getAIRecommendations(totalCost, materialCost, laborCost, workType, area);
}

// Функция для отображения графика
function showChart(totalCost, materialCost, laborCost) {
    const ctx = document.getElementById('cost-chart').getContext('2d');
    new Chart(ctx, {
        type: 'pie',
        data: {
            labels: ['Материалы', 'Работа'],
            datasets: [{
                data: [materialCost, laborCost],
                backgroundColor: ['#007bff', '#28a745'],
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    position: 'top',
                },
                title: {
                    display: true,
                    text: 'Распределение затрат',
                }
            }
        }
    });
}

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
        console.log("Sending data to server:", data); // Логируем данные

        const response = await fetch('/get-ai-recommendations/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: JSON.stringify(data)
        });

        const result = await response.json();
        console.log("Server response:", result); // Логируем ответ сервера

        if (result.success) {
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

// Функция для сохранения расчета
function saveCalculation() {
    const workType = document.getElementById('work-type').value;
    const area = document.getElementById('area').value;
    const material = document.getElementById('material').value;
    const includeMaterials = document.getElementById('include-materials').value;
    const urgency = document.getElementById('urgency').value;
    const totalCost = parseFloat(document.getElementById('result').innerText.replace('Примерная стоимость: €', ''));

    const calculation = {
        workType: workType,
        area: area,
        material: material,
        includeMaterials: includeMaterials,
        urgency: urgency,
        totalCost: totalCost,
        timestamp: new Date().toLocaleString()
    };

    fetch('/save-calculation/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
        },
        body: JSON.stringify(calculation)
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert('Расчет успешно сохранен!');
        } else {
            alert('Ошибка при сохранении расчета.');
        }
    })
    .catch(error => {
        console.error('Ошибка:', error);
        alert('Произошла ошибка. Пожалуйста, попробуйте позже.');
    });
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

// Инициализация при загрузке страницы
document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('work-type').addEventListener('change', function() {
        const workType = this.value;
        const materialGroup = document.getElementById('material-group');

        if (workType === 'demolition' || workType === 'cleaning') {
            materialGroup.style.display = 'none';
        } else {
            materialGroup.style.display = 'block';
        }
    });
});