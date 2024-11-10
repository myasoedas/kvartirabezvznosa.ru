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
    bgImage.src = 'https://images.unsplash.com/photo-1580281658623-88aa2d9369b0?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=MnwzNjUyOXwwfDF8c2VhcmNofDh8fGRvY3RvcnwwfHx8fDE2ODg3ODk0NzE&ixlib=rb-1.2.1&q=80&w=1080';

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
                top: targetSection.offsetTop - 60, // 60px для учета высоты фиксированной навигации
                behavior: 'smooth'
            });
        });
    });

    // Открытие попапа
    document.querySelectorAll('a[href="#contact"]').forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            document.getElementById('consultation-popup').style.display = 'flex';
        });
    });

    // Закрытие попапа
    document.querySelector('.close-popup').addEventListener('click', function() {
        document.getElementById('consultation-popup').style.display = 'none';
    });

    const form = document.getElementById('consultation-form');
    const nameInput = document.getElementById('popup-name');
    const phoneInput = document.getElementById('popup-phone');
    const messageInput = document.getElementById('popup-message');
    const nameError = document.getElementById('name-error');
    const phoneError = document.getElementById('phone-error');
    const submitButton = form.querySelector('button[type="submit"]');

    const namePattern = /^[А-ЯЁа-яё\s-]+$/; // Только русские буквы, пробелы, дефисы
    const phonePattern = /^79\d{9}$/; // Номер телефона должен начинаться с 79 и состоять из 11 цифр

    // Функция для проверки валидности формы
    function checkFormValidity() {
        let isValid = true;

        // Проверка имени
        if (!namePattern.test(nameInput.value)) {
            nameError.style.display = 'block';
            isValid = false;
        } else {
            nameError.style.display = 'none';
        }

        // Проверка телефона
        if (!phonePattern.test(phoneInput.value)) {
            phoneError.style.display = 'block';
            isValid = false;
        } else {
            phoneError.style.display = 'none';
        }

        // Активируем или деактивируем кнопку отправки в зависимости от валидности формы
        submitButton.disabled = !isValid;
    }

    // Проверка полей в реальном времени
    nameInput.addEventListener('input', checkFormValidity);
    phoneInput.addEventListener('input', checkFormValidity);

    // Валидация и отправка формы
    form.addEventListener('submit', function(e) {
        e.preventDefault();

        // Повторная проверка перед отправкой
        if (submitButton.disabled) {
            return;
        }

        let message = messageInput.value.trim();
        if (!message) {
            message = "Хочу записаться на консультацию";
        }

        const currentDate = new Date();
        const formattedDate = currentDate.toLocaleDateString();
        const formattedTime = currentDate.toLocaleTimeString();

        let whatsappMessage = `Имя: ${nameInput.value}%0A`;
        whatsappMessage += `Телефон: ${phoneInput.value}%0A`;
        whatsappMessage += `Сообщение: ${message}%0A`;
        whatsappMessage += `Дата и время отправки: ${formattedDate} ${formattedTime}`;

        const whatsappLink = `https://wa.me/79522672726?text=${whatsappMessage}`;
        window.open(whatsappLink, '_blank');

        document.getElementById('consultation-popup').style.display = 'none';
    });

    // Изначально кнопка должна быть неактивной
    submitButton.disabled = true;
});
