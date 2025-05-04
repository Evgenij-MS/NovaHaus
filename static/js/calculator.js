/* global Chart */
const prices = {
  apartment: { economy: 70, standard: 100, premium: 130 },
  house: { economy: 80, standard: 110, premium: 140 },
  office: { economy: 90, standard: 120, premium: 150 },
  warehouse: { economy: 50, standard: 70, premium: 90 },
  facade: { economy: 40, standard: 50, premium: 60 },
  insulation: { economy: 45, standard: 55, premium: 65 },
  demolition: 25,
  cleaning: 8
};

const additionalServices = {
  cleaning: 8,
  delivery: 100
};

function getCSRFToken() {
  const match = document.cookie.match(/(^|;)\s*csrftoken=([^;]+)/);
  return match ? match[2] : null;
}

function formatCurrency(amount, locale = 'de-DE') {
  return new Intl.NumberFormat(locale, { style: 'currency', currency: 'EUR' }).format(amount);
}

function getFormValues() {
  return {
    workType: document.getElementById('work-type').value,
    area: parseFloat(document.getElementById('area').value),
    material: document.getElementById('material').value,
    includeMaterials: document.getElementById('include-materials').value,
    urgency: document.getElementById('urgency').value,
    cleaning: document.getElementById('cleaning').checked,
    delivery: document.getElementById('delivery').checked
  };
}

function calculateCost() {
  const { workType, area, material, includeMaterials, urgency, cleaning, delivery } = getFormValues();
  const resultElement = document.getElementById('result');

  if (isNaN(area) || area <= 0) {
    resultElement.innerText = 'Fehler: Bitte geben Sie eine gültige Fläche ein!';
    resultElement.style.color = 'red';
    return;
  }

  let costPerSquareMeter = prices[workType][material] || prices[workType];
  if (urgency === 'fast') costPerSquareMeter *= 1.2;

  const materialPercentage = 0.4;
  const laborPercentage = 0.6;
  let materialCost = includeMaterials === 'yes' ? area * costPerSquareMeter * materialPercentage : 0;
  let laborCost = includeMaterials === 'yes' ? area * costPerSquareMeter * laborPercentage : area * costPerSquareMeter;

  let additionalCost = 0;
  if (cleaning) additionalCost += area * additionalServices.cleaning;
  if (delivery) additionalCost += additionalServices.delivery;

  const totalCost = materialCost + laborCost + additionalCost;

  resultElement.innerText = `Geschätzte Kosten: ${formatCurrency(totalCost)}`;
  resultElement.style.color = 'black';

  showChart(totalCost, materialCost, laborCost);

  getAIRecommendations(totalCost, materialCost, laborCost, workType, area)
    .catch(error => console.error('Fehler bei AI-Empfehlungen:', error));
}

function showChart(totalCost, materialCost, laborCost) {
  const chartElement = document.getElementById('cost-chart');
  if (!chartElement) {
    console.error('Element #cost-chart nicht gefunden.');
    return;
  }
  const ctx = chartElement.getContext('2d');

  if (ctx) {
    new Chart(ctx, {
      type: 'pie',
      data: {
        labels: ['Materialien', 'Arbeitskosten'],
        datasets: [{
          data: [materialCost, laborCost],
          backgroundColor: ['#007bff', '#28a745'],
        }]
      },
      options: {
        responsive: true,
        plugins: {
          legend: { position: 'top' },
          title: { display: true, text: 'Kostenverteilung' }
        }
      }
    });
  }
}

function saveCalculation() {
  const { workType, area, material, includeMaterials, urgency } = getFormValues();
  const totalCostText = document.getElementById('result').innerText.match(/[\d,.]+/);
  const totalCost = totalCostText ? parseFloat(totalCostText[0].replace(',', '.')) : 0;

  const calculation = {
    workType,
    area,
    material,
    includeMaterials,
    urgency,
    totalCost,
    timestamp: new Date().toLocaleString()
  };

  const csrfToken = getCSRFToken();
  if (!csrfToken) {
    console.error('CSRF-Token nicht gefunden');
    return;
  }

  fetch('/save-calculation/', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-CSRFToken': csrfToken
    },
    body: JSON.stringify(calculation)
  })
    .then(response => response.json())
    .then(data => {
      if (data.success) {
        alert('Berechnung erfolgreich gespeichert!');
      } else {
        alert('Fehler beim Speichern der Berechnung.');
      }
    })
    .catch(error => {
      console.error('Fehler:', error);
      const resultElement = document.getElementById('result');
      resultElement.innerText = 'Fehler beim Speichern. Bitte versuchen Sie es später.';
      resultElement.style.color = 'red';
    });
}

document.getElementById('calculate-button').addEventListener('click', calculateCost);
document.getElementById('save-button').addEventListener('click', saveCalculation);