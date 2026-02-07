"use client"

import { useState } from "react"
import {
    CheckCircle2,
    Clock,
    AlertCircle,
    MoreHorizontal,
    ExternalLink,
    ShieldAlert,
    Filter,
    ArrowUpRight,
    Search,
    RefreshCcw,
    Zap
} from "lucide-react"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import Link from "next/link"
import { cn } from "@/lib/utils"
import { motion, AnimatePresence } from "framer-motion"

const MOCK_CRM_TASKS = [
    {
        id: "T-8821",
        title: "Tier Demotion Warning: Gold to Silver",
        partner_id: "P11972",
        priority: "Critical",
        type: "Retention Email",
        deadline: "Today",
        status: "Pending",
        description: "Partner P11972 is 2% above the Silver demotion threshold. Send incentive package to maintain Gold status."
    },
    {
        id: "T-8822",
        title: "High Churn Probability Outreach",
        partner_id: "P88231",
        priority: "High",
        type: "Phone Call",
        deadline: "Tomorrow",
        status: "In Progress",
        description: "Login frequency dropped 45% in 14 days. Relationship Manager needs to schedule a recovery call."
    },
    {
        id: "T-8823",
        title: "Network Contagion Impact Assessment",
        partner_id: "P33892",
        priority: "Medium",
        type: "Investigation",
        deadline: "Feb 12",
        status: "Pending",
        description: "Underlying sub-affiliates showing 25% churn. Assess Master's risk exposure."
    },
    {
        id: "T-8824",
        title: "Payment Delay Resolution",
        partner_id: "P22104",
        priority: "Critical",
        type: "Issue Resolution",
        deadline: "Urgent",
        status: "Assigned",
        description: "Crypto withdrawal pending for 72h. Partner sentiment dropping. Escalated to accounts."
    },
    {
        id: "T-8825",
        title: "Loyalty Program Upgrade Offer",
        partner_id: "P55102",
        priority: "Low",
        type: "Retention Email",
        deadline: "Feb 15",
        status: "Pending",
        description: "High LTV partner showing stable growth. Offer early access to VIP platform features."
    },
    {
        id: "T-8826",
        title: "Marketing Asset Support",
        partner_id: "P44512",
        priority: "Medium",
        type: "Support",
        deadline: "Feb 10",
        status: "Completed",
        description: "Requested custom banners for local region campaign."
    }
]

