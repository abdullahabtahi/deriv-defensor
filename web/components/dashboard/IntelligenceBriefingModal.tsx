"use client"

import { useEffect, useState } from "react"
import {
    Dialog,
    DialogContent,
    DialogDescription,
    DialogFooter,
    DialogHeader,
    DialogTitle,
} from "@/components/ui/dialog"
import { Button } from "@/components/ui/button"
import { Brain, TrendingUp, AlertTriangle, ShieldCheck } from "lucide-react"

export function IntelligenceBriefingModal() {
    const [open, setOpen] = useState(false)
    const [briefingDate, setBriefingDate] = useState("")

    useEffect(() => {
        // Check local storage for today's briefing
        const today = new Date().toISOString().split('T')[0]
        const lastSeen = localStorage.getItem('lastSeenBriefing')

        setBriefingDate(new Date().toLocaleDateString('en-US', { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' }))

        if (lastSeen !== today) {
            // Add a small delay for dramatic effect
            const timer = setTimeout(() => {
                setOpen(true)
            }, 1500)
            return () => clearTimeout(timer)
        }
    }, [])

    const handleAcknowledge = () => {
        const today = new Date().toISOString().split('T')[0]
        localStorage.setItem('lastSeenBriefing', today)
        setOpen(false)
    }

    return (
        <Dialog open={open} onOpenChange={setOpen}>
            <DialogContent className="sm:max-w-[600px] border-deriv-red/20 shadow-2xl">
                <DialogHeader className="border-b border-gray-100 pb-4">
                    <DialogTitle className="flex items-center gap-2 text-xl font-bold text-gray-900">
                        <Brain className="text-deriv-red" />
                        Daily Intelligence Briefing
                    </DialogTitle>
                    <DialogDescription className="text-gray-500">
                        {briefingDate} • AI Surveillance Report
                    </DialogDescription>
                </DialogHeader>

                <div className="py-4 space-y-4">
                    {/* Insight 1: The 80/20 Rule */}
                    <div className="bg-blue-50/50 p-4 rounded-xl border border-blue-100 flex gap-4 items-start transition-all hover:bg-blue-50">
                        <div className="bg-blue-100 p-2.5 rounded-lg shrink-0">
                            <ShieldCheck className="text-blue-600" size={22} />
                        </div>
                        <div>
                            <h4 className="font-bold text-blue-900 leading-tight">Risk Concentration Alert</h4>
                            <p className="text-sm text-blue-700/90 mt-1.5 leading-relaxed">
                                <span className="font-semibold text-blue-800">The 80/20 Rule Verified:</span> Top 20% of partners are current driving 79.4% of commission revenue. Churn in the &quot;Gold&quot; tier has increased risk exposure by $2.4M this week.
                            </p>
                        </div>
                    </div>

                    {/* Insight 2: Churn Drivers */}
                    <div className="bg-red-50/50 p-4 rounded-xl border border-red-100 flex gap-4 items-start transition-all hover:bg-red-50">
                        <div className="bg-red-100 p-2.5 rounded-lg shrink-0">
                            <TrendingUp className="text-red-600" size={22} />
                        </div>
                        <div>
                            <h4 className="font-bold text-red-900 leading-tight">Top Churn Signal: Payment Friction</h4>
                            <p className="text-sm text-red-700/90 mt-1.5 leading-relaxed">
                                Partners experiencing payment delays (&gt;48h) are showing a <strong>3.2x higher likelihood</strong> of silence in the subsequent 30 days. Priority intervention recommended for 142 affected partners.
                            </p>
                        </div>
                    </div>

                    {/* Insight 3: Network Contagion */}
                    <div className="bg-orange-50/50 p-4 rounded-xl border border-orange-100 flex gap-4 items-start transition-all hover:bg-orange-50">
                        <div className="bg-orange-100 p-2.5 rounded-lg shrink-0">
                            <AlertTriangle className="text-orange-600" size={22} />
                        </div>
                        <div>
                            <h4 className="font-bold text-orange-900 leading-tight">Network Contagion Detection</h4>
                            <p className="text-sm text-orange-700/90 mt-1.5 leading-relaxed">
                                Master Affiliate risk increases by <strong>40%</strong> when 2+ sub-affiliates churn within 30 days. We have detected 5 active contagion clusters in LATAM region.
                            </p>
                        </div>
                    </div>
                </div>

                <DialogFooter className="border-t border-gray-100 pt-5">
                    <Button onClick={handleAcknowledge} className="w-full h-11 bg-deriv-red hover:bg-deriv-red/90 text-white font-bold shadow-lg shadow-deriv-red/20">
                        Acknowledge & Close
                    </Button>
                </DialogFooter>
            </DialogContent>
        </Dialog>
    )
}
