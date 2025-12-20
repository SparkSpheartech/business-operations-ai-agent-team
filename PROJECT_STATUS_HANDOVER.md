# SparkSphearAi Agent System - Project Status
**Date:** December 19, 2025
**Status:** Operational (Voice & Multi-Auth Enabled)

## 🚀 Overview
This project contains a multi-agent system powered by **Gemini 2.0-Flash**.
The main entry point is **Daisy** (Executive Assistant), who delegates specialized tasks to **Jayden** (Marketing) and **Onyx** (Engineering).

## 🔑 Key Features Implemented

### 1. Daisy (The Boss)
*   **Model:** `gemini-2.0-flash`
*   **Capabilities:**
    *   **Gmail**: Read/Send emails.
    *   **Calendar**: Manage events.
    *   **Drive/Docs**: Search and read files.
    *   **Sheets**: Manage spreadsheets.
    *   **Tasks**: Manage To-Do lists.
    *   **Smart Home**: Control SDM devices (requires verified Project ID).
    *   **Voice Mode**: Fully conversational via Microphone/Speakers.

### 2. Jayden (Marketing Specialist)
*   **Model:** `gemini-2.5-flash` (Advanced Reasoning)
*   **Capabilities:**
    *   **Blogger**: Posts directly to `sparkspheartechsolutions` blog.
    *   **Facebook**: Posts to Company Page via Business Suite (using `FACEBOOK_BUSINESS_ID`).
    *   **Multi-User Auth**: Uses a **separate** identity (`sparkspheartech4me@gmail.com`) for marketing tools while using the main account for billing.

### 3. Onyx (Engineering)
*   **Model:** `gemini-2.0-flash`
*   **Capabilities:** General coding and technical support.

---

## 🛠️ How to Run

### Option A: Text Interface (Standard)
Best for debugging or silent operation.
```powershell
.\adk.ps1 run daisy_executive_assistant
```

### Option B: Voice Interface (Hands-Free) 🎙️
Talk to Daisy using your microphone.
```powershell
python run_voice.py
```

---

## 📂 Configuration Files

*   **`.env`**: Contains sensitive keys (`GOOGLE_API_KEY`, `FACEBOOK_ACCESS_TOKEN`, `FACEBOOK_BUSINESS_ID`).
*   **`credentials.json`**: Google OAuth Client Secret (App Config).
*   **`token.json`**: Daisy's Login (Main Account).
*   **`token_marketing.json`**: Jayden's Login (Marketing Account).

## 🚧 Next Steps / Roadmap
1.  **Instagram Integration**: Requires complex "Media Container" API setup (currently stubbed).
2.  **Smart Home verification**: Finalize the Google Device Access Console link.
3.  **Document Ingestion**: Add ability for Daisy to read local PDFs/codebases (RAG).

---
**Happy Building!** - *Antigravity*
