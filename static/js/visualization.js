// Управление отображением 3D-моделей в проекте NovaHaus с использованием <model-viewer>

/**
 * Отображает 3D-модель в элементе model-viewer по указанному URL.
 * @param {string} modelUrl - URL 3D-модели.
 */
function show3DModel(modelUrl) {
    const viewer = document.getElementById('3d-viewer');
    if (!viewer) {
        console.error('[3D-Model] Элемент #3d-viewer не найден.');
        return;
    }
    if (!modelUrl) {
        console.error('[3D-Model] URL модели не предоставлен.');
        return;
    }
    viewer.src = modelUrl;
    viewer.style.display = 'block';
    console.log('[3D-Model] Модель загружена:', modelUrl);
}

/**
 * Скрывает 3D-модель и очищает model-viewer.
 */
function hide3DModel() {
    const viewer = document.getElementById('3d-viewer');
    if (!viewer) {
        console.error('[3D-Model] Элемент #3d-viewer не найден.');
        return;
    }
    viewer.style.display = 'none';
    viewer.src = '';
    console.log('[3D-Model] Модель скрыта.');
}