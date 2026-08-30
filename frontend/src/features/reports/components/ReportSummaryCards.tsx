import Card from "../../../shared/components/Card";

import type { InvestigationReportSummary } from "../types/report.types";

interface ReportSummaryCardsProps {
    summary: InvestigationReportSummary;
}

const cards = [
    {
        key: "total_cases",
        label: "Total Cases",
    },
    {
        key: "resolved_cases",
        label: "Resolved",
    },
    {
        key: "waiting_cases",
        label: "Waiting",
    },
    {
        key: "technical_investigation_cases",
        label: "Technical Investigation",
    },
    {
        key: "escalated_cases",
        label: "Escalated",
    },
] as const;

function ReportSummaryCards({
    summary,
}: ReportSummaryCardsProps) {
    return (
        <section className="grid gap-5 sm:grid-cols-2 xl:grid-cols-5">
            {cards.map((card) => (
                <Card key={card.key}>
                    <p className="text-sm font-medium text-slate-400">
                        {card.label}
                    </p>

                    <p className="mt-4 text-3xl font-bold text-white">
                        {summary[card.key]}
                    </p>
                </Card>
            ))}
        </section>
    );
}

export default ReportSummaryCards;