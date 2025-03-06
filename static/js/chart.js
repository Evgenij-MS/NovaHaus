// Визуализация данных с помощью Chart.js
function showChart(materialCost, laborCost, additionalCost) {
    const ctx = document.getElementById('cost-chart').getContext('2d');
    new Chart(ctx, {
        type: 'pie',
        data: {
            labels: ['Материалы', 'Работа', 'Дополнительные услуги'],
            datasets: [{
                data: [materialCost, laborCost, additionalCost],
                backgroundColor: ['#007bff', '#28a745', '#ffcc00'],
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