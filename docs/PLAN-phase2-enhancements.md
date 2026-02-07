# Phase 2: VP-Approved Enhancements

**Scope:** 3 features + Mock CRM Demonstration  
**Estimated Effort:** 4-6 hours total  

---

## Feature Overview

| # | Feature | Business Value | Effort |
|---|---------|----------------|--------|
| A | Outcome Tracking | Validates ROI claims, enables model improvement | 1.5h |
| B | Time-to-Churn | Urgency-based prioritization | 2h |
| C | Agentic Intervention Agent | Autonomous workflow orchestration | 2h |
| + | Mock CRM Panel | Demonstrates full vision without API | 30min |

---

## Feature A: Outcome Tracking (Feedback Loop)

### Rationale
Without tracking intervention outcomes, the 5.07x ROI is theoretical. This closes the loop.

### Implementation

#### [NEW] `dashboard/pages/2_Intervention_Log.py`
New page with:
- Table of intervened partners
- Status dropdown: `[Pending] [Saved ✓] [Churned ✗]`
- Timestamp of intervention
- Assigned team member (optional)

#### [MODIFY] `dashboard/utils.py`
Add:
```python
def log_intervention(partner_id, action_type, status="pending"):
    # Append to CSV or SQLite for persistence
    
def get_intervention_history():
    # Retrieve logged interventions
```

#### Data Storage
Use local CSV (`data/intervention_log.csv`) for simplicity:
```csv
partner_id,timestamp,action,status,assigned_to,outcome_date
P18477,2026-02-07T10:00:00,email_sent,pending,,
P10342,2026-02-06T15:30:00,call_scheduled,saved,John,2026-02-07
```

### Verification
- [ ] Can log new intervention from dashboard
- [ ] Can update status (pending → saved/churned)
- [ ] History persists across sessions
- [ ] Summary stats shown (e.g., "42 saved, 12 churned, 156 pending")

---

## Feature B: Time-to-Churn Prediction

### Rationale
Knowing *when* enables urgency triage. A partner churning in 7 days ≠ 90 days.

### Implementation

#### [MODIFY] `models/train_churn_model.py`
Add secondary model or modify output:
```python
# Option 1: Multi-class (7d, 30d, 90d, >90d)
# Option 2: Regression (days until churn)
# Recommendation: Multi-class for cleaner UX
```

#### [MODIFY] `dashboard/app.py`
Update Live Feed to show urgency:
```
🔴 P18477 • Risk: 94% • Churn in: ~7 days
🟡 P10342 • Risk: 88% • Churn in: ~30 days
```

#### Feature Engineering
Add temporal features:
- `days_since_last_payment`
- `trend_velocity` (rate of decline)
- `historical_churn_speed` (for similar profiles)

### Verification
- [ ] Model outputs time bucket prediction
- [ ] Dashboard displays urgency indicator
- [ ] Sorting by urgency works

---

## Feature C: Agentic Intervention Agent

### Rationale
The "wow factor" – autonomous AI that doesn't just predict, but acts.

### Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                   INTERVENTION AGENT                        │
├─────────────────────────────────────────────────────────────┤
│  Trigger:  Partner risk > 85% AND no recent intervention    │
├─────────────────────────────────────────────────────────────┤
│  Workflow:                                                  │
│    1. Generate retention email (GenAI)                      │
│    2. Create intervention log entry                         │
│    3. If Platinum tier → Flag for human review              │
│    4. Schedule follow-up (7 days)                           │
│    5. Emit audit event                                      │
├─────────────────────────────────────────────────────────────┤
│  Guardrails:                                                │
│    - Max 50 interventions/hour                              │
│    - Require human approval for Platinum+                   │
│    - Full audit trail                                       │
└─────────────────────────────────────────────────────────────┘
```

### Implementation

#### [NEW] `agents/intervention_agent.py`
```python
class InterventionAgent:
    def __init__(self, model, explainer, genai):
        self.model = model
        self.explainer = explainer
        self.genai = genai
        
    def scan_for_interventions(self, df, threshold=0.85):
        """Find partners needing intervention."""
        
    def execute_intervention(self, partner_id):
        """Full intervention workflow."""
        # 1. Get explanation
        # 2. Generate email
        # 3. Log intervention
        # 4. Return summary
        
    def batch_process(self, limit=50):
        """Process batch with rate limiting."""
```

#### [NEW] `dashboard/pages/3_Agent_Control.py`
Agent control panel:
- Start/Stop agent
- View agent activity log
- Configure threshold/limits
- Manual override queue

### Verification
- [ ] Agent identifies correct partners
- [ ] Email generation works
- [ ] Audit log captures all actions
- [ ] Rate limiting enforced
- [ ] Platinum partners flagged for review

---

## Mock CRM Panel (Bonus)

### Rationale
Shows full vision without API dependency. Judges understand this is a demo.

### Implementation

#### [NEW] `dashboard/pages/4_CRM_Simulation.py`
Simulated CRM view:
```
┌────────────────────────────────────────┐
│  Salesforce Tasks (Simulated)          │
├────────────────────────────────────────┤
│  ☐ P18477 - Retention Call - Due: 2/8  │
│  ☐ P10342 - Follow-up Email - Due: 2/9 │
│  ✓ P08821 - Completed - Saved          │
└────────────────────────────────────────┘
│  [↗️ In production, syncs with CRM API] │
└────────────────────────────────────────┘
```

### Verification
- [ ] Shows realistic CRM-like interface
- [ ] Disclaimer visible ("Simulation Mode")

---

## Task Breakdown

### Day 1: Foundation & Tracking (Features A + Mock CRM)
- [ ] Create `intervention_log.csv` schema
- [ ] Implement `log_intervention()` utility
- [ ] Build Intervention Log page
- [ ] Build Mock CRM Panel

### Day 2: Time-to-Churn (Feature B)
- [ ] Add temporal features to training data
- [ ] Train time-bucket classifier
- [ ] Update dashboard with urgency indicators

### Day 3: Agentic Agent (Feature C)
- [ ] Implement InterventionAgent class
- [ ] Build Agent Control Panel
- [ ] Add guardrails and audit logging
- [ ] End-to-end testing

---

## Decision Points

> [!IMPORTANT]
> **Time-to-Churn Model Choice**
> - Option 1: Multi-class (7d/30d/90d) – cleaner UX ✅
> - Option 2: Regression (exact days) – more precise but harder to interpret

> [!IMPORTANT]  
> **Agent Execution Mode**
> - Option 1: Manual trigger (user clicks "Run Agent") – safer for demo
> - Option 2: Scheduled (every 15 min) – more realistic but needs monitoring

**Recommendation:** Start with manual trigger, add scheduled option later.

---

## Verification Checklist (Final)

- [ ] Outcome tracking persists and shows stats
- [ ] Time-to-churn displays in dashboard
- [ ] Agent executes full workflow
- [ ] Audit trail captures all agent actions
- [ ] Mock CRM looks professional with disclaimer
