const fs = require('fs');
const path = require('path');

const dir = 'e:/GitHub Repo/school-management-system/frontend/pages/admin';

const headerTemplate = `<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>EduFlow Admin</title>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="../../assets/css/theme.css">
  <link rel="stylesheet" href="../../assets/css/admin-theme.css">
  <style>
    .mb-6 { margin-bottom: 1.5rem; }
    .flex { display: flex; }
    .items-center { align-items: center; }
    .justify-between { justify-content: space-between; }
    .gap-2 { gap: 0.5rem; }
    .text-2xl { font-size: 1.5rem; line-height: 2rem; }
    .font-semibold { font-weight: 600; }
    .text-white { color: var(--text-dark); }
    .w-5 { width: 1.25rem; }
    .h-5 { height: 1.25rem; }
    .p-4 { padding: 1rem; }
    .rounded-xl { border-radius: 0.75rem; }
    .shadow-sm { box-shadow: 0 1px 2px 0 rgba(0, 0, 0, 0.05); }
    .bg-white { background-color: #ffffff; }
    .w-full { width: 100%; }
    .table-auto { table-layout: auto; }
    .text-left { text-align: left; }
    .bg-gray-100 { background-color: #f3f4f6; }
    .p-2 { padding: 0.5rem; }
    .font-medium { font-weight: 500; }
    .text-center { text-align: center; }
    .text-gray-500 { color: #6b7280; }
    .modal-overlay{display:none;position:fixed;inset:0;background:rgba(0,0,0,.35);z-index:100;align-items:center;justify-content:center;}
    .modal-overlay.open{display:flex;}
    .modal{background:#fff;border-radius:14px;padding:28px;width:100%;max-width:480px;box-shadow:0 20px 60px rgba(0,0,0,.15);}
    .modal h2{font-size:17px;font-weight:700;margin-bottom:20px;}
    .form-row{display:grid;grid-template-columns:1fr 1fr;gap:12px;}
    .nav-item.active { background: linear-gradient(to right, #c39a48, #e8ce8a, #c39a48); color: #ffffff; font-weight: 700; border: none; box-shadow: 0 4px 15px rgba(0,0,0,0.3); }
    .grid { display: grid; }
    .grid-cols-1 { grid-template-columns: repeat(1, minmax(0, 1fr)); }
    @media(min-width: 768px) { .md\\:grid-cols-2 { grid-template-columns: repeat(2, minmax(0, 1fr)); } }
    @media(min-width: 1024px) { .lg\\:grid-cols-3 { grid-template-columns: repeat(3, minmax(0, 1fr)); } }
    .gap-4 { gap: 1rem; }
    .mt-4 { margin-top: 1rem; }
    .text-danger { color: #ef4444; }
    .bg-success { background-color: #22c55e; }
    .bg-gray-400 { background-color: #9ca3af; }
    .space-y-4 > * + * { margin-top: 1rem; }
    .animate-pulse { animation: pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite; }
    @keyframes pulse { 0%, 100% { opacity: 1; } 50% { opacity: .5; } }
  </style>
</head>
<body>
<div class="app-shell">
  <aside class="sidebar">
    <div class="sidebar-logo">
      <div class="sidebar-logo-icon">🎓</div>
      <div><div class="sidebar-logo-text">EduFlow</div><div class="sidebar-logo-sub">School Navigator</div></div>
    </div>
    <div class="sidebar-section-label">Main</div>
    <nav style="flex: 1; overflow-y: auto; padding-right: 4px;">
      <a href="dashboard.html"  class="nav-item">🏠 &nbsp;Dashboard</a>
      <a href="students.html"   class="nav-item">👥 &nbsp;Students</a>
      <a href="teachers.html"   class="nav-item">🧑‍🏫 &nbsp;Teachers</a>
      <a href="parents.html"    class="nav-item">👨‍👩‍👧 &nbsp;Parents</a>
      <a href="classes.html"    class="nav-item">🏫 &nbsp;Classes</a>
      <a href="subjects.html"   class="nav-item">📚 &nbsp;Subjects</a>
      <div class="sidebar-section-label" style="margin-top:16px;">Academics</div>
      <a href="attendance.html" class="nav-item">📅 &nbsp;Attendance</a>
      <a href="grades.html"     class="nav-item">📈 &nbsp;Grades</a>
      <a href="exams.html"      class="nav-item">📝 &nbsp;Exams</a>
      <a href="timetable.html"  class="nav-item">⏰ &nbsp;Timetable</a>
      <a href="academic-year.html" class="nav-item">🗓️ &nbsp;Academic Year</a>
      <div class="sidebar-section-label" style="margin-top:16px;">System</div>
      <a href="announcements.html" class="nav-item">📢 &nbsp;Announcements</a>
      <a href="reports.html"    class="nav-item">📊 &nbsp;Reports</a>
      <a href="notifications.html" class="nav-item">🔔 &nbsp;Notifications</a>
      <a href="audit-logs.html" class="nav-item">🛡️ &nbsp;Audit Logs</a>
      <a href="settings.html"   class="nav-item">⚙️ &nbsp;Settings</a>
    </nav>
    <div class="sidebar-footer">
      <button id="logout-btn" style="display:flex;align-items:center;gap:9px;padding:9px 12px;border-radius:8px;border:none;background:rgba(239,68,68,.12);color:#f87171;font-size:13px;font-weight:600;cursor:pointer;width:100%;">🚪 &nbsp;Logout</button>
    </div>
  </aside>

  <div class="main-content">
    <header class="top-header">
      <div class="header-search">🔍 <input placeholder="Search…" type="text" id="search-input"></div>
      <div class="header-right">
        <div class="header-user"><div class="header-avatar">A</div><span>Admin</span></div>
      </div>
    </header>

    <div class="page-body">
`;

const footerTemplate = `
    </div>
  </div>
</div>
<script>
  // Highlight active link
  const page = location.pathname.split('/').pop();
  document.querySelectorAll('.nav-item').forEach(link => {
    if (link.getAttribute('href') === page) link.classList.add('active');
  });
  
  const token = localStorage.getItem('access_token');
  if (!token) window.location.href = '../../login.html';
  const logoutBtn = document.getElementById('logout-btn');
  if (logoutBtn) {
    logoutBtn.onclick = () => {
      if(confirm("Are you sure you want to log out?")) {
        localStorage.removeItem('access_token');
        window.location.href = '../../login.html';
      }
    };
  }
</script>
</body>
</html>
`;

const files = fs.readdirSync(dir).filter(f => f.endsWith('.html'));

files.forEach(file => {
  if (file === 'dashboard.html' || file === 'teachers.html' || file === 'layout.html' || file === 'admin.html') return;
  const filePath = path.join(dir, file);
  let content = fs.readFileSync(filePath, 'utf8');
  
  if (content.includes('<!--#include virtual="layout.html" -->')) {
    // Replace the include and meta tag with the full header
    content = content.replace(/<!--#include virtual="layout.html" -->\r?\n?(<meta name="page-title"[^>]*>\r?\n?)?/, headerTemplate);
    
    // Add the footer
    if (!content.includes('</body>')) {
      content += footerTemplate;
    }
    
    fs.writeFileSync(filePath, content);
    console.log("Updated: " + file);
  }
});
