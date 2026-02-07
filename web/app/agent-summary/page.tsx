"use client"

import { useState, useEffect } from "react"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Skeleton } from "@/components/ui/skeleton"

interface AgentSummary {
    partner_id?: string
    churn_tendency?: number
    summary?: string
    metrics?: Record<string, any>
    reason_codes?: string[]
    recommended_action?: string
    timestamp?: string
}

export default function AgentSummaryPage() {
    const [summary, setSummary] = useState<AgentSummary>({})
    const [loading, setLoading] = useState(true)

    const fetchSummary = async () => {
        try {
            const response = await fetch('/api/agent-summary')
            const data = await response.json()
            setSummary(data)
            setLoading(false)
        } catch (error) {
            console.error("Failed to fetch agent summary:", error)
            setLoading(false)
        }
    }

    useEffect(() => {
        // Initial fetch
        fetchSummary()

        // Auto-refresh every 10 seconds
        const interval = setInterval(fetchSummary, 10000)

        return () => clearInterval(interval)
    }, [])

    const getRiskColor = (tendency?: number) => {
        if (!tendency) return "bg-gray-500"
        if (tendency >= 0.7) return "bg-deriv-red"
        if (tendency >= 0.4) return "bg-deriv-orange"
        return "bg-deriv-green"
    }

    const getRiskLabel = (tendency?: number) => {
        if (!tendency) return "Unknown"
        if (tendency >= 0.7) return "High Risk"
        if (tendency >= 0.4) return "Medium Risk"
        return "Low Risk"
    }

    if (loading) {
        return (
            <div className="container mx-auto p-6 max-w-4xl">
                <Skeleton className="h-96 w-full" />
            </div>
        )
    }

    if (!summary.partner_id) {
        return (
            <div className="container mx-auto p-6 max-w-4xl">
                <Card className="border-2 border-dashed border-gray-300">
                    <CardContent className="flex items-center justify-center h-64">
                        <div className="text-center space-y-2">
                            <div className="animate-pulse text-4xl">⏳</div>
                            <p className="text-xl font-medium text-gray-500">
                                Waiting for agent data...
                            </p>
                            <p className="text-sm text-gray-400">
                                The AI agent will post analysis results here
                            </p>
                        </div>
                    </CardContent>
                </Card>
            </div>
        )
    }

    return (
        <div className="container mx-auto p-6 max-w-4xl space-y-6">
            {/* Header */}
            <div className="flex items-center justify-between">
                <div>
                    <h1 className="text-3xl font-bold text-gray-900">Agent Analysis</h1>
                    <p className="text-sm text-gray-500 mt-1">
                        Last updated: {summary.timestamp ? new Date(summary.timestamp).toLocaleString() : 'N/A'}
                    </p>
                </div>
                <div className="animate-pulse text-xs text-gray-400">
                    Auto-refreshing...
                </div>
            </div>

            {/* Partner Info Card */}
            <Card className="border-l-4 border-l-deriv-red shadow-lg">
                <CardHeader>
                    <div className="flex items-center justify-between">
                        <CardTitle className="text-xl">Partner: {summary.partner_id}</CardTitle>
                        <Badge className={`${getRiskColor(summary.churn_tendency)} text-white px-4 py-1 text-sm`}>
                            {getRiskLabel(summary.churn_tendency)} ({Math.round((summary.churn_tendency || 0) * 100)}%)
                        </Badge>
                    </div>
                </CardHeader>
                <CardContent className="space-y-6">
                    {/* Summary */}
                    <div>
                        <h3 className="text-sm font-semibold text-gray-500 uppercase tracking-wide mb-2">
                            Analysis Summary
                        </h3>
                        <p className="text-gray-800 leading-relaxed bg-gradient-to-r from-green-50 to-blue-50 p-4 rounded-lg border border-green-200">
                            {summary.summary}
                        </p>
                    </div>

                    {/* Metrics Table */}
                    {summary.metrics && Object.keys(summary.metrics).length > 0 && (
                        <div>
                            <h3 className="text-sm font-semibold text-gray-500 uppercase tracking-wide mb-3">
                                Key Metrics
                            </h3>
                            <div className="bg-gray-50 rounded-lg border border-gray-200 overflow-hidden">
                                <table className="w-full">
                                    <tbody className="divide-y divide-gray-200">
                                        {Object.entries(summary.metrics).map(([key, value]) => (
                                            <tr key={key} className="hover:bg-gray-100 transition-colors">
                                                <td className="px-4 py-3 text-sm font-medium text-gray-700">
                                                    {key.replace(/_/g, ' ').toUpperCase()}
                                                </td>
                                                <td className="px-4 py-3 text-sm text-gray-900 text-right font-semibold">
                                                    {typeof value === 'number' ? value.toLocaleString() : value}
                                                </td>
                                            </tr>
                                        ))}
                                    </tbody>
                                </table>
                            </div>
                        </div>
                    )}

                    {/* Reason Codes */}
                    {summary.reason_codes && summary.reason_codes.length > 0 && (
                        <div>
                            <h3 className="text-sm font-semibold text-gray-500 uppercase tracking-wide mb-3">
                                Risk Factors
                            </h3>
                            <div className="flex flex-wrap gap-2">
                                {summary.reason_codes.map((code, idx) => (
                                    <Badge key={idx} variant="outline" className="bg-red-50 border-red-200 text-red-700">
                                        {code}
                                    </Badge>
                                ))}
                            </div>
                        </div>
                    )}

                    {/* Recommended Action */}
                    {summary.recommended_action && (
                        <div>
                            <h3 className="text-sm font-semibold text-gray-500 uppercase tracking-wide mb-2">
                                Recommended Action
                            </h3>
                            <div className="bg-blue-50 border-l-4 border-blue-500 p-4 rounded">
                                <p className="text-blue-900 font-medium">
                                    {summary.recommended_action}
                                </p>
                            </div>
                        </div>
                    )}
                </CardContent>
            </Card>
        </div>
    )
}
