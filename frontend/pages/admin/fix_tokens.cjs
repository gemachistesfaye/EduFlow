const fs = require('fs');
const path = require('path');
const dir = 'e:/GitHub Repo/school-management-system/frontend/pages/admin';
const files = fs.readdirSync(dir).filter(f => f.endsWith('.html'));

files.forEach(file => {
  const filePath = path.join(dir, file);
  let content = fs.readFileSync(filePath, 'utf8');
  content = content.replace(/const token = localStorage\.getItem/g, 'var token = localStorage.getItem');
  fs.writeFileSync(filePath, content);
  console.log('Fixed tokens in ' + file);
});
