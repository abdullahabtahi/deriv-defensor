import { NextRequest, NextResponse } from 'next/server'

// In-memory storage for the latest agent summary
let latestSummary: any = null

export async function POST(request: NextRequest) {
    try {
        const body = await request.json()

        // Store the summary
        latestSummary = {
            partner_id: body.partner_id,
            churn_tendency: body.churn_tendency,
            summary: body.summary,
            metrics: body.metrics,
            reason_codes: body.reason_codes,
            recommended_action: body.recommended_action,
            timestamp: new Date().toISOString()
        }

        return NextResponse.json({ status: "ok" })
    } catch (error) {
        return NextResponse.json(
            { status: "error", message: "Failed to process summary" },
            { status: 400 }
        )
    }
}

export async function GET() {
    return NextResponse.json(latestSummary || {})
}
