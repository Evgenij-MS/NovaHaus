// Функция для отображения 3D-модели
function show3DModel(modelUrl) {
    const viewer = document.getElementById('3d-viewer');
    viewer.src = modelUrl;
    viewer.style.display = 'block';
}

// Функция для скрытия 3D-модели
function hide3DModel() {
    const viewer = document.getElementById('3d-viewer');
    viewer.style.display = 'none';
}