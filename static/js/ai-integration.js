// Интеграция с ИИ
async function getAIRecommendation(workType, area) {
    const response = await fetch('https://api.example.com/ai-recommendation', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ workType, area })
    });
    const data = await response.json();
    return data.recommendation;
}

async function showAIRecommendation() {
    const workType = document.getElementById('work-type').value;
    const area = document.getElementById('area').value;

    const recommendation = await getAIRecommendation(workType, area);
    const content = `
        <h2>Рекомендации от ИИ</h2>
        <p>${recommendation}</p>
    `;
    openModal(content);
}