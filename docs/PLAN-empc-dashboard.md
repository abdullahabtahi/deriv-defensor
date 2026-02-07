# Implementation Plan: ROI & Business Impact Dashboard

> **Goal:** Visualize the 5.07x ROI improvement to satisfy the "Business Impact" judging criteria (20%).
> **Strategy:** Interactive "What-If" analysis with dynamic sliders to prove model robustness.

---

## 🏗️ Architecture & Layout

### 1. Dual-Location Strategy
We will place ROI metrics in two strategic locations to satisfy both Executive and Technical judges.

#### A. Home Page (The "Hook")
*   **Location:** Top-right Key Metric Card (Hero Section).
*   **Content:**
    *   Headline: **"5.07x ROI"** (Dynamic based on default settings).
    *   Subtext: "vs Random Targeting".
    *   Value: **"$32.1M"** (Projected Profit).

#### B. ROI Analysis Tab (The "Proof")
*   **Location:** Dedicated sidebar page or expandable section `pages/2_ROI_Analysis.py`.
*   **Layout:**
    1.  **Sidebar Controls:** Input sliders for assumptions.
    2.  **Main View:**
        *   **Row 1:** Evaluation Comparison (Bar Chart) - *Primary Visual*.
        *   **Row 2:** Key Metrics Table (Cost vs Revenue).
        *   **Row 3:** Cumulative Profit Curve (Lift Chart) - *Secondary Visual*.

---

## 🧩 Components & Logic

### 1. Interactive Controls (Sidebar)
Allow judges to test their own assumptions.

| Control | Label | Min | Max | Default |
|:---|:---|:---:|:---:|:---:|
| **Slider** | Intervention Cost ($) | $50 | $500 | **$100** |
| **Slider** | Success Rate (%) | 20% | 70% | **40%** |

### 2. Visualizations

#### Primary: Impact Comparison (Bar Chart)
A clear side-by-side comparison of **Random Targeting** vs **AI-Guided Targeting**.
*   **Library:** Plotly Express (`px.bar`).
*   **Data:**
    *   Baseline: `calculate_empc(..., strategy='random')`
    *   AI Model: `calculate_empc(..., strategy='model')`
*   **Annotation:** Show "5.07x Improvement" arrow or label.

#### Secondary: Cumulative Profit Curve (Lift Chart)
*   **Library:** Plotly Graph Objects (`go.Figure`).
*   **X-Axis:** % of Partner Base Contacted.
*   **Y-Axis:** Cumulative Net Profit.
*   **Lines:**
    *   🔴 Random Line (Linear growth).
    *   🟢 Model Line (Steep initial growth = "Skimming the cream").

### 3. Metric Logic (Backend)
Reuse `models/evaluation.py` logic but make it dynamic.

```python
def calculate_dynamic_empc(cost, success_rate):
    # Re-run calculation with new parameters from sliders
    ...
```

---

## 📝 Task Breakdown

### Phase 1: Core Setup
- [ ] Create `dashboard/app.py` (Main entry point).
- [ ] Create `dashboard/utils.py` (Helper functions for metric calc).
- [ ] Load Model & Data (Cached `@st.cache_resource`).

### Phase 2: ROI Logic
- [ ] Port `calculate_empc` to `dashboard/utils.py` with dynamic args.
- [ ] Implement `calculate_random_baseline` for comparison.

### Phase 3: UI Implementation
- [ ] Build **Home Page** Metric Card.
- [ ] Build **ROI Analysis Page**.
    - [ ] Add Sidebar Sliders.
    - [ ] Implement Bar Chart (Plotly).
    - [ ] Implement Lift Curve (Plotly).
    - [ ] metric breakdown table.

---

## ✅ Assessment Criteria
1.  **Interactivity:** Do metrics update instantly when sliders move?
2.  **Clarity:** Is the "5.07x" figure immediately visible on the Home Page?
3.  **Accuracy:** Does the profit calculation match the `evaluation.py` script?
