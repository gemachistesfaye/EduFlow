import { defineConfig } from 'vite';
import { resolve } from 'path';

export default defineConfig({
  root: '.',
  base: '/',
  build: {
    outDir: '../dist',
    emptyOutDir: true,
    rollupOptions: {
      input: {
        login: resolve(__dirname, 'login.html'),
        adminDashboard: resolve(__dirname, 'pages/admin/dashboard.html'),
        adminStudents: resolve(__dirname, 'pages/admin/students.html'),
        adminTeachers: resolve(__dirname, 'pages/admin/teachers.html'),
        adminClasses: resolve(__dirname, 'pages/admin/classes.html'),
        adminAttendance: resolve(__dirname, 'pages/admin/attendance.html'),
        adminGrades: resolve(__dirname, 'pages/admin/grades.html'),
        adminSettings: resolve(__dirname, 'pages/admin/settings.html'),
        studentDashboard: resolve(__dirname, 'pages/student/dashboard.html'),
        studentAttendance: resolve(__dirname, 'pages/student/attendance.html'),
        studentGrades: resolve(__dirname, 'pages/student/grades.html'),
        studentSettings: resolve(__dirname, 'pages/student/settings.html'),
        teacherDashboard: resolve(__dirname, 'pages/teacher/dashboard.html'),
        teacherStudents: resolve(__dirname, 'pages/teacher/students.html'),
        teacherAttendance: resolve(__dirname, 'pages/teacher/attendance.html'),
        teacherGrades: resolve(__dirname, 'pages/teacher/grades.html'),
        teacherSettings: resolve(__dirname, 'pages/teacher/settings.html')
      }
    }
  }
});
