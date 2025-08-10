# AI Product Manager Assistant

This is a Proof of Concept for an AI-powered assistant that helps product managers query data using natural language.

## Features

* Converts natural language questions into SQL queries.
* Presents an execution plan for user review before running.
* Displays mock data results.

## Setup and Running

1.  **Clone the repository:**
    \`\`\`bash
    git clone <your-repo-url>
    cd your-pm-agent
    \`\`\`

2.  **Install backend dependencies:**
    \`\`\`bash
    cd backend
    npm install express dotenv node-fetch@2
    \`\`\`

3.  **Create environment file:**
    * Create a file named `.env` inside the `backend` directory.
    * Add your Google Gemini API key to it:
        \`\`\`
        GEMINI_API_KEY="your_google_api_key_here"
        \`\`\`

4.  **Start the server:**
    \`\`\`bash
    node server.js
    \`\`\`

5.  **Open the application:**
    * Open your web browser and go to `http://localhost:3000`.
