import { hamburgerMenuToggle } from './components/hamburgerMenuToggle.js';
import { initHeroSection } from "./components/hero-section.js";
import { slider } from './components/slider.js';
import { setupThemeToggle } from './components/themeToggle.js';

// Вызываем функцию после загрузки страницы
document.addEventListener("DOMContentLoaded", () => {
    hamburgerMenuToggle();
    setupThemeToggle();
    initHeroSection();
    slider();
});
