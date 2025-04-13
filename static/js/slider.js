document.addEventListener('DOMContentLoaded', () => {
  const slides = document.querySelectorAll('#hero-slider video, #hero-slider img');
  const indicators = document.querySelectorAll('.slider-indicators button');
  let currentSlide = 0;

  function showSlide(index) {
    slides.forEach((slide, i) => {
      slide.classList.toggle('active', i === index);
      indicators[i].classList.toggle('active', i === index);
    });
  }

  function nextSlide() {
    currentSlide = (currentSlide + 1) % slides.length;
    showSlide(currentSlide);
  }

  indicators.forEach((button, index) => {
    button.addEventListener('click', () => {
      currentSlide = index;
      showSlide(index);
    });
  });

  showSlide(currentSlide);
  setInterval(nextSlide, 2000);
});