export default function CRMPage() {
    const [tasks] = useState(MOCK_CRM_TASKS)

    const getPriorityColor = (priority: string) => {
        switch (priority) {
            case "Critical": return "bg-red-50 text-red-600 border-red-200 ring-1 ring-red-100"
            case "High": return "bg-orange-50 text-orange-600 border-orange-200 ring-1 ring-orange-100"
            case "Medium": return "bg-blue-50 text-blue-600 border-blue-200 ring-1 ring-blue-100"
            default: return "bg-gray-50 text-gray-600 border-gray-200"
        }
    }

    const getStatusIcon = (status: string) => {
        switch (status) {
            case "Completed": return <CheckCircle2 size={16} className="text-emerald-500" />
            case "In Progress": return <Clock size={16} className="text-blue-500" />
            case "Assigned": return <AlertCircle size={16} className="text-orange-500" />
            default: return <Clock size={16} className="text-gray-400" />
        }
    }

    const container = {
        hidden: { opacity: 0 },
        show: {
            opacity: 1,
            transition: {
                staggerChildren: 0.1
            }
        }
    }

    const item = {
        hidden: { opacity: 0, y: 10 },
        show: { opacity: 1, y: 0 }
    }

    return (
        <div className="min-h-screen bg-gray-50/50 pb-20">
            {/* Sticky Glass Header */}
            <div className="sticky top-0 z-30 bg-white/80 backdrop-blur-md border-b border-gray-200">
                <div className="max-w-[1600px] mx-auto px-6 py-4">
                    <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
                        <div>
                            <h1 className="text-2xl font-bold text-gray-900 tracking-tight flex items-center gap-2">
                                <Zap size={24} className="text-deriv-red fill-current" />
                                CRM Intelligence
                            </h1>
                            <p className="text-gray-500 text-sm hidden md:block">Real-time partner intervention monitoring.</p>
                        </div>
                        <div className="flex items-center gap-3">
                            <div className="relative hidden md:block">
                                <Search className="absolute left-2.5 top-1/2 -translate-y-1/2 text-gray-400" size={14} />
                                <input
                                    type="text"
                                    placeholder="Search tasks or partners..."
                                    className="h-9 w-64 pl-8 pr-4 rounded-full bg-gray-100 border border-transparent focus:bg-white focus:border-deriv-red focus:ring-4 focus:ring-deriv-red/10 transition-all text-sm outline-none"
                                />
                            </div>
                            <Button variant="outline" size="sm" className="gap-2 rounded-full border-gray-300 hover:border-gray-400 text-gray-700">
                                <RefreshCcw size={14} /> Sync
                            </Button>
                            <Button size="sm" className="bg-[#FF444F] hover:bg-[#EB3E48] text-white shadow-lg shadow-red-500/20 rounded-full px-6 transition-all hover:scale-105 active:scale-95">
                                + New Task
                            </Button>
                        </div>
                    </div>
                </div>
            </div>

            <div className="max-w-[1600px] mx-auto px-6 py-8 space-y-8">

                {/* Motion Container for Page Content */}
                <motion.div
                    variants={container}
                    initial="hidden"
                    animate="show"
                    className="space-y-8"
                >
                    {/* Intelligence Briefing - Premium Feature Card */}
                    <motion.div variants={item} className="relative overflow-hidden bg-gradient-to-br from-gray-900 via-gray-800 to-gray-900 rounded-2xl shadow-floating border border-gray-800 group">
                        <div className="absolute top-0 right-0 w-96 h-96 bg-[#FF444F] rounded-full mix-blend-overlay filter blur-[100px] opacity-10 group-hover:opacity-20 transition-opacity duration-700"></div>
                        <div className="relative p-8 flex flex-col md:flex-row items-start md:items-center gap-8">
                            <div className="p-4 bg-white/5 rounded-2xl backdrop-blur-sm border border-white/10 shadow-lg">
                                <ShieldAlert className="text-[#FF444F] w-10 h-10" />
                            </div>
                            <div className="flex-1 space-y-2">
                                <div className="flex items-center gap-2">
                                    <Badge className="bg-[#FF444F] hover:bg-[#EB3E48] text-white border-none px-2 py-0.5 text-[10px] uppercase tracking-wider font-bold">Live Insight</Badge>
                                    <span className="text-gray-400 text-xs font-mono">UPDATED 2 MINS AGO</span>
                                </div>
                                <h3 className="text-xl font-bold text-white">12 Critical Interventions Detected</h3>
                                <p className="text-gray-300 text-sm max-w-2xl leading-relaxed">
                                    Our predictive engine has identified high-value partners at risk. Immediate action on these tasks could protect an estimated <strong className="text-white border-b border-[#FF444F]/50 pb-0.5">$4.2M in annual revenue</strong>.
                                </p>
                            </div>
                            <Button className="shrink-0 bg-white text-gray-900 hover:bg-gray-100 font-semibold shadow-glow transition-all hover:scale-105 active:scale-95 px-6">
                                View Analysis Report <ArrowUpRight size={16} className="ml-2" />
                            </Button>
                        </div>
                    </motion.div>

                    {/* Quick Stats - Enhanced Cards */}
                    <motion.div variants={container} className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
                        {[
                            { label: "Critical Priority", value: "12", trend: "+2", color: "text-red-500", trendColor: "text-red-500" },
                            { label: "Due Today", value: "5", trend: "-1", color: "text-gray-900", trendColor: "text-green-500" },
                            { label: "Pending Review", value: "28", trend: "+5", color: "text-gray-900", trendColor: "text-amber-500" },
                            { label: "Resolved (24h)", value: "142", trend: "+12%", color: "text-emerald-600", trendColor: "text-emerald-600" }
                        ].map((stat, i) => (
                            <motion.div
                                key={i}
                                variants={item}
                                whileHover={{ y: -4, transition: { duration: 0.2 } }}
                                className="bg-white p-6 rounded-xl border border-gray-100 shadow-card hover:shadow-lg transition-all cursor-default"
                            >
                                <div className="flex justify-between items-start">
                                    <div className="text-xs font-bold text-gray-400 uppercase tracking-widest">{stat.label}</div>
                                    <Badge variant="secondary" className={cn("text-[10px] h-5 px-1.5 font-mono bg-gray-50", stat.trendColor)}>
                                        {stat.trend}
                                    </Badge>
                                </div>
                                <div className={cn("text-4xl font-bold mt-4 tracking-tighter", stat.color)}>
                                    {stat.value}
                                </div>
                            </motion.div>
                        ))}
                    </motion.div>

                    {/* Task Table - Clean & Professional */}
                    <motion.div variants={item} className="bg-white rounded-2xl border border-gray-200 shadow-sm overflow-hidden">
                        <div className="p-6 border-b border-gray-200 flex items-center justify-between bg-gray-50/30">
                            <div>
                                <h3 className="font-bold text-lg text-gray-900">Task Queue</h3>
                                <p className="text-xs text-gray-500 mt-1">Sorted by Priority & Churn Risk</p>
                            </div>
                            <div className="flex gap-2">
                                <Button variant="outline" size="sm" className="h-8 text-xs font-medium border-dashed border-gray-300">
                                    <Filter size={12} className="mr-1.5" /> Filter View
                                </Button>
                            </div>
                        </div>
                        <div className="overflow-x-auto">
                            <table className="w-full text-left">
                                <thead>
                                    <tr className="border-b border-gray-100 bg-gray-50/50">
                                        {["Task Detail", "Partner ID", "Priority", "Status", "Deadline", "Action"].map((h, i) => (
                                            <th key={i} className={`px-6 py-4 text-xs font-bold text-gray-500 uppercase tracking-wider ${i === 5 ? "text-right" : ""}`}>
                                                {h}
                                            </th>
                                        ))}
                                    </tr>
                                </thead>
                                <tbody className="divide-y divide-gray-50">
                                    {tasks.map((task, index) => (
                                        <motion.tr
                                            key={task.id}
                                            initial={{ opacity: 0 }}
                                            animate={{ opacity: 1 }}
                                            transition={{ delay: 0.1 * index }}
                                            className="group hover:bg-gray-50/80 transition-colors"
                                        >
                                            <td className="px-6 py-4">
                                                <div className="flex flex-col gap-1">
                                                    <span className="font-semibold text-gray-900 text-sm group-hover:text-deriv-red transition-colors">{task.title}</span>
                                                    <span className="text-xs text-gray-500">{task.type}</span>
                                                </div>
                                            </td>
                                            <td className="px-6 py-4">
                                                <Link href={`/partners/${task.partner_id}`} className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-md bg-gray-100 text-gray-600 text-xs font-mono font-medium hover:bg-white hover:shadow-sm hover:text-deriv-red transition-all border border-transparent hover:border-gray-200">
                                                    {task.partner_id} <ExternalLink size={10} />
                                                </Link>
                                            </td>
                                            <td className="px-6 py-4">
                                                <Badge variant="outline" className={`px-2.5 py-0.5 rounded-full font-medium border ${getPriorityColor(task.priority)}`}>
                                                    {task.priority}
                                                </Badge>
                                            </td>
                                            <td className="px-6 py-4">
                                                <div className="flex items-center gap-2 text-sm text-gray-700 font-medium">
                                                    {getStatusIcon(task.status)}
                                                    {task.status}
                                                </div>
                                            </td>
                                            <td className="px-6 py-4">
                                                <span className={cn(
                                                    "text-sm font-medium tabular-nums",
                                                    task.deadline === "Urgent" || task.deadline === "Today" ? "text-red-600" : "text-gray-500"
                                                )}>
                                                    {task.deadline}
                                                </span>
                                            </td>
                                            <td className="px-6 py-4 text-right">
                                                <div className="flex justify-end gap-2 opacity-0 group-hover:opacity-100 transition-opacity">
                                                    <Button variant="ghost" size="icon" className="h-8 w-8 text-gray-400 hover:text-gray-900 hover:bg-gray-100 rounded-lg">
                                                        <MoreHorizontal size={16} />
                                                    </Button>
                                                    <Button size="sm" className="h-8 bg-white border border-gray-200 text-gray-700 hover:bg-gray-50 hover:text-gray-900 hover:border-gray-300 shadow-sm rounded-lg font-medium text-xs">
                                                        Acknowledge
                                                    </Button>
                                                </div>
                                            </td>
                                        </motion.tr>
                                    ))}
                                </tbody>
                            </table>
                        </div>
                    </motion.div>
                </motion.div>
            </div>
        </div>
    )
}

