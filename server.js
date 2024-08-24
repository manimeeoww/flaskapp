const express = require('express');
const cors = require('cors');

const app = express();
const port = process.env.PORT || 3000;

// Enable CORS for all origins (you can specify certain origins if needed)
app.use(cors());

// Define a test route
app.get('/', (req, res) => {
    res.send('Hello, world! Node.js server is running.');
});

// Define your predict route
app.post('/predict', (req, res) => {
    // Placeholder logic for prediction
    res.json({ message: 'Prediction result here' });
});

app.listen(port, () => {
    console.log(`Server is running on http://localhost:${port}`);
});
