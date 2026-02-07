"""
GenAI Explainer Agent for Deriv Defensor
Generates natural language explanations for partner churn risk.
"""

from typing import Dict, List, Any


class GenAIExplainer:
    """
    Generates human-readable explanations of partner churn risk using rule-based templates.
    In production, this would integrate with an LLM API for more nuanced explanations.
    """

    def __init__(self):
        """Initialize the explainer with explanation templates."""
        self.risk_thresholds = {
            "critical": 0.7,
            "high": 0.5,
            "medium": 0.3,
            "low": 0.0
        }

    def generate_narrative(self, partner: Dict[str, Any], churn_prob: float, reasons: List[Dict[str, Any]]) -> str:
        """
        Generate a natural language narrative explaining the partner's churn risk.

        Args:
            partner: Dictionary containing partner data
            churn_prob: Churn probability score (0-1)
            reasons: List of risk factors with descriptions and impact scores

        Returns:
            str: Natural language explanation of the churn risk
        """
        partner_id = partner.get('partner_id', 'Unknown')
        risk_level = self._get_risk_level(churn_prob)
        risk_pct = int(churn_prob * 100)

        # Build narrative sections
        header = f"**Risk Assessment for Partner {partner_id}**\n\n"

        summary = f"This partner shows a **{risk_pct}% probability of churn** within the next 30 days ({risk_level.upper()} RISK). "

        if churn_prob >= self.risk_thresholds['critical']:
            summary += "Immediate intervention is strongly recommended.\n\n"
        elif churn_prob >= self.risk_thresholds['high']:
            summary += "Early intervention recommended to prevent disengagement.\n\n"
        else:
            summary += "Monitor closely for any deterioration in engagement.\n\n"

        # Key indicators section
        indicators = "**Key Risk Indicators:**\n\n"
        for i, reason in enumerate(reasons[:5], 1):  # Top 5 reasons
            feature = reason.get('feature', 'Unknown')
            description = reason.get('description', 'No description')
            impact = reason.get('impact_score', 0)

            # Format feature name for readability
            feature_display = self._format_feature_name(feature)

            indicators += f"{i}. **{feature_display}**: {description}"
            if impact:
                indicators += f" (Impact: {impact:.1f}/10)"
            indicators += "\n"

        # Recommendation section
        recommendations = "\n**Recommended Actions:**\n"
        if churn_prob >= self.risk_thresholds['critical']:
            recommendations += "- 🚨 **Immediate personal outreach** by senior relationship manager\n"
            recommendations += "- 📧 Send personalized retention offer within 24 hours\n"
            recommendations += "- 📞 Schedule call to address specific concerns\n"
        elif churn_prob >= self.risk_thresholds['high']:
            recommendations += "- 📧 Send check-in email to assess satisfaction\n"
            recommendations += "- 🎁 Consider offering incentives or support resources\n"
            recommendations += "- 📊 Monitor engagement metrics daily\n"
        else:
            recommendations += "- 👀 Continue standard monitoring\n"
            recommendations += "- 📈 Track for any sudden changes in behavior\n"

        return header + summary + indicators + recommendations

    def _get_risk_level(self, churn_prob: float) -> str:
        """Determine risk level label from probability."""
        if churn_prob >= self.risk_thresholds['critical']:
            return "critical"
        elif churn_prob >= self.risk_thresholds['high']:
            return "high"
        elif churn_prob >= self.risk_thresholds['medium']:
            return "medium"
        else:
            return "low"

    def _format_feature_name(self, feature: str) -> str:
        """Convert feature name to human-readable format."""
        # Map common feature names to readable labels
        feature_map = {
            'login_trend_30d': 'Login Frequency Trend',
            'revenue_velocity': 'Revenue Growth Rate',
            'commission_trend_90d': 'Commission Trajectory',
            'payment_delay_flag': 'Payment Issues',
            'unresolved_ticket_count': 'Support Ticket Backlog',
            'negative_sentiment_score': 'Communication Sentiment',
            'tier_proximity_score': 'Tier Demotion Risk',
            'days_since_last_interaction': 'Engagement Recency',
            'login_count_30d': 'Login Activity',
            'conversion_rate_wow': 'Conversion Performance',
            'dashboard_usage_score': 'Platform Engagement',
            'subnetwork_avg_health_score': 'Network Health',
            'subnetwork_recent_churn_count': 'Network Contagion',
            'tenure_months': 'Partnership Duration',
            'avg_commission_3m': 'Recent Commission Average'
        }

        return feature_map.get(feature, feature.replace('_', ' ').title())
