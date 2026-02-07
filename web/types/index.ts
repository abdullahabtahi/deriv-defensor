export interface PartnerRisk {
    partner_id: str
    region: str
    tier: 'Bronze' | 'Silver' | 'Gold' | 'Platinum'
    churn_prob: number
    risk_category: 'High' | 'Medium' | 'Low'
    ltv: number
    login_trend_30d: number
    urgency_score: number
    status?: string
}

export interface Intervention {
    id: string
    partner_id: string
    action_type: string
    status: 'Pending' | 'Completed' | 'Failed'
    timestamp: string
}
