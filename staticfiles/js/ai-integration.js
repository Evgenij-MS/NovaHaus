async function processAIResponse(response, recommendationElement) {
    const result = await response.json();
    console.log("Serverantwort:", result);
    if (result.success && result.recommendation) {
        recommendationElement.innerText = result.recommendation;
    } else {
        console.error('Fehler bei Empfehlungen:', result.error);
        recommendationElement.innerText = 'Empfehlungen konnten nicht abgerufen werden. Bitte versuchen Sie es später.';
    }
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
    const recommendationElement = document.getElementById('ai-recommendation-text');

    try {
        console.log("Daten an Server gesendet:", data);
        const csrfToken = getCSRFToken();
        if (!csrfToken) {
            recommendationElement.innerText = 'Ошибка: CSRF-токен не найден.';
            console.error('CSRF-Token nicht gefunden');
            return;
        }

        const response = await fetch('/get-ai-recommendations/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken
            },
            body: JSON.stringify(data)
        });

        await processAIResponse(response, recommendationElement);
    } catch (error) {
        console.error('Fehler:', error);
        recommendationElement.innerText = 'Ein Fehler ist aufgetreten. Bitte versuchen Sie es später.';
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