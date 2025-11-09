// script.js — loader, theme toggle (auto + manual), mobile menu handling
document.addEventListener('DOMContentLoaded', function () {
  // Page loader: fade out once DOM is ready (and a short delay to show effect)
  const loader = document.getElementById('page-loader');
  setTimeout(() => {
    if (!loader) return;
    loader.style.opacity = '0';
    loader.style.visibility = 'hidden';
    loader.style.pointerEvents = 'none';
  }, 700);

  // Theme handling: supports auto (prefers-color-scheme) + manual toggle.
  const html = document.documentElement;
  // read previously selected theme from localStorage if present
  const saved = localStorage.getItem('theme-mode'); // 'light'|'dark'|'auto' or null
  const themeToggle = document.getElementById('theme-toggle');

  function applyTheme(mode) {
    // mode: 'light' | 'dark' | 'auto'
    if (mode === 'auto') {
      // choose based on system preference
      const prefersDark = window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches;
      html.setAttribute('data-theme', prefersDark ? 'dark' : 'light');
    } else {
      html.setAttribute('data-theme', mode);
    }
    localStorage.setItem('theme-mode', mode);
    updateToggleButton();
  }

  function updateToggleButton() {
    const mode = localStorage.getItem('theme-mode') || 'auto';
    // simple circular toggle: cycle through auto -> dark -> light -> auto
    if (!themeToggle) return;
    const m = mode;
    if (m === 'auto') themeToggle.title = 'Theme: Auto (system) — click to switch to Dark';
    else if (m === 'dark') themeToggle.title = 'Theme: Dark — click to switch to Light';
    else themeToggle.title = 'Theme: Light — click to switch to Auto';
  }

  // initial apply
  applyTheme(saved || 'auto');

  // clicking cycles modes: auto -> dark -> light -> auto
  if (themeToggle) {
    themeToggle.addEventListener('click', () => {
      const cur = localStorage.getItem('theme-mode') || 'auto';
      const next = cur === 'auto' ? 'dark' : (cur === 'dark' ? 'light' : 'auto');
      applyTheme(next);
    });
  }

  // Mobile menu toggle
  const menuToggle = document.getElementById('menu-toggle');
  const mobileMenu = document.getElementById('mobile-menu');
  if (menuToggle && mobileMenu) {
    menuToggle.addEventListener('click', () => {
      const showing = mobileMenu.style.display === 'block';
      mobileMenu.style.display = showing ? 'none' : 'block';
      // small animation
      if (!showing) {
        mobileMenu.animate([{ opacity: 0, transform: 'translateY(-6px)' }, { opacity: 1, transform: 'translateY(0)' }], { duration: 220, easing: 'ease-out' });
      }
    });
  }
});
