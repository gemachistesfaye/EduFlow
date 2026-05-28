// ================= DARK MODE ================= //
const themeToggleBtn = document.getElementById('theme-toggle');
const darkIcon = document.getElementById('theme-toggle-dark-icon');
const lightIcon = document.getElementById('theme-toggle-light-icon');

function applyDarkMode() {
    if (
        localStorage.getItem('color-theme') === 'dark' ||
        (!localStorage.getItem('color-theme') && window.matchMedia('(prefers-color-scheme: dark)').matches)
    ) {
        document.documentElement.classList.add('dark');
        lightIcon?.classList.remove('hidden');
        darkIcon?.classList.add('hidden');
    } else {
        document.documentElement.classList.remove('dark');
        darkIcon?.classList.remove('hidden');
        lightIcon?.classList.add('hidden');
    }
}

// Apply dark mode on page load
applyDarkMode();

themeToggleBtn?.addEventListener('click', () => {
    document.documentElement.classList.toggle('dark');
    darkIcon?.classList.toggle('hidden');
    lightIcon?.classList.toggle('hidden');

    if (document.documentElement.classList.contains('dark')) {
        localStorage.setItem('color-theme', 'dark');
    } else {
        localStorage.setItem('color-theme', 'light');
    }
});

// ================= SIDEBAR TOGGLE ================= //
const sidebar = document.getElementById('sidebar');
const overlay = document.getElementById('sidebar-overlay');

function toggleSidebar() {
    if (!sidebar || !overlay) return;
    const isHidden = sidebar.classList.contains('-translate-x-full');
    if (isHidden) {
        sidebar.classList.remove('-translate-x-full');
        overlay.classList.remove('hidden');
    } else {
        sidebar.classList.add('-translate-x-full');
        overlay.classList.add('hidden');
    }
}

overlay?.addEventListener('click', toggleSidebar);
window.toggleSidebar = toggleSidebar; // make accessible from HTML onclick

// Handle screen resize
window.addEventListener('resize', () => {
    if (!sidebar || !overlay) return;
    if (window.innerWidth >= 1024) {
        sidebar.classList.remove('-translate-x-full');
        overlay.classList.add('hidden');
    } else {
        sidebar.classList.add('-translate-x-full');
    }
});

// ================= NAVIGATION ================= //
const navItems = document.querySelectorAll('.nav-item');
navItems.forEach(item => {
    item.addEventListener('click', function(e) {
        e.preventDefault();
        navItems.forEach(nav => nav.classList.remove('active'));
        this.classList.add('active');

        if (window.innerWidth < 1024) toggleSidebar();

        const href = this.getAttribute('href');
        if (href && href !== '#') {
            window.location.href = href;
            return;
        }

        const pageName = this.getAttribute('data-page');
        if (pageName) {
            window.location.href = `${pageName}.html`;
        } else {
            console.log('Unknown page:', pageName);
        }
    });
});

// ================= LOGOUT ================= //
const logoutBtn = document.getElementById('logout-btn');
logoutBtn?.addEventListener('click', () => {
    const confirmLogout = confirm("Are you sure you want to logout?");
    if (confirmLogout) {
        window.location.href = '/login.html';
    }
});

// ================= INITIALIZE ICONS ================= //
if (typeof lucide !== 'undefined') lucide.createIcons();
