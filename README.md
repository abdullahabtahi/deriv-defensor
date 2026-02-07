# Deriv Defensor
> **The Agentic Decisioning Platform for Partner Retention.**

![Dashboard Overview](docs/images/dashboard-hero.png)

## 🚨 The $10M Problem
Affiliate partner churn is a silent revenue killer. By the time a high-value partner stops referring, it's too late. Traditional dashboards show you *what* happened. **Defensor shows you what *will* happen—and fixes it.**

### 💼 Business Impact (Simulated)
Based on our validation with generated transactional data:
- **$1.2M+** Potential Annual Revenue Saved
- **74%** Intervention Success Rate
- **88%** High-Risk Detection Precision

---

## 🛡️ The Solution: Agentic Defense

Defensor is not just a dashboard—it's an autonomous intervention system.

### 1. **Predictive Surveillance (The "Eyes")**
Real-time ingestion of partner behavior signals (commission drops, login gaps, sub-affiliate inactivity).
- **Tech:** LightGBM + SHAP (Explainable AI)
- **Output:** Dynamic Risk Scores (0-100)

### 2. **GenAI Intelligence (The "Brain")**
It doesn't just flag risk; it explains *why*. The system automatically drafts personalized retention strategies.
- **Tech:** LLM Integration
- **Output:** Natural Language Briefings & Email Drafts

### 3. **Autonomous Intervention (The "Hands")**
One-click or fully automated outreach execution.
- **Tech:** Agentic Workflow
- **Output:** Instant Email Execution & CRM Logging

---

## 🏗️ Technical Architecture

Built for scale, speed, and reliability.

```mermaid
graph TD
    Client[Next.js 14 Client] --> API[FastAPI Gateway]
    API --> Agent[Agentic Brain]
    Agent --> ML[LightGBM Model]
    Agent --> DB[(Supabase PostgreSQL)]
    
    subgraph "Intelligence Layer"
    ML -- "Risk Scores" --> Agent
    end
```

| Component | Tech Stack |
|-----------|------------|
| **Frontend** | Next.js 14 (App Router), Tailwind CSS, Shadcn/UI |
| **Backend** | FastAPI (Python), Pydantic |
| **Database** | Supabase (PostgreSQL + RLS) |
| **AI/ML** | LightGBM, SHAP, LLMs |

---

## 🚀 Quick Start

### Prerequisites
- Node.js 18+
- Python 3.10+
- Supabase Account

### Installation

1. **Clone & Install**
   ```bash
   git clone https://github.com/yourusername/deriv-defensor.git
   cd deriv-defensor
   
   # Backend
   pip install -r requirements.txt
   
   # Frontend
   cd web && npm install
   ```

2. **Environment Setup**
   Create `.env` files in root and `/web` (see `.env.example`).

3. **Run Development**
   ```bash
   # Terminal 1: Backend
   ./backend/run.sh
   
   # Terminal 2: Frontend
   cd web && npm run dev
   ```

---

## 🏆 Hackathon Context
**Built for the Deriv Advanced Agentic AI Challenge.**
*Team: [Your Team Name]*

---
*Defensor: predicting the preventable, protecting the profitable.*
