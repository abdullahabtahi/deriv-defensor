import { PartnerRisk } from "@/types"

// Mock Data Types
export interface DashboardStats {
    totalExposure: number
    recoverableRevenue: number
    activeInterventions: number
    riskTrend: number // Percentage
}

export const MOCK_STATS: DashboardStats = {
    totalExposure: 80700000,
    recoverableRevenue: 24200000,
    activeInterventions: 142,
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
    }
]

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://127.0.0.1:8001"

export const api = {
    getStats: async (): Promise<DashboardStats> => {
        try {
            const response = await fetch(`${API_BASE_URL}/stats`, { cache: 'no-store' })
            if (!response.ok) throw new Error("Failed to fetch stats")
            const data = await response.json()

            // Map FastAPI response (daily_stats table) to DashboardStats interface
            return {
                totalExposure: data.total_revenue_exposed || 0,
                recoverableRevenue: data.total_recovered_revenue || 0,
                activeInterventions: data.total_partners_at_risk || 0,
                riskTrend: 0 // Not yet implemented in backend
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
            return await response.json()
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
    }
}



