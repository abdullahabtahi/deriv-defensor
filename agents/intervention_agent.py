"""
Intervention Agent - Simplified for Demo

P3: Agentic AI - Autonomous workflow orchestration with manual trigger.

De-risked scope:
- Manual trigger only (no scheduled complexity)
- Basic rate limiting
- Audit trail via intervention log

Challenge Prompt Alignment:
- "alerts relationship managers before it's too late" -> Autonomous scanning + alert generation
"""

import sys
import os
from typing import List, Dict, Optional

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agents.genai_explainer import GenAIExplainer


class InterventionAgent:
    """
    Simplified autonomous intervention agent for hackathon demo.
    
    Workflow:
    1. Scan partners above risk threshold
    2. Generate GenAI explanation for each
    3. Draft retention email
    4. Log intervention to audit trail
    
    Note: Manual trigger only - no scheduled execution complexity.
    """
    
    def __init__(self, model=None, explainer=None, genai: Optional[GenAIExplainer] = None):
        self.model = model
        self.explainer = explainer
        self.genai = genai or GenAIExplainer()
        self.max_batch_size = 50  # Rate limiting
    
    def scan_for_interventions(self, df, threshold: float = 0.85, limit: int = 25) -> List[Dict]:
        """
        Find partners needing intervention.
        
        Args:
            df: DataFrame with partner data and risk scores
            threshold: Minimum risk score to trigger intervention
            limit: Maximum partners to return
            
        Returns:
            List of partner dictionaries
        """
        if 'risk_score' not in df.columns and 'churn_prob' not in df.columns:
            return []
        
        risk_col = 'risk_score' if 'risk_score' in df.columns else 'churn_prob'
        high_risk = df[df[risk_col] > threshold].nlargest(min(limit, self.max_batch_size), risk_col)
        
        return high_risk.to_dict('records')
    
    def execute_intervention(self, partner_data: Dict) -> Dict:
        """
        Full intervention workflow for one partner.
        
        Workflow:
        1. Generate SHAP-based reason codes (mocked if explainer unavailable)
        2. Generate GenAI explanation
        3. Draft retention email
        4. Log to audit trail
        
        Returns:
            dict with partner_id, explanation, email, logged status
        """
        from dashboard.utils import log_intervention
        
        partner_id = partner_data.get('partner_id', 'Unknown')
        
        # Step 1: Get reason codes
        reason_codes = self._get_reason_codes(partner_data)
        
        # Step 2: Generate explanation
        risk_score = partner_data.get('risk_score', partner_data.get('churn_prob', 0.85))
        explanation = self.genai.generate_narrative(partner_data, risk_score, reason_codes)
        
        # Step 3: Draft email
        email = self.genai.generate_retention_email(partner_data, reason_codes)
        
        # Step 4: Log intervention
        log_intervention(
            partner_id=partner_id,
            action='email',
            status='pending',
            assigned_to='AI Agent'
        )
        
        return {
            'partner_id': partner_id,
            'risk_score': risk_score,
            'explanation': explanation,
            'email': email,
            'reason_codes': reason_codes,
            'logged': True
        }
    
    def batch_process(self, df, threshold: float = 0.85, limit: int = 25) -> List[Dict]:
        """
        Process batch of high-risk partners with rate limiting.
        
        Args:
            df: DataFrame with partner data
            threshold: Risk threshold for intervention
            limit: Max partners to process
            
        Returns:
            List of intervention results
        """
        targets = self.scan_for_interventions(df, threshold, min(limit, self.max_batch_size))
        
        results = []
        for partner in targets:
            result = self.execute_intervention(partner)
            results.append(result)
        
        return results
    
    def _get_reason_codes(self, partner_data: Dict) -> List[Dict]:
        """
        Get reason codes from explainer or generate mocks.
        """
        if self.explainer is not None:
            try:
                return self.explainer.get_reason_codes(partner_data)
            except:
                pass
        
        # Mock reason codes based on partner data
        reason_codes = []
        
        login_trend = partner_data.get('login_trend_30d', 0)
        if login_trend < -30:
            reason_codes.append({
                'feature': 'login_trend_30d',
                'description': f'Login activity dropped {abs(int(login_trend))}% in 30 days',
                'impact_score': min(15, abs(login_trend) / 5)
            })
        
        if partner_data.get('payment_delay_flag', False):
            reason_codes.append({
                'feature': 'payment_delay_flag',
                'description': 'Payment delayed 14+ days',
                'impact_score': 8.5
            })
        
        days_inactive = partner_data.get('days_since_last_interaction', 0)
        if days_inactive > 14:
            reason_codes.append({
                'feature': 'days_since_last_interaction',
                'description': f'No platform interaction for {days_inactive} days',
                'impact_score': min(10, days_inactive / 3)
            })
        
        tickets = partner_data.get('unresolved_ticket_count', 0)
        if tickets > 0:
            reason_codes.append({
                'feature': 'unresolved_ticket_count',
                'description': f'{tickets} unresolved support tickets',
                'impact_score': tickets * 2.5
            })
        
        # Ensure at least one reason code
        if not reason_codes:
            reason_codes.append({
                'feature': 'risk_score',
                'description': 'Elevated behavioral risk indicators',
                'impact_score': 7.0
            })
        
        return sorted(reason_codes, key=lambda x: x['impact_score'], reverse=True)[:3]


if __name__ == "__main__":
    # Test the agent
    import pandas as pd
    
    print("🤖 Testing Intervention Agent...")
    
    agent = InterventionAgent()
    
    # Mock data
    test_df = pd.DataFrame({
        'partner_id': ['P18477', 'P10342', 'P08821'],
        'risk_score': [0.94, 0.88, 0.72],
        'tier': ['Gold', 'Platinum', 'Silver'],
        'region': ['MENA', 'EU', 'APAC'],
        'login_trend_30d': [-80, -45, -20],
        'payment_delay_flag': [True, False, False],
        'days_since_last_interaction': [21, 14, 7],
        'unresolved_ticket_count': [3, 1, 0]
    })
    
    # Scan
    targets = agent.scan_for_interventions(test_df, threshold=0.80)
    print(f"Found {len(targets)} partners above 80% risk")
    
    # Execute single intervention
    if targets:
        result = agent.execute_intervention(targets[0])
        print(f"\n✅ Intervention for {result['partner_id']}:")
        print(f"   Explanation: {result['explanation'][:100]}...")
        print(f"   Logged: {result['logged']}")
