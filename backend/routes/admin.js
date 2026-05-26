import express from 'express';
import { authorize } from '../middleware/authorize.js';
import { ROLE } from '../config/roles.js';

const router = express.Router();

// Example: /api/admin/billing – accessible only to SCHOOL_ADMIN (80) and above
router.get('/admin/billing', authorize(ROLE.SCHOOL_ADMIN.level), (req, res) => {
  // Placeholder: real billing logic would go here
  res.json({ message: 'Billing dashboard – authorized access' });
});

// Example: /api/superadmin/backups – only SUPER_ADMIN (100)
router.get('/superadmin/backups', authorize(ROLE.SUPER_ADMIN.level), (req, res) => {
  res.json({ message: 'System backups – super admin only' });
});

export default router;
