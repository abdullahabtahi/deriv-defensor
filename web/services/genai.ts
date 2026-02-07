
export interface GenAIAnalysis {
    explanation: string;
    emailSubject: string;
    emailBody: string;
    recommendedAction: string;
}

export const mockGenAIAnalysis = async (partnerId: string): Promise<GenAIAnalysis> => {
    // Simulate network delay
    await new Promise(resolve => setTimeout(resolve, 1500));

    return {
        explanation: `**Risk Analysis for ${partnerId}**\n\nThis partner shows a **85% probability of churn** within the next 7 days. Key indicators include:\n\n1.  **Sudden Drop in Activity**: Trading volume decreased by 60% week-over-week.\n2.  **Payment Friction**: 2 failed deposit attempts recorded on Feb 5th.\n3.  **Support Silence**: No response to the last check-in email (3 days ago).\n\n*Recommended Strategy*: Immediate personal outreach addressing the deposit issues to restore trust.`,
        emailSubject: "Action Required: Issue with your recent deposit?",
        emailBody: `Hi [Partner Name],\n\nI noticed you had some trouble with your recent deposits on the platform. I wanted to reach out personally to see if I can help resolve this for you.\n\nWe value your partnership and want to ensure your operations run smoothly. If you're available for a quick chat, I can walk you through a workaround or expedite a support ticket for you.\n\nBest regards,\n[Your Name]\nDeriv Partnership Team`,
        recommendedAction: "Call & Email"
    };
};
