"use client"

import Link from "next/link"
import { usePathname } from "next/navigation"
import { LayoutDashboard, Users, History, Briefcase, BarChart3, ShieldAlert } from "lucide-react"
import { cn } from "@/lib/utils"

const navItems = [
    { href: "/", label: "Dashboard", icon: LayoutDashboard },
    { href: "/interventions", label: "Intervention Log", icon: History },
    { href: "/crm", label: "CRM Tasks", icon: Briefcase },
    { href: "/roi", label: "ROI Deep Dive", icon: BarChart3 },
    { href: "/alerts", label: "Alert Monitor", icon: ShieldAlert },
]



export default function Sidebar() {
    const pathname = usePathname()

    return (
        <aside className="w-[240px] fixed left-0 top-[48px] bottom-0 bg-white border-r border-gray-200 z-40 hidden md:block">
            <div className="flex flex-col py-6 px-4 gap-2">
                <div className="text-xs font-semibold text-gray-400 uppercase tracking-wider mb-2 pl-2">
                    Defensor Tools
                </div>

                {navItems.map((item) => {
                    const isActive = pathname === item.href
                    return (
                        <Link
                            key={item.href}
                            href={item.href}
                            className={cn(
                                "flex items-center gap-3 px-3 py-2.5 rounded-md text-sm font-medium transition-colors",
                                isActive
                                    ? "bg-deriv-red/10 text-deriv-red"
                                    : "text-gray-600 hover:bg-gray-50 hover:text-gray-900"
                            )}
                        >
                            <item.icon size={18} className={isActive ? "text-deriv-red" : "text-gray-400"} />
                            {item.label}
                        </Link>
                    )
                })}
            </div>

            {/* Footer Info */}
            <div className="absolute bottom-6 left-0 right-0 px-6 text-xs text-gray-400 text-center">
                Deriv Defensor v2.0 <br />
                Powered by GenAI
            </div>
        </aside>
    )
}
