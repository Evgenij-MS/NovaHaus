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

    // Валидация ввода
    if (isNaN(area) || area <= 0) {
        alert("Пожалуйста, введите корректную площадь.");
        return;
    }

    // Расчет стоимости за м²
    let costPerSquareMeter = prices[workType][material] || prices[workType];
    if (urgency === 'fast') costPerSquareMeter *= 1.2; // Срочные работы дороже на 20%

    // Расчет стоимости материалов и работы
    const materialPercentage = 0.4; // 40% на материалы
    const laborPercentage = 0.6;    // 60% на работу
    let materialCost = includeMaterials === 'yes' ? area * costPerSquareMeter * materialPercentage : 0;
    let laborCost = includeMaterials === 'yes' ? area * costPerSquareMeter * laborPercentage : area * costPerSquareMeter;

    // Дополнительные услуги
    let additionalCost = 0;
    if (cleaning) additionalCost += area * additionalServices.cleaning;
    if (delivery) additionalCost += additionalServices.delivery;

    // Итоговая стоимость
    const totalCost = materialCost + laborCost + additionalCost;

    // Отображение результата
    const resultElement = document.getElementById('result');
    if (resultElement) {
        resultElement.innerText = `Примерная стоимость: €${totalCost.toFixed(2)}`;
    }

    // Показ графика
    showChart(totalCost, materialCost, laborCost);

    // Получение рекомендаций от ИИ
    getAIRecommendations(totalCost, materialCost, laborCost, workType, area)
        .catch(error => console.error('Ошибка при получении рекомендаций:', error));
}

// Функция для отображения графика
function showChart(totalCost, materialCost, laborCost) {
    const ctx = document.getElementById('cost-chart')?.getContext('2d');
    if (ctx) {
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

    // Отправка данных на сервер
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