"use client"

import { useState } from "react"
import { api } from "@/services/api"
import { useRouter } from "next/navigation"
import { Button } from "@/components/ui/button"
import { ExternalLink, Send } from "lucide-react"

interface PartnerActionsProps {
    partnerId: string
}

export function PartnerActions({ partnerId }: PartnerActionsProps) {
    const [isTriggering, setIsTriggering] = useState(false)
    const router = useRouter()

    const handleTrigger = async () => {
        setIsTriggering(true)
        try {
            const result = await api.triggerIntervention(partnerId)
            if (result && result.status === 'success') {
                router.refresh()
            }
        } catch (error) {
            console.error("Failed to trigger intervention:", error)
        } finally {
            setIsTriggering(false)
        }
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
