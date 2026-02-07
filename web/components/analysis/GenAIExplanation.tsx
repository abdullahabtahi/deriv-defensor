"use client"

import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Skeleton } from "@/components/ui/skeleton"
import { Sparkles, AlertCircle, TrendingDown } from "lucide-react"

interface GenAIExplanationProps {
    partnerId: string
    summary: any
    isLoading?: boolean
}

export function GenAIExplanation({ partnerId, summary, isLoading }: GenAIExplanationProps) {
    if (isLoading) {
        return (
            <Card className="border-deriv-red/20 overflow-hidden">
                <CardHeader className="bg-deriv-red/5">
                    <CardTitle className="text-sm flex items-center gap-2">
                        <Sparkles size={16} className="text-deriv-red animate-pulse" />
                        AI Risk Analysis
                    </CardTitle>
                </CardHeader>
                <CardContent className="p-6 space-y-4">
                    <Skeleton className="h-4 w-full" />
                    <Skeleton className="h-4 w-3/4" />
                    <Skeleton className="h-4 w-5/6" />
                </CardContent>
            </Card>
        )
    }

    if (!summary || !summary.summary) {
        return (
            <Card className="border-gray-200">
                <CardContent className="p-10 flex flex-col items-center justify-center text-center space-y-2">
                    <AlertCircle size={40} className="text-gray-300" />
                    <p className="text-gray-500 font-medium">No AI analysis available for this partner yet.</p>
                    <p className="text-sm text-gray-400">Trigger standard intervention to generate insights.</p>
                </CardContent>
            </Card>
        )
    }

    return (
        <Card className="border-deriv-red/20 overflow-hidden shadow-lg">
            <CardHeader className="bg-deriv-red/5 border-b border-deriv-red/10 flex flex-row items-center justify-between">
                <CardTitle className="text-sm flex items-center gap-2 font-bold text-deriv-red">
                    <Sparkles size={16} />
                    GEN-AI ANALYSIS
                </CardTitle>
                <Badge variant="outline" className="bg-white text-deriv-red border-deriv-red/20">
                    {summary.churn_tendency >= 0.7 ? "High Urgency" : "Monitor Closely"}
                </Badge>
            </CardHeader>
            <CardContent className="p-6">
                <div className="space-y-4">
                    <div className="flex items-start gap-3">
                        <div className="p-2 bg-deriv-red/10 rounded-full mt-1">
                            <TrendingDown size={14} className="text-deriv-red" />
                        </div>
                        <div>
                            <h4 className="text-sm font-semibold text-gray-900 mb-1">Key Findings</h4>
                            <p className="text-sm text-gray-600 leading-relaxed whitespace-pre-wrap">
                                {summary.summary}
                            </p>
                        </div>
                    </div>

                    {summary.metrics && (
                        <div className="pt-4 border-t border-gray-100 grid grid-cols-2 gap-4">
                            {Object.entries(summary.metrics).map(([key, value]: [string, any]) => (
                                <div key={key}>
                                    <span className="text-[10px] uppercase text-gray-400 block font-bold tracking-wider">{key.replace(/_/g, ' ')}</span>
                                    <span className="text-sm font-medium text-gray-700">{typeof value === 'number' ? `${(value * 100).toFixed(0)}%` : value}</span>
                                </div>
                            ))}
                        </div>
                    )}
                </div>
            </CardContent>
        </Card>
    )
}
