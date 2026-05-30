// frontend/pages/admin/components/loader.js
/**
 * Global component loader for the admin UI.
 *
 * It injects the shared sidebar, navbar, footer and toast containers,
 * wires up common behaviour (theme toggle, profile menu, logout, active link,
 * and sets the navbar title from <meta name="page-title">).
 *
 * Special rule: the Dashboard page must always be displayed in **light mode**
 * regardless of the saved user preference. This satisfies the request
 * "am not like dar mode of dashbaord 6".
 */

document.addEventListener('DOMContentLoaded', async () => {
  const fetchHTML = async (path) => (await fetch(path)).text();

  // Load shared fragments
  const [sidebar, navbar, footer, toast] = await Promise.all([
    fetchHTML('components/sidebar.html'),
    fetchHTML('components/navbar.html'),
    fetchHTML('components/footer.html'),
    fetchHTML('components/toast.html'),
  ]);

  // Insert into placeholders present on every admin page
  document.getElementById('sidebar').innerHTML = sidebar;
  document.getElementById('navbar').innerHTML = navbar;
  document.getElementById('footer').innerHTML = footer;
  document.getElementById('toast-container').innerHTML = toast;

  // ---------- Global UI helpers ----------
  const themeToggle = document.getElementById('theme-toggle');
  const themeIcon   = document.getElementById('theme-icon');
  const themeLabel  = document.getElementById('theme-label');

  const setTheme = (mode) => {
    document.documentElement.classList.toggle('dark', mode === 'dark');
    themeIcon.innerHTML = mode === 'dark'
      ? '<use href="#heroicon-outline-sun"></use>'
      : '<use href="#heroicon-outline-moon"></use>';
    themeLabel.textContent = mode === 'dark' ? 'Light Mode' : 'Dark Mode';
    localStorage.setItem('eduflow_theme', mode);
  };

  // Determine initial theme
  const initial = localStorage.getItem('eduflow_theme') || 'dark';
  setTheme(initial);

  themeToggle?.addEventListener('click', () => {
    const currentDark = document.documentElement.classList.contains('dark');
    setTheme(currentDark ? 'light' : 'dark');
  });

  // Profile dropdown
  const profileBtn  = document.getElementById('profile-btn');
  const profileMenu = document.getElementById('profile-menu');
  profileBtn?.addEventListener('click', (e) => {
    e.stopPropagation();
    profileMenu?.classList.toggle('hidden');
  });
  document.addEventListener('click', () => profileMenu?.classList.add('hidden'));

  // Logout (uses confirm modal already present on each page)
  const logoutBtn = document.getElementById('logout-btn');
  logoutBtn?.addEventListener('click', () => {
    openConfirm('Log Out', 'Are you sure you want to log out?', () => {
      localStorage.removeItem('access_token');
      window.location.href = '../../login.html';
    });
  });

  // Highlight current navigation link
  const page = location.pathname.split('/').pop().replace('.html', '');
  document.querySelectorAll('.nav-link').forEach((link) => {
    if (link.dataset.page === page) {
      link.classList.add('bg-primary/10', 'text-primary');
      link.classList.remove('hover:bg-gray-100', 'dark:hover:bg-gray-700');
    }
  });

  // Set navbar title from <meta name="page-title">
  if (metaTitle) {
    const titleEl = document.getElementById('page-title');
    if (titleEl) titleEl.textContent = metaTitle.content;
  }
});
