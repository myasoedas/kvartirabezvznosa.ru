document.addEventListener("DOMContentLoaded", () => {
    const track = document.querySelector(".slider__track");
    const slides = document.querySelectorAll(".slider__slide");
    const prevButton = document.querySelector(".slider__arrow--left");
    const nextButton = document.querySelector(".slider__arrow--right");
    const dotsContainer = document.querySelector(".slider__dots");

    let currentIndex = 0;
    const totalSlides = slides.length;
    let autoSlideInterval;

    // Создание точек
    slides.forEach((_, index) => {
        const dot = document.createElement("span");
        dot.classList.add("slider__dot");
        if (index === 0) dot.classList.add("slider__dot--active");
        dot.dataset.index = index;
        dotsContainer.appendChild(dot);
    });

    const dots = document.querySelectorAll(".slider__dot");

    function updateSlide(position) {
        track.style.transform = `translateX(-${position * 100}%)`;
        dots.forEach(dot => dot.classList.remove("slider__dot--active"));
        dots[position].classList.add("slider__dot--active");
    }

    function nextSlide() {
        currentIndex = (currentIndex + 1) % totalSlides;
        updateSlide(currentIndex);
    }

    function prevSlide() {
        currentIndex = (currentIndex - 1 + totalSlides) % totalSlides;
        updateSlide(currentIndex);
    }

    function resetAutoSlide() {
        clearInterval(autoSlideInterval);
        autoSlideInterval = setInterval(nextSlide, 5000);
    }

    prevButton.addEventListener("click", () => {
        prevSlide();
        resetAutoSlide();
    });

    nextButton.addEventListener("click", () => {
        nextSlide();
        resetAutoSlide();
    });

    dots.forEach(dot => {
        dot.addEventListener("click", () => {
            currentIndex = parseInt(dot.dataset.index);
            updateSlide(currentIndex);
            resetAutoSlide();
        });
    });

    // Запускаем автопрокрутку
    autoSlideInterval = setInterval(nextSlide, 5000);
});
