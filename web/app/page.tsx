import { KpiCard } from "@/components/dashboard/KpiCard"
import { RiskChart } from "@/components/dashboard/RiskChart"
import { PartnerList } from "@/components/dashboard/PartnerList"
import { MOCK_STATS } from "@/services/api"
import { AlertTriangle, DollarSign, Activity } from "lucide-react"
import Link from "next/link"


import { api } from "@/services/api"

export default async function Home() {
    const stats = await api.getStats()
    const partners = await api.getHighRiskPartners()


    return (
        <div className="space-y-8">
            <div className="flex items-center justify-between">
                <h1 className="text-2xl font-bold text-gray-900">Dashboard Overview</h1>
                <div className="text-sm text-gray-500">Last updated: Just now</div>
            </div>

            {/* KPI Grid */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                <KpiCard
                    title="Total Risk Exposure"
                    value={`$${(stats.totalExposure / 1000000).toFixed(1)}M`}
                    trend={12}
                    trendLabel="from last month"
                    icon={<AlertTriangle size={20} />}
                    color="red"
                />
                <KpiCard
                    title="Recoverable Revenue"
                    value={`$${(stats.recoverableRevenue / 1000000).toFixed(1)}M`}
                    trendLabel="High probability success"
                    icon={<DollarSign size={20} />}
                    color="green"
                />
                <Link href="/interventions" className="block">
                    <KpiCard
                        title="Active Interventions"
                        value={stats.activeInterventions}
                        trendLabel="Assignments pending"
                        icon={<Activity size={20} />}
                        color="blue"
                    />
                </Link>

            </div>

            {/* Main Content Area */}
            <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
                {/* Partner Risks Table */}
                <div className="lg:col-span-2 bg-white p-6 rounded-lg shadow-sm border border-gray-200">
                    <h2 className="text-lg font-semibold mb-4 text-gray-900">High Risk Partners</h2>
                    <PartnerList partners={partners} />
                </div>

                {/* Risk Distribution Chart */}
                <div className="bg-white p-6 rounded-lg shadow-sm border border-gray-200">
                    <h2 className="text-lg font-semibold mb-4 text-gray-900">Risk Distribution</h2>
                    <RiskChart partners={partners} />
                    <div className="mt-4 text-center text-xs text-gray-400">
                        Segmented by churn probability &gt; 50%
                    </div>
                </div>

            </div>
        </div>
    )
}
