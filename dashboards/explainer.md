# How the Watchtower Dashboard Code Works (Code Architecture Overview)

## 1. Project Structure

The `dashboards` folder is organized into several main parts, each with a specific role:

```
dashboards/
├── backend/      # The main server (API, logic, database)
├── frontend/     # The web dashboard (user interface)
├── streamlit/    # Alternative dashboard (quick prototyping)
├── notebooks/    # Jupyter notebooks for data analysis
├── data/         # Database files and uploads
├── test_api.py   # Script to test the backend API
├── docker-compose.yml  # Orchestrates all services
└── ...           # Other helper/config files
```

---

## 2. Backend (FastAPI, Python)
- **Purpose:** Acts as the "brain" of the system. Handles all data, logic, and communication between parts.
- **Key Files:**
  - `main.py`: The main entry point. Sets up the API, WebSocket, and service initialization.
  - `models/`: Defines database tables and data structures using SQLAlchemy.
  - `services/`: Contains business logic, such as alerting and data processing.
  - `physics/`: Implements the physics-based sensor degradation models.
  - `api/`: Defines the API endpoints (routes) for the frontend and other clients.

**How it works:**
- Receives requests from the frontend (e.g., "give me sensor health").
- Runs calculations (like physics models) and fetches/stores data in the database.
- Sends back results as JSON.
- Provides real-time updates via WebSocket.
- Handles file uploads and data exports.

---

## 3. Frontend (Next.js, TypeScript, Tailwind CSS)
- **Purpose:** The main user interface. What you see in your browser.
- **Key Files:**
  - `pages/`: Each file is a web page (e.g., dashboard, upload, alerts).
  - `components/`: Reusable UI pieces (gauges, tables, alert panels, etc.).
  - `styles/`: Tailwind CSS configuration for the dark/military theme.

**How it works:**
- Fetches data from the backend API and displays it in real time.
- Uses WebSocket to get live updates (e.g., sensor health changes instantly).
- Lets users upload files, view alerts, and export data.
- All UI is built with reusable components for maintainability.

---

## 4. Streamlit App
- **Purpose:** A quick, alternative dashboard for rapid prototyping or data exploration.
- **Key Files:**
  - `app.py`: The main Streamlit script.
- **How it works:** Runs a simple web app that connects to the backend, displays sensor data, and allows basic interaction—great for demos or quick checks.

---

## 5. Jupyter Notebooks
- **Purpose:** For advanced users to do custom data analysis, visualization, or experiments.
- **Key Files:**
  - `.ipynb` files in `notebooks/`
- **How it works:** Users can run Python code interactively, analyze sensor data, and visualize results, all in the browser.

---

## 6. Database (SQLite + SQLAlchemy)
- **Purpose:** Stores all persistent data (sensor readings, uploads, etc.).
- **How it works:** The backend uses SQLAlchemy to interact with a SQLite database file in the `data/` folder. All data is read/written through Python code—no manual database work needed.

---

## 7. WebSocket (Real-Time Updates)
- **Purpose:** Keeps the dashboard live and interactive.
- **How it works:** The backend pushes updates to the frontend instantly (e.g., if a sensor's health changes, the UI updates without refreshing).

---

## 8. Docker & docker-compose
- **Purpose:** Makes it easy to run everything together, no matter your computer setup.
- **How it works:** Each part (backend, frontend, streamlit, jupyter) runs in its own container. `docker-compose.yml` defines how they connect and share data.

---

## 9. Testing & Utilities
- **test_api.py / test_api.ps1:** Scripts to check if the backend API is working as expected.
- **start.bat:** Batch file to start all services easily on Windows.

---

# How It All Fits Together

1. **User opens the dashboard in a browser (frontend).**
2. **Frontend requests data from the backend API.**
3. **Backend fetches data, runs calculations, and returns results.**
4. **Frontend displays the data, updating live via WebSocket.**
5. **User can upload data, trigger exports, or view alerts.**
6. **All data is stored in the database, and advanced users can analyze it in Jupyter.**
7. **Everything is managed and run together using Docker for simplicity.**

---

**In summary:**  
The code is organized so each part has a clear job (backend = logic, frontend = UI, streamlit = quick view, jupyter = analysis, database = storage, docker = orchestration). They communicate through APIs and real-time channels, making the system modular, maintainable, and easy to run.

If you want a more detailed walkthrough of any specific part (e.g., how the physics models are coded, how the WebSocket works, or how the frontend fetches data), just ask! 