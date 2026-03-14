# HRMS - Lightweight Integration Guide

## 📌 Overview
Hello Team (Device 3)!
You are building the **Human Resources Management System (HRMS)**. This system serves as the post-hire employee destination. Once the AI platform (**TalentFlow**, on Device 1) identifies and successfully places a candidate, that candidate crosses the bridge and becomes an "Employee" in your HRMS.

TalentFlow uses a modern stack (Next.js, FastAPI, PostgreSQL). Your HRMS should also be built loosely coupled, exposing clean APIs to accept incoming successful hires and provide workforce layout data (Departments, Roles) back to the AI.

## 🎯 Goal: The "Lite" HRMS
We do NOT need a fully bloated enterprise HRMS for this prototype. Please focus on a microservice approach that handles core employee lifecycles.

**Keep ONLY the following core modules:**
1. **Employee Directory:** Name, Role, Email, Manager, Start Date.
2. **Onboarding Status:** Tracking whether they have completed basic paperwork.
3. **Department/Role Structure:** A taxonomy of the company's teams (Engineering, Sales, etc.).

**Skip:** Payroll processing, complex tax calculations, performance reviews, and heavy asset management.

---

## 🔗 Integration Architecture: How We Connect

The connection between TalentFlow and the HRMS is a **Two-Way Synchronization**:

### 1. The Handoff (TalentFlow → HRMS)
When a recruiter clicks "Mark as Hired" in TalentFlow, the AI will send a clean, structured payload to your HRMS to seamlessly convert the "Candidate" into an "Employee".

**Your Task:**
Expose an ingestion API endpoint:
*   **Endpoint:** `POST /api/employees/onboard`
*   **Expected Payload:**
```json
{
  "talentflow_candidate_id": "cnd_928173",
  "first_name": "John",
  "last_name": "Smith",
  "personal_email": "john@email.com",
  "work_email": "jsmith@company.com",
  "department_id": "engineering",
  "role": "Senior Frontend Developer",
  "top_skills": ["React", "Typescript", "Next.js"],
  "hire_date": "2026-03-20"
}
```
*   **Action:** Your HRMS takes this payload and creates a new Employee Record, initiating their "Onboarding" status.

### 2. The Context Sync (HRMS → TalentFlow)
TalentFlow's AI needs to know what the current company structure looks like so it can accurately match candidates to departments.

**Your Task:**
Expose a read-only endpoint for TalentFlow to pull company structure.
*   **Endpoint:** `GET /api/structure/departments`
*   **Response:**
```json
{
  "departments": [
    { "id": "eng", "name": "Engineering", "open_headcount": 3 },
    { "id": "sls", "name": "Sales", "open_headcount": 1 }
  ]
}
```

## 🛠️ Action Items for Device 3
1. Set up a lightweight backend (Express.js, Django, or FastAPI) and a simple frontend dashboard.
2. Define the Employee and Department database schemas.
3. Create the `POST /api/employees/onboard` endpoint and test it via Postman or cURL.
4. Expose the API to the local network so Device 1 (TalentFlow) can route successful candidates to you.
5. Ensure your system rejects duplicate emails to maintain database integrity.
