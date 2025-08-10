# AI Product Manager Assistant

This is a Proof of Concept for an AI-powered assistant that helps product managers query data using natural language.

## Features

* Converts natural language questions into SQL queries.
* Presents an execution plan for user review before running.
* Displays mock data results.

## Quick Start

Get up and running in two commands:

```bash
./scripts/dev_setup.sh  # Setup virtual environment and install dependencies
make run               # Start the FastAPI development server
```

Then browse to:
- **API Documentation**: http://127.0.0.1:8000/docs
- **Health Check**: http://127.0.0.1:8000/ping

## Detailed Setup

### Prerequisites
- Python 3.8+
- Git

### Installation

1.  **Clone the repository:**
    ```bash
    git clone <your-repo-url>
    cd greg-mvp
    ```

2.  **Setup development environment:**
    ```bash
    ./scripts/dev_setup.sh
    ```
    This will:
    - Create a virtual environment
    - Upgrade pip
    - Install all Python dependencies
    - Show installed versions

3.  **Configure environment (optional):**
    ```bash
    cp .env.example .env
    # Edit .env with your API keys
    ```

4.  **Start the server:**
    ```bash
    make run
    ```

### Alternative Running Methods

```bash
# Using Python module
python -m backend.app

# Using uvicorn directly
source venv/bin/activate
uvicorn backend.app.main:app --reload
```

### Available Make Commands

- `make install` - Install dependencies and setup virtual environment
- `make run` - Start the FastAPI development server
- `make test` - Run tests (when available)
- `make versions` - Show installed package versions
- `make lock` - Generate requirements.lock file
- `make clean` - Clean up generated files and cache
- `make env` - Create .env file from .env.example if missing

### Docker (Optional)

```bash
# Build image
docker build -t greg-mvp .

# Run container
docker run -p 8000:8000 greg-mvp
```

## Legacy Node.js Backend

The repository also contains a Node.js/Express backend in `backend/server.js`. To run it:

```bash
cd backend
npm install express dotenv node-fetch@2
node server.js
```

Then browse to http://localhost:3000.
