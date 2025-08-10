// backend/server.js
require('dotenv').config();
const express = require('express');
const fetch = require('node-fetch'); // Use `node-fetch` version 2 for CommonJS

const app = express();
app.use(express.json());
app.use(express.static('public')); // Serve the index.html file

const GEMINI_API_KEY = process.env.GEMINI_API_KEY;
const GEMINI_API_URL = `https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key=${GEMINI_API_KEY}`;

// This single endpoint will handle both SQL generation and plan generation
app.post('/api/generate', async (req, res) => {
    if (!GEMINI_API_KEY) {
        return res.status(500).json({ error: 'API key not configured.' });
    }

    try {
        const payload = req.body; // Forward the payload from the frontend

        const response = await fetch(GEMINI_API_URL, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });

        if (!response.ok) {
            const errorText = await response.text();
            console.error("Google API Error:", errorText);
            return res.status(response.status).json({ error: `Google API Error: ${errorText}` });
        }

        const data = await response.json();
        res.json(data);

    } catch (error) {
        console.error('Proxy server error:', error);
        res.status(500).json({ error: 'Internal server error.' });
    }
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
    console.log(`Server listening on port ${PORT}`);
});
