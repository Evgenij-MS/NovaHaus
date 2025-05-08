/* global Chart */
function getCSRFToken() {
    const match = document.cookie.match(/(^|;)\s*csrftoken=([^;]+)/);
    return match ? match[2] : null;
}

function formatCurrency(amount, locale = navigator.language || 'de-DE') {
    return new Intl.NumberFormat(locale, { style: 'currency', currency: 'EUR' }).format(amount);
}

async function calculateCost(event) {
    event.preventDefault();
    const form = document.getElementById('calculator-form');
    const resultElement = document.getElementById('result');
    const formData = new FormData(form);
    const csrfToken = getCSRFToken();

    try {
        const response = await fetch('/calculate_cost/', {
            method: 'POST',
            headers: { 'X-CSRFToken': csrfToken },
            body: formData
        });
        const data = await response.json();
        if (data.success) {
            resultElement.innerText = `Примерная стоимость: ${formatCurrency(data.total_cost)}`;
            resultElement.style.color = 'black';
            showChart(data.total_cost, data.material_cost, data.labor_cost);
            await getAIRecommendations(data);
        } else {
            resultElement.innerText = `Ошибка: ${data.error}`;
            resultElement.style.color = 'red';
        }
    } catch (error) {
        resultElement.innerText = 'Ошибка при расчете. Попробуйте снова.';
        resultElement.style.color = 'red';
        console.error('Ошибка:', error);
    }
}

function showChart(totalCost, materialCost, laborCost) {
    const chartElement = document.getElementById('cost-chart');
    if (!chartElement) {
        console.error('Элемент #cost-chart не найден.');
        return;
    }
    const ctx = chartElement.getContext('2d');
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
                    legend: { position: 'top' },
                    title: { display: true, text: 'Распределение затрат' }
                }
            }
        });
    }
}

async function getAIRecommendations(data) {
    const recommendationElement = document.getElementById('ai-recommendation-text');
    try {
        const response = await fetch('/get-ai-recommendations/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCSRFToken()
            },
            body: JSON.stringify({
                totalCost: data.total_cost,
                materialCost: data.material_cost,
                laborCost: data.labor_cost,
                workType: String(data.work_type), // Преобразование в строку
                area: data.area,
                language: navigator.language.split('-')[0] || 'de'
            })
        });
        const result = await response.json();
        if (result.success) {
            recommendationElement.innerText = result.recommendation;
        } else {
            recommendationElement.innerText = 'Не удалось получить рекомендации.';
        }
    } catch (error) {
        recommendationElement.innerText = 'Ошибка при получении рекомендаций.';
        console.error('Ошибка AI:', error);
    }
}

async function saveCalculation() {
    const form = document.getElementById('calculator-form');
    const formData = new FormData(form);
    const data = {
        workType: String(formData.get('work-type')), // Преобразование в строку
        area: parseFloat(formData.get('area')),
        material: String(formData.get('material-quality')), // Преобразование в строку
        totalCost: parseFloat(document.getElementById('result').innerText.match(/[\d,.]+/)?.[0]?.replace(',', '.')) || 0,
        materialCost: parseFloat(document.getElementById('result').dataset.materialCost || 0),
        laborCost: parseFloat(document.getElementById('result').dataset.laborCost || 0),
        timestamp: new Date().toLocaleString()
    };
    const csrfToken = getCSRFToken();

    try {
        const response = await fetch('/save-calculation/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken
            },
            body: JSON.stringify(data)
        });
        const result = await response.json();
        if (result.success) {
            alert('Расчет успешно сохранен!');
        } else {
            alert('Ошибка при сохранении расчета.');
        }
    } catch (error) {
        alert('Ошибка при сохранении. Попробуйте снова.');
        console.error('Ошибка:', error);
    }
}

document.getElementById('calculator-form').addEventListener('submit', calculateCost);
document.getElementById('save-button').addEventListener('click', saveCalculation);