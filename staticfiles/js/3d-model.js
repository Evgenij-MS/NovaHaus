// Функция для отображения 3D-модели
function show3DModel(modelUrl) {
    const viewer = document.getElementById('3d-viewer');
    viewer.src = modelUrl; // Указываем URL 3D-модели
    viewer.style.display = 'block'; // Показываем iframe
}

// Функция для скрытия 3D-модели
function hide3DModel() {
    const viewer = document.getElementById('3d-viewer');
    viewer.style.display = 'none'; // Скрываем iframe
    viewer.src = ''; // Убираем URL, чтобы освободить ресурс
}
