"use client"

import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Cell } from "recharts"

interface ShapChartProps {
    data?: any[]
}

const DEFAULT_SHAP = [
    { feature: "Login Trend", value: -0.45 },
    { feature: "Avg Commission", value: -0.25 },
    { feature: "Support Delay", value: 0.15 },
    { feature: "Relationship", value: 0.10 },
    { feature: "Tier Seniority", value: 0.05 },
]

export function ShapChart({ data: explicitData }: ShapChartProps) {
    const data = explicitData || DEFAULT_SHAP

    return (
        <div className="w-full h-[300px]">
            <ResponsiveContainer width="100%" height="100%">
                <BarChart
                    data={data}
                    layout="vertical"
                    margin={{ top: 5, right: 30, left: 40, bottom: 5 }}
                >
                    <CartesianGrid strokeDasharray="3 3" horizontal={true} vertical={false} />
                    <XAxis type="number" hide />
                    <YAxis
                        dataKey="feature"
                        type="category"
                        tick={{ fontSize: 12, fill: '#666' }}
                        width={100}
                    />
                    <Tooltip
                        contentStyle={{ borderRadius: '8px', border: 'none', boxShadow: '0 4px 12px rgba(0,0,0,0.1)' }}
                        itemStyle={{ fontWeight: 600 }}
                        formatter={(value: number) => [value.toFixed(2), "Impact"]}
                    />
                    <Bar dataKey="value" radius={[0, 4, 4, 0]}>
                        {data.map((entry, index) => (
                            <Cell
                                key={`cell-${index}`}
                                fill={entry.value < 0 ? "#FF444F" : "#008832"}
                            />
                        ))}
                    </Bar>
                </BarChart>
            </ResponsiveContainer>
        </div>
    )
}
