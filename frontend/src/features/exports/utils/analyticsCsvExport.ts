import type {
    InvestigationAnalyticsResponse,
} from "../../analytics/types/analytics.types";

function escapeCsvValue(
    value: string | number,
): string {
    const text = String(value).replace(
        /"/g,
        '""',
    );

    return `"${text}"`;
}

function downloadFile(
    content: string,
    filename: string,
    mimeType: string,
): void {
    const blob = new Blob(
        [content],
        {
            type: mimeType,
        },
    );

    const url =
        URL.createObjectURL(blob);

    const link =
        document.createElement("a");

    link.href = url;
    link.download = filename;

    document.body.appendChild(link);

    link.click();
    link.remove();

    URL.revokeObjectURL(url);
}

export function exportAnalyticsToCsv(
    analytics: InvestigationAnalyticsResponse,
): void {
    const rows: Array<
        Array<string | number>
    > = [
            [
                "Andiny Atlas Investigation Analytics",
            ],
            [],
            [
                "Start Date",
                analytics.start_date,
            ],
            [
                "End Date",
                analytics.end_date,
            ],
            [
                "Interval",
                analytics.interval,
            ],
            [],
            ["KPI", "Value"],
            [
                "Total Cases",
                analytics.kpis.total_cases,
            ],
            [
                "Resolved Cases",
                analytics.kpis.resolved_cases,
            ],
            [
                "Waiting Cases",
                analytics.kpis.waiting_cases,
            ],
            [
                "Technical Investigation Cases",
                analytics.kpis
                    .technical_investigation_cases,
            ],
            [
                "Escalated Cases",
                analytics.kpis.escalated_cases,
            ],
            [
                "Resolution Rate",
                `${analytics.kpis.resolution_rate}%`,
            ],
            [
                "Escalation Rate",
                `${analytics.kpis.escalation_rate}%`,
            ],
            [],
            [
                "Trend Period",
                "Investigation Count",
            ],
            ...analytics.trend.map(
                (item) => [
                    item.period,
                    item.count,
                ],
            ),
            [],
            [
                "Status",
                "Count",
                "Percentage",
            ],
            ...analytics.status_distribution.map(
                (item) => [
                    item.status,
                    item.count,
                    `${item.percentage}%`,
                ],
            ),
            [],
            [
                "Investigator",
                "Investigator ID",
                "Investigation Count",
            ],
            ...analytics.investigator_workload.map(
                (item) => [
                    item.investigator_name,
                    item.investigator_id,
                    item.count,
                ],
            ),
        ];

    const csv = rows
        .map((row) =>
            row
                .map(escapeCsvValue)
                .join(","),
        )
        .join("\n");

    const filename =
        `investigation-analytics-${analytics.start_date}-to-${analytics.end_date}.csv`;

    downloadFile(
        csv,
        filename,
        "text/csv;charset=utf-8;",
    );
}