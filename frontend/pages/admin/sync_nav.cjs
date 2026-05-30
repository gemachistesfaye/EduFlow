const fs = require('fs');
const path = require('path');

const dir = 'e:/GitHub Repo/school-management-system/frontend/pages/admin';

const newNav = `<nav style="flex: 1; overflow-y: auto; padding-right: 4px;">
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
    </nav>`;

const files = fs.readdirSync(dir).filter(f => f.endsWith('.html'));

files.forEach(file => {
  if (file === 'layout.html' || file === 'admin.html') return;
  const filePath = path.join(dir, file);
  let content = fs.readFileSync(filePath, 'utf8');
  
  // Replace the nav block
  content = content.replace(/<nav[\s\S]*?<\/nav>/, newNav);
  
  // Also fix the active link dynamically if it was hardcoded (we already have a script for this, but let's make sure we don't have hardcoded 'active' classes in the nav string)
  // Wait, the newNav has no active classes, so it relies on the script at the bottom.
  // Let's add the active script to the bottom if it's missing.
  if (!content.includes('location.pathname.split(\'/\').pop()')) {
    const activeScript = `
<script>
  document.addEventListener('DOMContentLoaded', () => {
    const page = location.pathname.split('/').pop().replace('.html', '');
    document.querySelectorAll('.nav-item').forEach(link => {
      if (link.getAttribute('href') === page + '.html' || link.getAttribute('href') === page) {
        link.classList.add('active');
      } else {
        link.classList.remove('active');
      }
    });
  });
</script>
</body>`;
    content = content.replace('</body>', activeScript);
  }
  
  fs.writeFileSync(filePath, content);
  console.log("Updated nav in: " + file);
});
