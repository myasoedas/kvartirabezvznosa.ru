export function hamburgerMenuToggle() {
    const hamburgerIcon = document.getElementById('hamburger-icon');
    const popupMenu = document.getElementById('popup-menu');

    if (!hamburgerIcon || !popupMenu) return;

    function toggleMenu(event) {
        event.preventDefault(); // Предотвращает стандартное поведение
        hamburgerIcon.classList.toggle('active');
        popupMenu.classList.toggle('open');

        // Добавляем класс к body, чтобы запретить скролл при открытом меню
        if (popupMenu.classList.contains('open')) {
            document.body.style.overflow = 'hidden';
        } else {
            document.body.style.overflow = '';
        }
    }

    function closeMenu(event) {
        if (!popupMenu.contains(event.target) && !hamburgerIcon.contains(event.target)) {
            hamburgerIcon.classList.remove('active');
            popupMenu.classList.remove('open');
            document.body.style.overflow = ''; // Разрешаем скролл
        }
    }

    hamburgerIcon.addEventListener('click', toggleMenu);
    document.addEventListener('click', closeMenu);
}
