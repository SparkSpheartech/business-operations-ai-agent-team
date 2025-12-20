# Daisy AI System: n8n Workflow Implementation Guide

## Introduction
This document provides a detailed, step-by-step technical blueprint for creating the n8n workflows that power the Daisy AI System. Each section outlines a specific workflow's objective, trigger, and a node-by-node implementation guide with key parameter configurations.

---

## Workflow 1: The Prospector & Enricher

### Critical Objective
The primary goal of this workflow is to fully automate the most labor-intensive part of cold outreach: **finding and understanding potential leads**. It takes a high-level search query, finds real businesses, and enriches them with AI-driven insights, producing a high-quality, actionable list for the email drafting stage. This workflow is the engine of Daisy's research capabilities.

### Trigger
*   **Node Type:** `Webhook` (n8n-nodes-base.webhook)
*   **Purpose:** To allow this complex workflow to be started on-demand by a single, simple command.
*   **Key Parameters:**
    *   `HTTP Method`: `POST`
    *   `Path`: `daisy-prospector` (or a unique name of your choice)
    *   `Authentication`: `None` (for ease of use, as the URL is private)

### Node-by-Node Implementation

**1. Apify Actor: Find Leads**
*   **Node Type:** `Apify` (@apify/n8n-nodes-apify.apify)
*   **Purpose:** To execute a pre-built web scraping actor that finds businesses on Google Maps and extracts their data. This is the "get the data" step.
*   **Key Parameters:**
    *   `Operation`: `Run actor and get dataset`
    *   `Actor ID`: `impenetrable_syrup/google-map-leads-with-emails`
    *   `Input`: A JSON object defining the search. Example:
        ```json
        {
            "countryCode": "us",
            "language": "en",
            "locationQuery": "Fort Wayne, IN, USA",
            "onlyWithEmails": true,
            "searchStringsArray": ["Law Firm"]
        }
        ```
    *   **Credentials:** You must select your Apify account credentials.

**2. Item Lists: Split Leads**
*   **Node Type:** `Item Lists` (n8n-nodes-base.itemLists)
*   **Purpose:** The Apify actor returns a single item containing an array of all leads. This node splits that array so that each lead becomes a separate item that can be processed individually in the subsequent steps. This is the "split the data" step.
*   **Key Parameters:**
    *   `Operation`: `Split Out Items`
    *   `Field to Split Out`: `{{ $json.defaultDataset` }} (or whatever field Apify returns the array in)

**3. Code: Standardize Data**
*   **Node Type:** `Code` (n8n-nodes-base.code)
*   **Purpose:** To clean up the raw Apify data and map it to a clean, predictable structure. This prevents errors in later steps and makes the data easier to work with.
*   **Key Parameters:**
    *   `Mode`: `Run Once for Each Item`
    *   `JavaScript`:
        ```javascript
        // Create a clean object with only the fields we care about
        const lead = $input.item.json;
        const cleanLead = {
          title: lead.title,
          address: lead.address,
          city: lead.city,
          state: lead.state,
          website: lead.website,
          // Filter out non-personal or junk emails
          emails: (lead.emails || []).filter(e => e && !e.includes('sentry.wixpress.com') && !e.includes('example.com')),
          facebook: (lead.facebooks || [])[0] || null,
          linkedIn: (lead.linkedIns || [])[0] || null
        };
        return cleanLead;
        ```

**4. Google Gemini: Enrich Data (The "AI Brain")**
*   **Node Type:** `Google Gemini` (@n8n/n8n-nodes-langchain.googleGemini)
*   **Purpose:** This is the core AI enrichment step. It analyzes the cleaned data for each lead and generates the crucial personalization insights.
*   **Key Parameters:**
    *   `Model`: `gemini-pro`
    *   `JSON Output`: `Enabled` (This is critical for the output to be machine-readable)
    *   `Messages > Content`: Use an expression to insert the lead's data into the prompt.
        ```
        As a B2B analyst, your task is to enrich the provided business data. Based on the JSON object below, identify a 'potentialPainPoint' and a 'personalizationHook'.

        - 'potentialPainPoint': Infer a likely business challenge. Be specific (e.g., 'Managing seasonal client intake for a landscaping business,' 'Generating qualified leads for high-value legal services').
        - 'personalizationHook': Find the single most interesting talking point (e.g., their specific legal specialty, a unique feature mentioned on their website, their large number of social media followers).

        Return ONLY the original JSON object for the company, updated with these two new keys.

        Input Data:
        {{ JSON.stringify($json) }}
        ```
    *   **Credentials:** You must select your Google Gemini API credentials.

**5. Item Lists: Aggregate Results**
*   **Node Type:** `Item Lists` (n8n-nodes-base.itemLists)
*   **Purpose:** To merge all the individually processed and enriched leads back into a single item containing a final array.
*   **Key Parameters:**
    *   `Operation`: `Merge`

