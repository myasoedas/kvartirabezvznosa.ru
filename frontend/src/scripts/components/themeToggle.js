export function setupThemeToggle() {
    const toggleButton = document.getElementById('theme-toggle'); // Кнопка-переключатель
    if (!toggleButton) return;
  
    // Можно использовать localStorage для сохранения выбранной темы
    const savedTheme = localStorage.getItem('theme') || 'light';
    setTheme(savedTheme);
  
    toggleButton.addEventListener('click', () => {
      const currentTheme = document.body.classList.contains('theme-dark') ? 'dark' : 'light';
      const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
      setTheme(newTheme);
      localStorage.setItem('theme', newTheme);
    });
  }
  
  function setTheme(theme) {
    if (theme === 'dark') {
      document.body.classList.add('theme-dark');
    } else {
      document.body.classList.remove('theme-dark');
    }
  }
  