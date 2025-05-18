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

const calculationCache = new Map();

function formatCurrency(amount, locale = navigator.language || 'de-DE') {
    return new Intl.NumberFormat(locale, { style: 'currency', currency: 'EUR' }).format(amount);
}

async function fetchData(url, options) {
    try {
        const response = await fetch(url, options);
        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }
        return await response.json();
    } catch (error) {
        console.error(`Ошибка при запросе к ${url}:`, error);
        return { success: false, error: error.message };
    }
}

function debounce(func, wait) {
    let timeout;
    return function (...args) {
        clearTimeout(timeout);
        timeout = setTimeout(() => func.apply(this, args), wait);
    };
}

async function calculateCost(event) {
    event.preventDefault();
    const form = document.getElementById('calculator-form');
    const resultElement = document.getElementById('result');
    const recommendationElement = document.getElementById('ai-recommendation-text');
    const loader = document.getElementById('loader');

    if (!form || !resultElement || !recommendationElement || !loader) return;

    try {
        const csrfToken = getCSRFToken();
        const formData = new FormData(form);
        const area = parseFloat(formData.get('area') || '0');
        const workType = formData.get('work-type');
        const materialQuality = formData.get('material-quality');

        if (!workType || !materialQuality || area <= 0 || isNaN(area)) {
            resultElement.innerText = 'Ошибка: Пожалуйста, заполните все поля корректными значениями.';
            resultElement.style.color = 'red';
            return;
        }

        const cacheKey = `${workType}-${area}-${materialQuality}`;
        if (calculationCache.has(cacheKey)) {
            const cached = calculationCache.get(cacheKey);
            updateUI(cached.costData, cached.aiData, workType, materialQuality);
            return;
        }

        loader.style.display = 'block';

        const costData = await fetchData('/calculate_cost/', {
            method: 'POST',
            headers: { 'X-CSRFToken': csrfToken },
            body: formData
        });

        if (!costData.success) {
            resultElement.innerText = `Ошибка: ${costData.error || 'Неизвестная ошибка'}`;
            resultElement.style.color = 'red';
            loader.style.display = 'none';
            return;
        }

        const laborCost = costData.labor_cost || 0;
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

        if (!aiData.success) {
            recommendationElement.innerText = `Ошибка: ${aiData.error || 'Неизвестная ошибка'}`;
        } else {
            recommendationElement.innerText = aiData.recommendation || 'Нет рекомендаций';
        }

        calculationCache.set(cacheKey, { costData, aiData });
        updateUI(costData, aiData, workType, materialQuality);
    } catch (error) {
        console.error(error);
        resultElement.innerText = 'Ошибка: ' + error.message;
        resultElement.style.color = 'red';
    } finally {
        loader.style.display = 'none';
    }
}

function updateUI(costData, aiData, workType, materialQuality) {
    const resultElement = document.getElementById('result');
    const recommendationElement = document.getElementById('ai-recommendation-text');
    const laborCost = costData.labor_cost || 0;
    const materialCost = aiData?.material_cost || 0;
    const totalCost = laborCost + materialCost;

    resultElement.innerText = `Примерная стоимость: ${formatCurrency(totalCost)}`;
    resultElement.style.color = 'black';
    resultElement.dataset.materialCost = materialCost.toString();
    resultElement.dataset.laborCost = laborCost.toString();

    recommendationElement.innerText = aiData?.recommendation || 'Нет рекомендаций';

    showChart(totalCost, materialCost, laborCost);
    show3DModel(workType, materialQuality);
}

function show3DModel(workType, materialQuality) {
    const viewer = document.getElementById('viewer');
    if (!viewer) {
        console.error('Элемент #viewer не найден.');
        return;
    }
    const modelUrl = modelMap[workType]?.[materialQuality] || '/static/models/sample_model.glb';
    viewer.setAttribute('src', modelUrl);
    viewer.setAttribute('loading', 'lazy');
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

    try {
        const csrfToken = getCSRFToken();
        const formData = new FormData(form);
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
    } catch (error) {
        console.error(error);
        alert('Ошибка: ' + error.message);
    }
}

document.getElementById('calculator-form')?.addEventListener('submit', debounce(calculateCost, 300));
document.getElementById('save-button')?.addEventListener('click', saveCalculation);