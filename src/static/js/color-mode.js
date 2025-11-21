const htmlElement = document.documentElement; // Représente la balise <html>
const iconElement = document.getElementById('themeToggleIcon');

// 1. Récupération du thème dans localStorage, par défaut "light"
const savedTheme = localStorage.getItem('bsTheme') || 'light';
applyTheme(savedTheme);

// 2. Au clic sur l'icône, on bascule de "light" à "dark" (ou inversement)
iconElement.addEventListener('click', () => {
  const currentTheme = htmlElement.getAttribute('data-bs-theme');
  const newTheme = (currentTheme === 'light') ? 'dark' : 'light';
  applyTheme(newTheme);
});

/**
 * Applique le thème (light ou dark), change l’icône et sauvegarde dans localStorage
 * @param {string} theme - "light" ou "dark"
 */
function applyTheme(theme) {
  // 1. Appliquer l'attribut data-bs-theme
  htmlElement.setAttribute('data-bs-theme', theme);

  // 2. Déterminer l’icône en fonction du thème
  if (theme === 'dark') {
    // Si on est en sombre, on affiche l’icône Soleil
    iconElement.classList.remove('bi-moon-stars');
    iconElement.classList.add('bi-sun');
  } else {
    // Si on est en clair, on affiche l’icône Lune
    iconElement.classList.remove('bi-sun');
    iconElement.classList.add('bi-moon-stars');
  }

  // 3. Sauvegarder la préférence
  localStorage.setItem('bsTheme', theme);
}  