import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { ArrowUpRight, ArrowDownRight, Activity } from "lucide-react"
import { cn } from "@/lib/utils"

interface KpiCardProps {
    title: string
    value: string | number
    trend?: number
    trendLabel?: string
    icon?: React.ReactNode
    color?: "red" | "green" | "blue" | "orange"
}

export function KpiCard({ title, value, trend, trendLabel, icon, color = "blue" }: KpiCardProps) {
    const isPositive = trend && trend > 0
    const isNegative = trend && trend < 0

    const colorStyles = {
        red: "border-l-deriv-red text-deriv-red bg-deriv-red/5",
        green: "border-l-deriv-green text-deriv-green bg-deriv-green/5",
        blue: "border-l-deriv-blue text-deriv-blue bg-deriv-blue/5",
        orange: "border-l-deriv-orange text-deriv-orange bg-deriv-orange/5",
    }

    return (
        <Card className={cn("border-l-4 shadow-sm hover:shadow-md transition-shadow", colorStyles[color].split(" ")[0])}>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                <CardTitle className="text-sm font-medium text-gray-500 uppercase tracking-wide">
                    {title}
                </CardTitle>
                {icon && <div className={cn("p-2 rounded-full", colorStyles[color].split(" ")[2])}>{icon}</div>}
            </CardHeader>
            <CardContent>
                <div className="text-2xl font-bold text-gray-900">{value}</div>
                {(trend || trendLabel) && (
                    <p className="text-xs font-medium mt-1 flex items-center gap-1">
                        {isPositive && <ArrowUpRight size={14} className="text-deriv-red" />}
                        {isNegative && <ArrowDownRight size={14} className="text-deriv-green" />}
                        <span
                            className={cn(
                                isPositive ? "text-deriv-red" : isNegative ? "text-deriv-green" : "text-gray-500"
                            )}
                        >
                            {trend ? `${Math.abs(trend)}%` : ""}
                        </span>
                        <span className="text-gray-400 ml-1">{trendLabel}</span>
                    </p>
                )}
            </CardContent>
        </Card>
    )
}
