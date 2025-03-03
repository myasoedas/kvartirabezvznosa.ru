import { hamburgerMenuToggle } from './components/hamburgerMenuToggle.js';
import { initHeroSection } from "./components/hero-section.js";
import { setupThemeToggle } from './components/themeToggle.js';

// Вызываем функцию после загрузки страницы
document.addEventListener("DOMContentLoaded", () => {
    hamburgerMenuToggle();
    setupThemeToggle();
    initHeroSection();
});
