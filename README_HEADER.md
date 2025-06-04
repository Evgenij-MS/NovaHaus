[ Шапка: 3D-навигация с параллаксом ]
[ Липкий хедер с лого, навигацией, переключателем языка, кнопками AR/Калькулятор ]
 Умная навигация с 3D-эффектами
Элементы:

Параллакс-меню: При скролле элементы двигаются в 3D-пространстве

AI-ассистент: Иконка чат-бота с пульсирующей анимацией

Геолокатор: Автоопределение района (Ehrenfeld/St. Pauli)

Код анимации:

javascript
window.addEventListener("scroll", () => {
  const depth = window.scrollY * 0.5;
  navItems.forEach(item => {
    item.style.transform = `translateZ(${depth}px) rotateY(${depth}deg)`;
  });
});
