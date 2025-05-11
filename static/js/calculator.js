/* global Chart */
const modelMap = {
    'apartment': {
        'economy': '/static/models/apartment_economy.glb',
        'standard': '/static/models/apartment_standard.glb',
        'premium': '/static/models/apartment_premium.glb'
    },
    'house': {
        'economy': '/static/models/house_economy.glb',
        'standard': '/static/models/house_standard.glb',
        'premium': '/static/models/house_premium.glb'
    },
    'office': {
        'economy': '/static/models/office_economy.glb',
        'standard': '/static/models/office_standard.glb',
        'premium': '/static/models/office_premium.glb'
    },
    'warehouse': {
        'economy': '/static/models/warehouse_economy.glb',
        'standard': '/static/models/warehouse_standard.glb',
        'premium': '/static/models/warehouse_premium.glb'
    },
    'facade': {
        'economy': '/static/models/facade_economy.glb',
        'standard': '/static/models/facade_standard.glb',
        'premium': '/static/models/facade_premium.glb'
    },
    'bathroom': {
        'economy': '/static/models/bathroom_economy.glb',
        'standard': '/static/models/bathroom_standard.glb',
        'premium': '/static/models/bathroom_premium.glb'
    }
};

function formatCurrency(amount, locale = navigator.language || 'de-DE') {
    return new Intl.NumberFormat(locale, { style: 'currency', currency: 'EUR' }).format(amount);
}

async function fetchData(url, options) {
    try {
        const response = await fetch(url, options);
        if (!response.ok) {
            console.error(`HTTP error! Status: ${response.status}`);
            return null;
        }
        return await response.json();
    } catch (error) {
        console.error(`Ошибка при запросе к ${url}:`, error);
        return null;
    }
}

async function calculateCost(event) {
    event.preventDefault();
    const form = document.getElementById('calculator-form');
    const resultElement = document.getElementById('result');
    const recommendationElement = document.getElementById('ai-recommendation-text');
    if (!form || !resultElement || !recommendationElement) return;

    const formData = new FormData(form);
    const csrfToken = getCSRFToken();

    const costData = await fetchData('/calculate_cost/', {
        method: 'POST',
        headers: { 'X-CSRFToken': csrfToken },
        body: formData
    });
    console.log('Ответ calculate_cost:', costData);

    if (!costData || !costData.success) {
        resultElement.innerText = `Ошибка: ${costData?.error || 'Неизвестная ошибка'}`;
        resultElement.style.color = 'red';
        return;
    }

    const laborCost = costData.labor_cost || 0;
    const workType = String(formData.get('work-type') || '');
    const area = parseFloat(formData.get('area') || '0');
    const materialQuality = String(formData.get('material-quality') || 'standard');

    const aiData = await fetchData('/get-ai-recommendations/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken
        },
        body: JSON.stringify({
            laborCost,
            workType,
            area,
            materialQuality,
            language: navigator.language.split('-')[0] || 'de'
        })
    });
    console.log('Ответ get-ai-recommendations:', aiData);

    const recommendation = aiData?.recommendation || 'Нет рекомендаций';
    const materialCost = aiData?.material_cost || 0;

    if (aiData?.success) {
        recommendationElement.innerText = recommendation;
    } else {
        recommendationElement.innerText = `Ошибка: ${aiData?.error || 'Неизвестная ошибка'}`;
    }

    const totalCost = laborCost + materialCost;

    resultElement.innerText = `Примерная стоимость: ${formatCurrency(totalCost)}`;
    resultElement.style.color = 'black';
    resultElement.dataset.materialCost = materialCost.toString();
    resultElement.dataset.laborCost = laborCost.toString();

    showChart(totalCost, materialCost, laborCost);
    show3DModel(workType, materialQuality);
    saveCalculation(totalCost, materialCost, laborCost);
}

function show3DModel(workType, materialQuality) {
    const viewer = document.getElementById('viewer');
    if (!viewer) {
        console.error('Элемент #viewer не найден.');
        return;
    }
    const modelUrl = modelMap[workType]?.[materialQuality] || '/static/models/sample_model.glb';
    viewer.setAttribute('src', modelUrl);
    viewer.style.display = 'block';
    console.log('Загружена модель:', modelUrl);
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
                    backgroundColor: ['#007bff', '#28a745']
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
    const resultElement = document.getElementById('result');
    if (!form || !resultElement) return;

    const formData = new FormData(form);
    const csrfToken = getCSRFToken();
    const data = {
        workType: String(formData.get('work-type') || ''),
        area: parseFloat(formData.get('area') || '0'),
        material: String(formData.get('material-quality') || ''),
        totalCost: parseFloat(resultElement.innerText.match(/[\d,.]+/)?.[0]?.replace(',', '.') || '0'),
        materialCost: parseFloat(resultElement.dataset.materialCost || '0'),
        laborCost: parseFloat(resultElement.dataset.laborCost || '0'),
        timestamp: new Date().toLocaleString()
    };

    const result = await fetchData('/save-calculation/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken
        },
        body: JSON.stringify(data)
    });

    alert(result?.success ? 'Расчет успешно сохранен!' : 'Ошибка при сохранении расчета.');
}

document.getElementById('calculator-form')?.addEventListener('submit', calculateCost);
document.getElementById('save-button')?.addEventListener('click', saveCalculation);