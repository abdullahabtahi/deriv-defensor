"use client"

import { useEffect, useState } from "react"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { AlertTriangle, TrendingUp, Clock } from "lucide-react"

interface Partner {
    partner_id: string
    region: string
    tier: string
    churn_prob: number
    risk_category: string
    ltv: number
    login_trend_30d: number
    urgency_score: number
}

export default function AlertsPage() {
    const [alerts, setAlerts] = useState<Partner[]>([])
    const [loading, setLoading] = useState(true)

    useEffect(() => {
        async function fetchAlerts() {
            try {
                const response = await fetch('http://localhost:8001/partners?limit=50')
                const partners = await response.json()

                // Filter for high-risk partners (churn_prob > 0.7)
                const highRisk = partners
                    .filter((p: Partner) => p.churn_prob >= 0.7)
                    .sort((a: Partner, b: Partner) => b.urgency_score - a.urgency_score)
                    .slice(0, 15)

                setAlerts(highRisk)
            } catch (error) {
                console.error('Error fetching alerts:', error)
            } finally {
                setLoading(false)
            }
        }

        fetchAlerts()
    }, [])

    if (loading) {
        return <div className="p-8">Loading alerts...</div>
    }

    const criticalCount = alerts.filter(a => a.urgency_score >= 80).length
    const highCount = alerts.filter(a => a.urgency_score >= 60 && a.urgency_score < 80).length
    const mediumCount = alerts.filter(a => a.urgency_score < 60).length

    return (
        <div className="space-y-6">
            <div>
                <h1 className="text-3xl font-bold text-gray-900">Alert Monitor</h1>
                <p className="text-gray-500 mt-1">Real-time high-risk partner surveillance</p>
            </div>

            {/* Alert Summary */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                <Card className="border-red-200 bg-red-50">
                    <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                        <CardTitle className="text-sm font-medium">Critical Alerts</CardTitle>
                        <AlertTriangle className="h-4 w-4 text-red-600" />
                    </CardHeader>
                    <CardContent>
                        <div className="text-2xl font-bold text-red-600">{criticalCount}</div>
                        <p className="text-xs text-red-700">Urgency Score ≥ 80</p>
                    </CardContent>
                </Card>

                <Card className="border-orange-200 bg-orange-50">
                    <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                        <CardTitle className="text-sm font-medium">High Priority</CardTitle>
                        <TrendingUp className="h-4 w-4 text-orange-600" />
                    </CardHeader>
                    <CardContent>
                        <div className="text-2xl font-bold text-orange-600">{highCount}</div>
                        <p className="text-xs text-orange-700">Urgency Score 60-79</p>
                    </CardContent>
                </Card>

                <Card className="border-yellow-200 bg-yellow-50">
                    <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                        <CardTitle className="text-sm font-medium">Medium Priority</CardTitle>
                        <Clock className="h-4 w-4 text-yellow-600" />
                    </CardHeader>
                    <CardContent>
                        <div className="text-2xl font-bold text-yellow-600">{mediumCount}</div>
                        <p className="text-xs text-yellow-700">Urgency Score \u003c 60</p>
                    </CardContent>
                </Card>
            </div>

            {/* Alert List */}
            <Card>
                <CardHeader>
                    <CardTitle>Active High-Risk Alerts</CardTitle>
                </CardHeader>
                <CardContent>
                    {alerts.length === 0 ? (
                        <p className="text-gray-500 text-center py-8">No high-risk partners at this time.</p>
                    ) : (
                        <div className="space-y-3">
                            {alerts.map((alert) => {
                                const urgencyColor =
                                    alert.urgency_score >= 80
                                        ? 'bg-red-100 text-red-800 border-red-200'
                                        : alert.urgency_score >= 60
                                            ? 'bg-orange-100 text-orange-800 border-orange-200'
                                            : 'bg-yellow-100 text-yellow-800 border-yellow-200'

                                return (
                                    <div
                                        key={alert.partner_id}
                                        className={`p-4 rounded-lg border ${urgencyColor} flex items-center justify-between`}
                                    >
                                        <div className="flex-1">
                                            <div className="flex items-center gap-3">
                                                <AlertTriangle className="h-5 w-5" />
                                                <div>
                                                    <p className="font-semibold">{alert.partner_id}</p>
                                                    <p className="text-sm opacity-90">
                                                        {alert.region} • {alert.tier} Tier
                                                    </p>
                                                </div>
                                            </div>
                                        </div>
                                        <div className="flex items-center gap-4">
                                            <div className="text-right">
                                                <p className="text-sm font-medium">Churn Risk</p>
                                                <p className="text-lg font-bold">
                                                    {Math.round(alert.churn_prob * 100)}%
                                                </p>
                                            </div>
                                            <div className="text-right">
                                                <p className="text-sm font-medium">Urgency</p>
                                                <Badge variant="outline" className="text-base font-bold">
                                                    {alert.urgency_score}
                                                </Badge>
                                            </div>
                                            <div className="text-right">
                                                <p className="text-sm font-medium">LTV</p>
                                                <p className="text-lg font-bold">
                                                    ${(alert.ltv / 1000).toFixed(0)}K
                                                </p>
                                            </div>
                                        </div>
                                    </div>
                                )
                            })}
                        </div>
                    )}
                </CardContent>
            </Card>
        </div>
    )
}
