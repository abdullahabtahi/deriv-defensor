"use client"

import { PieChart, Pie, Cell, ResponsiveContainer, Tooltip, Legend } from "recharts"

interface RiskChartProps {
    partners?: any[]
    data?: { name: string; value: number; color: string }[]
}

const DEFAULT_DATA = [
    { name: "High Risk", value: 45, color: "#FF444F" },
    { name: "Medium Risk", value: 30, color: "#FF9C13" },
    { name: "Low Risk", value: 25, color: "#008832" },
]

export function RiskChart({ partners, data: explicitData }: RiskChartProps) {
    let data = explicitData || DEFAULT_DATA

    if (partners && !explicitData) {
        const high = partners.filter(p => p.churn_prob >= 0.7).length
        const med = partners.filter(p => p.churn_prob >= 0.4 && p.churn_prob < 0.7).length
        const low = partners.filter(p => p.churn_prob < 0.4).length

        data = [
            { name: "High Risk", value: high, color: "#FF444F" },
            { name: "Medium Risk", value: med, color: "#FF9C13" },
            { name: "Low Risk", value: low, color: "#008832" },
        ].filter(d => d.value > 0)
    }

    return (
        <div className="w-full h-[300px]">
            <ResponsiveContainer width="100%" height="100%">
                <PieChart>
                    <Pie
                        data={data}
                        cx="50%"
                        cy="50%"
                        innerRadius={60}
                        outerRadius={100}
                        paddingAngle={2}
                        dataKey="value"
                    >
                        {data.map((entry, index) => (
                            <Cell key={`cell-${index}`} fill={entry.color} stroke={entry.color} />
                        ))}
                    </Pie>
                    <Tooltip
                        contentStyle={{ borderRadius: '8px', border: 'none', boxShadow: '0 4px 12px rgba(0,0,0,0.1)' }}
                        itemStyle={{ color: '#333', fontWeight: 500 }}
                    />
                    <Legend
                        verticalAlign="bottom"
                        height={36}
                        iconType="circle"
                        formatter={(value) => <span className="text-gray-600 font-medium ml-1">{value}</span>}
                    />
                </PieChart>
            </ResponsiveContainer>
        </div>
    )
}
