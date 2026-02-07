import os
import random
from typing import List, Dict, Optional
try:
    import anthropic
except ImportError:
    anthropic = None

class GenAIExplainer:
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv('ANTHROPIC_API_KEY')
        self.client = None
        
        if self.api_key and anthropic:
            try:
                self.client = anthropic.Anthropic(api_key=self.api_key)
            except Exception as e:
                print(f"Warning: Failed to initialize Anthropic client: {e}")
                self.client = None
    
    def generate_narrative(self, partner_data: Dict, risk_score: float, reason_codes: List[Dict]) -> str:
        """
        Generate a manager-friendly explanation for the partner's churn risk.
        """
        if self.client:
            return self._generate_with_llm(partner_data, risk_score, reason_codes)
        else:
            return self._generate_template(partner_data, risk_score, reason_codes)

    def generate_retention_email(self, partner_data: Dict, reason_codes: List[Dict]) -> str:
        """
        Generate a draft retention email for the Relationship Manager to send.
        """
        if self.client:
            return self._generate_email_with_llm(partner_data, reason_codes)
        else:
            return self._generate_email_template(partner_data, reason_codes)

    def _generate_email_template(self, partner_data: Dict, reason_codes: List[Dict]) -> str:
        """
        Deterministic email template fallback.
        """
        name = partner_data.get('partner_id', 'Partner')
        primary_issue = reason_codes[0]['description'].lower() if reason_codes else "recent account activity"
        
        subject = f"Improving your Deriv partnership - {name}"
        
        body = f"""Subject: {subject}

Hi {name},

I noticed {primary_issue}, and I wanted to reach out personally.

We view you as a key partner in the {partner_data.get('region', 'Global')} region. I'd love to schedule a quick 10-minute call to discuss how we can support you better this month.

Are you free this Thursday after 2 PM?

Best regards,
Deriv Partnership Team"""
        return body

    def _generate_email_with_llm(self, partner_data: Dict, reason_codes: List[Dict]) -> str:
        """
        Use Claude to draft a personalized email.
        """
        try:
            reasons_text = ", ".join([r['description'] for r in reason_codes])
            prompt = f"""
            Draft a short, empathetic retention email to a churn-risk partner.
            
            Partner Context:
            - ID: {partner_data.get('partner_id')}
            - Tier: {partner_data.get('tier')}
            - Risk Factors: {reasons_text}
            
            Tone: Professional but personal. Focus on solutions, not the problem. Keep it under 100 words.
            """
            
            message = self.client.messages.create(
                model="claude-3-sonnet-20240229",
                max_tokens=200,
                temperature=0.7,
                messages=[{"role": "user", "content": prompt}]
            )
            return message.content[0].text.strip()
        except Exception:
            return self._generate_email_template(partner_data, reason_codes)

    def _generate_template(self, partner_data: Dict, risk_score: float, reason_codes: List[Dict]) -> str:
        """
        Fallback deterministic generator when no API key is available.
        """
        risk_level = "High" if risk_score > 0.7 else "Medium" if risk_score > 0.3 else "Low"
        
        if not reason_codes:
            return f"Partner is {risk_level} Risk ({risk_score:.1%}). No specific risk factors identified."
            
        primary_reason = reason_codes[0]
        secondary_reason = reason_codes[1] if len(reason_codes) > 1 else None
        
        # Template logic
        tier = partner_data.get('tier', 'Unknown')
        text = f"Partner is {risk_level} Risk ({risk_score:.1%}) [{tier} Tier]. "
        text += f"Primary driver is {primary_reason['description'].lower()}."
        
        if secondary_reason:
            text += f" Also showing signs of {secondary_reason['description'].lower()}."
            
        # Actionable recommendation
        text += " " + self._get_recommendation(primary_reason['feature'])
        
        return text

    def _get_recommendation(self, feature: str) -> str:
        recommendations = {
            'payment_delay_flag': "Immediate finance callback recommended.",
            'days_since_last_interaction': "Schedule a check-in call to re-engage.",
            'login_trend_30d': "Send 'What's New' newsletter or platform demo.",
            'tier_proximity_score': "Highlight benefits of maintaining current tier.",
            'subnetwork_recent_churn_count': "Urgent: Master affiliate network audit required.",
            'negative_sentiment_score': "Senior manager should review recent support tickets."
        }
        return recommendations.get(feature, "Review account status.")

    def _generate_with_llm(self, partner_data: Dict, risk_score: float, reason_codes: List[Dict]) -> str:
        """
        Use Claude to generate a nuanced, human-like explanation.
        """
        try:
            reasons_text = "\\n".join([
                f"- {r['description']} (Impact: {r['impact_score']:.1f})" 
                for r in reason_codes
            ])
            
            prompt = f"""
            You are a CRM assistant. Explain why this partner is at {risk_score:.1%} churn risk.
            
            Top Risk Factors:
            {reasons_text}
            
            Partner Context:
            - Region: {partner_data.get('region')}
            - Tier: {partner_data.get('tier')}
            
            Output a 2-sentence summary for a Relationship Manager. Be direct and actionable. No greeting.
            """
            
            message = self.client.messages.create(
                model="claude-3-sonnet-20240229",
                max_tokens=100,
                temperature=0.7,
                messages=[{"role": "user", "content": prompt}]
            )
            return message.content[0].text.strip()
            
        except Exception as e:
            print(f"LLM Generation failed: {e}. Falling back to template.")
            return self._generate_template(partner_data, risk_score, reason_codes)

if __name__ == "__main__":
    # Test
    explainer = GenAIExplainer()
    
    dummy_data = {'region': 'LATAM', 'tier': 'Gold'}
    dummy_reasons = [
        {'feature': 'payment_delay_flag', 'description': 'Payment delayed', 'impact_score': 10.0},
        {'feature': 'days_since_last_interaction', 'description': 'Silent for 21 days', 'impact_score': 5.0}
    ]
    
    print("Test Narrative:")
    print(explainer.generate_narrative(dummy_data, 0.85, dummy_reasons))
