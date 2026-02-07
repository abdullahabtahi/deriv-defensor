
"use client"

// Force rebuild
import { useState, useEffect } from "react"
import { IntelligenceBriefingModal } from "./IntelligenceBriefingModal"

export function DailyBriefing() {
    const [open, setOpen] = useState(false)

    useEffect(() => {
        // Only run on client side
        const lastSeen = localStorage.getItem('lastSeenBriefing')
        const today = new Date().toISOString().split('T')[0]

        // If not seen today, show it
        if (lastSeen !== today) {
            setOpen(true)
        }
    }, [])

    return (
        <IntelligenceBriefingModal
            open={open}
            onOpenChange={setOpen}
        />
    )
}
