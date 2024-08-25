// server.js

const express = require('express');
const cors = require('cors');
const fileUpload = require('express-fileupload');
const path = require('path');
const fs = require('fs');
const { exec } = require('child_process');

const app = express();
const port = process.env.PORT || 5000;

// Middleware
app.use(cors()); // Enable CORS for all origins (adjust as needed)
app.use(express.json()); // Parse JSON bodies
app.use(express.urlencoded({ extended: true })); // Parse URL-encoded bodies
app.use(fileUpload()); // Enable file upload handling

// Define the /predict endpoint
app.post('/predict', (req, res) => {
    if (!req.files || !req.files.file) {
        return res.status(400).json({ error: 'No file uploaded' });
    }

    const file = req.files.file;
    const uploadPath = path.join(__dirname, 'uploads', file.name);

    // Save the file to the uploads directory
    file.mv(uploadPath, (err) => {
        if (err) {
            return res.status(500).json({ error: 'File upload failed' });
        }

        // Process the uploaded file (e.g., call a prediction script)
        // Replace with your own logic or command to handle the file
        exec(`python3 predict.py ${uploadPath}`, (error, stdout, stderr) => {
            if (error) {
                console.error(`Error executing prediction script: ${stderr}`);
                return res.status(500).json({ error: 'Prediction failed' });
            }

            // Parse prediction results (assumed to be JSON)
            let result;
            try {
                result = JSON.parse(stdout);
            } catch (e) {
                console.error('Error parsing prediction result:', e);
                return res.status(500).json({ error: 'Failed to parse prediction result' });
            }

            // Clean up: delete the uploaded file
            fs.unlink(uploadPath, (err) => {
                if (err) console.error('Error deleting file:', err);
            });

            // Send the result back to the client
            res.json(result);
        });
    });
});

// Start the server
app.listen(port, () => {
    console.log(`Server running at http://localhost:${port}`);
});
