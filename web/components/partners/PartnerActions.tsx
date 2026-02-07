"use client"

import { Button } from "@/components/ui/button"
import { ExternalLink, Send } from "lucide-react"
import { useState } from "react"

interface PartnerActionsProps {
    partnerId: string
}

export function PartnerActions({ partnerId }: PartnerActionsProps) {
    const [isTriggering, setIsTriggering] = useState(false)

    const handleTrigger = async () => {
        setIsTriggering(true)
        // Simulate API call to trigger intervention
        setTimeout(() => {
            setIsTriggering(false)
            alert(`Intervention triggered for ${partnerId}! Check the Intervention Log for updates.`)
        }, 1500)
    }

    const handleCRM = () => {
        alert("Opening CRM entry for " + partnerId)
    }

    return (
        <div className="flex gap-2">
            <Button variant="outline" className="gap-2" onClick={handleCRM}>
                <ExternalLink size={16} />
                View CRM
            </Button>
            <Button
                className="bg-deriv-red hover:bg-deriv-red/90 gap-2"
                onClick={handleTrigger}
                disabled={isTriggering}
            >
                <Send size={16} className={isTriggering ? "animate-pulse" : ""} />
                {isTriggering ? "Triggering..." : "Trigger Intervention"}
            </Button>
        </div>
    )
}
