

function saveCalculation(totalCost, materialCost, laborCost) {
    const calculation = {
        workType: document.getElementById('work-type').value,
        area: document.getElementById('area').value,
        material: document.getElementById('material').value,
        includeMaterials: document.getElementById('include-materials').value,
        urgency: document.getElementById('urgency').value,
        totalCost: totalCost,
        materialCost: materialCost,
        laborCost: laborCost,
        timestamp: new Date().toLocaleString()
    };

    // Отправляем данные на сервер
    fetch('/save-calculation/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken') // Для защиты от CSRF
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


// Цены на дополнительные услуги
const additionalServices = {
    cleaning: 8, // € за м²
    delivery: 100 // Фиксированная стоимость
};


function calculateCost() {
    const workType = document.getElementById('work-type').value;
    const area = parseFloat(document.getElementById('area').value);
    const material = document.getElementById('material').value;
    const includeMaterials = document.getElementById('include-materials').value;
    const urgency = document.getElementById('urgency').value;
    const cleaning = document.getElementById('cleaning').checked;
    const delivery = document.getElementById('delivery').checked;

    let costPerSquareMeter;

    if (workType === 'demolition' || workType === 'cleaning') {
        costPerSquareMeter = prices[workType];
    } else {
        costPerSquareMeter = prices[workType][material];
    }

    if (urgency === 'fast') {
        costPerSquareMeter *= 1.2;
    }

    let materialCost = 0;
    let laborCost = 0;

    if (includeMaterials === 'yes') {
        materialCost = area * costPerSquareMeter * 0.4; // 40% на материалы
        laborCost = area * costPerSquareMeter * 0.6;   // 60% на работу
    } else {
        laborCost = area * costPerSquareMeter; // Только работа
    }

    let additionalCost = 0;
    if (cleaning) additionalCost += area * additionalServices.cleaning;
    if (delivery) additionalCost += additionalServices.delivery;

    const totalCost = materialCost + laborCost + additionalCost;

    // Отображаем результат
    document.getElementById('result').innerText = `Примерная стоимость: €${totalCost.toFixed(2)}`;

    // Показываем график
    showChart(totalCost, materialCost, laborCost, additionalCost);
}

// Средние цены на услуги в Кельне (€ за м²)
const prices = {
    apartment: { economy: 70, standard: 100, premium: 130 }, // Ремонт квартир
    house: { economy: 80, standard: 110, premium: 140 },     // Ремонт домов
    office: { economy: 90, standard: 120, premium: 150 },    // Ремонт офисов
    warehouse: { economy: 50, standard: 70, premium: 90 },   // Ремонт складов
    facade: { economy: 40, standard: 50, premium: 60 },      // Фасадные работы
    insulation: { economy: 45, standard: 55, premium: 65 },  // Утепление домов
    demolition: 25,                                          // Демонтажные работы (фиксированная цена за м²)
    cleaning: 8                                              // Уборка после ремонта (фиксированная цена за м²)
};

// Коэффициенты для стоимости без материалов
const materialCostRatio = 0.6; // 60% от общей стоимости (40% — материалы, 60% — работа)

// Описания для площади
const areaDescriptions = {
    apartment: "Введите общую площадь стен, потолков и пола.",
    house: "Введите общую площадь стен, потолков и пола.",
    office: "Введите общую площадь стен, потолков и пола.",
    warehouse: "Введите общую площадь стен, потолков и пола.",
    facade: "Введите площадь фасада.",
    insulation: "Введите площадь утепляемых поверхностей (стены, кровля, фундамент).",
    demolition: "Введите площадь демонтируемых конструкций.",
    cleaning: "Введите общую площадь уборки."
};

// Обновление описания площади при выборе типа работ
function updateAreaDescription() {
    const workType = document.getElementById('work-type').value;
    document.getElementById('area-description').innerText = areaDescriptions[workType];
}



// Скрываем выбор материала для демонтажа и уборки
document.getElementById('work-type').addEventListener('change', function() {
    const workType = this.value;
    const materialGroup = document.getElementById('material-group');

    if (workType === 'demolition' || workType === 'cleaning') {
        materialGroup.style.display = 'none';
    } else {
        materialGroup.style.display = 'block';
    }
});

// Инициализация при загрузке страницы
updateAreaDescription();