/* global Chart */
let costChart = null;

function getTranslations(lang) {
    const translations = {
        de: {
            materials: 'Materialien',
            labor: 'Arbeitskosten',
            additional: 'Zusätzliche Dienstleistungen',
            title: 'Kostenverteilung',
            currency: 'EUR'
        },
        en: {
            materials: 'Materials',
            labor: 'Labor Costs',
            additional: 'Additional Services',
            title: 'Cost Distribution',
            currency: 'EUR'
        },
        tr: {
            materials: 'Malzemeler',
            labor: 'İşçilik Maliyetleri',
            additional: 'Ek Hizmetler',
            title: 'Maliyet Dağılımı',
            currency: 'EUR'
        },
        ru: {
            materials: 'Материалы',
            labor: 'Стоимость работы',
            additional: 'Дополнительные услуги',
            title: 'Распределение затрат',
            currency: 'EUR'
        }
    };
    return translations[lang] || translations.de;
}

function showChart(materialCost, laborCost, additionalCost) {
    const lang = document.documentElement.lang || 'de';
    const t = getTranslations(lang);
    const ctx = document.getElementById('cost-chart')?.getContext('2d');

    if (!ctx) {
        console.error('Canvas #cost-chart nicht gefunden.');
        return;
    }

    if (costChart) {
        costChart.destroy();
    }

    costChart = new Chart(ctx, {
        type: 'pie',
        data: {
            labels: [t.materials, t.labor, t.additional],
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
                title: { display: true, text: t.title },
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            const label = context.label || '';
                            const value = context.raw || 0;
                            return `${label}: ${new Intl.NumberFormat(lang, { style: 'currency', currency: t.currency }).format(value)}`;
                        }
                    }
                }
            }
        }
    });
}