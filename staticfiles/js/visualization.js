// Функция для отображения круговой диаграммы
function showChart(totalCost, materialCost, laborCost) {
    const ctx = document.getElementById('cost-chart').getContext('2d');

    // Удаляем предыдущий график, если он существует
    if (window.myChart) {
        window.myChart.destroy();
    }

    // Создаем новый график
    window.myChart = new Chart(ctx, {
        type: 'pie',
        data: {
            labels: ['Материалы', 'Работа'],
            datasets: [{
                data: [materialCost, laborCost],
                backgroundColor: ['#007bff', '#28a745'], // Цвета для секторов
                borderColor: '#ffffff', // Цвет границ
                borderWidth: 2
            }]
        },
        options: {
            responsive: true, // Адаптивность
            plugins: {
                legend: {
                    position: 'top', // Положение легенды
                },
                title: {
                    display: true,
                    text: 'Распределение затрат', // Заголовок графика
                    font: {
                        size: 16
                    }
                }
            }
        }
    });
}