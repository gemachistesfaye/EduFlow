const express = require('express');
const cors = require('cors');
require('dotenv').config();

const app = express();
const PORT = process.env.PORT || 5000;

// Middleware
app.use(cors());
app.use(express.json());

// Basic route
app.get('/api', (req, res) => {
  res.json({ message: 'School Management System Backend API is running...' });
});

app.listen(PORT, () => {
  console.log(`Server is running on port ${PORT}`);
});