**6. Write Binary File: Save Final Output**
*   **Node Type:** `Write Binary File` (n8n-nodes-base.writeBinaryFile)
*   **Purpose:** To save the complete, enriched dataset to your computer, ready for Daisy to read and use for drafting emails.
*   **Key Parameters:**
    *   `File Name`: `C:\Users\shaza\Downloads\Daisy - Enriched Leads.json`
    *   `Data`: `{{ JSON.stringify($json) }}`

### Final Output
A single JSON file named `Daisy - Enriched Leads.json` containing a list of all the leads, each one now enriched with a `potentialPainPoint` and a `personalizationHook`.

---

## Workflow 2: The Mail Sender

### Critical Objective
To create a secure, single-purpose, and reusable micro-service for sending emails. By decoupling the sending mechanism, we protect the email credentials and simplify other workflows that need to send mail. This workflow acts as Daisy's dedicated post office.

### Trigger
*   **Node Type:** `Webhook` (n8n-nodes-base.webhook)
*   **Purpose:** To listen for a request containing pre-written email content.
*   **Key Parameters:**
    *   `HTTP Method`: `POST`
    *   `Path`: `daisy-send-mail`

### Node-by-Node Implementation

**1. Send Email: Dispatch Message**
*   **Node Type:** `Send Email` (n8n-nodes-base.sendEmail)
*   **Purpose:** To connect to your email provider and send the email.
*   **Key Parameters:**
    *   `To`: `{{ $json.body.to }}`
    *   `Subject`: `{{ $json.body.subject }}`
    *   `HTML`: `{{ $json.body.html }}` (Using HTML allows for links and formatting)
    *   **Credentials:** Select your securely pre-configured SMTP or email provider credentials for `daisy@sparkspheartechsolutions.com`.

### Final Output
An email is sent to the specified recipient.

---

## Workflow 3: The Automated Follow-up (Advanced)

### Critical Objective
To maximize engagement by ensuring no lead is forgotten. This workflow provides persistence and intelligence, automatically re-engaging prospects who have not responded, thereby increasing the probability of a conversion without any additional manual work.

### Trigger
*   **Node Type:** `Schedule` (n8n-nodes-base.schedule)
*   **Purpose:** To run this check automatically on a recurring basis.
*   **Key Parameters:**
    *   `Interval`: `Every Day`
    *   `Hour`: `9` (To run at 9 AM daily)

### Node-by-Node Implementation

**1. Google Sheets: Get Outreach Status**
*   **Node Type:** `Google Sheets` (n8n-nodes-base.googleSheets)
*   **Purpose:** To read the master list of prospects that have been contacted. (This assumes you are keeping a status log in a spreadsheet).
*   **Key Parameters:**
    *   `Operation`: `Read`
    *   `Spreadsheet ID`: The ID of your master tracking sheet.

**2. IF: Check Follow-up Condition**
*   **Node Type:** `IF` (n8n-nodes-base.if)
*   **Purpose:** To filter for only those leads that need a follow-up.
*   **Key Parameters:**
    *   `Conditions > Date & Time`: Add a condition where the `emailSentDate` from the spreadsheet is `before` a relative date, e.g., `{{ new Date(new Date().setDate(new Date().getDate() - 3)).toISOString() }}` (3 days ago).
    *   `Conditions > String`: Add a condition where the `status` column is `Not Equal` to `Responded`.

**3. HTTP Request: Trigger Mail Sender**
*   **Node Type:** `HTTP Request` (n8n-nodes-base.httpRequest)
*   **Purpose:** To call the "Mail Sender" workflow we created (Workflow 2) for each lead that passes the `IF` condition. This promotes reusability.
*   **Key Parameters:**
    *   `Method`: `POST`
    *   `URL`: The webhook URL for Workflow 2 (`.../daisy-send-mail`).
    *   `Body Content Type`: `JSON`
    *   `Body`:
        ```json
        {
          "to": "{{ $json.email }}",
          "subject": "Re: {{ $json.originalSubject }}",
          "html": "Hello,<br><br>Just following up on my previous note. Would you be open to taking 5 minutes to try our complimentary Operational Efficiency Assessment?<br><br>You can access it here: [LINK TO YOUR WEB APP]<br><br>Best regards,<br>Daisy"
        }
        ```

**4. Google Sheets: Update Status**
*   **Node Type:** `Google Sheets` (n8n-nodes-base.googleSheets)
*   **Purpose:** To update the lead's status so they do not receive more follow-ups.
*   **Key Parameters:**
    *   `Operation`: `Update`
    *   Use the `rowIndex` from the trigger sheet and set the `status` column to `Follow-up Sent`.

### Final Output
Follow-up emails are sent to cold leads, and their status is updated in the tracking sheet.
