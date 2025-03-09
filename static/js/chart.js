let costChart = null;

function showChart(materialCost, laborCost, additionalCost) {
    const ctx = document.getElementById('cost-chart').getContext('2d');

    if (costChart) {
        costChart.destroy();
    }

    costChart = new Chart(ctx, {
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
            animation: {
                duration: 1000,
                easing: 'easeInOutQuad'
            },
            plugins: {
                legend: { position: 'top' },
                title: { display: true, text: 'Распределение затрат' },
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            const label = context.label || '';
                            const value = context.raw || 0;
                            return `${label}: ${value} руб.`;
                        }
                    }
                }
            }
        }
    });
}