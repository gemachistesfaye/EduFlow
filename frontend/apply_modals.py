import os
import glob

MODAL_HTML = """
<!-- Confirm Modal -->
<div class="modal-overlay" id="confirm-modal" style="z-index: 1000;">
  <div class="modal" style="max-width: 400px; text-align: center; padding: 32px;">
    <h2 style="font-size: 18px; margin-bottom: 12px;" id="confirm-title">Are you sure?</h2>
    <p style="color: #6b7280; margin-bottom: 24px;" id="confirm-msg">This action cannot be undone.</p>
    <div style="display: flex; gap: 12px; justify-content: center;">
      <button class="btn btn-outline" onclick="closeConfirm()" style="flex: 1;">Cancel</button>
      <button class="btn btn-primary" id="confirm-btn" style="flex: 1; background: #ef4444; color: white; border-color: #ef4444;">Confirm</button>
    </div>
  </div>
</div>
"""

JS_FUNCTIONS = """
  let confirmCallback = null;
  function openConfirm(title, msg, callback) {
    document.getElementById('confirm-title').textContent = title;
    document.getElementById('confirm-msg').textContent = msg;
    confirmCallback = callback;
    document.getElementById('confirm-modal').classList.add('open');
  }
  function closeConfirm() { document.getElementById('confirm-modal').classList.remove('open'); }
  document.getElementById('confirm-btn').onclick = () => { if(confirmCallback) confirmCallback(); closeConfirm(); };
"""

LOGOUT_1 = "  document.getElementById('logout-btn').onclick = () => { localStorage.removeItem('access_token'); window.location.href='../../login.html'; };"
LOGOUT_2 = """  document.getElementById('logout-btn').onclick = () => {
    localStorage.removeItem('access_token'); window.location.href = '../../login.html';
  };"""
LOGOUT_NEW = """  document.getElementById('logout-btn').onclick = () => {
    openConfirm("Log Out", "Are you sure you want to log out of your session?", () => {
      localStorage.removeItem('access_token'); window.location.href = '../../login.html';
    });
  };"""

DEL_CLASS_ORIG = """  async function del(id) {
    if (!confirm('Delete class?')) return;
    await fetch(`/api/admin/classes/${id}`, { method:'DELETE', headers:{ Authorization:'Bearer '+token } });
    load();
  }"""

DEL_CLASS_NEW = """  function del(id) {
    openConfirm("Delete Class", "Are you sure you want to permanently delete this class?", async () => {
      await fetch(`/api/admin/classes/${id}`, { method:'DELETE', headers:{ Authorization:'Bearer '+token } });
      load();
    });
  }"""

DEL_TEACHER_ORIG = """  async function del(id) {
    if (!confirm('Delete teacher?')) return;
    await fetch(`/api/admin/teachers/${id}`, { method:'DELETE', headers:{Authorization:'Bearer '+token} });
    load();
  }"""

DEL_TEACHER_NEW = """  function del(id) {
    openConfirm("Delete Teacher", "Are you sure you want to permanently delete this teacher record?", async () => {
      await fetch(`/api/admin/teachers/${id}`, { method:'DELETE', headers:{Authorization:'Bearer '+token} });
      load();
    });
  }"""

def process_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    if 'id="confirm-modal"' in content:
        print(f"Skipping {filepath}")
        return

    content = content.replace('<script>', MODAL_HTML + '\n<script>')
    content = content.replace('<script>', '<script>\n' + JS_FUNCTIONS)
    
    if LOGOUT_1 in content:
        content = content.replace(LOGOUT_1, LOGOUT_NEW)
    elif LOGOUT_2 in content:
        content = content.replace(LOGOUT_2, LOGOUT_NEW)

    if DEL_CLASS_ORIG in content:
        content = content.replace(DEL_CLASS_ORIG, DEL_CLASS_NEW)
        
    if DEL_TEACHER_ORIG in content:
        content = content.replace(DEL_TEACHER_ORIG, DEL_TEACHER_NEW)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Processed {filepath}")

files = glob.glob('e:/GitHub Repo/school-management-system/frontend/pages/admin/*.html')
for f in files:
    process_file(f)
