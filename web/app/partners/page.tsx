import { api } from "@/services/api"
import { Badge } from "@/components/ui/badge"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import Link from "next/link"
import { ArrowRight } from "lucide-react"

export default async function PartnersListPage() {
    const partners = await api.getHighRiskPartners()

    return (
        <div className="space-y-6">
            <div>
                <h1 className="text-3xl font-bold text-gray-900">Partner Analysis</h1>
                <p className="text-gray-500 mt-1">Select a partner to view detailed risk analysis and SHAP insights</p>
            </div>

            <Card>
                <CardHeader>
                    <CardTitle>All Partners</CardTitle>
                </CardHeader>
                <CardContent>
                    <div className="space-y-2">
                        {partners.map((partner: any) => {
                            const riskColor =
                                partner.churn_prob >= 0.7
                                    ? 'bg-red-100 text-red-800 border-red-200'
                                    : partner.churn_prob >= 0.4
                                        ? 'bg-orange-100 text-orange-800 border-orange-200'
                                        : 'bg-green-100 text-green-800 border-green-200'

                            return (
                                <Link
                                    key={partner.partner_id}
                                    href={`/partners/${partner.partner_id}`}
                                    className="block"
                                >
                                    <div
                                        className={`p-4 rounded-lg border ${riskColor} hover:shadow-md transition-shadow cursor-pointer flex items-center justify-between`}
                                    >
                                        <div className="flex-1">
                                            <div className="flex items-center gap-4">
                                                <div>
                                                    <p className="font-semibold text-lg">{partner.partner_id}</p>
                                                    <p className="text-sm opacity-90">
                                                        {partner.region} • {partner.tier} Tier
                                                    </p>
                                                </div>
                                            </div>
                                        </div>
                                        <div className="flex items-center gap-6">
                                            <div className="text-right">
                                                <p className="text-sm font-medium opacity-75">Churn Risk</p>
                                                <p className="text-xl font-bold">
                                                    {Math.round(partner.churn_prob * 100)}%
                                                </p>
                                            </div>
                                            <div className="text-right">
                                                <p className="text-sm font-medium opacity-75">LTV</p>
                                                <p className="text-xl font-bold">
                                                    ${(partner.ltv / 1000).toFixed(0)}K
                                                </p>
                                            </div>
                                            <Badge variant="outline" className="text-base">
                                                {partner.risk_category}
                                            </Badge>
                                            <ArrowRight className="h-5 w-5 opacity-50" />
                                        </div>
                                    </div>
                                </Link>
                            )
                        })}
                    </div>
                </CardContent>
            </Card>
        </div>
    )
}
