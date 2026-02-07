import { PartnerRisk } from "@/types"

// Mock Data Types
export interface DashboardStats {
    totalExposure: number
    recoverableRevenue: number
    activeInterventions: number
    riskTrend: number // Percentage
}

export const MOCK_STATS: DashboardStats = {
    totalExposure: 12500000,
    recoverableRevenue: 4200000,
    activeInterventions: 1240,
    riskTrend: 12
}

export const MOCK_PARTNERS = [
    {
        partner_id: "P11972",
        region: "Latin America",
        tier: "Gold",
        churn_prob: 0.95,
        risk_category: "High",
        ltv: 125000,
        login_trend_30d: -85,
        urgency_score: 92
    },
    {
        partner_id: "P88231",
        region: "Asia Pacific",
        tier: "Platinum",
        churn_prob: 0.78,
        risk_category: "High",
        ltv: 340000,
        login_trend_30d: -45,
        urgency_score: 75
    },
    {
        partner_id: "P22104",
        region: "Europe",
        tier: "Silver",
        churn_prob: 0.65,
        risk_category: "Medium",
        ltv: 45000,
        login_trend_30d: -20,
        urgency_score: 45
    },
    {
        partner_id: "P33892",
        region: "Africa",
        tier: "Bronze",
        churn_prob: 0.55,
        risk_category: "Medium",
        ltv: 12000,
        login_trend_30d: -15,
        urgency_score: 40
    },
    {
        partner_id: "P44512",
        region: "CIS",
        tier: "Silver",
        churn_prob: 0.48,
        risk_category: "Medium",
        ltv: 38000,
        login_trend_30d: -10,
        urgency_score: 35
    },
    {
        partner_id: "P55102",
        region: "MENA",
        tier: "Gold",
        churn_prob: 0.82,
        risk_category: "High",
        ltv: 95000,
        login_trend_30d: -60,
        urgency_score: 80
    },
    {
        partner_id: "P66201",
        region: "Latin America",
        tier: "Platinum",
        churn_prob: 0.35,
        risk_category: "Low",
        ltv: 210000,
        login_trend_30d: 5,
        urgency_score: 20
    },
    {
        partner_id: "P77394",
        region: "Asia Pacific",
        tier: "Silver",
        churn_prob: 0.52,
        risk_category: "Medium",
        ltv: 28000,
        login_trend_30d: -12,
        urgency_score: 38
    },
    {
        partner_id: "P88410",
        region: "Europe",
        tier: "Bronze",
        churn_prob: 0.25,
        risk_category: "Low",
        ltv: 8000,
        login_trend_30d: 10,
        urgency_score: 15
    },
    {
        partner_id: "P99505",
        region: "Africa",
        tier: "Gold",
        churn_prob: 0.60,
        risk_category: "Medium",
        ltv: 75000,
        login_trend_30d: -18,
        urgency_score: 55
    }
]

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://127.0.0.1:8001"

export const api = {
    getStats: async (): Promise<DashboardStats> => {
        try {
            const response = await fetch(`${API_BASE_URL}/stats`, { cache: 'no-store' })
            if (!response.ok) throw new Error("Failed to fetch stats")
            const data = await response.json()

            // HYBRID APPROACH: Use MOCK_STATS as baseline to ensure high numbers for demo, 
            // but allow backend to add to it if available. 
            // This ensures "Active Interventions" is always > 1000 as requested.
            return {
                totalExposure: MOCK_STATS.totalExposure + (data.total_revenue_exposed || 0),
                recoverableRevenue: MOCK_STATS.recoverableRevenue + (data.total_recovered_revenue || 0),
                activeInterventions: MOCK_STATS.activeInterventions + (data.total_partners_at_risk || 0),
                riskTrend: 12
            }
        } catch (error) {
            console.error("Error fetching stats:", error)
            return MOCK_STATS
        }
    },

    getHighRiskPartners: async () => {
        try {
            const response = await fetch(`${API_BASE_URL}/partners?limit=10`)
            if (!response.ok) throw new Error("Failed to fetch partners")
            const realPartners = await response.json()

            // HYBRID APPROACH: Combine generic mock partners with real backend partners
            // This ensures the list is always populated and diverse
            return [...realPartners, ...MOCK_PARTNERS].slice(0, 15) // Limit to 15 mixed
        } catch (error) {
            console.error("Error fetching partners:", error)
            return MOCK_PARTNERS
        }
    },

    getPartner: async (id: string) => {
        try {
            const response = await fetch(`${API_BASE_URL}/partners/${id}`)
            if (!response.ok) throw new Error("Failed to fetch partner")
            return await response.json()
        } catch (error) {
            console.error("Error fetching partner:", error)
            return null
        }
    },

    getPartnerSummary: async (id: string) => {
        try {
            const response = await fetch(`${API_BASE_URL}/partners/${id}/summary`)
            if (!response.ok) throw new Error("Failed to fetch summary")
            return await response.json()
        } catch (error) {
            console.error("Error fetching summary:", error)
            return null
        }
    },

    getInterventions: async () => {
        try {
            const response = await fetch(`${API_BASE_URL}/interventions`)
            if (!response.ok) throw new Error("Failed to fetch interventions")
            return await response.json()
        } catch (error) {
            console.error("Error fetching interventions:", error)
            return []
        }
    },

    triggerIntervention: async (id: string) => {
        try {
            const response = await fetch(`${API_BASE_URL}/partners/${id}/trigger`, {
                method: 'POST'
            })
            if (!response.ok) throw new Error("Failed to trigger intervention")
            return await response.json()
        } catch (error) {
            console.error("Error triggering intervention:", error)
            return null
        }
    }
}



