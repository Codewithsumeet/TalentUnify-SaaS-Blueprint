# OpenCATS ATS - Lightweight Integration Guide

## 📌 Overview
Hello Team (Device 2)! 
You are tasked with building the **Applicant Tracking System (ATS)** using a lightweight, stripped-down version of [OpenCATS](https://github.com/opencats/OpenCATS.git). Your system will act as one of the primary ingestion sources for our central AI recruiting platform: **TalentFlow** (being built on Device 1).

TalentFlow uses a modern stack (Next.js, FastAPI, PostgreSQL, Pinecone, LlamaParse). OpenCATS is a traditional PHP/MySQL monolith. Our goal is to extract *just* the candidate and job tracking features from OpenCATS and seamlessly integrate them into TalentFlow's AI parsing engine.

## 🎯 Goal: The "Lite" OpenCATS
OpenCATS is massive. Please strip out or disable modules that are NOT absolutely essential. 
**Keep ONLY the following core modules:**
1. **CandidatesModule:** Adding, editing, and storing candidate profiles and attached Resumes (PDF/DOCX).
2. **JobOrders Module:** Creating and tracking active job openings.
3. **Pipelines / Activity:** Moving candidates through stages (Screening, Interview, Hired).

**Disable/Remove:** CRM, Invoicing, Calendar, complex reporting, and email campaign modules. We want this to be extremely fast and lightweight.

---

## 🔗 Integration Architecture: How We Connect

Because your system is the "Source of Truth" for raw applications, we need your ATS to communicate with the TalentFlow AI Backend. We will use a **Webhook / REST Integration Strategy**.

### Option 1: Webhooks (Recommended)
When a recruiter uploads a new candidate & resume into your OpenCATS system, OpenCATS should immediately fire a webhook payload to the TalentFlow FastAPI backend.

**Your Task:**
Write a simple PHP cURL trigger inside the `Candidates.php` add-hook.
*   **Destination:** `POST http://<talentflow_ip>:8000/api/v1/integrations/ats/webhook`
*   **Payload:**
```json
{
  "source": "opencats",
  "ats_candidate_id": "1049",
  "first_name": "Jane",
  "last_name": "Doe",
  "email": "jane.doe@example.com",
  "resume_url": "http://<opencats_ip>/attachments/resume_1049.pdf",
  "job_order_id": "42"
}
```
*TalentFlow will grab the `resume_url`, process it using LlamaParse & Pinecone, and compute the AI Match Score.*

### Option 2: Polling API (Fallback)
If webhooks are too complex to build into the legacy PHP codebase, build a simple read-only REST endpoint on your end.
**Your Task:**
Create `/api/candidates/recent.php`
*   **Behavior:** Returns a JSON list of all candidates added in the last 24 hours, along with secure, direct links to download their `.pdf`. TalentFlow's Celery tasks will poll this endpoint every hour.

## 🛠️ Action Items for Device 2
1. Clone the `opencats` repository.
2. Remove legacy clutter and run it via Docker (`docker-compose up` preferably) so it is isolated.
3. Test the basic upload flow of a Candidate.
4. Implement the simple Webhook push to TalentFlow's local IP address or expose the REST endpoint.
5. Provide Device 1 with your Local IP and Port to test the connection.
