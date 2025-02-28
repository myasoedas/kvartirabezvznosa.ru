export function hamburgerMenuToggle() {
    const hamburgerIcon = document.getElementById('hamburger-icon');
    const popupMenu = document.getElementById('popup-menu');

    if (!hamburgerIcon || !popupMenu) return;

    // Функция переключения меню
    function toggleMenu(event) {
        event.stopPropagation(); // Предотвращает всплытие события на `document`
        hamburgerIcon.classList.toggle('active');
        popupMenu.classList.toggle('open');
    }

    // Функция закрытия меню при клике вне меню
    function closeMenu(event) {
        if (!popupMenu.contains(event.target) && !hamburgerIcon.contains(event.target)) {
            hamburgerIcon.classList.remove('active');
            popupMenu.classList.remove('open');
        }
    }

    // Назначаем обработчик на клик по иконке гамбургера
    hamburgerIcon.addEventListener('click', toggleMenu);

    // Назначаем обработчик на клик по документу, чтобы закрыть меню
    document.addEventListener('click', closeMenu);
}
