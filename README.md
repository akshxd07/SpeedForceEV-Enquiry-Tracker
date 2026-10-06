# SpeedForce EV - Vehicle Enquiry Tracker

A full-stack, lightweight Vehicle Enquiry Tracker built for sales enquiry management using **FastAPI** (Backend REST API), **SQLite** (Database), and **Streamlit** (Frontend Dashboard).

---

## Features

- **Backend API (FastAPI):**
  - `POST /enquiries`: Logs customer enquiries with validation (10-digit Indian phone validation starting with 6–9 and non-empty name checks).
  - `GET /enquiries`: Lists enquiries with status and city filter parameters.
  - `PATCH /enquiries/{id}/status`: Updates enquiry workflow status (`New`, `Contacted`, `Test Ride Done`, `Purchased`, `Lost`).
  - `DELETE /enquiries/{id}`: Removes an enquiry entry.
  - `GET /summary`: Aggregates total enquiry count grouped by status.
- **Frontend Dashboard (Streamlit):**
  - Intuitive form for logging customer leads.
  - Interactive table showing existing records with live city and status filtering.
  - Dedicated controls to update status or delete records.
  - Real-time status summary counts displayed on the sidebar.
  - **Bonus Feature:** One-click CSV export for filtered enquiry data.
- **Automated Tests:** `pytest` suite testing endpoint logic, data validation boundaries, and summary counts.

---

## Repository Structure

```text
SpeedForce-EV-Enquiry-Tracker/
│
├── backend/
│   ├── database.py      # SQLite connection & SQLAlchemy session configuration
│   ├── models.py        # SQLAlchemy models and status Enum definitions
│   ├── schemas.py       # Pydantic schemas for payload validation
│   └── main.py          # FastAPI application & endpoint definitions
│
├── frontend/
│   └── app.py           # Streamlit user interface & API integration
│
├── tests/
│   └── test_main.py     # Pytest automated test cases
│
├── requirements.txt     # Python dependencies
└── README.md            # Documentation & setup guide
