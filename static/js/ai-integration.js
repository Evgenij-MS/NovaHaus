function getCSRFToken() {
  const match = document.cookie.match(/(^|;)\s*csrftoken=([^;]+)/);
  return match ? match[2] : null;
}

async function getAIRecommendations(totalCost, materialCost, laborCost, workType, area) {
  const data = {
    totalCost,
    materialCost,
    laborCost,
    workType,
    area,
    language: document.documentElement.lang || 'de'
  };

  try {
    console.log("Daten an Server gesendet:", data);
    const csrfToken = getCSRFToken();
    if (!csrfToken) throw new Error('CSRF-Token nicht gefunden');

    const response = await fetch('/get-ai-recommendations/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': csrfToken
      },
      body: JSON.stringify(data)
    });

    const result = await response.json();
    console.log("Serverantwort:", result);

    if (result.success && result.recommendation) {
      const recommendation = result.recommendation;
      document.getElementById('ai-recommendation-text').innerText = recommendation;
    } else {
      console.error('Fehler bei Empfehlungen:', result.error);
      document.getElementById('ai-recommendation-text').innerText = 'Empfehlungen konnten nicht abgerufen werden. Bitte versuchen Sie es später.';
    }
  } catch (error) {
    console.error('Fehler:', error);
    document.getElementById('ai-recommendation-text').innerText = 'Ein Fehler ist aufgetreten. Bitte versuchen Sie es später.';
  }
}

document.addEventListener('DOMContentLoaded', () => {
  const calculateButton = document.getElementById('calculate-button');
  if (calculateButton) {
    calculateButton.addEventListener('click', async () => {
      const totalCost = parseFloat(document.getElementById('total-cost')?.value || 0);
      const materialCost = parseFloat(document.getElementById('material-cost')?.value || 0);
      const laborCost = parseFloat(document.getElementById('labor-cost')?.value || 0);
      const workType = document.getElementById('work-type').value;
      const area = parseFloat(document.getElementById('area').value);

      if (totalCost && materialCost && laborCost) {
        await getAIRecommendations(totalCost, materialCost, laborCost, workType, area);
      }
    });
  }
});