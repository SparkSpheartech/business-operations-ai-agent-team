# 🤖 SparkSphear AI Agents — Google ADK Agent Team

> **A team of autonomous AI agents built with Google Agent Development Kit (ADK)**  
> Daisy, Jayden, Onyx, and Shazaly — working together to run SparkSphear Tech.

---

## 🧠 AI Agent Team Architecture

```mermaid
graph TB
    subgraph TEAM["🤖 SparkSphear AI Agent Team"]
        DAISY[Daisy\nExecutive Assistant Agent]
        JAYDEN[Jayden\nMarketing Agent]
        ONYX[Onyx\nEngineer Agent]
        SHAZ[Shazaly\nCEO Agent]
    end

    subgraph CAPABILITIES["⚡ Agent Capabilities"]
        C1[Task Management]
        C2[Calendar & Scheduling]
        C3[Content Creation]
        C4[Code Development]
        C5[Data Analysis]
        C6[Decision Support]
    end

    subgraph PLATFORM["🔧 Google ADK Platform"]
        P1[Agent Runtime]
        P2[Tool Registry]
        P3[Conversation Memory]
    end

    DAISY --> C1
    DAISY --> C2
    JAYDEN --> C3
    JAYDEN --> C5
    ONYX --> C4
    ONYX --> C5
    SHAZ --> C6
    SHAZ --> C1
    DAISY --> P1
    JAYDEN --> P1
    ONYX --> P1
    SHAZ --> P1
    P1 --> P2
    P1 --> P3

    style DAISY fill:#4CAF50,stroke:#333,color:#fff
    style JAYDEN fill:#2196F3,stroke:#333,color:#fff
    style ONYX fill:#FF9800,stroke:#333,color:#fff
    style SHAZ fill:#9C27B0,stroke:#333,color:#fff
```

## 🤖 AI Agents

| Agent | Role | Function |
|-------|------|----------|
| **Daisy** | Executive Assistant | Task management, calendar, scheduling, admin support |
| **Jayden** | Marketing Agent | Content creation, social media, analytics, SEO |
| **Onyx** | Engineer Agent | Code development, automation, technical build-out |
| **Shazaly** | CEO Agent | Strategic decisions, oversight, coordination |

## 🛠 Tech Stack

| Component | Technology | Agent Role |
|-----------|-----------|------------|
| **Agent Framework** | Google ADK | Agent orchestration & tool use |
| **Runtime** | Python 3.11+ | Agent execution environment |
| **Voice** | `run_voice.py` | Voice interface for agent interaction |
| **Authentication** | `credentials.json` + `token.json` | OAuth for Google services |

## ⚡ Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Run the voice-enabled agent team
python run_voice.py
```

---

Built by **[Shazaly Musa](https://github.com/SparkSpheartech)** — Founder, SparkSphear Tech  
*AI Agents for Business Operations (Powered by Google ADK)*