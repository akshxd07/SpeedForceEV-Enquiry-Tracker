# SpeedForce EV - Vehicle Enquiry Tracker

A lightweight Vehicle Enquiry Tracker built for sales enquiry management using **FastAPI** (Backend REST API), **SQLite** (Database), and **Streamlit** (Frontend Dashboard).

---

## Features

- **Backend API (FastAPI):**
  - POST /enquiries: Logs customer enquiries with validation (10-digit Indian phone starting with 6–9 and non-empty name checks).
  - GET /enquiries: Lists enquiries with status and city filter parameters.
  - PATCH /enquiries/{id}/status: Updates enquiry workflow status (New, Contacted, Test Ride Done, Purchased, Lost).
  - DELETE /enquiries/{id}: Removes an enquiry entry.
  - GET /summary: Aggregates total enquiry count grouped by status.
- **Frontend Dashboard (Streamlit):**
  - Form to log customer leads.
  - Interactive table with live status and city filters.
  - Controls to change lead status or delete records.
  - Real-time status summary counts and metrics panel.
  - Bonus Feature: Export filtered lead list as CSV.
- **Automated Tests:** pytest suite validating core endpoint logic, validation rules, and summary counts.

---

## How to Setup & Run

### 1. Clone & Install Dependencies
git clone https://github.com/akshxd07/SpeedForce-EV-Enquiry-Tracker.git
cd SpeedForce-EV-Enquiry-Tracker

# Optional: Create a virtual environment
python -m venv venv
# Windows: venv\Scripts\activate | Mac/Linux: source venv/bin/activate

pip install -r requirements.txt

### 2. Start Backend Server (FastAPI)
uvicorn backend.main:app --reload

*Backend runs on http://127.0.0.1:8000. Interactive Swagger UI docs are at http://127.0.0.1:8000/docs.*

### 3. Start Frontend App (Streamlit)
Open a second terminal window/tab and run:
streamlit run frontend/app.py

*Frontend opens at http://localhost:8501.*

### 4. Run Automated Tests
python -m pytest

---

## Assumptions Made

1. Phone Number Sanitization & Validation:
   - Validates 10-digit Indian mobile numbers starting with 6, 7, 8, or 9.
   - Formatting characters like spaces or dashes are automatically stripped prior to validation.

2. Default Status & Workflow:
   - Newly submitted enquiries default to New status automatically unless explicitly overridden.
   - Status transitions follow: New -> Contacted -> Test Ride Done -> Purchased / Lost.

3. Database Architecture:
   - Uses an embedded SQLite database (sql_app.db) managed via SQLAlchemy ORM, ensuring the project runs out-of-the-box on fresh clones without external database setup.

4. Name Validation:
   - Customer names cannot be empty or consist solely of whitespace characters.
