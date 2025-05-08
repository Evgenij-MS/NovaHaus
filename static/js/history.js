// Функция для сохранения расчета в локальном хранилище
function saveCalculation(totalCost, materialCost, laborCost) {
    const calculation = {
        workType: document.getElementById('work-type').value,
        area: document.getElementById('area').value,
        totalCost,
        materialCost,
        laborCost,
        timestamp: new Date().toLocaleString()
    };
    const history = JSON.parse(localStorage.getItem('calculationHistory')) || [];
    history.push(calculation);
    localStorage.setItem('calculationHistory', JSON.stringify(history));
}

// Функция для отображения истории расчетов
function showHistory() {
    const history = JSON.parse(localStorage.getItem('calculationHistory')) || [];
    const content = history.map((calc, index) => `
        <div class="history-item">
            <h3>Расчет #${index + 1}</h3>
            <p>Тип работ: ${calc.workType}</p>
            <p>Площадь: ${calc.area} м²</p>
            <p>Общая стоимость: €${calc.totalCost.toFixed(2)}</p>
            <p>Дата: ${calc.timestamp}</p>
        </div>
    `).join('');
    openModal(`<h2>История расчетов</h2>${content}`);
}

// Привязка к кнопке для отображения истории
document.getElementById('show-history-button')?.addEventListener('click', showHistory);