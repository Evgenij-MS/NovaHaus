// Управление отображением 3D-моделей в проекте NovaHaus с использованием <model-viewer>

/**
 * Отображает 3D-модель в элементе model-viewer по указанному URL.
 * @param {string} modelUrl - URL 3D-модели.
 */
export function show3DModel(modelUrl) {
    const viewer = document.getElementById('viewer');
    if (!viewer || !modelUrl || typeof modelUrl !== 'string') {
        console.error('[3D-Model] Недействительный viewer или URL модели.');
        return;
    }
    viewer.src = modelUrl;
    viewer.style.display = 'block';
    console.log('[3D-Model] Модель загружена:', modelUrl);
}

/**
 * Скрывает 3D-модель и очищает model-viewer.
 */
export function hide3DModel() {
    const viewer = document.getElementById('viewer');
    if (!viewer) {
        console.error('[3D-Model] Элемент #viewer не найден.');
        return;
    }
    viewer.style.display = 'none';
    viewer.removeAttribute('src');
    console.log('[3D-Model] Модель скрыта.');
}

// Обработка ошибок загрузки модели
document.addEventListener('DOMContentLoaded', () => {
    const viewer = document.getElementById('viewer');
    if (viewer) {
        viewer.addEventListener('error', () => {
            console.error('[3D-Model] Не удалось загрузить модель.');
            document.getElementById('3d-viewer-error').innerText = 'Не удалось загрузить 3D-модель.';
        });
    }

    document.getElementById('show-model')?.addEventListener('click', () => {
        const workType = document.getElementById('work-type').value;
        const materialQuality = document.getElementById('material-quality').value;
        const modelUrl = window.modelMap[workType]?.[materialQuality] || '/static/models/sample_model.glb';
        show3DModel(modelUrl);
    });
    document.getElementById('hide-model')?.addEventListener('click', hide3DModel);
});