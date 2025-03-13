document.addEventListener("DOMContentLoaded", function () {
    const track = document.querySelector(".slider__track");
    const slides = document.querySelectorAll(".slider__slide");
    const prevBtn = document.querySelector(".slider__button--prev");
    const nextBtn = document.querySelector(".slider__button--next");
    const dots = document.querySelectorAll(".slider__dot");

    let currentIndex = 0;
    const totalSlides = slides.length;

    function updateSlider() {
        track.style.transform = `translateX(-${currentIndex * 100}%)`;
        dots.forEach((dot, index) => {
            dot.classList.toggle("active", index === currentIndex);
        });
    }

    prevBtn.addEventListener("click", () => {
        currentIndex = (currentIndex === 0) ? totalSlides - 1 : currentIndex - 1;
        updateSlider();
    });

    nextBtn.addEventListener("click", () => {
        currentIndex = (currentIndex === totalSlides - 1) ? 0 : currentIndex + 1;
        updateSlider();
    });

    dots.forEach((dot, index) => {
        dot.addEventListener("click", () => {
            currentIndex = index;
            updateSlider();
        });
    });

    updateSlider();
});
