# 🚀 Spark Sphear Solo-preneur OS: Desktop Setup Guide

Welcome to your local business command center. This guide will help you get **Daisy** and her team (Onyx, Travis, and Eissa) running on your local machine.

## 🛠 Prerequisites

1.  **Python 3.11+**: [Download here](https://www.python.org/downloads/)
2.  **uv**: The high-speed package manager.
    *   *Windows*: `powershell -c "irm https://astral.sh/uv/install.ps1 | iex"`
    *   *Mac/Linux*: `curl -LsSf https://astral.sh/uv/install.sh | sh`
3.  **Google Cloud SDK (gcloud)**: [Install Guide](https://cloud.google.com/sdk/docs/install)

---

## 🚀 One-Click Launch

### 1. Authenticate (Only once)
Open your terminal and run:
```bash
gcloud auth login
gcloud auth application-default login
gcloud config set project YOUR_PROJECT_ID
```

### 2. Setup & Run
From inside this folder:
```bash
# Install everything
make install

# Start the Team Playground
make playground
```
**Access the UI at:** `http://127.0.0.1:8501`

---

## 📂 Manual Installation (Alternative)
If you prefer not to use `make`, use `uv` directly:
```bash
uv venv
source .venv/bin/activate  # (or .venv\Scripts\activate on Windows)
uv pip install -r requirements.txt
uv run adk web . --port 8501
```

---

## 👥 Meet Your Team

*   **Daisy (Lead Assistant)**: Your COO. Start conversations here. She manages the roadmap and Gmail.
*   **Onyx (Engineer)**: Handles automation, coding, and technical audits.
*   **Travis (Security/Arch)**: Ensures everything is secure and scalable.
*   **Eissa (Growth/Sales)**: Performs keyword research and market analysis.
*   **Email Drafter**: Specialized tool for professional communication.

---

## 🔑 Environment Variables
Ensure your `.env` file has the following (already configured for you):
- `GOOGLE_CLOUD_PROJECT=gen-lang-client-0323197942`
- `GOOGLE_CLOUD_LOCATION=us-central1`
- `MODEL=gemini-2.5-flash`
- `DISABLE_WEB_DRIVER=1`
