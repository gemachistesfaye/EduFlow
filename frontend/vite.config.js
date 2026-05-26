import { defineConfig } from 'vite';
import { resolve } from 'path';

export default defineConfig({
  root: 'frontend',
  base: '/',
  build: {
    outDir: '../dist',
    emptyOutDir: true,
    rollupOptions: {
      input: {
        login: resolve(__dirname, 'frontend/login.html'),
        adminDashboard: resolve(__dirname, 'frontend/pages/admin/dashboard.html'),
        adminStudents: resolve(__dirname, 'frontend/pages/admin/students.html'),
        adminTeachers: resolve(__dirname, 'frontend/pages/admin/teachers.html'),
        adminClasses: resolve(__dirname, 'frontend/pages/admin/classes.html'),
        adminAttendance: resolve(__dirname, 'frontend/pages/admin/attendance.html'),
        adminGrades: resolve(__dirname, 'frontend/pages/admin/grades.html'),
        adminSettings: resolve(__dirname, 'frontend/pages/admin/settings.html'),
        studentDashboard: resolve(__dirname, 'frontend/pages/student/dashboard.html'),
        studentAttendance: resolve(__dirname, 'frontend/pages/student/attendance.html'),
        studentGrades: resolve(__dirname, 'frontend/pages/student/grades.html'),
        studentSettings: resolve(__dirname, 'frontend/pages/student/settings.html'),
        teacherDashboard: resolve(__dirname, 'frontend/pages/teacher/dashboard.html'),
        teacherStudents: resolve(__dirname, 'frontend/pages/teacher/students.html'),
        teacherAttendance: resolve(__dirname, 'frontend/pages/teacher/attendance.html'),
        teacherGrades: resolve(__dirname, 'frontend/pages/teacher/grades.html'),
        teacherSettings: resolve(__dirname, 'frontend/pages/teacher/settings.html')
      }
    }
  }
});
