// Код чтобы при повторном нажати на кнопку главного меню оно закрывалосьЫ
document.addEventListener('DOMContentLoaded', function () {
    const toggler = document.querySelector('.navbar-toggler');
    const menu = document.querySelector('#navbarNav');

    toggler.addEventListener('click', function () {
        menu.classList.toggle('show');
    });
});

document.addEventListener("DOMContentLoaded", function() {
    const heroSection = document.getElementById('hero-section');
    const bgImage = new Image();
    bgImage.src = '/static/img/hero_section_img-1.jpg';

    bgImage.onload = function() {
        heroSection.style.backgroundImage = `url('${bgImage.src}')`;
        heroSection.setAttribute("data-fallback", "false");
    };

    bgImage.onerror = function() {
        heroSection.setAttribute("data-fallback", "true");
    };

    // Плавный скролл при клике на ссылки меню
    const menuLinks = document.querySelectorAll('.navbar-nav .nav-link');

    menuLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const targetID = this.getAttribute('href').substring(1);
            const targetSection = document.getElementById(targetID);

            window.scrollTo({
                top: targetSection.offsetTop - 60, 
                behavior: 'smooth'
            });
        });
    });  

});

document.addEventListener('click', function (event) {
    const menu = document.getElementById('navbarNav'); // Само меню
    const toggler = document.querySelector('.navbar-toggler'); // Кнопка меню

    // Проверяем, если меню открыто и клик не на меню и не на кнопке
    if (menu.classList.contains('show') && !menu.contains(event.target) && !toggler.contains(event.target)) {
        toggler.click(); // Программно "нажимаем" на кнопку, чтобы закрыть меню
    }
});
