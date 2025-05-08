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
        // Запрос трудовых затрат
        // @ts-ignore
        const costResponse = await fetch('/calculate_cost/', {
            method: 'POST',
            headers: { 'X-CSRFToken': csrfToken },
            body: formData
        });
        const costData = await costResponse.json();
        console.log('Ответ calculate_cost:', costData);

        if (!costData.success) {
            resultElement.innerText = `Ошибка: ${costData.error}`;
            resultElement.style.color = 'red';
            return;
        }

        const laborCost = costData.labor_cost || 0;
        const workType = costData.work_type || '';
        const area = costData.area || 0;
        const materialQuality = formData.get('material-quality') || 'standard';

        // Запрос материальных затрат и рекомендаций
        // @ts-ignore
        const aiResponse = await fetch('/get-ai-recommendations/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken
            },
            body: JSON.stringify({
                laborCost: laborCost,
                workType: workType,
                area: area,
                materialQuality: materialQuality,
                language: navigator.language.split('-')[0] || 'de'
            })
        });
        const aiData = await aiResponse.json();
        console.log('Ответ get-ai-recommendations:', aiData);

        const recommendationElement = document.getElementById('ai-recommendation-text');
        if (aiData.success) {
            recommendationElement.innerText = aiData.recommendation || 'Нет рекомендаций';
        } else {
            recommendationElement.innerText = `Ошибка: ${aiData.error}`;
        }

        const materialCost = aiData.material_cost || 0;
        const totalCost = laborCost + materialCost;

        // Отображение результата
        resultElement.innerText = `Примерная стоимость: ${formatCurrency(totalCost)}`;
        resultElement.style.color = 'black';
        resultElement.dataset.materialCost = materialCost;
        resultElement.dataset.laborCost = laborCost;

        // Обновление диаграммы
        showChart(totalCost, materialCost, laborCost);
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

async function saveCalculation() {
    const form = document.getElementById('calculator-form');
    const formData = new FormData(form);
    const resultElement = document.getElementById('result');
    const data = {
        workType: String(formData.get('work-type') || ''),
        area: parseFloat(formData.get('area')) || 0,
        material: String(formData.get('material-quality') || ''),
        totalCost: parseFloat(resultElement.innerText.match(/[\d,.]+/)?.[0]?.replace(',', '.')) || 0,
        materialCost: parseFloat(resultElement.dataset.materialCost || 0),
        laborCost: parseFloat(resultElement.dataset.laborCost || 0),
        timestamp: new Date().toLocaleString()
    };
    const csrfToken = getCSRFToken();

    try {
        // @ts-ignore
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