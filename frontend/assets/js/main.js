/* file: frontend/assets/js/main.js */
window.App = (() => {
  // ----- Theme (dark / light) -----
  const html = document.documentElement;

  function setTheme(mode) {
    const icon  = document.getElementById('theme-icon');
    const label = document.getElementById('theme-label');
    if (mode === 'dark') {
      html.classList.add('dark');
      if (icon)  icon.innerHTML  = '<use href="#heroicon-outline-moon"></use>';
      if (label) label.textContent = 'Light Mode';
    } else {
      html.classList.remove('dark');
      if (icon)  icon.innerHTML  = '<use href="#heroicon-outline-sun"></use>';
      if (label) label.textContent = 'Dark Mode';
    }
    localStorage.setItem('eduflow_theme', mode);
  }

  const stored = localStorage.getItem('eduflow_theme') || 'dark';
  setTheme(stored);

  document.addEventListener('DOMContentLoaded', () => {
    const toggleBtn = document.getElementById('theme-toggle');
    if (toggleBtn) {
      toggleBtn.addEventListener('click', () => {
        setTheme(html.classList.contains('dark') ? 'light' : 'dark');
      });
    }

    // Sidebar collapse (mobile)
    const sidebar      = document.getElementById('main-sidebar');
    const sidebarToggle = document.getElementById('sidebar-toggle');
    if (sidebarToggle && sidebar) {
      sidebarToggle.addEventListener('click', () => {
        sidebar.classList.toggle('-translate-x-full');
      });
    }

    // Profile dropdown
    const profileBtn  = document.getElementById('profile-btn');
    const profileMenu = document.getElementById('profile-menu');
    if (profileBtn && profileMenu) {
      profileBtn.addEventListener('click', (e) => {
        e.stopPropagation();
        profileMenu.classList.toggle('hidden');
      });
      document.addEventListener('click', (e) => {
        if (profileMenu && !profileMenu.contains(e.target)) {
          profileMenu.classList.add('hidden');
        }
      });
    }

    // Logout
    const logoutBtn = document.getElementById('logout-btn');
    if (logoutBtn) {
      logoutBtn.addEventListener('click', () => {
        localStorage.removeItem('access_token');
        window.location.href = '../../login.html';
      });
    }

    // Highlight active nav link
    const page = window.location.pathname.split('/').pop().replace('.html', '');
    document.querySelectorAll('.nav-link').forEach(link => {
      if (link.dataset.page === page) {
        link.classList.add('bg-primary/10', 'text-primary');
        link.classList.remove('hover:bg-gray-100', 'dark:hover:bg-gray-700', 'text-gray-600', 'dark:text-gray-300');
      }
    });
  });

  // ----- Toasts -----
  function toast(message, type = 'info', duration = 4000) {
    const container = document.getElementById('toast-container');
    if (!container) return;
    const el = document.createElement('div');
    const colors = { success: 'bg-green-100 text-green-800 border-green-300', error: 'bg-red-100 text-red-800 border-red-300', info: 'bg-blue-100 text-blue-800 border-blue-300', warning: 'bg-yellow-100 text-yellow-800 border-yellow-300' };
    el.className = `flex items-center gap-2 px-4 py-3 rounded-lg shadow-lg border text-sm font-medium w-80 max-w-full transition-all duration-300 ${colors[type] || colors.info}`;
    el.textContent = message;
    container.appendChild(el);
    setTimeout(() => { el.style.opacity = '0'; setTimeout(() => el.remove(), 300); }, duration);
  }

  // ----- Modal helpers -----
  function openModal(id) {
    const el = document.getElementById(id);
    if (el) el.classList.remove('hidden');
  }
  function closeModal(id) {
    const el = document.getElementById(id);
    if (el) el.classList.add('hidden');
  }

  return { toast, openModal, closeModal, setTheme };
})();
