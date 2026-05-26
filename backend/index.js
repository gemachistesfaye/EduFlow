import dotenv from 'dotenv';
dotenv.config();
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

// Google client ID endpoint
app.get('/api/config/google-client-id', (req, res) => {
  res.json({ clientId: process.env.GOOGLE_CLIENT_ID });
});

app.listen(PORT, () => {
  console.log(`Server is running on port ${PORT}`);
});
