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
    variant?: "default" | "premium"
}

export function KpiCard({ title, value, trend, trendLabel, icon, color = "blue", variant = "default" }: KpiCardProps) {
    const isPositive = trend && trend > 0
    const isNegative = trend && trend < 0

    const colorStyles = {
        red: "border-l-deriv-red text-deriv-red bg-deriv-red/5",
        green: "border-l-deriv-green text-deriv-green bg-deriv-green/5",
        blue: "border-l-deriv-blue text-deriv-blue bg-deriv-blue/5",
        orange: "border-l-deriv-orange text-deriv-orange bg-deriv-orange/5",
    }

    if (variant === "premium") {
        const premiumConfig = {
            red: {
                glow: "bg-[#FF444F]",
                iconWrapper: "bg-[#FF444F]/10 border-[#FF444F]/20 text-[#FF444F]",
                trendPositive: "text-[#FF444F] bg-[#FF444F]/10",
                trendNegative: "text-emerald-400 bg-emerald-500/10"
            },
            green: {
                glow: "bg-emerald-500",
                iconWrapper: "bg-emerald-500/10 border-emerald-500/20 text-emerald-400",
                trendPositive: "text-emerald-400 bg-emerald-500/10",
                trendNegative: "text-[#FF444F] bg-[#FF444F]/10"
            },
            blue: {
                // Using a vivid blue for the glow
                glow: "bg-blue-500",
                iconWrapper: "bg-blue-500/10 border-blue-500/20 text-blue-400",
                trendPositive: "text-blue-400 bg-blue-500/10",
                trendNegative: "text-orange-400 bg-orange-500/10"
            },
            orange: {
                glow: "bg-orange-500",
                iconWrapper: "bg-orange-500/10 border-orange-500/20 text-orange-400",
                trendPositive: "text-orange-400 bg-orange-500/10",
                trendNegative: "text-gray-400 bg-gray-500/10"
            }
        }

        const styles = premiumConfig[color] || premiumConfig.blue

        return (
            <div className="relative overflow-hidden bg-gradient-to-br from-gray-900 via-gray-800 to-gray-900 rounded-xl shadow-lg border border-gray-800 group transition-all hover:scale-[1.02] hover:shadow-xl duration-300">
                <div className={cn("absolute top-0 right-0 w-32 h-32 rounded-full mix-blend-overlay filter blur-[60px] opacity-15 group-hover:opacity-25 transition-opacity duration-700", styles.glow)}></div>

                <div className="relative p-6">
                    <div className="flex flex-row items-center justify-between space-y-0 pb-2 mb-2">
                        <div className="text-xs font-bold text-gray-400 uppercase tracking-wider">
                            {title}
                        </div>
                        {icon && <div className={cn("p-2 rounded-lg border shadow-sm backdrop-blur-sm", styles.iconWrapper)}>{icon}</div>}
                    </div>

                    <div className="text-3xl font-bold text-white mb-2 tracking-tight">{value}</div>

                    {(trend || trendLabel) && (
                        <p className="text-xs font-medium flex items-center gap-2">
                            <span className={cn(
                                "flex items-center gap-1 px-1.5 py-0.5 rounded font-semibold",
                                isPositive && styles.trendPositive,
                                isNegative && styles.trendNegative,
                                !isPositive && !isNegative && "text-gray-400"
                            )}>
                                {isPositive && <ArrowUpRight size={12} strokeWidth={3} />}
                                {isNegative && <ArrowDownRight size={12} strokeWidth={3} />}
                                {trend ? `${Math.abs(trend)}%` : ""}
                            </span>
                            <span className="text-gray-500">{trendLabel}</span>
                        </p>
                    )}
                </div>
            </div>
        )
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
