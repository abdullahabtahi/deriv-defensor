"use client"

import { useEffect, useState } from "react"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { TrendingUp, TrendingDown, DollarSign, CheckCircle, XCircle, Clock } from "lucide-react"

interface InterventionStats {
    total: number
    saved: number
    failed: number
    pending: number
    totalLtvProtected: number
    successRate: number
}

export default function ROIPage() {
    const [stats, setStats] = useState<InterventionStats | null>(null)
    const [loading, setLoading] = useState(true)

    useEffect(() => {
        async function fetchStats() {
            try {
                const response = await fetch('http://localhost:8001/interventions')
                const interventions = await response.json()

                // Calculate stats from interventions
                const total = interventions.length
                const saved = interventions.filter((i: any) => i.outcome_label === 'Saved').length
                const failed = interventions.filter((i: any) => i.outcome_label === 'Failed').length
                const pending = interventions.filter((i: any) => i.status === 'Pending').length

                // Calculate total LTV protected (mock calculation based on saved partners)
                const totalLtvProtected = saved * 185000 // Average LTV

                const successRate = total > 0 ? Math.round((saved / total) * 100) : 0

                setStats({
                    total,
                    saved,
                    failed,
                    pending,
                    totalLtvProtected,
                    successRate
                })
            } catch (error) {
                console.error('Error fetching ROI stats:', error)
            } finally {
                setLoading(false)
            }
        }

        fetchStats()
    }, [])

    if (loading) {
        return <div className="p-8">Loading ROI metrics...</div>
    }

    if (!stats) {
        return <div className="p-8">Failed to load ROI data.</div>
    }

    return (
        <div className="space-y-6">
            <div>
                <h1 className="text-3xl font-bold text-gray-900">ROI Deep Dive</h1>
                <p className="text-gray-500 mt-1">Intervention outcomes and lifetime value protected</p>
            </div>

            {/* Summary Cards */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
                <Card>
                    <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                        <CardTitle className="text-sm font-medium">Total Interventions</CardTitle>
                        <Clock className="h-4 w-4 text-muted-foreground" />
                    </CardHeader>
                    <CardContent>
                        <div className="text-2xl font-bold">{stats.total}</div>
                        <p className="text-xs text-muted-foreground">Executed to date</p>
                    </CardContent>
                </Card>

                <Card>
                    <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                        <CardTitle className="text-sm font-medium">Success Rate</CardTitle>
                        <TrendingUp className="h-4 w-4 text-green-600" />
                    </CardHeader>
                    <CardContent>
                        <div className="text-2xl font-bold text-green-600">{stats.successRate}%</div>
                        <p className="text-xs text-muted-foreground">{stats.saved} partners saved</p>
                    </CardContent>
                </Card>

                <Card>
                    <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                        <CardTitle className="text-sm font-medium">LTV Protected</CardTitle>
                        <DollarSign className="h-4 w-4 text-blue-600" />
                    </CardHeader>
                    <CardContent>
                        <div className="text-2xl font-bold text-blue-600">
                            ${(stats.totalLtvProtected / 1000000).toFixed(1)}M
                        </div>
                        <p className="text-xs text-muted-foreground">From successful interventions</p>
                    </CardContent>
                </Card>

                <Card>
                    <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                        <CardTitle className="text-sm font-medium">Failed Interventions</CardTitle>
                        <XCircle className="h-4 w-4 text-red-600" />
                    </CardHeader>
                    <CardContent>
                        <div className="text-2xl font-bold text-red-600">{stats.failed}</div>
                        <p className="text-xs text-muted-foreground">Partners lost despite outreach</p>
                    </CardContent>
                </Card>
            </div>

            {/* Outcome Breakdown */}
            <Card>
                <CardHeader>
                    <CardTitle>Intervention Outcome Distribution</CardTitle>
                    <CardDescription>Breakdown of all intervention actions</CardDescription>
                </CardHeader>
                <CardContent>
                    <div className="space-y-4">
                        <div className="flex items-center justify-between">
                            <div className="flex items-center gap-3">
                                <CheckCircle className="h-5 w-5 text-green-600" />
                                <div>
                                    <p className="font-medium">Saved</p>
                                    <p className="text-sm text-gray-500">Partners successfully retained</p>
                                </div>
                            </div>
                            <div className="text-right">
                                <p className="text-2xl font-bold text-green-600">{stats.saved}</p>
                                <Badge variant="outline" className="mt-1">
                                    {stats.total > 0 ? Math.round((stats.saved / stats.total) * 100) : 0}%
                                </Badge>
                            </div>
                        </div>

                        <div className="flex items-center justify-between">
                            <div className="flex items-center gap-3">
                                <XCircle className="h-5 w-5 text-red-600" />
                                <div>
                                    <p className="font-medium">Failed</p>
                                    <p className="text-sm text-gray-500">Partners churned despite intervention</p>
                                </div>
                            </div>
                            <div className="text-right">
                                <p className="text-2xl font-bold text-red-600">{stats.failed}</p>
                                <Badge variant="outline" className="mt-1">
                                    {stats.total > 0 ? Math.round((stats.failed / stats.total) * 100) : 0}%
                                </Badge>
                            </div>
                        </div>

                        <div className="flex items-center justify-between">
                            <div className="flex items-center gap-3">
                                <Clock className="h-5 w-5 text-yellow-600" />
                                <div>
                                    <p className="font-medium">Pending</p>
                                    <p className="text-sm text-gray-500">Awaiting outcome confirmation</p>
                                </div>
                            </div>
                            <div className="text-right">
                                <p className="text-2xl font-bold text-yellow-600">{stats.pending}</p>
                                <Badge variant="outline" className="mt-1">
                                    {stats.total > 0 ? Math.round((stats.pending / stats.total) * 100) : 0}%
                                </Badge>
                            </div>
                        </div>
                    </div>
                </CardContent>
            </Card>
        </div>
    )
}
