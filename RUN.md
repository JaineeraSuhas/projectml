# IDCFSS - Intelligent Data Cleaning & Feature Selection System

This project is a high-performance web application featuring a stunning Vincent Lowe-inspired Vanilla JS/CSS frontend and a Python FastAPI backend for seamless data processing.

## Prerequisites

- Python 3.9+
- pip (Python package installer)

## Setup & Running the Application

1. **Install Backend Dependencies**
   Navigate to the project root and install the required Python packages:
   ```bash
   pip install fastapi uvicorn pandas numpy scikit-learn python-multipart
   ```

2. **Start the Development Server**
   Run the FastAPI backend using `uvicorn`. This serves both the API endpoints and the frontend static files.
   ```bash
   cd backend
   python -m uvicorn main:app --reload --port 8000
   ```

3. **Access the Application**
   Open your browser and navigate to:
   ```
   http://localhost:8000
   ```

## Development Notes

- **Frontend Architecture:** The frontend is intentionally built with pure HTML, CSS, and Vanilla JS. We avoid heavy frameworks like React or Shadcn to ensure blazing fast loading speeds, fluid animations (using `requestAnimationFrame`), and complete control over the bespoke cinematic aesthetic.
- **Dynamic Theming:** The aesthetic is powered by CSS variables (`var(--bg)`, `var(--fg)`). The site defaults to a minimalist Light Mode, but features a beautifully animated Sun/Moon toggle to seamlessly transition into a deep-space Dark Mode with interactive canvas grids.
- **Backend:** `main.py` handles the static file serving for the `frontend/` directory and exposes the `/upload` API for processing data.
