import { render, screen } from "@testing-library/react"
import { KpiCard } from "@/components/dashboard/KpiCard"

describe("KpiCard", () => {
    it("renders the title and value correctly", () => {
        render(
            <KpiCard
                title="Total Risk"
                value="$10M"
                color="red"
            />
        )

        expect(screen.getByText("Total Risk")).toBeInTheDocument()
        expect(screen.getByText("$10M")).toBeInTheDocument()
    })

    it("displays the trend percentage when provided", () => {
        render(
            <KpiCard
                title="Total Risk"
                value="$10M"
                trend={12}
                trendLabel="upward"
            />
        )

        expect(screen.getByText("12%")).toBeInTheDocument()
        expect(screen.getByText("upward")).toBeInTheDocument()
    })
})
