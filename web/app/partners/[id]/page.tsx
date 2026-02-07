import { api } from "@/services/api"
import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import { GenAIExplanation } from "@/components/analysis/GenAIExplanation"
import { ShapChart } from "@/components/analysis/ShapChart"
import { ArrowLeft, Send, ExternalLink } from "lucide-react"
import Link from "next/link"
import { notFound } from "next/navigation"

export default async function PartnerPage({ params }: { params: { id: string } }) {
    const partner = await api.getPartner(params.id)
    const summary = await api.getPartnerSummary(params.id)

    if (!partner) {
        notFound()
    }

    return (
        <div className="space-y-6">
            {/* Header */}
            <div className="flex items-center justify-between">
                <div className="flex items-center gap-4">
                    <Link href="/">
                        <Button variant="ghost" size="icon" className="rounded-full">
                            <ArrowLeft size={18} />
                        </Button>
                    </Link>
                    <div>
                        <div className="flex items-center gap-2 mb-1">
                            <h1 className="text-2xl font-bold text-gray-900">{partner.partner_id}</h1>
                            <Badge variant="outline" className="border-deriv-blue text-deriv-blue font-semibold">
                                {partner.tier}
                            </Badge>
                        </div>
                        <p className="text-gray-500 text-sm">Region: {partner.region} • Partner since: {partner.join_date}</p>
                    </div>
                </div>
                <div className="flex gap-2">
                    <Button variant="outline" className="gap-2">
                        <ExternalLink size={16} />
                        View CRM
                    </Button>
                    <Button className="bg-deriv-red hover:bg-deriv-red/90 gap-2">
                        <Send size={16} />
                        Trigger Intervention
                    </Button>
                </div>
            </div>

            {/* Content Grid */}
            <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
                {/* Left Column: Metrics & SHAP */}
                <div className="lg:col-span-2 space-y-6">
                    {/* Key Metrics Row */}
                    <div className="grid grid-cols-3 gap-4">
                        <div className="bg-white p-4 rounded-lg border border-gray-100 shadow-sm">
                            <span className="text-xs text-gray-400 block mb-1">CHURN PROBABILITY</span>
                            <span className={`text-xl font-bold ${partner.churn_prob >= 0.7 ? 'text-deriv-red' : 'text-deriv-orange'}`}>
                                {(partner.churn_prob * 100).toFixed(0)}%
                            </span>
                        </div>
                        <div className="bg-white p-4 rounded-lg border border-gray-100 shadow-sm">
                            <span className="text-xs text-gray-400 block mb-1">EST. LTV EXPOSED</span>
                            <span className="text-xl font-bold text-gray-900">
                                ${(partner.ltv / 1000).toFixed(1)}k
                            </span>
                        </div>
                        <div className="bg-white p-4 rounded-lg border border-gray-100 shadow-sm">
                            <span className="text-xs text-gray-400 block mb-1">URGENCY SCORE</span>
                            <span className="text-xl font-bold text-gray-900">
                                {partner.urgency_score}/100
                            </span>
                        </div>
                    </div>

                    {/* SHAP Explanation */}
                    <div className="bg-white p-6 rounded-lg border border-gray-200 shadow-sm">
                        <h2 className="text-lg font-semibold mb-4 text-gray-900">Model Decision Factors</h2>
                        <p className="text-sm text-gray-500 mb-6 italic">Visualizing the positive and negative contributors to the churn risk score.</p>
                        <ShapChart />
                    </div>
                </div>

                {/* Right Column: AI Analysis & Context */}
                <div className="space-y-6">
                    <GenAIExplanation partnerId={params.id} summary={summary} />

                    {/* Relationship Network Context */}
                    <div className="bg-gray-900 p-6 rounded-lg text-white">
                        <h3 className="text-sm font-bold text-gray-400 uppercase tracking-wider mb-4">Network Context</h3>
                        <div className="space-y-3">
                            <div className="flex justify-between items-center">
                                <span className="text-sm text-gray-300">Sub-affiliates</span>
                                <span className="font-mono">8 active</span>
                            </div>
                            <div className="flex justify-between items-center">
                                <span className="text-sm text-gray-300">Total Network ROI</span>
                                <span className="text-deriv-green">+$45k/mo</span>
                            </div>
                            <div className="mt-4 p-3 bg-white/5 rounded text-xs text-gray-400 italic">
                                High contagion risk: 3 sub-affiliates show similar login decline.
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    )
}
